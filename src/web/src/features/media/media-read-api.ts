import axios from 'axios';
import { api } from '@/features/auth/api/auth-api';
import { MediaReadController, MediaReadFailure } from './read-controller';
import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';

/** Scope is selected by the page, never forwarded as an authorization claim. */
export function createMediaReadController(scope: 'public' | 'admin') {
  return new MediaReadController(async (items, signal) => {
    const controller = new AbortController();
    const cancel = () => controller.abort();
    signal.addEventListener('abort', cancel);
    if (signal.aborted) controller.abort();
    try {
      const response = scope === 'admin'
        ? await api.authorizeAdminMediaApiV1AdminMediaReadAuthorizationsPost({ items }, { signal: controller.signal, timeout: 10000 })
        : await api.authorizePublicMediaApiV1MediaReadAuthorizationsPost({ items }, { signal: controller.signal, timeout: 10000 });
      if (!response.data.data) throw new MediaReadFailure(false);
      return response.data.data;
    } catch (error) {
      if (signal.aborted) throw new DOMException('Cancelled', 'AbortError');
      // Keep Axios request/config and signed URLs out of rendering/telemetry errors.
      throw new MediaReadFailure(axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0));
    } finally {
      signal.removeEventListener('abort', cancel);
    }
  }, () => performance.now(), event => { void trackUsageEvent('media_read', event, {clientType: scope === 'admin' ? 'web_admin' : 'web_catalog'}); });
}
