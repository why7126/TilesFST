const { miniappApiConfig } = require('../utils/env');
const { reportPerformanceMetric } = require('./performance');

const DEFAULT_BASE_URL = miniappApiConfig.apiBaseUrl;
const CLIENT_TYPE = 'wechat_miniapp';
const CLIENT_REQUEST_ID_PREFIX = 'miniapp';
const BEHAVIOR_TRACE_ID_PREFIX = 'bt:miniapp';
const BEHAVIOR_EVENT_ID_PREFIX = 'be:miniapp';

let activeBehaviorContext = null;

function baseUrl() {
  const app = getApp();
  return (app.globalData && app.globalData.apiBaseUrl) || DEFAULT_BASE_URL;
}

function baseUrls() {
  const app = getApp();
  const fallbackUrls = (app.globalData && app.globalData.apiFallbackBaseUrls) || [];
  return [baseUrl(), ...fallbackUrls].filter((url, index, urls) => url && urls.indexOf(url) === index);
}

function mediaUrl(value, currentBaseUrl) {
  if (typeof value === 'string' && value.indexOf('/media/') === 0) {
    return `${currentBaseUrl}${value}`;
  }
  return value;
}

function normalizeMediaUrls(value, currentBaseUrl) {
  if (Array.isArray(value)) {
    return value.map((item) => normalizeMediaUrls(item, currentBaseUrl));
  }
  if (value && typeof value === 'object') {
    const next = {};
    Object.keys(value).forEach((key) => {
      next[key] = normalizeMediaUrls(value[key], currentBaseUrl);
    });
    return next;
  }
  return mediaUrl(value, currentBaseUrl);
}

function createClientRequestId() {
  try {
    return `${CLIENT_REQUEST_ID_PREFIX}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch (error) {
    return undefined;
  }
}

function createBehaviorId(prefix) {
  try {
    return `${prefix}:${Date.now().toString(36)}:${Math.random().toString(36).slice(2, 10)}`;
  } catch (error) {
    return undefined;
  }
}

function setActiveBehaviorContext(behaviorTraceId, behaviorEventId) {
  activeBehaviorContext = behaviorTraceId && behaviorEventId ? { behaviorTraceId, behaviorEventId } : null;
}

function cleanProperties(properties) {
  const next = {};
  Object.keys(properties).forEach((key) => {
    const value = properties[key];
    if (value !== undefined && value !== null) {
      next[key] = value;
    }
  });
  return next;
}

function isTelemetryPath(path) {
  return path.indexOf('/api/v1/usage-events') === 0 || path.indexOf('/api/v1/performance-events') === 0;
}

function request(path, options = {}) {
  const skipPerformanceTracking = Boolean(options.skipPerformanceTracking);
  const behaviorTraceId = options.behaviorTraceId;
  const behaviorEventId = options.behaviorEventId;
  const requestOptions = { ...options };
  delete requestOptions.skipPerformanceTracking;
  delete requestOptions.behaviorTraceId;
  delete requestOptions.behaviorEventId;
  const shouldReportPerformance = !skipPerformanceTracking && !isTelemetryPath(path);
  const urls = baseUrls();
  const clientRequestId = createClientRequestId();
  const behaviorContext = activeBehaviorContext;
  const effectiveBehaviorTraceId = behaviorTraceId || (behaviorContext && behaviorContext.behaviorTraceId);
  const effectiveBehaviorEventId = behaviorEventId || (behaviorContext && behaviorContext.behaviorEventId);
  const attempts = [];

  function tryRequest(index) {
    const currentBaseUrl = urls[index] || DEFAULT_BASE_URL;
    const url = `${currentBaseUrl}${path}`;
    const startedAt = Date.now();
    return new Promise((resolve, reject) => {
      wx.request({
        ...requestOptions,
        url,
        header: {
          'content-type': 'application/json',
          ...(requestOptions.header || {}),
          'x-client-type': CLIENT_TYPE,
          ...(clientRequestId ? { 'x-client-request-id': clientRequestId } : {}),
          ...(effectiveBehaviorTraceId ? { 'x-behavior-trace-id': effectiveBehaviorTraceId } : {}),
          ...(effectiveBehaviorEventId ? { 'x-behavior-event-id': effectiveBehaviorEventId } : {}),
        },
        success: (res) => {
          const body = res.data;
          if (shouldReportPerformance) {
            reportPerformanceMetric({
              page_key: path,
              metric_name: 'api_duration',
              duration_ms: Date.now() - startedAt,
              device_class: 'miniapp',
              request_id: clientRequestId,
            });
          }
          if (res.statusCode >= 200 && res.statusCode < 300 && body && body.code === 0) {
            resolve(normalizeMediaUrls(body.data, currentBaseUrl));
            return;
          }
          attempts.push({
            url,
            statusCode: res.statusCode,
            message: (body && body.message) || `request failed: ${res.statusCode}`,
          });
          if (res.statusCode >= 500 && index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          const error = new Error((body && body.message) || `request failed: ${res.statusCode}`);
          error.attempts = attempts;
          reject(error);
        },
        fail: (error) => {
          if (shouldReportPerformance) {
            reportPerformanceMetric({
              page_key: path,
              metric_name: 'api_failed_duration',
              duration_ms: Date.now() - startedAt,
              device_class: 'miniapp',
              request_id: clientRequestId,
            });
          }
          attempts.push({
            url,
            errMsg: error && error.errMsg,
          });
          if (index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          if (error) {
            error.attempts = attempts;
          }
          reject(error);
        },
      });
    });
  }

  return tryRequest(0);
}

function track(eventName, properties) {
  const cleanedProperties = cleanProperties(properties);
  const behaviorTraceId = createBehaviorId(BEHAVIOR_TRACE_ID_PREFIX);
  const behaviorEventId = createBehaviorId(BEHAVIOR_EVENT_ID_PREFIX);
  setActiveBehaviorContext(behaviorTraceId, behaviorEventId);
  request('/api/v1/usage-events', {
    method: 'POST',
    skipPerformanceTracking: true,
    behaviorTraceId,
    behaviorEventId,
    data: {
      event_name: eventName,
      client_type: CLIENT_TYPE,
      page_path: String(cleanedProperties.page_path || ''),
      client_request_id: createClientRequestId(),
      behavior_trace_id: behaviorTraceId,
      behavior_event_id: behaviorEventId,
      properties: {
        ...cleanedProperties,
        client_type: CLIENT_TYPE,
        behavior_trace_id: behaviorTraceId,
        behavior_event_id: behaviorEventId,
      },
    },
  }).catch(() => {
    // 埋点失败不阻断用户浏览、分享或咨询。
  });
}

module.exports = {
  request,
  track,
};
