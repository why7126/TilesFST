const DEFAULT_BASE_URL = 'http://localhost:8000';

type ApiResponse<T> = {
  code: number;
  message: string;
  data: T;
};

function baseUrl(): string {
  const app = getApp<{ globalData?: { apiBaseUrl?: string; apiFallbackBaseUrls?: string[] } }>();
  return app.globalData?.apiBaseUrl || DEFAULT_BASE_URL;
}

function baseUrls(): string[] {
  const app = getApp<{ globalData?: { apiBaseUrl?: string; apiFallbackBaseUrls?: string[] } }>();
  const fallbackUrls = app.globalData?.apiFallbackBaseUrls || [];
  return [baseUrl(), ...fallbackUrls].filter(
    (url, index, urls): url is string => Boolean(url) && urls.indexOf(url) === index,
  );
}

function mediaUrl(value: unknown, currentBaseUrl: string): unknown {
  if (typeof value === 'string' && value.indexOf('/media/') === 0) {
    return `${currentBaseUrl}${value}`;
  }
  return value;
}

function normalizeMediaUrls(value: unknown, currentBaseUrl: string): unknown {
  if (Array.isArray(value)) {
    return value.map((item) => normalizeMediaUrls(item, currentBaseUrl));
  }
  if (value && typeof value === 'object') {
    const next: Record<string, unknown> = {};
    Object.keys(value as Record<string, unknown>).forEach((key) => {
      next[key] = normalizeMediaUrls((value as Record<string, unknown>)[key], currentBaseUrl);
    });
    return next;
  }
  return mediaUrl(value, currentBaseUrl);
}

export function request<T>(path: string, options: WechatMiniprogram.RequestOption = {}): Promise<T> {
  const urls = baseUrls();
  const attempts: Array<{
    url: string;
    statusCode?: number;
    message?: string;
    errMsg?: string;
  }> = [];

  function tryRequest(index: number): Promise<T> {
    const currentBaseUrl = urls[index] || DEFAULT_BASE_URL;
    const url = `${currentBaseUrl}${path}`;
    return new Promise((resolve, reject) => {
      wx.request<ApiResponse<T>>({
        ...options,
        url,
        header: {
          'content-type': 'application/json',
          ...(options.header || {}),
        },
        success: (res) => {
          const body = res.data;
          if (res.statusCode >= 200 && res.statusCode < 300 && body?.code === 0) {
            resolve(normalizeMediaUrls(body.data, currentBaseUrl) as T);
            return;
          }
          attempts.push({
            url,
            statusCode: res.statusCode,
            message: body?.message || `request failed: ${res.statusCode}`,
          });
          if (index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          const error = new Error(body?.message || `request failed: ${res.statusCode}`) as Error & {
            attempts?: typeof attempts;
          };
          error.attempts = attempts;
          reject(error);
        },
        fail: (error) => {
          attempts.push({
            url,
            errMsg: error.errMsg,
          });
          if (index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          (error as WechatMiniprogram.GeneralCallbackResult & { attempts?: typeof attempts }).attempts =
            attempts;
          reject(error);
        },
      });
    });
  }

  return tryRequest(0);
}

export function track(eventName: string, properties: Record<string, unknown>): void {
  request('/api/v1/usage-events', {
    method: 'POST',
    data: {
      event_name: eventName,
      client_type: 'wechat_miniapp',
      page_path: String(properties.page_path || ''),
      properties: {
        ...properties,
        client_type: 'wechat_miniapp',
      },
    },
  }).catch(() => {
    // 埋点失败不阻断用户浏览、分享或咨询。
  });
}
