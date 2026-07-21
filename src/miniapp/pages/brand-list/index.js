const { request, track } = require('../../services/api');

const PAGE_SIZE = 20;

function requestId() {
  return `brand-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

Page({
  data: {
    title: '品牌列表',
    status: 'loading',
    banners: [],
    items: [],
    page: 1,
    pageSize: PAGE_SIZE,
    total: 0,
    hasMore: true,
    loadingMore: false,
    loadMoreError: '',
    requestId: '',
    sourcePage: 'tabbar',
    imageFallback: '/assets/tile-placeholder.png',
    skeletons: [1, 2, 3, 4],
  },

  onLoad(query) {
    this.setCurrentTab();
    this.setData({
      sourcePage: query.sourcePage || query.source || 'tabbar',
      requestId: requestId(),
    });
    this.loadBrands(true);
  },

  onShow() {
    this.setCurrentTab();
  },

  onPullDownRefresh() {
    this.setData({ requestId: requestId() });
    this.loadBrands(true);
  },

  onReachBottom() {
    this.loadBrands(false);
  },

  onShareAppMessage() {
    return {
      title: '菲尚特品牌列表',
      path: '/pages/brand-list/index?sourcePage=share',
    };
  },

  setCurrentTab() {
    const tabBar = this.getTabBar && this.getTabBar();
    if (tabBar) {
      tabBar.setData({ selected: 2 });
    }
  },

  loadBrands(reset) {
    if (this.data.loadingMore) return;
    if (!reset && !this.data.hasMore) return;
    const nextPage = reset ? 1 : this.data.page + 1;
    this.setData({
      status: reset ? 'loading' : this.data.status,
      loadingMore: !reset,
      loadMoreError: '',
      ...(reset ? { items: [], page: 1, hasMore: true } : {}),
    });

    request(`/api/v1/miniapp/brands?page=${nextPage}&pageSize=${this.data.pageSize}`)
      .then((data) => {
        const incoming = data.items || [];
        const merged = reset ? incoming : this.mergeBrands(this.data.items, incoming);
        const status = merged.length ? 'ready' : 'empty';
        this.setData({
          status,
          banners: data.banners || [],
          items: merged,
          page: data.page || nextPage,
          pageSize: data.page_size || this.data.pageSize,
          total: data.total || merged.length,
          hasMore: Boolean(data.has_more),
          loadingMore: false,
        });
        this.trackBrandListEvent('brand_list_page_view', {
          sourcePage: this.data.sourcePage,
          resultCount: data.total || merged.length,
        });
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        this.setData({
          status: reset ? 'error' : this.data.status,
          loadingMore: false,
          loadMoreError: reset ? '' : '加载更多失败，点击重试',
        });
        wx.stopPullDownRefresh();
      });
  },

  mergeBrands(current, incoming) {
    const seen = new Set();
    const result = [];
    current.concat(incoming).forEach((item) => {
      if (!item || seen.has(item.brand_id)) return;
      seen.add(item.brand_id);
      result.push(item);
    });
    return result;
  },

  retryLoad() {
    this.setData({ requestId: requestId() });
    this.loadBrands(true);
  },

  retryLoadMore() {
    this.loadBrands(false);
  },

  openBanner(event) {
    const banner = event.currentTarget.dataset.banner;
    const index = Number(event.currentTarget.dataset.index || 0);
    if (!banner) return;
    this.trackBrandListEvent('brand_list_carousel_click', {
      jumpType: banner.jump_type || 'none',
      bannerId: banner.id,
      positionIndex: index,
    });
    if (banner.jump_type === 'product' && banner.target_id) {
      wx.navigateTo({ url: `/pages/tile-detail/index?skuId=${banner.target_id}&source=brand-carousel` });
      return;
    }
    if (banner.jump_type === 'brand' && banner.target_id) {
      wx.navigateTo({ url: `/pages/brand-detail/index?brandId=${banner.target_id}&source=brand-carousel` });
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

  onBrandTap(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    const brand = this.data.items[index];
    if (!brand) return;
    this.trackBrandListEvent('brand_list_card_click', {
      brandId: brand.brand_id,
      positionIndex: index,
      sourcePage: 'brand-list',
      sourceEntry: this.data.sourcePage,
    });
  },

  onImageError(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`banners[${index}].image_url`]: this.data.imageFallback });
  },

  openCategory() {
    wx.switchTab({ url: '/pages/category/index' });
  },

  trackBrandListEvent(eventName, extra) {
    track(eventName, {
      page_path: '/pages/brand-list/index',
      client_type: 'wechat_miniapp',
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
