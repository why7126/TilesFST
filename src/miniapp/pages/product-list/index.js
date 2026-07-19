const { request, track } = require('../../services/api');

const PAGE_SIZE = 12;
const SORT_OPTIONS = [
  { value: 'default', label: '默认' },
  { value: 'latest', label: '最新' },
  { value: 'price_asc', label: '价格升序' },
  { value: 'price_desc', label: '价格降序' },
];

function requestId() {
  return `plist-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

Page({
  data: {
    categoryId: 0,
    categoryName: '',
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
    sort: 'default',
    sortLabel: '默认',
    filterDrawerVisible: false,
    filterSnapshot: {
      brandId: '',
      categoryId: '',
      spec: '',
      priceRange: '',
    },
    draftFilter: {
      brandId: '',
      categoryId: '',
      spec: '',
      priceRange: '',
    },
    activeFilterChips: [],
    sortOptions: SORT_OPTIONS,
    facets: {
      brands: [],
      categories: [],
      specs: [],
      price_ranges: [],
    },
    skeletons: [1, 2, 3],
    items: [],
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query) {
    const categoryName = decodeURIComponent(query.categoryName || '');
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
      brandId,
      keyword,
      sourcePage,
      section,
      title,
      requestId: requestId(),
      filterSnapshot: {
        ...this.data.filterSnapshot,
        brandId: brandId ? String(brandId) : '',
        categoryId: categoryId ? String(categoryId) : '',
      },
      draftFilter: {
        ...this.data.draftFilter,
        brandId: brandId ? String(brandId) : '',
        categoryId: categoryId ? String(categoryId) : '',
      },
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
          facets: {
            brands: (data.facets && data.facets.brands) || [],
            categories: (data.facets && data.facets.categories) || [],
            specs: (data.facets && data.facets.specs) || [],
            price_ranges: (data.facets && data.facets.price_ranges) || [],
          },
          activeFilterChips: this.buildFilterChips(),
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
    const filters = this.data.filterSnapshot;
    const params = [
      `page=${page}`,
      `pageSize=${this.data.pageSize}`,
      `sort=${this.data.sort}`,
      this.data.keyword ? `keyword=${encodeURIComponent(this.data.keyword)}` : '',
      this.data.section ? `section=${encodeURIComponent(this.data.section)}` : '',
      filters.categoryId ? `categoryId=${encodeURIComponent(filters.categoryId)}` : '',
      filters.brandId ? `brandId=${encodeURIComponent(filters.brandId)}` : '',
      filters.spec ? `spec=${encodeURIComponent(filters.spec)}` : '',
      filters.priceRange ? `priceRange=${encodeURIComponent(filters.priceRange)}` : '',
      this.data.categoryName ? 'filter_type=category' : '',
      this.data.categoryName ? `filter_value=${encodeURIComponent(this.data.categoryName)}` : '',
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

  openSearch() {
    wx.navigateTo({
      url: `/pages/search/index?keyword=${encodeURIComponent(this.data.keyword)}&scope=${encodeURIComponent(this.data.categoryName || 'all')}&sourcePage=product-list&categoryName=${encodeURIComponent(this.data.categoryName)}`,
    });
  },

  openFilter() {
    this.setData({ filterDrawerVisible: true, draftFilter: { ...this.data.filterSnapshot } });
    this.trackListEvent('product_list_filter_open', {});
  },

  closeFilter() {
    this.setData({ filterDrawerVisible: false });
  },

  selectFilter(event) {
    const key = String(event.currentTarget.dataset.key || '');
    const value = String(event.currentTarget.dataset.value || '');
    this.setData({ [`draftFilter.${key}`]: value });
  },

  resetFilter() {
    this.setData({
      draftFilter: {
        brandId: '',
        categoryId: this.data.categoryId ? String(this.data.categoryId) : '',
        spec: '',
        priceRange: '',
      },
    });
  },

  clearFilters() {
    this.setData({
      filterSnapshot: {
        brandId: '',
        categoryId: this.data.categoryId ? String(this.data.categoryId) : '',
        spec: '',
        priceRange: '',
      },
      requestId: requestId(),
    });
    this.loadProducts({ reset: true });
  },

  applyFilter() {
    this.setData({
      filterSnapshot: { ...this.data.draftFilter },
      filterDrawerVisible: false,
      requestId: requestId(),
    });
    this.trackListEvent('product_list_filter_apply', { resultCount: this.data.total });
    this.loadProducts({ reset: true });
  },

  removeFilter(event) {
    const key = String(event.currentTarget.dataset.key || '');
    this.setData({
      [`filterSnapshot.${key}`]: key === 'categoryId' && this.data.categoryId ? String(this.data.categoryId) : '',
      requestId: requestId(),
    });
    this.loadProducts({ reset: true });
  },

  changeSort(event) {
    const sort = String(event.currentTarget.dataset.sort || 'default');
    const found = SORT_OPTIONS.find((item) => item.value === sort) || SORT_OPTIONS[0];
    this.setData({ sort: found.value, sortLabel: found.label, requestId: requestId() });
    wx.pageScrollTo({ scrollTop: 0, duration: 120 });
    this.trackListEvent('product_list_sort_change', { resultCount: this.data.total });
    this.loadProducts({ reset: true });
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

  buildFilterChips() {
    const filters = this.data.filterSnapshot;
    const chips = [];
    const brand = this.data.facets.brands.find((item) => item.value === filters.brandId);
    const category = this.data.facets.categories.find((item) => item.value === filters.categoryId);
    if (brand) chips.push({ key: 'brandId', label: brand.label });
    if (category && Number(filters.categoryId) !== this.data.categoryId) chips.push({ key: 'categoryId', label: category.label });
    if (filters.spec) chips.push({ key: 'spec', label: filters.spec });
    if (filters.priceRange) chips.push({ key: 'priceRange', label: this.priceLabel(filters.priceRange) });
    return chips;
  },

  priceLabel(value) {
    const item = this.data.facets.price_ranges.find((option) => option.value === value);
    return (item && item.label) || value;
  },

  emptyText() {
    if (this.data.activeFilterChips.length) return '当前筛选暂无匹配商品';
    if (this.data.keyword) return `没有找到“${this.data.keyword}”相关商品，可缩短关键词或清空筛选`;
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
      categoryId: this.data.filterSnapshot.categoryId || undefined,
      brandId: this.data.filterSnapshot.brandId || undefined,
      keyword: this.data.keyword || undefined,
      filterSnapshot: this.data.filterSnapshot,
      sort: this.data.sort,
      page: this.data.page,
      pageSize: this.data.pageSize,
      resultCount: this.data.total,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
