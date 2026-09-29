import type { UploadAuthorization, UploadResult, UploadSessionCreate, UploadSessionCreated, UploadSessionRenewed, UploadSessionStatus } from '@/shared/api/generated';
import type { UploadStage } from './media-upload-status';

export type UploadObservation = {
  action: 'start' | 'retry' | 'stage' | 'cancel' | 'save'; stage?: UploadStage;
  duration_ms?: number; task_trace_id?: string | null;
  mode: 'pending' | 'proxy' | 'cos_direct'; media_kind: UploadSessionCreate['media_kind']; file_size_bytes: number;
};
export type UploadSnapshot = { stage: UploadStage; progress: number; error?: string; retryable?: boolean; warning?: string };
export interface UploadControlTransport {
  create(input: UploadSessionCreate, signal: AbortSignal): Promise<UploadSessionCreated>;
  query(id: string, signal: AbortSignal): Promise<UploadSessionStatus>;
  renew(id: string, signal: AbortSignal): Promise<UploadSessionRenewed>;
  authorizePart(id: string, part: number, signal: AbortSignal): Promise<UploadAuthorization>;
  confirm(id: string, signal: AbortSignal): Promise<UploadSessionStatus>;
  cancel(id: string): Promise<UploadSessionStatus>;
  retryProcessing?(id: string, signal: AbortSignal): Promise<UploadSessionStatus>;
}
export type PutUpload = (authorization: UploadAuthorization, bytes: Blob, signal: AbortSignal, onBytes: (loaded: number) => void) => Promise<void>;
export class MediaUploadFailure extends Error {
  constructor(message: string, public readonly retryable = true) { super(message); }
}
class ObjectUploadFailure extends Error {
  constructor(public readonly status: number) { super('文件传输失败'); }
}
const abortError = () => new DOMException('上传已取消', 'AbortError');
const paused = (ms: number, signal: AbortSignal) => new Promise<void>((resolve, reject) => {
  const abort = () => { clearTimeout(timer); signal.removeEventListener('abort', abort); reject(abortError()); };
  const timer = setTimeout(() => { signal.removeEventListener('abort', abort); resolve(); }, ms);
  signal.addEventListener('abort', abort, { once: true });
  if (signal.aborted) abort();
});
function retryable(error: unknown): boolean {
  if (error instanceof MediaUploadFailure) return error.retryable;
  if (error instanceof ObjectUploadFailure) return error.status === 0 || error.status === 403 || error.status === 408 || error.status === 429 || error.status >= 500;
  const status = (error as { response?: { status?: number } })?.response?.status;
  return !status || status === 408 || status === 429 || status >= 500;
}

/** A separate XHR intentionally carries no application token or tracking headers. */
export const putAuthorizedObject: PutUpload = (authorization, bytes, signal, onBytes) => new Promise((resolve, reject) => {
  if (signal.aborted) { reject(abortError()); return; }
  const request = new XMLHttpRequest();
  const abort = () => request.abort();
  const finish = (error?: Error) => { signal.removeEventListener('abort', abort); error ? reject(error) : resolve(); };
  request.open('PUT', authorization.url);
  request.withCredentials = false;
  request.timeout = 120000;
  if (bytes.type) request.setRequestHeader('Content-Type', bytes.type);
  // Content-Length is a forbidden browser header; XHR derives it from this exact Blob.
  request.upload.onprogress = event => onBytes(Math.min(bytes.size, event.loaded));
  request.onload = () => request.status >= 200 && request.status < 300 ? finish() : finish(new ObjectUploadFailure(request.status));
  request.onerror = () => finish(new ObjectUploadFailure(0));
  request.ontimeout = () => finish(new ObjectUploadFailure(408));
  request.onabort = () => finish(abortError());
  signal.addEventListener('abort', abort, { once: true });
  if (bytes.size !== authorization.length) { finish(new MediaUploadFailure('分片大小与授权不符', false)); return; }
  request.send(bytes);
});

