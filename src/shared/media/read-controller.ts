import type { MediaReadData, MediaReadDescriptor, MediaReadReference } from '../../web/src/shared/api/generated';

export interface MediaAbortSignal {
  readonly aborted: boolean;
  addEventListener(type: 'abort', callback: () => void, options?: { once?: boolean }): void;
  removeEventListener(type: 'abort', callback: () => void): void;
}
export class MediaAbortController {
  private callbacks = new Set<() => void>();
  readonly signal: MediaAbortSignal & { aborted: boolean } = {
    aborted: false,
    addEventListener: (_type: 'abort', callback: () => void) => { this.callbacks.add(callback); },
    removeEventListener: (_type: 'abort', callback: () => void) => { this.callbacks.delete(callback); },
  };
  abort() {
    if (this.signal.aborted) return;
    this.signal.aborted = true;
    for (const callback of this.callbacks) callback();
    this.callbacks.clear();
  }
}

type Transport = (items: MediaReadReference[], signal: MediaAbortSignal) => Promise<MediaReadData>;
export type MediaReadObservation = { resource_type: string; variant: string; phase: 'authorization' | 'refresh' | 'recovery' | 'degraded' | 'proxy' | 'load' | 'preview' | 'play'; result: 'success' | 'failed'; outcome: 'success' | 'failed' | 'started' | 'unavailable' };
type Pending = { ref: MediaReadReference; resolve: (value: MediaReadDescriptor) => void; reject: (error: unknown) => void };
export class MediaReadFailure extends Error {
  constructor(public readonly terminal: boolean) { super(terminal ? '媒体不可用' : '媒体加载失败，请重试'); }
}
const keyOf = (ref: MediaReadReference) => JSON.stringify([ref.resource_type, ref.resource_id, ref.media_id ?? null, ref.variant ?? 'original']);
const cancelled = () => Object.assign(new Error('Cancelled'), { name: 'AbortError' });

/** One instance per identity; discard it on logout, account changes or page teardown. */
export class MediaReadController {
  private cache = new Map<string, { descriptor: MediaReadDescriptor; until: number }>();
  private inFlight = new Map<string, Promise<MediaReadDescriptor>>();
  private retries = new Map<string, number>();
  private terminal = new Set<string>();
  private recovering = new Map<string, Promise<MediaReadDescriptor>>();
  private queue: Pending[] = [];
  private active = 0;
  private disposed = false;
  private requests = new Set<MediaAbortController>();
  private delays = new Set<() => void>();

  constructor(private transport: Transport, private now: () => number = () => Date.now(), private observe?: (event: MediaReadObservation) => void) {}

  report(ref: MediaReadReference, phase: MediaReadObservation['phase'], result: MediaReadObservation['outcome']) {
    try { this.observe?.({resource_type: ref.resource_type, variant: ref.variant ?? 'original', phase, result: result === 'failed' || result === 'unavailable' ? 'failed' : 'success', outcome: result}); } catch { /* Observability never affects media. */ }
  }

  read(ref: MediaReadReference, options: { force?: boolean; signal?: MediaAbortSignal } = {}): Promise<MediaReadDescriptor> {
    if (this.disposed || options.signal?.aborted) return Promise.reject(cancelled());
    const key = keyOf(ref);
    if (this.terminal.has(key)) return Promise.reject(new MediaReadFailure(true));
    const cached = this.cache.get(key);
    let promise: Promise<MediaReadDescriptor>;
    if (!options.force && cached && cached.until > this.now()) promise = Promise.resolve(cached.descriptor);
    else {
      const existing = this.inFlight.get(key);
      if (existing) promise = existing;
      else {
        promise = new Promise<MediaReadDescriptor>((resolve, reject) => { this.queue.push({ ref, resolve, reject }); });
        this.inFlight.set(key, promise);
        void promise.finally(() => this.inFlight.delete(key)).catch(() => {});
        void Promise.resolve().then(() => this.pump());
      }
    }
    return this.subscribe(promise, options.signal);
  }

  private subscribe(promise: Promise<MediaReadDescriptor>, signal?: MediaAbortSignal): Promise<MediaReadDescriptor> {
    if (!signal) return promise;
    if (signal.aborted) return Promise.reject(cancelled());
    return new Promise((resolve, reject) => {
      const abort = () => reject(cancelled());
      signal.addEventListener('abort', abort, { once: true });
      promise.then(value => { if (!signal.aborted) resolve(value); }, reject)
        .finally(() => signal.removeEventListener('abort', abort));
    });
  }

