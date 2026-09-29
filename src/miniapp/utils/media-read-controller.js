// Generated from src/shared/media/read-controller.ts; run node scripts/sync-media-read-controller.cjs.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MediaReadController = exports.MediaReadFailure = exports.MediaAbortController = void 0;
class MediaAbortController {
    constructor() {
        this.callbacks = new Set();
        this.signal = {
            aborted: false,
            addEventListener: (_type, callback) => { this.callbacks.add(callback); },
            removeEventListener: (_type, callback) => { this.callbacks.delete(callback); },
        };
    }
    abort() {
        if (this.signal.aborted)
            return;
        this.signal.aborted = true;
        for (const callback of this.callbacks)
            callback();
        this.callbacks.clear();
    }
}
exports.MediaAbortController = MediaAbortController;
class MediaReadFailure extends Error {
    constructor(terminal) {
        super(terminal ? '媒体不可用' : '媒体加载失败，请重试');
        this.terminal = terminal;
    }
}
exports.MediaReadFailure = MediaReadFailure;
const keyOf = (ref) => { var _a, _b; return JSON.stringify([ref.resource_type, ref.resource_id, (_a = ref.media_id) !== null && _a !== void 0 ? _a : null, (_b = ref.variant) !== null && _b !== void 0 ? _b : 'original']); };
const cancelled = () => Object.assign(new Error('Cancelled'), { name: 'AbortError' });
/** One instance per identity; discard it on logout, account changes or page teardown. */
class MediaReadController {
    constructor(transport, now = () => Date.now(), observe) {
        this.transport = transport;
        this.now = now;
        this.observe = observe;
        this.cache = new Map();
        this.inFlight = new Map();
        this.retries = new Map();
        this.terminal = new Set();
        this.recovering = new Map();
        this.queue = [];
        this.active = 0;
        this.disposed = false;
        this.requests = new Set();
        this.delays = new Set();
    }
    report(ref, phase, result) {
        var _a, _b;
        try {
            (_a = this.observe) === null || _a === void 0 ? void 0 : _a.call(this, { resource_type: ref.resource_type, variant: (_b = ref.variant) !== null && _b !== void 0 ? _b : 'original', phase, result: result === 'failed' || result === 'unavailable' ? 'failed' : 'success', outcome: result });
        }
        catch ( /* Observability never affects media. */_c) { /* Observability never affects media. */ }
    }
    read(ref, options = {}) {
        var _a;
        if (this.disposed || ((_a = options.signal) === null || _a === void 0 ? void 0 : _a.aborted))
            return Promise.reject(cancelled());
        const key = keyOf(ref);
        if (this.terminal.has(key))
            return Promise.reject(new MediaReadFailure(true));
        const cached = this.cache.get(key);
        let promise;
        if (!options.force && cached && cached.until > this.now())
            promise = Promise.resolve(cached.descriptor);
        else {
            const existing = this.inFlight.get(key);
            if (existing)
                promise = existing;
            else {
                promise = new Promise((resolve, reject) => { this.queue.push({ ref, resolve, reject }); });
                this.inFlight.set(key, promise);
                void promise.finally(() => this.inFlight.delete(key)).catch(() => { });
                void Promise.resolve().then(() => this.pump());
            }
        }
        return this.subscribe(promise, options.signal);
    }
    subscribe(promise, signal) {
        if (!signal)
            return promise;
        if (signal.aborted)
            return Promise.reject(cancelled());
        return new Promise((resolve, reject) => {
            const abort = () => reject(cancelled());
            signal.addEventListener('abort', abort, { once: true });
            promise.then(value => { if (!signal.aborted)
                resolve(value); }, reject)
                .finally(() => signal.removeEventListener('abort', abort));
        });
    }
    recover(ref, signal) {
        const key = keyOf(ref);
        if (this.terminal.has(key))
            return Promise.reject(new MediaReadFailure(true));
        const existing = this.recovering.get(key);
        if (this.disposed || (signal === null || signal === void 0 ? void 0 : signal.aborted))
            return Promise.reject(cancelled());
        if (existing)
            return this.subscribe(existing, signal);
        const promise = this.performRecovery(ref);
        this.recovering.set(key, promise);
        void promise.finally(() => this.recovering.delete(key)).catch(() => { });
        return this.subscribe(promise, signal);
    }
    async performRecovery(ref, signal) {
        var _a;
        const key = keyOf(ref);
        const count = (_a = this.retries.get(key)) !== null && _a !== void 0 ? _a : 0;
        if (count >= 2)
            throw new MediaReadFailure(false);
        this.retries.set(key, count + 1);
        this.report(ref, 'refresh', 'started');
        await new Promise((resolve, reject) => {
            const abort = () => { clearTimeout(timer); this.delays.delete(abort); signal === null || signal === void 0 ? void 0 : signal.removeEventListener('abort', abort); reject(cancelled()); };
            const timer = setTimeout(() => { this.delays.delete(abort); signal === null || signal === void 0 ? void 0 : signal.removeEventListener('abort', abort); resolve(); }, count === 0 ? 1000 : 3000);
            this.delays.add(abort);
            signal === null || signal === void 0 ? void 0 : signal.addEventListener('abort', abort, { once: true });
            if (this.disposed || (signal === null || signal === void 0 ? void 0 : signal.aborted))
                abort();
        });
        try {
            const value = await this.read(ref, { force: true, signal });
            this.report(ref, 'refresh', 'success');
            return value;
        }
        catch (error) {
            if ((error === null || error === void 0 ? void 0 : error.name) !== 'AbortError')
                this.report(ref, 'refresh', 'failed');
            throw error;
        }
    }
    manualRetry(ref, signal) {
        this.retries.delete(keyOf(ref));
        this.terminal.delete(keyOf(ref));
        return this.read(ref, { force: true, signal });
    }
    dispose() {
        this.disposed = true;
        for (const request of this.requests)
            request.abort();
        for (const abort of this.delays)
            abort();
        for (const pending of this.queue.splice(0))
            pending.reject(cancelled());
        this.cache.clear();
        this.retries.clear();
        this.terminal.clear();
    }
    pump() {
        while (!this.disposed && this.active < 4 && this.queue.length) {
            const batch = this.queue.splice(0, 50);
            this.active++;
            void this.send(batch).finally(() => { this.active--; this.pump(); });
        }
    }
    async send(batch) {
        const abort = new MediaAbortController();
        this.requests.add(abort);
        let timer;
        try {
            const data = await Promise.race([
                this.transport(batch.map(item => item.ref), abort.signal),
                new Promise((_, reject) => {
                    abort.signal.addEventListener('abort', () => reject(cancelled()), { once: true });
                    timer = setTimeout(() => { reject(new MediaReadFailure(false)); abort.abort(); }, 10000);
                }),
            ]);
            if (this.disposed)
                throw cancelled();
            const serverTime = Date.parse(data.server_time);
            const results = new Map(data.items.map(item => [keyOf(item.reference), item]));
            for (const pending of batch) {
                const key = keyOf(pending.ref);
                const result = results.get(key);
                if ((result === null || result === void 0 ? void 0 : result.status) === 'ready' && result.descriptor) {
                    const descriptor = result.descriptor;
                    const remaining = descriptor.expires_at ? Math.min(300000, Date.parse(descriptor.expires_at) - serverTime) : 0;
                    this.cache.set(key, { descriptor, until: this.now() + Math.max(0, remaining - 30000) });
                    this.report(pending.ref, 'authorization', 'success');
                    if (descriptor.degraded)
                        this.report(pending.ref, 'degraded', 'success');
                    if (descriptor.read_mode === 'proxy')
                        this.report(pending.ref, 'proxy', 'success');
                    pending.resolve(descriptor);
                }
                else {
                    if ((result === null || result === void 0 ? void 0 : result.status) === 'unavailable')
                        this.terminal.add(key);
                    this.report(pending.ref, 'authorization', (result === null || result === void 0 ? void 0 : result.status) === 'unavailable' ? 'unavailable' : 'failed');
                    pending.reject(new MediaReadFailure((result === null || result === void 0 ? void 0 : result.status) === 'unavailable'));
                }
            }
        }
        catch (error) {
            for (const pending of batch) {
                if (error instanceof MediaReadFailure && error.terminal)
                    this.terminal.add(keyOf(pending.ref));
                if ((error === null || error === void 0 ? void 0 : error.name) !== 'AbortError')
                    this.report(pending.ref, 'authorization', 'failed');
                pending.reject(error);
            }
        }
        finally {
            clearTimeout(timer);
            this.requests.delete(abort);
        }
    }
}
exports.MediaReadController = MediaReadController;
