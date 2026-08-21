import { miniappApiConfig } from '../utils/env';
import { PRODUCT_VERSION } from '../utils/product-version';

const CLIENT_TYPE = 'wechat_miniapp';
const SAMPLE_RATE = 1;
let cachedNetworkType = '';
let cachedBaseUrl = '';

type PerformanceMetric = {
  page_key: string;
  metric_name: string;
  duration_ms: number;
  app_version?: string;
  network_type?: string;
  device_class?: string;
  occurred_at?: string;
  request_id?: string;
};

function baseUrls(): string[] {
  try {
    const app = getApp<{
      globalData?: { apiBaseUrl?: string; apiFallbackBaseUrls?: string[] };
    }>();
    const fallbackUrls = app.globalData?.apiFallbackBaseUrls || miniappApiConfig.apiFallbackBaseUrls;
    return [cachedBaseUrl, app.globalData?.apiBaseUrl || miniappApiConfig.apiBaseUrl, ...fallbackUrls].filter(
      (url, index, urls): url is string => Boolean(url) && urls.indexOf(url) === index,
    );
  } catch {
    return [cachedBaseUrl, miniappApiConfig.apiBaseUrl, ...miniappApiConfig.apiFallbackBaseUrls].filter(
      (url, index, urls): url is string => Boolean(url) && urls.indexOf(url) === index,
    );
  }
}

function appVersion(): string {
  try {
    const account = wx.getAccountInfoSync();
    return account.miniProgram.version || PRODUCT_VERSION;
  } catch {
    return PRODUCT_VERSION;
  }
}

function createRumRequestId(): string | undefined {
  try {
    return `miniapp-rum:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch {
    return undefined;
  }
}

function normalizePageKey(value: string): string {
  return value.replace(/^\//, '').split('?')[0] || 'miniapp/unknown';
}

function resolveNetworkType(input: string | undefined, callback: (networkType: string) => void): void {
  if (input) {
    callback(input);
    return;
  }
  if (cachedNetworkType) {
    callback(cachedNetworkType);
    return;
  }
  wx.getNetworkType({
    success: (result) => {
      cachedNetworkType = result.networkType || 'unknown';
      callback(cachedNetworkType);
    },
    fail: () => {
      callback('unknown');
    },
  });
}

export function reportPerformanceMetric(metric: PerformanceMetric): void {
  if (!Number.isFinite(metric.duration_ms) || metric.duration_ms < 0) {
    return;
  }
  resolveNetworkType(metric.network_type, (networkType) => {
    const urls = baseUrls();
    const event = {
      client_type: CLIENT_TYPE,
      page_key: normalizePageKey(metric.page_key),
      app_version: metric.app_version || appVersion(),
      network_type: networkType,
      device_class: metric.device_class || 'miniapp',
      metric_name: metric.metric_name,
      duration_ms: Math.round(metric.duration_ms),
      sample_rate: SAMPLE_RATE,
      occurred_at: metric.occurred_at || new Date().toISOString(),
      request_id: metric.request_id || createRumRequestId(),
    };
    const tryReport = (index: number): void => {
      const currentBaseUrl = urls[index] || miniappApiConfig.apiBaseUrl;
      wx.request({
        url: `${currentBaseUrl}/api/v1/performance-events`,
        method: 'POST',
        data: {
          events: [event],
        },
        header: {
          'content-type': 'application/json',
          'x-client-type': CLIENT_TYPE,
        },
        success: (result) => {
          if (result.statusCode >= 500 && index + 1 < urls.length) {
            tryReport(index + 1);
            return;
          }
          if (result.statusCode >= 200 && result.statusCode < 300) {
            cachedBaseUrl = currentBaseUrl;
          }
        },
        fail: () => {
          if (index + 1 < urls.length) {
            tryReport(index + 1);
          }
          // RUM 上报失败不阻断小程序主流程。
        },
      });
    };
    tryReport(0);
  });
}

export function createPagePerformanceTracker(pageKey: string) {
  const startedAt = Date.now();
  return {
    mark(metricName: string) {
      reportPerformanceMetric({
        page_key: pageKey,
        metric_name: metricName,
        duration_ms: Date.now() - startedAt,
      });
    },
  };
}
