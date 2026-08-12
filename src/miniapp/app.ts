import { miniappApiConfig } from './utils/env';
import { reportPerformanceMetric } from './services/performance';

App({
  onLaunch() {
    const launchedAt = Date.now();
    try {
      wx.removeStorageSync('miniapp_share_add_guide_session_closed_v1');
    } catch (error) {
      console.warn('[miniapp] reset share add guide session failed', error);
    }
    reportPerformanceMetric({
      page_key: 'app/launch',
      metric_name: 'app_launch_ready',
      duration_ms: Date.now() - launchedAt,
    });
  },

  globalData: {
    environment: miniappApiConfig.environment,
    apiBaseUrl: miniappApiConfig.apiBaseUrl,
    apiFallbackBaseUrls: miniappApiConfig.apiFallbackBaseUrls,
  },
});