/** One file per task. Only file/part state lives in memory; no persistent credentials. */
export class MediaUploadTask {
  private session?: UploadSessionStatus;
  private completed = new Set<number>();
  private inFlight = new Map<number, number>();
  private abort?: AbortController;
  private running = false;
  private cancelled = false;
  private proxyMode = false;
  private idempotencyKey = crypto.randomUUID();
  private progress = 0;
  private runs = 0;
  private saved = false;
  private observedStage?: UploadStage;
  private observedAt = 0;

  constructor(readonly file: File, private businessId: number | undefined,
    private transport: UploadControlTransport,
    private update: (snapshot: UploadSnapshot) => void,
    private proxy: (signal: AbortSignal, progress: (loaded: number) => void) => Promise<UploadResult>,
    private put: PutUpload = putAuthorizedObject,
    private wait = paused,
    private mediaKind: UploadSessionCreate['media_kind'] = 'sku_video',
    private observe?: (value: UploadObservation) => void | Promise<void>,
  ) {}

  get sessionId() { return this.session?.session_id; }
  setListener(listener: (snapshot: UploadSnapshot) => void) { this.update = listener; }

  private report(action: UploadObservation['action'], stage?: UploadStage, duration_ms?: number) {
    try {
      void Promise.resolve(this.observe?.({action, stage, duration_ms, task_trace_id:this.session?.task_trace_id,
        mode:this.proxyMode ? 'proxy' : this.session ? 'cos_direct' : 'pending',
        media_kind:this.mediaKind, file_size_bytes:this.file.size})).catch(() => {});
    } catch { /* Observability cannot affect upload state. */ }
  }

  private emit(stage: UploadStage, extra: Partial<UploadSnapshot> = {}) {
    if (stage !== this.observedStage) {
      if (this.observedStage) this.report('stage', this.observedStage, Math.round(performance.now()-this.observedAt));
      this.observedStage = stage; this.observedAt = performance.now();
      if (['uploaded','failed','cancelled'].includes(stage)) {
        this.report('stage', stage, 0); this.observedStage = undefined;
      }
    }
    this.update({ stage, progress: this.progress, ...extra });
  }

  private async retry<T>(operation: () => Promise<T>, signal: AbortSignal): Promise<T> {
    for (let attempt = 0; ; attempt++) {
      if (signal.aborted) throw abortError();
      try { return await operation(); }
      catch (error) {
        if (signal.aborted || attempt >= 3 || !retryable(error)) throw error;
        await this.wait(1000 * 2 ** attempt + Math.random() * 250, signal);
      }
    }
  }

