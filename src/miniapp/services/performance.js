const { miniappApiConfig } = require('../utils/env');

const CLIENT_TYPE = 'wechat_miniapp';
const SAMPLE_RATE = 1;
let cachedNetworkType = '';

function baseUrl() {
  try {
    const app = getApp();
    return (app.globalData && app.globalData.apiBaseUrl) || miniappApiConfig.apiBaseUrl;
  } catch (error) {
    return miniappApiConfig.apiBaseUrl;
  }
}

function appVersion() {
  try {
    const account = wx.getAccountInfoSync();
    return (account.miniProgram && account.miniProgram.version) || miniappApiConfig.environment || 'dev';
  } catch (error) {
    return miniappApiConfig.environment || 'dev';
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
