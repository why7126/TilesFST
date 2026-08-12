import { miniappApiConfig } from '../utils/env';

const CLIENT_TYPE = 'wechat_miniapp';
const SAMPLE_RATE = 1;
let cachedNetworkType = '';

type PerformanceMetric = {
  page_key: string;
  metric_name: string;
  duration_ms: number;
  app_version?: string;
  network_type?: string;
  device_class?: string;
  occurred_at?: string;
};

function baseUrl(): string {
  try {
    const app = getApp<{
      globalData?: { apiBaseUrl?: string };
    }>();
    return app.globalData?.apiBaseUrl || miniappApiConfig.apiBaseUrl;
  } catch {
    return miniappApiConfig.apiBaseUrl;
  }
}

function appVersion(): string {
  try {
    const account = wx.getAccountInfoSync();
    return account.miniProgram.version || miniappApiConfig.environment || 'dev';
  } catch {
    return miniappApiConfig.environment || 'dev';
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
    wx.request({
      url: `${baseUrl()}/api/v1/performance-events`,
      method: 'POST',
      data: {
        events: [
          {
            client_type: CLIENT_TYPE,
            page_key: normalizePageKey(metric.page_key),
            app_version: metric.app_version || appVersion(),
            network_type: networkType,
            device_class: metric.device_class || 'miniapp',
            metric_name: metric.metric_name,
            duration_ms: Math.round(metric.duration_ms),
            sample_rate: SAMPLE_RATE,
            occurred_at: metric.occurred_at || new Date().toISOString(),
          },
        ],
      },
      header: {
        'content-type': 'application/json',
        'x-client-type': CLIENT_TYPE,
      },
      fail: () => {
        // RUM 上报失败不阻断小程序主流程。
      },
    });
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