  recover(ref: MediaReadReference, signal?: MediaAbortSignal): Promise<MediaReadDescriptor> {
    const key = keyOf(ref);
    if (this.terminal.has(key)) return Promise.reject(new MediaReadFailure(true));
    const existing = this.recovering.get(key);
    if (this.disposed || signal?.aborted) return Promise.reject(cancelled());
    if (existing) return this.subscribe(existing, signal);
    const promise = this.performRecovery(ref);
    this.recovering.set(key, promise);
    void promise.finally(() => this.recovering.delete(key)).catch(() => {});
    return this.subscribe(promise, signal);
  }

  private async performRecovery(ref: MediaReadReference, signal?: MediaAbortSignal): Promise<MediaReadDescriptor> {
    const key = keyOf(ref);
    const count = this.retries.get(key) ?? 0;
    if (count >= 2) throw new MediaReadFailure(false);
    this.retries.set(key, count + 1);
    this.report(ref, 'refresh', 'started');
    await new Promise<void>((resolve, reject) => {
      const abort = () => { clearTimeout(timer); this.delays.delete(abort); signal?.removeEventListener('abort', abort); reject(cancelled()); };
      const timer = setTimeout(() => { this.delays.delete(abort); signal?.removeEventListener('abort', abort); resolve(); }, count === 0 ? 1000 : 3000);
      this.delays.add(abort);
      signal?.addEventListener('abort', abort, { once: true });
      if (this.disposed || signal?.aborted) abort();
    });
    try {
      const value = await this.read(ref, { force: true, signal });
      this.report(ref, 'refresh', 'success');
      return value;
    } catch (error) {
      if ((error as Error)?.name !== 'AbortError') this.report(ref, 'refresh', 'failed');
      throw error;
    }
  }

  manualRetry(ref: MediaReadReference, signal?: MediaAbortSignal) {
    this.retries.delete(keyOf(ref));
    this.terminal.delete(keyOf(ref));
    return this.read(ref, { force: true, signal });
  }

  dispose() {
    this.disposed = true;
    for (const request of this.requests) request.abort();
    for (const abort of this.delays) abort();
    for (const pending of this.queue.splice(0)) pending.reject(cancelled());
    this.cache.clear();
    this.retries.clear();
    this.terminal.clear();
  }

  private pump() {
    while (!this.disposed && this.active < 4 && this.queue.length) {
      const batch = this.queue.splice(0, 50);
      this.active++;
      void this.send(batch).finally(() => { this.active--; this.pump(); });
    }
  }

  private async send(batch: Pending[]) {
    const abort = new MediaAbortController();
    this.requests.add(abort);
    let timer: ReturnType<typeof setTimeout> | undefined;
    try {
      const data = await Promise.race([
        this.transport(batch.map(item => item.ref), abort.signal),
        new Promise<never>((_, reject) => {
          abort.signal.addEventListener('abort', () => reject(cancelled()), { once: true });
          timer = setTimeout(() => { reject(new MediaReadFailure(false)); abort.abort(); }, 10000);
        }),
      ]);
      if (this.disposed) throw cancelled();
      const serverTime = Date.parse(data.server_time);
      const results = new Map(data.items.map(item => [keyOf(item.reference), item]));
      for (const pending of batch) {
        const key = keyOf(pending.ref);
        const result = results.get(key);
        if (result?.status === 'ready' && result.descriptor) {
          const descriptor = result.descriptor;
          const remaining = descriptor.expires_at ? Math.min(300000, Date.parse(descriptor.expires_at) - serverTime) : 0;
          this.cache.set(key, { descriptor, until: this.now() + Math.max(0, remaining - 30000) });
          this.report(pending.ref, 'authorization', 'success');
          if (descriptor.degraded) this.report(pending.ref, 'degraded', 'success');
          if (descriptor.read_mode === 'proxy') this.report(pending.ref, 'proxy', 'success');
          pending.resolve(descriptor);
        } else {
          if (result?.status === 'unavailable') this.terminal.add(key);
          this.report(pending.ref, 'authorization', result?.status === 'unavailable' ? 'unavailable' : 'failed');
          pending.reject(new MediaReadFailure(result?.status === 'unavailable'));
        }
      }
    } catch (error) {
      for (const pending of batch) {
        if (error instanceof MediaReadFailure && error.terminal) this.terminal.add(keyOf(pending.ref));
        if ((error as Error)?.name !== 'AbortError') this.report(pending.ref, 'authorization', 'failed');
        pending.reject(error);
      }
    } finally {
      clearTimeout(timer);
      this.requests.delete(abort);
    }
  }
}
