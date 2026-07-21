const { request, track } = require('../../services/api');

const CATEGORY_CACHE_KEY = 'miniapp_category_tree_cache_v1';
const CATEGORY_PAGE_STATE_KEY = 'miniapp_category_page_state_v1';
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;
const CLICK_DEBOUNCE_MS = 300;

function normalizeTree(data) {
  return {
    version: data.version || 'empty',
    items: data.items || [],
  };
}

Page({
  data: {
    categories: [],
    currentPrimaryId: 0,
    currentPrimaryName: '',
    currentChildren: [],
    loading: true,
    refreshing: false,
    error: '',
    hasCache: false,
    leftScrollTop: 0,
    rightScrollTop: 0,
  },

  onLoad() {
    const cached = this.readCache();
    const savedState = this.readSavedState();
    if (cached) {
      this.applyTree(cached, savedState.currentPrimaryId, { fromCache: true });
    }
    track('category_page_view', {
      page_path: '/pages/category/index',
      has_cache: Boolean(cached),
    });
    this.fetchTree(Boolean(cached));
  },

  onShow() {
    const tabBar = this.getTabBar && this.getTabBar();
    if (tabBar) {
      tabBar.setData({ selected: 1 });
    }
    const savedState = this.readSavedState();
    if (this.data.categories.length && savedState.currentPrimaryId) {
      this.selectPrimaryById(savedState.currentPrimaryId, { trackClick: false });
      this.setData({
        leftScrollTop: savedState.leftScrollTop || 0,
        rightScrollTop: savedState.rightScrollTop || 0,
      });
    }
  },

  onHide() {
    this.savePageState();
  },

  onUnload() {
    this.savePageState();
  },

  readCache() {
    try {
      const cache = wx.getStorageSync(CATEGORY_CACHE_KEY);
      if (!cache || !Array.isArray(cache.items)) {
        return null;
      }
      if (cache.cachedAt && Date.now() - cache.cachedAt > CACHE_TTL_MS) {
        return null;
      }
      return { version: cache.version, items: cache.items };
    } catch (error) {
      return null;
    }
  },

  readSavedState() {
    try {
      return wx.getStorageSync(CATEGORY_PAGE_STATE_KEY) || {};
    } catch (error) {
      return {};
    }
  },

  savePageState() {
    wx.setStorage({
      key: CATEGORY_PAGE_STATE_KEY,
      data: {
        currentPrimaryId: this.data.currentPrimaryId,
        leftScrollTop: this.data.leftScrollTop,
        rightScrollTop: this.data.rightScrollTop,
      },
    });
  },

  fetchTree(hasCache) {
    this.setData({ refreshing: hasCache, loading: !hasCache, error: '' });
    request('/api/v1/miniapp/categories/tree?depth=2')
      .then((payload) => {
        const tree = normalizeTree(payload);
        const currentId = this.data.currentPrimaryId;
        this.applyTree(tree, currentId, { fromCache: false });
        wx.setStorage({
          key: CATEGORY_CACHE_KEY,
          data: {
            version: tree.version,
            cachedAt: Date.now(),
            items: tree.items,
          },
        });
      })
      .catch(() => {
        track('category_load_failed', {
          page_path: '/pages/category/index',
          error_code: 'request_failed',
          has_cache: hasCache,
        });
        this.setData({
          loading: false,
          refreshing: false,
          hasCache,
          error: hasCache ? '' : '分类加载失败，请检查网络后重试',
        });
        if (hasCache) {
          wx.showToast({ title: '网络异常，已展示缓存', icon: 'none' });
        }
      });
  },

  applyTree(tree, preferredId, options) {
    const categories = tree.items || [];
    const preferred = categories.find((item) => item.id === preferredId);
    const current = preferred || categories[0];
    this.setData({
      categories,
      currentPrimaryId: current ? current.id : 0,
      currentPrimaryName: current ? current.name : '',
      currentChildren: current ? current.children : [],
      loading: false,
      refreshing: false,
      error: '',
      hasCache: options.fromCache,
      rightScrollTop: preferred ? this.data.rightScrollTop : 0,
    });
  },

  selectPrimary(event) {
    const id = Number(event.currentTarget.dataset.id);
    const index = Number(event.currentTarget.dataset.index);
    this.selectPrimaryById(id, { trackClick: true, index });
  },

  selectPrimaryById(id, options) {
    const current = this.data.categories.find((item) => item.id === id) || this.data.categories[0];
    if (!current) {
      return;
    }
    this.setData({
      currentPrimaryId: current.id,
      currentPrimaryName: current.name,
      currentChildren: current.children,
      rightScrollTop: 0,
    });
    if (options.trackClick) {
      track('primary_category_click', {
        page_path: '/pages/category/index',
        category_id: current.id,
        category_index: options.index || 0,
      });
    }
  },

  onLeftScroll(event) {
    this.setData({ leftScrollTop: event.detail.scrollTop });
  },

  onRightScroll(event) {
    this.setData({ rightScrollTop: event.detail.scrollTop });
  },

  retryLoad() {
    this.fetchTree(false);
  },

  openPrimaryProducts(event) {
    const now = Date.now();
    if (this.lastPrimaryProductClickAt && now - this.lastPrimaryProductClickAt < CLICK_DEBOUNCE_MS) {
      return;
    }
    this.lastPrimaryProductClickAt = now;
    const id = Number(event.currentTarget.dataset.id || this.data.currentPrimaryId);
    const name = String(event.currentTarget.dataset.name || this.data.currentPrimaryName || '');
    const index = this.data.categories.findIndex((item) => item.id === id);
    if (!id || !name) {
      wx.showToast({ title: '该分类暂未上架商品', icon: 'none' });
      return;
    }
    track('primary_category_product_list_click', {
      page_path: '/pages/category/index',
      category_id: id,
      category_name: name,
      category_level: 'primary',
      sourcePage: 'category',
      category_index: index >= 0 ? index : 0,
      action: 'product_list_entry',
    });
    wx.navigateTo({
      url: `/pages/product-list/index?categoryId=${id}&categoryName=${encodeURIComponent(name)}&categoryLevel=primary&sourcePage=category`,
      fail: () => {
        wx.showToast({ title: '页面打开失败，请重试', icon: 'none' });
      },
    });
  },

  openSecondary(event) {
    const now = Date.now();
    if (this.lastSecondaryClickAt && now - this.lastSecondaryClickAt < CLICK_DEBOUNCE_MS) {
      return;
    }
    this.lastSecondaryClickAt = now;
    const id = Number(event.currentTarget.dataset.id);
    const name = String(event.currentTarget.dataset.name || '');
    const index = Number(event.currentTarget.dataset.index);
    track('secondary_category_click', {
      page_path: '/pages/category/index',
      category_id: id,
      category_name: name,
      category_level: 'secondary',
      parent_category_id: this.data.currentPrimaryId,
      category_index: index,
      sourcePage: 'category',
      action: 'product_list_entry',
    });
    wx.navigateTo({
      url: `/pages/product-list/index?categoryId=${id}&categoryName=${encodeURIComponent(name)}&categoryLevel=secondary&sourcePage=category`,
      fail: () => {
        wx.showToast({ title: '页面打开失败，请重试', icon: 'none' });
      },
    });
  },

  lastPrimaryProductClickAt: 0,
  lastSecondaryClickAt: 0,
});
