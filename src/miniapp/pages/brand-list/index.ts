import { request, track } from '../../services/api';

type BrandBanner = {
  id: number;
  title: string;
  subtitle?: string;
  image_url: string;
  jump_type: 'none' | 'product' | 'brand' | 'search' | 'store';
  target_id?: number;
  search_keyword?: string;
};

type BrandItem = {
  brand_id: number;
  brand_name: string;
  brand_short_name?: string | null;
  brand_logo_url?: string | null;
  brand_logo_thumbnail_url?: string | null;
  brand_entry_path: string;
  product_count: number;
  leaf_category_names?: string[];
  leaf_categories?: BrandCategory[];
  description?: string | null;
  available: boolean;
};

type BrandCategory = {
  category_id: number;
  category_name: string;
};

type BrandListItem = BrandItem & {
  product_count_text: string;
  category_items: BrandCategory[];
  fallback_text: string;
};

type BrandListResponse = {
  banners: BrandBanner[];
  items: BrandItem[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
};

const PAGE_SIZE = 20;
function requestId(): string {
  return `brand-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function safeText(value: unknown, fallback = ''): string {
  if (typeof value !== 'string') return fallback;
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : fallback;
}

function fallbackText(name: string): string {
  const compact = safeText(name, '品牌').replace(/\s/g, '');
  return compact ? compact.slice(0, 2).toUpperCase() : '品牌';
}

function normalizeCategoryItems(categories?: BrandCategory[], names?: string[]): BrandCategory[] {
  const seen = new Set<string>();
  const result: BrandCategory[] = [];
  (categories || []).forEach((item) => {
    const text = safeText(item.category_name);
    const id = Number(item.category_id || 0);
    if (!id || !text || seen.has(text)) return;
    seen.add(text);
    result.push({ category_id: id, category_name: text });
  });
  (names || []).forEach((name, index) => {
    const text = safeText(name);
    if (!text || seen.has(text)) return;
    seen.add(text);
    result.push({ category_id: 0 - index, category_name: text });
  });
  return result;
}

function normalizeBrandItem(item: BrandItem): BrandListItem {
  const categories = normalizeCategoryItems(item.leaf_categories, item.leaf_category_names);
  const productCount = Number(item.product_count || 0);
  return {
    ...item,
    product_count: productCount,
    product_count_text: `${productCount} 款商品`,
    category_items: categories,
    fallback_text: fallbackText(item.brand_name || item.brand_short_name || ''),
  };
}

Page({
  data: {
    title: '品牌',
    status: 'loading',
    banners: [] as BrandBanner[],
    items: [] as BrandListItem[],
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

  onLoad(query: Record<string, string>) {
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

  loadBrands(reset: boolean) {
    if (this.data.loadingMore) return;
    if (!reset && !this.data.hasMore) return;
    const nextPage = reset ? 1 : this.data.page + 1;
    this.setData({
      status: reset ? 'loading' : this.data.status,
      loadingMore: !reset,
      loadMoreError: '',
      ...(reset ? { items: [], page: 1, hasMore: true } : {}),
    });

    request<BrandListResponse>(`/api/v1/miniapp/brands?page=${nextPage}&pageSize=${this.data.pageSize}`)
      .then((data) => {
        const incoming = (data.items || []).map(normalizeBrandItem);
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

  mergeBrands(current: BrandListItem[], incoming: BrandListItem[]): BrandListItem[] {
    const seen = new Set<number>();
    const result: BrandListItem[] = [];
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

  openBanner(event: WechatMiniprogram.TouchEvent) {
    const banner = event.currentTarget.dataset.banner as BrandBanner;
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
      const keyword = (banner.search_keyword || banner.title || '').trim();
      if (!keyword) {
        wx.showToast({ title: '内容建设中', icon: 'none' });
        return;
      }
      wx.navigateTo({
        url: `/pages/search/index?keyword=${encodeURIComponent(keyword)}`,
      });
      return;
    }
    if (banner.jump_type === 'store') {
      wx.navigateTo({ url: '/pages/store-info/index' });
      return;
    }
    wx.showToast({ title: '内容建设中', icon: 'none' });
  },

  onBrandInfoTap(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    const brand = this.data.items[index];
    if (!brand) return;
    this.trackBrandListEvent('brand_list_card_click', {
      brandId: brand.brand_id,
      brandName: brand.brand_name,
      positionIndex: index,
      sourcePage: 'brand-list',
      sourceEntry: this.data.sourcePage,
    });
    if (!brand.available || !brand.brand_entry_path) {
      wx.showToast({ title: '暂无内容', icon: 'none' });
      return;
    }
    wx.navigateTo({
      url: brand.brand_entry_path,
      fail: () => wx.showToast({ title: '暂无内容', icon: 'none' }),
    });
  },

  onCategoryTap(event: WechatMiniprogram.TouchEvent) {
    const brandIndex = Number(event.currentTarget.dataset.brandIndex || 0);
    const categoryIndex = Number(event.currentTarget.dataset.categoryIndex || 0);
    const brand = this.data.items[brandIndex];
    const category = brand?.category_items?.[categoryIndex];
    if (!brand || !category || category.category_id <= 0) {
      wx.showToast({ title: '暂无内容', icon: 'none' });
      return;
    }
    this.trackBrandListEvent('brand_list_category_click', {
      brandId: brand.brand_id,
      brandName: brand.brand_name,
      categoryId: category.category_id,
      categoryName: category.category_name,
      positionIndex: brandIndex,
      categoryIndex,
      sourcePage: 'brand-list',
      sourceEntry: this.data.sourcePage,
    });
    wx.navigateTo({
      url:
        `/pages/product-list/index?brandId=${encodeURIComponent(String(brand.brand_id))}` +
        `&categoryId=${encodeURIComponent(String(category.category_id))}` +
        '&categoryLevel=secondary' +
        `&categoryName=${encodeURIComponent(category.category_name)}` +
        '&sourcePage=brand-list-category',
      fail: () => wx.showToast({ title: '暂无内容', icon: 'none' }),
    });
  },

  onImageError(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`banners[${index}].image_url`]: this.data.imageFallback });
  },

  onLogoError(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({
      [`items[${index}].brand_logo_thumbnail_url`]: '',
      [`items[${index}].brand_logo_url`]: '',
    });
  },

  openCategory() {
    wx.switchTab({ url: '/pages/category/index' });
  },

  trackBrandListEvent(eventName: string, extra: Record<string, unknown>) {
    track(eventName, {
      page_path: '/pages/brand-list/index',
      client_type: 'wechat_miniapp',
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
