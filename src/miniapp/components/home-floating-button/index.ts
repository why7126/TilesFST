const HOME_URL = '/pages/index/index';
const UNLOCK_DELAY_MS = 800;
const LOCK_TIMEOUT_MS = 1600;

Component({
  properties: {
    show: { type: Boolean, value: true },
    offset: { type: String, value: 'default' },
  },

  data: {
    navigating: false,
    unlockTimer: 0,
    lockStartedAt: 0,
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
      this.setData({ navigating: false, lockStartedAt: 0 });
    },

    unlockNavigation() {
      this.clearUnlockTimer();
      const unlockTimer = setTimeout(() => {
        this.setData({ navigating: false, unlockTimer: 0, lockStartedAt: 0 });
      }, UNLOCK_DELAY_MS);
      this.setData({ unlockTimer });
    },

    isNavigationLocked() {
      if (!this.data.navigating) return false;

      const startedAt = this.data.lockStartedAt || 0;
      if (startedAt && Date.now() - startedAt > LOCK_TIMEOUT_MS) {
        this.resetNavigationLock();
        return false;
      }

      return true;
    },

    handleReturnHome() {
      if (this.isNavigationLocked()) return;

      let fallbackStarted = false;
      this.setData({ navigating: true, lockStartedAt: Date.now() });
      wx.switchTab({
        url: HOME_URL,
        success: () => {
          this.triggerEvent('returnhome', { url: HOME_URL });
        },
        fail: () => {
          fallbackStarted = true;
          wx.reLaunch({
            url: HOME_URL,
            fail: () => {
              wx.showToast({ title: '暂时无法返回首页', icon: 'none' });
            },
            complete: () => this.unlockNavigation(),
          });
        },
        complete: () => {
          if (!fallbackStarted) {
            this.unlockNavigation();
          }
        },
      });
    },
  },
});
