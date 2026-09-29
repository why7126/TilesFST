// Generated from TypeScript; run node scripts/sync-media-read-controller.cjs.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.preparePageImages = void 0;
exports.acquirePageMedia = acquirePageMedia;
exports.beginPageMedia = beginPageMedia;
exports.endPageMedia = endPageMedia;
exports.readPageMedia = readPageMedia;
exports.isPageMediaActive = isPageMediaActive;
exports.reportPageMedia = reportPageMedia;
exports.preparePageFiles = preparePageFiles;
const media_read_1 = require("./media-read");
const pages = new WeakMap();
/** All visible image widgets on one page share batching and concurrency, without persistent URLs. */
function acquirePageMedia(owner) {
    const stack = getCurrentPages();
    const page = stack[stack.length - 1] || owner;
    let entry = pages.get(page);
    if (!entry) {
        entry = { controller: (0, media_read_1.createMiniappMediaReadController)(), owners: 0 };
        pages.set(page, entry);
    }
    entry.owners++;
    let released = false;
    return { controller: entry.controller, release: () => {
            if (released)
                return;
            released = true;
            if (--entry.owners === 0) {
                entry.controller.dispose();
                pages.delete(page);
            }
        } };
}
const media_read_controller_1 = require("./media-read-controller");
const activePages = new WeakMap();
function beginPageMedia(page) {
    endPageMedia(page);
    activePages.set(page, { scope: acquirePageMedia(page), abort: new media_read_controller_1.MediaAbortController(), downloads: new Set() });
}
function endPageMedia(page) {
    const value = activePages.get(page);
    if (value) {
        value.abort.abort();
        for (const cancel of value.downloads)
            cancel();
        value.scope.release();
        activePages.delete(page);
    }
}
function readPageMedia(page, reference, mode = 'fresh') {
    const value = activePages.get(page);
    if (!value)
        return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
    if (mode === 'manual')
        return value.scope.controller.manualRetry(reference, value.abort.signal);
    return mode === 'recover' ? value.scope.controller.recover(reference, value.abort.signal)
        : value.scope.controller.read(reference, { force: true, signal: value.abort.signal });
}
function isPageMediaActive(page) { return activePages.has(page); }
function reportPageMedia(page, reference, phase, result) {
    var _a;
    (_a = activePages.get(page)) === null || _a === void 0 ? void 0 : _a.scope.controller.report(reference, phase, result);
}
/** Native albums cannot renew remote URLs after opening. Prepare session-local files first. */
async function preparePageFiles(page, references) {
    var _a;
    const active = activePages.get(page);
    const cancelled = () => Object.assign(new Error('Cancelled'), { name: 'AbortError' });
    if (!active || references.length > 50)
        throw cancelled();
    (_a = active.cancelPreview) === null || _a === void 0 ? void 0 : _a.call(active);
    let stopped = false;
    const ownDownloads = new Set();
    const stop = () => { stopped = true; for (const cancel of ownDownloads)
        cancel(); };
    active.cancelPreview = stop;
    const descriptors = await Promise.all(references.map(reference => readPageMedia(page, reference)));
    if (stopped)
        throw cancelled();
    const files = new Array(references.length);
    let cursor = 0;
    async function download(url) {
        if (stopped || activePages.get(page) !== active)
            throw cancelled();
        let task;
        let cancel = () => { };
        try {
            return await new Promise((resolve, reject) => {
                cancel = () => { task === null || task === void 0 ? void 0 : task.abort(); reject(cancelled()); };
                active.downloads.add(cancel);
                ownDownloads.add(cancel);
                task = wx.downloadFile({ url, timeout: 10000,
                    success: result => result.statusCode === 200 && result.tempFilePath ? resolve(result.tempFilePath) : reject(new Error('文件暂不可读取')),
                    fail: () => reject(activePages.get(page) === active ? new Error('文件暂不可读取') : cancelled()),
                });
            });
        }
        finally {
            active.downloads.delete(cancel);
            ownDownloads.delete(cancel);
        }
    }
    await Promise.all(Array.from({ length: Math.min(4, references.length) }, async () => {
        while (!stopped && cursor < references.length) {
            const index = cursor++;
            let descriptor = descriptors[index];
            for (let attempt = 0; attempt < 3; attempt++) {
                try {
                    files[index] = await download(descriptor.url);
                    break;
                }
                catch (error) {
                    if (error.name === 'AbortError' || attempt === 2)
                        throw error;
                    descriptor = await readPageMedia(page, references[index], 'recover');
                }
            }
        }
    })).catch(error => { stop(); throw error; });
    if (stopped || activePages.get(page) !== active)
        throw cancelled();
    return files;
}
exports.preparePageImages = preparePageFiles;
