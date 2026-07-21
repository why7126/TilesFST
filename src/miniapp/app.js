App({
  onLaunch() {
    try {
      wx.removeStorageSync('miniapp_share_add_guide_session_closed_v1');
    } catch (error) {
      console.warn('[miniapp] reset share add guide session failed', error);
    }
  },

  globalData: {
    apiBaseUrl: 'http://127.0.0.1:8010',
    apiFallbackBaseUrls: ['http://localhost:8010', 'http://localhost:8000'],
  },
});
