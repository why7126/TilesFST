import { request, track } from '../../services/api';

type ProductCard = {
  product_id: number;
  product_name: string;
  sku_code: string;
  cover_image?: string | null;
  specification: string;
  category_name?: string | null;
  brand_name?: string | null;
  price_display: string;
};

type ProductListResponse = {
  items: ProductCard[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
};

const PAGE_SIZE = 12;
const CATEGORY_LEVELS = new Set(['primary', 'secondary']);
const PRODUCT_LIST_SHARE_KEYS = [
  'categoryId',
  'categoryLevel',
  'categoryName',
  'brandId',
  'keyword',
  'section',
  'sourcePage',
] as const;

function requestId(): string {
  return `plist-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function encodeShareValue(value: unknown): string {
  return encodeURIComponent(String(value).slice(0, 80));
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
    items: [] as ProductCard[],
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query: Record<string, string>) {
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

  onShareAppMessage() {
    this.trackShare('wechat_friend');
    return {
      title: this.shareTitle(),
      path: `/pages/product-list/index?${this.buildShareQuery()}`,
      imageUrl: this.data.items[0]?.cover_image || this.data.imageFallback,
    };
  },

  onShareTimeline() {
    this.trackShare('wechat_timeline');
    return {
      title: this.shareTitle(),
      query: this.buildShareQuery(),
      imageUrl: this.data.items[0]?.cover_image || this.data.imageFallback,
    };
  },

  loadProducts(options: { reset: boolean; eventName?: string }) {
    if (this.data.loadingMore || (!options.reset && this.data.loading)) return;
    if (!options.reset && !this.data.hasMore) return;
    const nextPage = options.reset ? 1 : this.data.page + 1;
    this.setData({
      loading: options.reset,
      loadingMore: !options.reset,
      error: '',
      loadMoreError: '',
      ...(options.reset ? { items: [], hasMore: true, page: 1 } : {}),
    });

    request<ProductListResponse>(`/api/v1/miniapp/products?${this.buildQuery(nextPage)}`)
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
            resultCount: data.items?.length || 0,
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

  buildQuery(page: number): string {
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

  buildShareQuery(): string {
    const values: Record<(typeof PRODUCT_LIST_SHARE_KEYS)[number], string | number> = {
      categoryId: this.data.categoryId,
      categoryLevel: this.data.categoryId ? this.data.categoryLevel : '',
      categoryName: this.data.categoryName,
      brandId: this.data.brandId,
      keyword: this.data.keyword,
      section: this.data.section,
      sourcePage: 'share',
    };
    return PRODUCT_LIST_SHARE_KEYS
      .map((key) => {
        const value = values[key];
        return value ? `${key}=${encodeShareValue(value)}` : '';
      })
      .filter(Boolean)
      .join('&');
  },

  shareTitle(): string {
    if (this.data.keyword) return `搜索：${this.data.keyword}`;
    if (this.data.categoryName) return `${this.data.categoryName}瓷砖`;
    if (this.data.brandId) return '品牌商品';
    if (this.data.section === 'new') return '新品榜';
    if (this.data.section === 'hot') return '热销榜';
    return '全部商品';
  },

  mergeProducts(current: ProductCard[], incoming: ProductCard[]): ProductCard[] {
    const seen = new Set<number>();
    const result: ProductCard[] = [];
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

  openProduct(event: WechatMiniprogram.TouchEvent) {
    const id = Number(event.currentTarget.dataset.id || 0);
    const index = Number(event.currentTarget.dataset.index || 0);
    if (!id) return;
    this.trackListEvent('product_list_item_click', { skuId: id, positionIndex: index });
    wx.navigateTo({
      url: `/pages/tile-detail/index?skuId=${id}&source=product-list&requestId=${encodeURIComponent(this.data.requestId)}`,
      fail: () => wx.showToast({ title: '商品打开失败，请重试', icon: 'none' }),
    });
  },

  onImageError(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`items[${index}].cover_image`]: this.data.imageFallback });
  },

  emptyText(): string {
    if (this.data.keyword) return `没有找到“${this.data.keyword}”相关商品，可返回搜索页调整关键词`;
    if (this.data.categoryName) return '该分类暂未上架商品';
    if (this.data.brandId) return '该品牌暂未上架商品';
    return '暂无可浏览商品';
  },

  errorText(): string {
    if (this.data.categoryName) return '分类商品加载失败，请重试';
    if (this.data.keyword) return '搜索商品加载失败，请重试';
    return '商品列表加载失败，请重试';
  },

  trackPageView() {
    this.trackListEvent('product_list_page_view', {});
  },

  trackItems(items: ProductCard[]) {
    items.slice(0, 12).forEach((item, index) => {
      this.trackListEvent('product_list_item_exposure', {
        skuId: item.product_id,
        positionIndex: index,
      });
    });
  },

  trackListEvent(eventName: string, extra: Record<string, unknown>) {
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

  trackShare(shareChannel: 'wechat_friend' | 'wechat_timeline') {
    this.trackListEvent('product_list_share_click', {
      share_channel: shareChannel,
      share_path: `/pages/product-list/index?${this.buildShareQuery()}`,
    });
  },
});
