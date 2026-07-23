const { request, track } = require('../../services/api');

const PAGE_SIZE = 12;
const SHARE_ADD_GUIDE_SESSION_KEY = 'miniapp_share_add_guide_session_closed_v1';
const HOME_SHARE_PATH = '/pages/index/index?source=share';
let shareAddGuideDismissedInSession = false;

const QUICK_ENTRIES = [
  { key: 'select', title: '选瓷砖', icon: '▦', url: '/pages/category/index' },
  { key: 'brand', title: '品牌', icon: '▣', url: '/pages/brand-list/index' },
  { key: 'new', title: '新品榜', icon: 'NEW', section: 'new' },
  { key: 'hot', title: '热销榜', icon: '♨', section: 'hot' },
];

Page({
  data: {
    loading: true,
    error: '',
    home: null,
    imageFallback: '/assets/tile-placeholder.png',
    errorDetail: '',
    quickEntries: QUICK_ENTRIES,
    allProducts: [],
    productsPage: 1,
    productsPageSize: PAGE_SIZE,
    productsTotal: 0,
    productsLoading: false,
    productsError: '',
    productsHasMore: true,
    productsFinished: false,
    pageAlive: true,
    shareAddGuideVisible: false,
    shareAddGuideStyle: 'top: 112px; right: 52px;',
  },

  onLoad() {
    this.setData({ pageAlive: true });
    this.prepareShareAddGuide();
    this.loadHome();
    this.loadAllProducts(true);
  },

  onUnload() {
    this.setData({ pageAlive: false });
  },

  onReachBottom() {
    this.loadAllProducts(false);
  },

  onShareAppMessage() {
    this.trackHomeShare('wechat_friend');
    return {
      title: (this.data.home && this.data.home.store.name) || '菲尚特瓷砖馆',
      path: HOME_SHARE_PATH,
    };
  },

  onShareTimeline() {
    this.trackHomeShare('wechat_timeline');
    return {
      title: (this.data.home && this.data.home.store.name) || '菲尚特瓷砖馆',
      query: 'source=share',
    };
  },

  trackHomeShare(shareChannel) {
    track('home_share', {
      page_path: '/pages/index/index',
      share_channel: shareChannel,
      source: 'share',
    });
  },

  prepareShareAddGuide() {
    let storageClosed = false;
    try {
      storageClosed = wx.getStorageSync(SHARE_ADD_GUIDE_SESSION_KEY) === 'closed';
    } catch (error) {
      console.warn('[miniapp-home] read share add guide state failed', error);
    }
    this.setData({
      shareAddGuideVisible: !shareAddGuideDismissedInSession && !storageClosed,
      shareAddGuideStyle: this.resolveShareAddGuideStyle(),
    });
  },

  resolveShareAddGuideStyle() {
    const fallbackGuideTop = 112;
    const fallbackGuideRight = 52;
    try {
      const systemInfo = wx.getSystemInfoSync();
      const menuButton = typeof wx.getMenuButtonBoundingClientRect === 'function'
        ? wx.getMenuButtonBoundingClientRect()
        : null;
      const guideTop = menuButton && menuButton.bottom
        ? menuButton.bottom + 8
        : fallbackGuideTop;
      const guideRight = menuButton && typeof menuButton.right === 'number'
        ? Math.max(systemInfo.windowWidth - menuButton.right + 44, 48)
        : fallbackGuideRight;
      return `top: ${guideTop}px; right: ${guideRight}px;`;
    } catch (error) {
      console.warn('[miniapp-home] resolve share add guide metrics failed', error);
      return `top: ${fallbackGuideTop}px; right: ${fallbackGuideRight}px;`;
    }
  },

  dismissShareAddGuide() {
    shareAddGuideDismissedInSession = true;
    this.setData({ shareAddGuideVisible: false });
    try {
      wx.setStorageSync(SHARE_ADD_GUIDE_SESSION_KEY, 'closed');
    } catch (error) {
      console.warn('[miniapp-home] write share add guide state failed', error);
    }
  },

  loadHome() {
    this.setData({ loading: true, error: '', errorDetail: '' });
    request('/api/v1/miniapp/home')
      .then((home) => {
        if (!this.data.pageAlive) return;
        this.setData({ home, loading: false });
      })
      .catch((error) => {
        if (!this.data.pageAlive) return;
        console.error('[miniapp-home] loadHome failed', error);
        const attempts = (error && error.attempts) || [];
        const detail = attempts.length
          ? attempts.map((item) => `${item.url} ${item.errMsg || item.statusCode || item.message}`).join(' | ')
          : (error && (error.errMsg || error.message)) || '未知请求错误';
        this.setData({
          error: '网络开小差了，请检查本地后端或开发工具网络面板',
          errorDetail: detail,
          loading: false,
        });
      });
  },

  loadAllProducts(reset) {
    if (this.data.productsLoading) return;
    if (!reset && !this.data.productsHasMore) return;
    const nextPage = reset ? 1 : this.data.productsPage + 1;
    const resetState = reset ? { allProducts: [], productsPage: 1, productsHasMore: true } : {};
    this.setData({
      productsLoading: true,
      productsError: '',
      productsFinished: reset ? false : this.data.productsFinished,
      ...resetState,
    });
    track('miniapp_home_waterfall_load', {
      page_path: '/pages/index/index',
      page: nextPage,
      page_size: this.data.productsPageSize,
    });
    request(`/api/v1/miniapp/products?page=${nextPage}&page_size=${this.data.productsPageSize}`)
      .then((data) => {
        if (!this.data.pageAlive) return;
        const merged = this.mergeProducts(reset ? [] : this.data.allProducts, data.items || []);
        const hasMore = typeof data.has_more === 'boolean'
          ? data.has_more
          : merged.length < data.total;
        this.setData({
          allProducts: merged,
          productsPage: data.page || nextPage,
          productsTotal: data.total || merged.length,
          productsLoading: false,
          productsHasMore: hasMore,
          productsFinished: !hasMore,
        });
        if (!hasMore) {
          track('miniapp_home_waterfall_end_reached', {
            page_path: '/pages/index/index',
            page: data.page || nextPage,
            total: data.total || merged.length,
          });
        }
      })
      .catch((error) => {
        if (!this.data.pageAlive) return;
        console.error('[miniapp-home] loadAllProducts failed', error);
        this.setData({
          productsLoading: false,
          productsError: '加载失败，点击重试',
        });
        track('miniapp_home_waterfall_load_failed', {
          page_path: '/pages/index/index',
          page: nextPage,
          reason: 'request_failed',
        });
      });
  },

  mergeProducts(existing, incoming) {
    const seen = new Set();
    const result = [];
    existing.concat(incoming).forEach((item) => {
      if (!item || seen.has(item.product_id)) return;
      seen.add(item.product_id);
      result.push(item);
    });
    return result;
  },

  openSearch() {
    track('miniapp_home_search_click', { page_path: '/pages/index/index' });
    wx.navigateTo({ url: '/pages/search/index' });
  },

  openStoreInfo() {
    wx.navigateTo({ url: '/pages/store-info/index' });
  },

  openQuickEntry(event) {
    const entry = event.currentTarget.dataset.entry;
    if (!entry) return;
    track('miniapp_home_quick_entry_click', {
      page_path: '/pages/index/index',
      entry_key: entry.key,
    });
    if (entry.url) {
      wx.switchTab({ url: entry.url });
      return;
    }
    if (entry.section) {
      wx.navigateTo({ url: `/pages/product-list/index?section=${entry.section}` });
      return;
    }
    wx.showToast({ title: entry.fallback || '功能建设中', icon: 'none' });
  },

  openSection(event) {
    const section = event.currentTarget.dataset.section;
    wx.navigateTo({ url: `/pages/product-list/index?section=${section}` });
  },

  openProduct(event) {
    const id = event.currentTarget.dataset.id;
    const source = event.currentTarget.dataset.source || 'home';
    if (id) {
      const eventName = source === 'new'
        ? 'miniapp_home_new_product_click'
        : source === 'hot'
          ? 'miniapp_home_hot_product_click'
          : 'miniapp_home_waterfall_product_click';
      track(eventName, {
        product_id: Number(id),
        page_path: '/pages/index/index',
        source,
      });
      wx.navigateTo({ url: `/pages/tile-detail/index?id=${id}` });
    }
  },

  openBanner(event) {
    const banner = event.currentTarget.dataset.banner;
    if (!banner) return;
    if (banner.jump_type === 'product' && banner.target_id) {
      wx.navigateTo({ url: `/pages/tile-detail/index?id=${banner.target_id}` });
      return;
    }
    if (banner.jump_type === 'brand' && banner.target_id) {
      wx.navigateTo({ url: `/pages/brand-detail/index?brandId=${banner.target_id}&source=home-carousel` });
      return;
    }
    if (banner.jump_type === 'search') {
      wx.navigateTo({
        url: `/pages/search/index?keyword=${encodeURIComponent(banner.search_keyword || banner.title)}`,
      });
      return;
    }
    if (banner.jump_type === 'store') {
      wx.navigateTo({ url: '/pages/store-info/index' });
      return;
    }
    wx.showToast({ title: '内容建设中', icon: 'none' });
  },

  retryAllProducts() {
    this.loadAllProducts(this.data.allProducts.length === 0);
  },

  onImageError(event) {
    const key = event.currentTarget.dataset.key;
    if (key) {
      this.setData({ [key]: this.data.imageFallback });
    }
  },
});
