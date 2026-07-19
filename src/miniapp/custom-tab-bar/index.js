Component({
  data: {
    selected: 0,
    color: '#8c8376',
    selectedColor: '#C8A055',
    list: [
      {
        pagePath: '/pages/index/index',
        text: '首页',
        iconPath: '/assets/tabbar/home-default.png',
        selectedIconPath: '/assets/tabbar/home-active.png',
      },
      {
        pagePath: '/pages/category/index',
        text: '分类',
        iconPath: '/assets/tabbar/category-default.png',
        selectedIconPath: '/assets/tabbar/category-active.png',
      },
      {
        pagePath: '/pages/find/index',
        text: '找砖',
        iconPath: '/assets/tabbar/find-default.png',
        selectedIconPath: '/assets/tabbar/find-active.png',
      },
      {
        pagePath: '/pages/favorites/index',
        text: '收藏',
        iconPath: '/assets/tabbar/profile-default.png',
        selectedIconPath: '/assets/tabbar/profile-active.png',
      },
      {
        pagePath: '/pages/certificates/index',
        text: '证书',
        iconPath: '/assets/tabbar/profile-default.png',
        selectedIconPath: '/assets/tabbar/profile-active.png',
      },
    ],
  },

  lifetimes: {
    attached() {
      const pages = getCurrentPages();
      const currentPage = pages.length ? pages[pages.length - 1] : null;
      const route = `/${(currentPage && currentPage.route) || 'pages/index/index'}`;
      const selected = this.data.list.findIndex((item) => item.pagePath === route);
      if (selected >= 0) {
        this.setData({ selected });
      }
    },
  },

  methods: {
    switchTab(event) {
      const { path, index } = event.currentTarget.dataset;
      const item = this.data.list[index];
      this.setData({ selected: index });
      if (item && item.text === '证书') {
        const pages = getCurrentPages();
        const currentPage = pages.length ? pages[pages.length - 1] : null;
        if (!currentPage || `/${currentPage.route}` !== path) {
          wx.switchTab({ url: path });
        }
        return;
      }
      wx.switchTab({ url: path });
    },
  },
});
