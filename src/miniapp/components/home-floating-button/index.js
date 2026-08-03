const HOME_URL = '/pages/index/index';
const UNLOCK_DELAY_MS = 800;

Component({
  properties: {
    show: { type: Boolean, value: true },
    offset: { type: String, value: 'default' },
  },

  data: {
    navigating: false,
    unlockTimer: 0,
  },

  lifetimes: {
    detached() {
      this.clearUnlockTimer();
    },
  },

  pageLifetimes: {
    show() {
      this.resetNavigationLock();
    },
  },

  methods: {
    clearUnlockTimer() {
      if (this.data.unlockTimer) {
        clearTimeout(this.data.unlockTimer);
        this.setData({ unlockTimer: 0 });
      }
    },

    resetNavigationLock() {
      this.clearUnlockTimer();
      this.setData({ navigating: false });
    },

    unlockNavigation() {
      this.clearUnlockTimer();
      const unlockTimer = setTimeout(() => {
        this.setData({ navigating: false, unlockTimer: 0 });
      }, UNLOCK_DELAY_MS);
      this.setData({ unlockTimer });
    },

    handleReturnHome() {
      if (this.data.navigating) return;

      this.setData({ navigating: true });
      wx.switchTab({
        url: HOME_URL,
        success: () => {
          this.triggerEvent('returnhome', { url: HOME_URL });
          this.unlockNavigation();
        },
        fail: () => {
          wx.reLaunch({
            url: HOME_URL,
            fail: () => {
              wx.showToast({ title: '暂时无法返回首页', icon: 'none' });
            },
            complete: () => this.unlockNavigation(),
          });
        },
      });
    },
  },
});
