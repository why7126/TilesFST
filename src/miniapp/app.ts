import { miniappApiConfig } from './utils/env';

App({
  onLaunch() {
    try {
      wx.removeStorageSync('miniapp_share_add_guide_session_closed_v1');
    } catch (error) {
      console.warn('[miniapp] reset share add guide session failed', error);
    }
  },

  globalData: {
    environment: miniappApiConfig.environment,
    apiBaseUrl: miniappApiConfig.apiBaseUrl,
    apiFallbackBaseUrls: miniappApiConfig.apiFallbackBaseUrls,
  },
});
