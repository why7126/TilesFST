const { request, track } = require('../../services/api');

const PAGE_SIZE = 12;
const CATEGORY_LEVELS = new Set(['primary', 'secondary']);

function requestId() {
  return `plist-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

Page({
  data: {
    categoryId: 0,
    categoryName: '',
    categoryLevel: '',
    brandId: 0,
    keyword: '',
    sourcePage: 'direct',
    section: '',
    title: '全部商品',
    page: 1,
    pageSize: PAGE_SIZE,
    total: 0,
    hasMore: true,
    loading: true,
    refreshing: false,
    loadingMore: false,
    error: '',
    loadMoreError: '',
    emptyText: '暂无可浏览商品',
    requestId: '',
    skeletons: [1, 2, 3, 4],
    items: [],
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query) {
    const categoryName = decodeURIComponent(query.categoryName || '');
    const rawCategoryLevel = String(query.categoryLevel || '');
    const categoryLevel = CATEGORY_LEVELS.has(rawCategoryLevel) ? rawCategoryLevel : '';
    const keyword = decodeURIComponent(query.keyword || '');
    const sourcePage = query.sourcePage || query.source || 'direct';
    const section = query.section || '';
    const brandId = Number(query.brandId || 0);
    const categoryId = Number(query.categoryId || 0);
    const title = keyword
      ? `搜索：${keyword}`
      : categoryName || (brandId ? '品牌商品' : section === 'new' ? '新品榜' : section === 'hot' ? '热销榜' : '全部商品');

    this.setData({
      categoryId,
      categoryName,
      categoryLevel,
      brandId,
      keyword,
      sourcePage,
      section,
      title,
      requestId: requestId(),
    });
    wx.setNavigationBarTitle({ title });
    this.trackPageView();
    this.loadProducts({ reset: true });
  },

  onPullDownRefresh() {
    this.setData({ refreshing: true, requestId: requestId() });
    this.loadProducts({ reset: true, eventName: 'product_list_refresh' });
  },

  onReachBottom() {
    this.loadProducts({ reset: false, eventName: 'product_list_load_more' });
  },

  loadProducts(options) {
    if (this.data.loadingMore || (!options.reset && this.data.loading)) return;
    if (!options.reset && !this.data.hasMore) return;
    const nextPage = options.reset ? 1 : this.data.page + 1;
    const resetState = options.reset ? { items: [], hasMore: true, page: 1 } : {};
    this.setData({
      loading: options.reset,
      loadingMore: !options.reset,
      error: '',
      loadMoreError: '',
      ...resetState,
    });

    request(`/api/v1/miniapp/products?${this.buildQuery(nextPage)}`)
      .then((data) => {
        const merged = options.reset ? data.items || [] : this.mergeProducts(this.data.items, data.items || []);
        const hasMore = Boolean(data.has_more);
        this.setData({
          items: merged,
          total: data.total || merged.length,
          page: data.page || nextPage,
          pageSize: data.page_size || this.data.pageSize,
          hasMore,
          loading: false,
          refreshing: false,
          loadingMore: false,
          emptyText: this.emptyText(),
        });
        this.trackItems(merged);
        if (options.eventName) {
          this.trackListEvent(options.eventName, {
            page: nextPage,
            pageSize: this.data.pageSize,
            resultCount: (data.items && data.items.length) || 0,
          });
        }
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        const patch = options.reset
          ? { error: this.errorText(), loading: false, refreshing: false }
          : { loadMoreError: '加载更多失败，点击重试', loadingMore: false };
        this.setData(patch);
        this.trackListEvent('product_list_load_failed', {
          page: nextPage,
          pageSize: this.data.pageSize,
          errorCode: options.reset ? 'first_page_failed' : 'load_more_failed',
        });
        wx.stopPullDownRefresh();
      });
  },

  buildQuery(page) {
    const shouldKeepCategoryLevel = Boolean(this.data.categoryId && this.data.categoryLevel);
    const params = [
      `page=${page}`,
      `pageSize=${this.data.pageSize}`,
      'sort=default',
      this.data.keyword ? `keyword=${encodeURIComponent(this.data.keyword)}` : '',
      this.data.section ? `section=${encodeURIComponent(this.data.section)}` : '',
      this.data.categoryId ? `categoryId=${encodeURIComponent(String(this.data.categoryId))}` : '',
      shouldKeepCategoryLevel ? `categoryLevel=${encodeURIComponent(this.data.categoryLevel)}` : '',
      this.data.brandId ? `brandId=${encodeURIComponent(String(this.data.brandId))}` : '',
      this.data.categoryName && !this.data.categoryId ? 'filter_type=category' : '',
      this.data.categoryName && !this.data.categoryId ? `filter_value=${encodeURIComponent(this.data.categoryName)}` : '',
    ];
    return params.filter(Boolean).join('&');
  },

  mergeProducts(current, incoming) {
    const seen = new Set();
    const result = [];
    current.concat(incoming).forEach((item) => {
      if (!item || seen.has(item.product_id)) return;
      seen.add(item.product_id);
      result.push(item);
    });
    return result;
  },

  retryLoad() {
    this.loadProducts({ reset: true });
  },

  retryLoadMore() {
    this.loadProducts({ reset: false, eventName: 'product_list_load_more' });
  },

  openProduct(event) {
    const id = Number(event.currentTarget.dataset.id || 0);
    const index = Number(event.currentTarget.dataset.index || 0);
    if (!id) return;
    this.trackListEvent('product_list_item_click', { skuId: id, positionIndex: index });
    wx.navigateTo({
      url: `/pages/tile-detail/index?skuId=${id}&source=product-list&requestId=${encodeURIComponent(this.data.requestId)}`,
      fail: () => wx.showToast({ title: '商品打开失败，请重试', icon: 'none' }),
    });
  },

  onImageError(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`items[${index}].cover_image`]: this.data.imageFallback });
  },

  emptyText() {
    if (this.data.keyword) return `没有找到“${this.data.keyword}”相关商品，可返回搜索页调整关键词`;
    if (this.data.categoryName) return '该分类暂未上架商品';
    if (this.data.brandId) return '该品牌暂未上架商品';
    return '暂无可浏览商品';
  },

  errorText() {
    if (this.data.categoryName) return '分类商品加载失败，请重试';
    if (this.data.keyword) return '搜索商品加载失败，请重试';
    return '商品列表加载失败，请重试';
  },

  trackPageView() {
    this.trackListEvent('product_list_page_view', {});
  },

  trackItems(items) {
    items.slice(0, 12).forEach((item, index) => {
      this.trackListEvent('product_list_item_exposure', {
        skuId: item.product_id,
        positionIndex: index,
      });
    });
  },

  trackListEvent(eventName, extra) {
    track(eventName, {
      page_path: '/pages/product-list/index',
      client_type: 'wechat_miniapp',
      sourcePage: this.data.sourcePage,
      categoryId: this.data.categoryId || undefined,
      categoryName: this.data.categoryName || undefined,
      categoryLevel: this.data.categoryLevel || undefined,
      brandId: this.data.brandId || undefined,
      keyword: this.data.keyword || undefined,
      sort: 'default',
      page: this.data.page,
      pageSize: this.data.pageSize,
      resultCount: this.data.total,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
