type NavigationMetrics = {
  navHeight: number;
  navBarStyle: string;
  reserveStyle: string;
};

function resolveNavigationMetrics(): NavigationMetrics {
  const fallbackStatusBarHeight = 44;
  const fallbackContentHeight = 62;
  const fallbackReserveWidth = 92;
  try {
    const systemInfo = wx.getSystemInfoSync();
    const statusBarHeight = systemInfo.statusBarHeight || fallbackStatusBarHeight;
    const menuButton = typeof wx.getMenuButtonBoundingClientRect === 'function'
      ? wx.getMenuButtonBoundingClientRect()
      : null;
    const contentHeight = menuButton && menuButton.height
      ? Math.max(menuButton.height + 16, fallbackContentHeight)
      : fallbackContentHeight;
    const reserveWidth = menuButton && menuButton.width
      ? Math.max(systemInfo.windowWidth - menuButton.left + 8, fallbackReserveWidth)
      : fallbackReserveWidth;
    const navHeight = statusBarHeight + contentHeight;
    return {
      navHeight,
      navBarStyle: `height: ${navHeight}px; padding-top: ${statusBarHeight}px;`,
      reserveStyle: `width: ${reserveWidth}px; flex-basis: ${reserveWidth}px;`,
    };
  } catch (error) {
    const navHeight = fallbackStatusBarHeight + fallbackContentHeight;
    return {
      navHeight,
      navBarStyle: `height: ${navHeight}px; padding-top: ${fallbackStatusBarHeight}px;`,
      reserveStyle: `width: ${fallbackReserveWidth}px; flex-basis: ${fallbackReserveWidth}px;`,
    };
  }
}

Component({
  properties: {
    variant: { type: String, value: 'subpage' },
    title: { type: String, value: '' },
    subtitle: { type: String, value: '' },
    storeName: { type: String, value: '' },
    logoSrc: { type: String, value: '' },
  },

  data: {
    navHeight: 106,
    navBarStyle: 'height: 106px; padding-top: 44px;',
    reserveStyle: 'width: 92px; flex-basis: 92px;',
  },

  lifetimes: {
    attached() {
      this.setData(resolveNavigationMetrics());
    },
  },

  methods: {
    handleBack() {
      const pages = typeof getCurrentPages === 'function' ? getCurrentPages() : [];
      if (pages.length > 1) {
        wx.navigateBack({
          delta: 1,
          fail: () => wx.switchTab({ url: '/pages/index/index' }),
        });
        return;
      }
      wx.switchTab({
        url: '/pages/index/index',
        fail: () => wx.reLaunch({ url: '/pages/index/index' }),
      });
    },
  },
});