  async run(): Promise<UploadResult> {
    if (this.running) throw new MediaUploadFailure('当前文件仍在上传，请稍候', false);
    if (this.cancelled) throw new MediaUploadFailure('本次上传已取消，请重新选择文件', false);
    this.report(this.runs++ ? 'retry' : 'start');
    this.running = true;
    this.abort = new AbortController();
    const signal = this.abort.signal;
    try {
      this.emit('authorizing');
      if (!this.session && !this.proxyMode) {
        const capability = await this.retry(() => this.transport.create({
          media_kind: this.mediaKind, business_id: this.businessId, expected_size: this.file.size,
          mime_type: this.file.type, client_idempotency_key: this.idempotencyKey,
        }, signal), signal);
        if (signal.aborted) throw abortError();
        this.proxyMode = capability.mode === 'proxy';
        this.session = capability.session ?? undefined;
        if (!this.proxyMode && !this.session) throw new MediaUploadFailure('未获取到上传会话', false);
      }
      if (this.proxyMode) {
        const result = await this.proxy(signal, progress => {
          this.progress = progress;
          this.emit(progress >= 99 ? 'saving' : 'transferring');
        });
        if (signal.aborted) throw abortError();
        this.progress = 100; this.emit('uploaded'); return result;
      }
      let status = await this.retry(() => this.transport.query(this.session!.session_id, signal), signal);
      if (status.state === 'created') status = (await this.retry(() => this.transport.renew(status.session_id, signal), signal)).session;
      this.session = status;
      if (status.state === 'uploading') {
        await this.transfer(signal);
        if (signal.aborted) throw abortError();
        this.progress = 100; this.emit('verifying');
        status = await this.retry(() => this.transport.confirm(status.session_id, signal), signal);
      } else if (status.state === 'failed' && status.retryable) {
        this.emit('verifying');
        status = await this.retry(() => status.error_code === 30084 && this.transport.retryProcessing
          ? this.transport.retryProcessing(status.session_id, signal)
          : this.transport.confirm(status.session_id, signal), signal);
      }
      const deadline = Date.now() + 10 * 60 * 1000;
      let polls = 0;
      while (['verifying', 'processing'].includes(status.state)) {
        this.emit(status.state === 'processing' ? 'processing' : 'verifying');
        await this.wait(750, signal);
        if (Date.now() > deadline) throw new MediaUploadFailure('文件仍在校验，请稍后重试确认');
        status = await this.retry(() => status.state === 'verifying' && ++polls % 10 === 0
          ? this.transport.confirm(status.session_id, signal)
          : this.transport.query(status.session_id, signal), signal);
      }
      if (signal.aborted) throw abortError();
      this.session = status;
      if (!['ready', 'bound'].includes(status.state) || !status.media) {
        throw new MediaUploadFailure(status.error_code === 30083 ? '文件校验不通过，请检查文件后重新选择' : '文件尚未就绪，请重试或重新选择', Boolean(status.retryable));
      }
      this.progress = 100; this.emit('uploaded', { warning: status.media.processing_warning ? '图片已处理，但未达到目标体积，仍可保存' : undefined });
      return { ...status.media, task_trace_id: status.task_trace_id, task_type: 'media_direct_upload' };
    } catch (error) {
      this.abort.abort();
      if (!this.cancelled) {
        const failure = error instanceof MediaUploadFailure ? error : new MediaUploadFailure('上传未完成，请检查网络后重试', retryable(error));
        this.emit('failed', { error: failure.message, retryable: failure.retryable });
        throw failure;
      }
      throw abortError();
    } finally { this.running = false; }
  }

  private async transfer(signal: AbortSignal) {
    const session = this.session!;
    const count = session.part_count;
    const total = this.file.size;
    if (count < 1 || session.part_size < 1 || count !== Math.ceil(total / session.part_size)) throw new MediaUploadFailure('上传分片参数无效', false);
    let next = 1;
    const progress = () => {
      let loaded = 0;
      for (const number of this.completed) loaded += Math.min(session.part_size, total - (number - 1) * session.part_size);
      for (const bytes of this.inFlight.values()) loaded += bytes;
      this.progress = Math.min(100, Math.floor(loaded * 100 / total));
      if (!signal.aborted) this.emit('transferring');
    };
    const worker = async () => {
      while (next <= count) {
        const number = next++;
        if (this.completed.has(number)) continue;
        const bytes = this.file.slice((number - 1) * session.part_size, Math.min(number * session.part_size, total), this.file.type);
        await this.retry(async () => {
          this.inFlight.delete(number); progress();
          const grant = count === 1
            ? (await this.transport.renew(session.session_id, signal)).authorization
            : await this.transport.authorizePart(session.session_id, number, signal);
          if (!grant) throw new MediaUploadFailure('未获取到文件上传授权', false);
          await this.put(grant, bytes, signal, loaded => { this.inFlight.set(number, Math.min(bytes.size, loaded)); progress(); });
        }, signal);
        this.inFlight.delete(number); this.completed.add(number); progress();
      }
    };
    const workers = Array.from({ length: Math.min(2, count) }, worker);
    try { await Promise.all(workers); }
    catch (error) { this.abort!.abort(); await Promise.allSettled(workers); this.inFlight.clear(); throw error; }
  }

  markSaved() {
    if (!this.saved) { this.saved = true; this.report('save'); }
  }

  async cancel() {
    if (this.saved) return;
    if (!this.cancelled) this.report('cancel');
    this.cancelled = true;
    this.abort?.abort();
    this.emit('cancelling');
    try {
      if (this.session) await this.transport.cancel(this.session.session_id);
      this.emit('cancelled');
    } catch {
      this.emit('failed', { error: '取消未成功，请刷新后检查文件状态', retryable: false });
      throw new MediaUploadFailure('取消未成功，请重试取消', false);
    }
  }
}
