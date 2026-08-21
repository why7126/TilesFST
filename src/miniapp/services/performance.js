const { miniappApiConfig } = require('../utils/env');
const { PRODUCT_VERSION } = require('../utils/product-version');

const CLIENT_TYPE = 'wechat_miniapp';
const SAMPLE_RATE = 1;
let cachedNetworkType = '';
let cachedBaseUrl = '';

function baseUrls() {
  try {
    const app = getApp();
    const fallbackUrls = (app.globalData && app.globalData.apiFallbackBaseUrls) || miniappApiConfig.apiFallbackBaseUrls;
    return [
      cachedBaseUrl,
      (app.globalData && app.globalData.apiBaseUrl) || miniappApiConfig.apiBaseUrl,
      ...fallbackUrls,
    ].filter((url, index, urls) => url && urls.indexOf(url) === index);
  } catch (error) {
    return [cachedBaseUrl, miniappApiConfig.apiBaseUrl, ...miniappApiConfig.apiFallbackBaseUrls].filter(
      (url, index, urls) => url && urls.indexOf(url) === index,
    );
  }
}

function appVersion() {
  try {
    const account = wx.getAccountInfoSync();
    return (account.miniProgram && account.miniProgram.version) || PRODUCT_VERSION;
  } catch (error) {
    return PRODUCT_VERSION;
  }
}

function createRumRequestId() {
  try {
    return `miniapp-rum:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch (error) {
    return undefined;
  }
}

function normalizePageKey(value) {
  return String(value || '').replace(/^\//, '').split('?')[0] || 'miniapp/unknown';
}

function resolveNetworkType(input, callback) {
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
      cachedNetworkType = (result && result.networkType) || 'unknown';
      callback(cachedNetworkType);
    },
    fail: () => {
      callback('unknown');
    },
  });
}

function reportPerformanceMetric(metric) {
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
    const tryReport = (index) => {
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
          if (result && result.statusCode >= 500 && index + 1 < urls.length) {
            tryReport(index + 1);
            return;
          }
          if (result && result.statusCode >= 200 && result.statusCode < 300) {
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

function createPagePerformanceTracker(pageKey) {
  const startedAt = Date.now();
  return {
    mark(metricName) {
      reportPerformanceMetric({
        page_key: pageKey,
        metric_name: metricName,
        duration_ms: Date.now() - startedAt,
      });
    },
  };
}

module.exports = {
  reportPerformanceMetric,
  createPagePerformanceTracker,
};
