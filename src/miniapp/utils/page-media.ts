import { createMiniappMediaReadController } from './media-read';
const pages = new WeakMap<object, { controller: ReturnType<typeof createMiniappMediaReadController>; owners: number }>();
/** All visible image widgets on one page share batching and concurrency, without persistent URLs. */
export function acquirePageMedia(owner: object) {
  const stack = getCurrentPages();
  const page = stack[stack.length - 1] || owner;
  let entry = pages.get(page);
  if (!entry) { entry = { controller: createMiniappMediaReadController(), owners: 0 }; pages.set(page, entry); }
  entry.owners++;
  let released = false;
  return { controller: entry.controller, release: () => {
    if (released) return;
    released = true;
    if (--entry!.owners === 0) { entry!.controller.dispose(); pages.delete(page); }
  } };
}

import { MediaAbortController } from './media-read-controller';
import type { MediaReadReference } from '../../web/src/shared/api/generated';
const activePages = new WeakMap<object, { scope: ReturnType<typeof acquirePageMedia>; abort: MediaAbortController; downloads: Set<() => void>; cancelPreview?: () => void }>();
export function beginPageMedia(page: object) {
  endPageMedia(page);
  activePages.set(page, { scope: acquirePageMedia(page), abort: new MediaAbortController(), downloads: new Set() });
}
export function endPageMedia(page: object) {
  const value = activePages.get(page);
  if (value) { value.abort.abort(); for (const cancel of value.downloads) cancel(); value.scope.release(); activePages.delete(page); }
}
export function readPageMedia(page: object, reference: MediaReadReference, mode: 'fresh' | 'recover' | 'manual' = 'fresh') {
  const value = activePages.get(page);
  if (!value) return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
  if (mode === 'manual') return value.scope.controller.manualRetry(reference, value.abort.signal);
  return mode === 'recover' ? value.scope.controller.recover(reference, value.abort.signal)
    : value.scope.controller.read(reference, { force: true, signal: value.abort.signal });
}
export function isPageMediaActive(page: object) { return activePages.has(page); }
export function reportPageMedia(page: object, reference: MediaReadReference, phase: import('./media-read-controller').MediaReadObservation['phase'], result: import('./media-read-controller').MediaReadObservation['outcome']) {
  activePages.get(page)?.scope.controller.report(reference, phase, result);
}

/** Native albums cannot renew remote URLs after opening. Prepare session-local files first. */
export async function preparePageFiles(page: object, references: MediaReadReference[]): Promise<string[]> {
  const active = activePages.get(page);
  const cancelled = () => Object.assign(new Error('Cancelled'), {name:'AbortError'});
  if (!active || references.length > 50) throw cancelled();
  active.cancelPreview?.();
  let stopped = false;
  const ownDownloads = new Set<() => void>();
  const stop = () => { stopped = true; for (const cancel of ownDownloads) cancel(); };
  active.cancelPreview = stop;
  const descriptors = await Promise.all(references.map(reference => readPageMedia(page, reference)));
  if (stopped) throw cancelled();
  const files = new Array<string>(references.length);
  let cursor = 0;
  async function download(url: string): Promise<string> {
    if (stopped || activePages.get(page) !== active) throw cancelled();
    let task: WechatMiniprogram.DownloadTask | undefined;
    let cancel: () => void = () => {};
    try {
      return await new Promise<string>((resolve,reject) => {
        cancel = () => { task?.abort(); reject(cancelled()); };
        active!.downloads.add(cancel); ownDownloads.add(cancel);
        task = wx.downloadFile({url,timeout:10000,
          success: result => result.statusCode === 200 && result.tempFilePath ? resolve(result.tempFilePath) : reject(new Error('文件暂不可读取')),
          fail: () => reject(activePages.get(page) === active ? new Error('文件暂不可读取') : cancelled()),
        });
      });
    } finally { active!.downloads.delete(cancel); ownDownloads.delete(cancel); }
  }
  await Promise.all(Array.from({length:Math.min(4,references.length)},async () => {
    while (!stopped && cursor < references.length) {
      const index = cursor++;
      let descriptor = descriptors[index];
      for (let attempt=0;attempt<3;attempt++) {
        try { files[index] = await download(descriptor.url); break; }
        catch (error) {
          if ((error as Error).name === 'AbortError' || attempt === 2) throw error;
          descriptor = await readPageMedia(page,references[index],'recover');
        }
      }
    }
  })).catch(error => { stop(); throw error; });
  if (stopped || activePages.get(page) !== active) throw cancelled();
  return files;
}

export const preparePageImages = preparePageFiles;
