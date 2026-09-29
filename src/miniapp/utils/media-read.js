// Generated from media-read.ts; run node scripts/sync-media-read-controller.cjs.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MiniappMediaScope = void 0;
exports.createMiniappMediaReadController = createMiniappMediaReadController;
const api_1 = require("../services/api");
const media_read_controller_1 = require("./media-read-controller");
/** Page-owned instance: onHide/dispose cancels all work; onShow creates a fresh instance. */
function createMiniappMediaReadController() {
    const timer = typeof wx.getPerformance === 'function' ? wx.getPerformance() : null;
    return new media_read_controller_1.MediaReadController(async (items, signal) => {
        let task;
        const abort = () => task === null || task === void 0 ? void 0 : task.abort();
        signal.addEventListener('abort', abort);
        try {
            return await (0, api_1.request)('/api/v1/media/read-authorizations', {
                method: 'POST', data: { items }, timeout: 10000, singleAttempt: true,
                onRequestTask: value => { task = value; if (signal.aborted)
                    task.abort(); },
            });
        }
        catch (error) {
            if (signal.aborted)
                throw Object.assign(new Error('Cancelled'), { name: 'AbortError' });
            const attempts = error.attempts || [];
            throw new media_read_controller_1.MediaReadFailure(attempts.some(item => item.statusCode === 401 || item.statusCode === 403));
        }
        finally {
            signal.removeEventListener('abort', abort);
        }
    }, () => timer ? timer.now() : Infinity, event => { (0, api_1.track)('media_read', event); });
}
const media_read_controller_2 = require("./media-read-controller");
/** Bind these lifecycle methods to an existing page; no background refresh loop. */
class MiniappMediaScope {
    constructor() {
        this.controller = null;
        this.selection = new media_read_controller_2.MediaAbortController();
    }
    show() {
        this.hide();
        this.controller = createMiniappMediaReadController();
        this.selection = new media_read_controller_2.MediaAbortController();
    }
    hide() {
        var _a;
        this.selection.abort();
        (_a = this.controller) === null || _a === void 0 ? void 0 : _a.dispose();
        this.controller = null;
    }
    selectMedia() {
        this.selection.abort();
        this.selection = new media_read_controller_2.MediaAbortController();
    }
    read(ref, recover = false) {
        if (!this.controller)
            return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
        return recover ? this.controller.recover(ref, this.selection.signal) : this.controller.read(ref, { signal: this.selection.signal });
    }
    retry(ref) {
        if (!this.controller)
            return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
        return this.controller.manualRetry(ref, this.selection.signal);
    }
}
exports.MiniappMediaScope = MiniappMediaScope;
