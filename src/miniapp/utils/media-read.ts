import { request, track } from '../services/api';
import { MediaReadController, MediaReadFailure } from './media-read-controller';
import type { MediaReadData } from '../../web/src/shared/api/generated';

/** Page-owned instance: onHide/dispose cancels all work; onShow creates a fresh instance. */
export function createMiniappMediaReadController() {
  const timer = typeof wx.getPerformance === 'function' ? wx.getPerformance() : null;
  return new MediaReadController(async (items, signal) => {
    let task: WechatMiniprogram.RequestTask | undefined;
    const abort = () => task?.abort();
    signal.addEventListener('abort', abort);
    try {
      return await request<MediaReadData>('/api/v1/media/read-authorizations', {
        method: 'POST', data: { items }, timeout: 10000, singleAttempt: true,
        onRequestTask: value => { task = value; if (signal.aborted) task.abort(); },
      });
    } catch (error) {
      if (signal.aborted) throw Object.assign(new Error('Cancelled'), { name: 'AbortError' });
      const attempts = (error as { attempts?: { statusCode?: number }[] }).attempts || [];
      throw new MediaReadFailure(attempts.some(item => item.statusCode === 401 || item.statusCode === 403));
    } finally {
      signal.removeEventListener('abort', abort);
    }
  }, () => timer ? timer.now() : Infinity, event => { track('media_read', event); });
}

import { MediaAbortController } from './media-read-controller';
import type { MediaReadReference } from '../../web/src/shared/api/generated';

/** Bind these lifecycle methods to an existing page; no background refresh loop. */
export class MiniappMediaScope {
  private controller: MediaReadController | null = null;
  private selection = new MediaAbortController();

  show() {
    this.hide();
    this.controller = createMiniappMediaReadController();
    this.selection = new MediaAbortController();
  }
  hide() {
    this.selection.abort();
    this.controller?.dispose();
    this.controller = null;
  }
  selectMedia() {
    this.selection.abort();
    this.selection = new MediaAbortController();
  }
  read(ref: MediaReadReference, recover = false) {
    if (!this.controller) return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
    return recover ? this.controller.recover(ref, this.selection.signal) : this.controller.read(ref, { signal: this.selection.signal });
  }
  retry(ref: MediaReadReference) {
    if (!this.controller) return Promise.reject(Object.assign(new Error('Cancelled'), { name: 'AbortError' }));
    return this.controller.manualRetry(ref, this.selection.signal);
  }
}
