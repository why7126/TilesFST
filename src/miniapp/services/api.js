const DEFAULT_BASE_URL = 'http://localhost:8000';

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

function request(path, options = {}) {
  const urls = baseUrls();
  const attempts = [];

  function tryRequest(index) {
    const currentBaseUrl = urls[index] || DEFAULT_BASE_URL;
    const url = `${currentBaseUrl}${path}`;
    return new Promise((resolve, reject) => {
      wx.request({
        ...options,
        url,
        header: {
          'content-type': 'application/json',
          ...(options.header || {}),
        },
        success: (res) => {
          const body = res.data;
          if (res.statusCode >= 200 && res.statusCode < 300 && body && body.code === 0) {
            resolve(normalizeMediaUrls(body.data, currentBaseUrl));
            return;
          }
          attempts.push({
            url,
            statusCode: res.statusCode,
            message: (body && body.message) || `request failed: ${res.statusCode}`,
          });
          if (index + 1 < urls.length) {
            tryRequest(index + 1).then(resolve).catch(reject);
            return;
          }
          const error = new Error((body && body.message) || `request failed: ${res.statusCode}`);
          error.attempts = attempts;
          reject(error);
        },
        fail: (error) => {
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

module.exports = {
  request,
  track,
};
