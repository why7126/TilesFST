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

type Suggestion = {
  id: string;
  text: string;
  entity_type: 'keyword' | 'sku' | 'brand' | 'category' | 'spec';
  group_label?: string;
  target_id?: number;
  target_path?: string;
  scope: string;
};

type FacetOption = {
  value: string;
  label: string;
  count: number;
  selected?: boolean;
};

type SearchSection = {
  entity_type: 'sku' | 'brand' | 'category' | 'certificate';
  title: string;
  count: number;
  items: Array<Record<string, unknown>>;
};

type SearchResponse = {
  keyword: string;
  normalized_keyword: string;
  request_id: string;
  active_tab: string;
  tabs: FacetOption[];
  best_match?: Record<string, unknown> | null;
  sections: SearchSection[];
  facets: {
    brands: FacetOption[];
    categories: FacetOption[];
    specs: FacetOption[];
    price_ranges: FacetOption[];
  };
  items: ProductCard[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
  recommended_keywords: string[];
};

const HISTORY_KEY = 'miniapp_search_recent_keywords_v1';
const BROWSING_KEY = 'miniapp_recent_browsing_v1';
const DEBOUNCE_MS = 300;
const DEFAULT_SCOPE = 'all';
const DEFAULT_TABS = [
  { value: 'all', label: '综合', count: 0, selected: true },
  { value: 'brand', label: '品牌', count: 0 },
  { value: 'sku', label: 'SKU', count: 0 },
  { value: 'certificate', label: '证书', count: 0 },
];

function normalizeKeyword(value: string): string {
  return value.trim().replace(/\s+/g, ' ');
}

function meetsSuggestThreshold(value: string): boolean {
  if (!value) return false;
  return /[\u4e00-\u9fa5]/.test(value) ? value.length >= 1 : value.length >= 2;
}

function readStringList(key: string): string[] {
  try {
    const value = wx.getStorageSync(key);
    return Array.isArray(value) ? value.filter((item) => typeof item === 'string') : [];
  } catch {
    return [];
  }
}

function writeStringList(key: string, values: string[]) {
  wx.setStorage({ key, data: values });
}

Page({
  suggestionTimer: 0 as unknown as number,
  suggestionSeq: 0,
  searchSeq: 0,

  data: {
    keyword: '',
    normalizedKeyword: '',
    scope: DEFAULT_SCOPE,
    sourcePage: 'direct',
    requestId: '',
    searchMode: 'home',
    activeTab: 'all',
    loading: false,
    suggesting: false,
    error: '',
    suggestions: [] as Suggestion[],
    brandSuggestions: [] as Suggestion[],
    skuSuggestions: [] as Suggestion[],
    recentSearches: [] as string[],
    hotKeywords: [] as string[],
    recentBrowsing: [] as ProductCard[],
    recommendedKeywords: [] as string[],
    tabs: DEFAULT_TABS as FacetOption[],
    sections: [] as SearchSection[],
    displaySections: [] as Array<SearchSection & { card_label: string }>,
    activeDisplaySection: null as (SearchSection & { card_label: string }) | null,
    items: [] as ProductCard[],
    bestMatch: null as Record<string, unknown> | null,
    total: 0,
    hasResults: false,
    page: 1,
    pageSize: 20,
    hasMore: false,
    filterDrawerOpen: false,
    filterSnapshot: {} as Record<string, string>,
    facets: {
      brands: [] as FacetOption[],
      categories: [] as FacetOption[],
      specs: [] as FacetOption[],
      price_ranges: [] as FacetOption[],
    },
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query: Record<string, string>) {
    const keyword = normalizeKeyword(decodeURIComponent(query.keyword || ''));
    const scope = decodeURIComponent(query.scope || query.categoryName || DEFAULT_SCOPE);
    const sourcePage = decodeURIComponent(query.sourcePage || 'direct');
    this.setData({
      keyword,
      normalizedKeyword: keyword,
      scope: scope || DEFAULT_SCOPE,
      sourcePage,
      searchMode: keyword ? 'result' : 'home',
      activeTab: query.tab || 'all',
      requestId: this.nextRequestId(keyword),
      recentSearches: readStringList(HISTORY_KEY).slice(0, 20),
    });
    this.loadSearchHome();
    track('search_page_view', this.trackBase({ page_path: '/pages/search/index' }));
    if (keyword) {
      this.submitSearch();
    }
  },

  onSearchEntryInput(event: WechatMiniprogram.CustomEvent<{ keyword: string }>) {
    this.onInput({ detail: { value: event.detail.keyword || '' } } as WechatMiniprogram.Input);
  },

  onSearchEntrySubmit(event: WechatMiniprogram.CustomEvent<{ keyword: string }>) {
    const keyword = normalizeKeyword(event.detail.keyword || this.data.keyword);
    this.setData({ keyword, normalizedKeyword: keyword });
    this.submitSearch();
  },

  onUnload() {
    if (this.suggestionTimer) {
      clearTimeout(this.suggestionTimer);
    }
  },

  loadSearchHome() {
    request<{ hot_keywords: string[]; recent_browsing: ProductCard[] }>('/api/v1/miniapp/search/home')
      .then((data) => {
        const localBrowsing = this.readRecentBrowsing();
        this.setData({
          hotKeywords: data.hot_keywords || [],
          recentBrowsing: localBrowsing.length ? localBrowsing : (data.recent_browsing || []).slice(0, 10),
        });
      })
      .catch(() => {
        this.setData({
          hotKeywords: ['岩板', '柔光砖', '800×800', '客厅'],
          recentBrowsing: this.readRecentBrowsing(),
        });
      });
  },

  onInput(event: WechatMiniprogram.Input) {
    const keyword = event.detail.value;
    const normalized = normalizeKeyword(keyword);
    const requestId = this.nextRequestId(normalized);
    this.setData({ keyword, normalizedKeyword: normalized, requestId, searchMode: normalized ? 'suggest' : 'home', error: '' });
    track('search_input', this.trackBase({ keyword, normalizedKeyword: normalized }));
    if (this.suggestionTimer) {
      clearTimeout(this.suggestionTimer);
    }
    if (!meetsSuggestThreshold(normalized)) {
      this.setData({ suggestions: [], brandSuggestions: [], skuSuggestions: [], suggesting: false });
      return;
    }
    this.suggestionTimer = setTimeout(() => this.loadSuggestions(normalized, requestId), DEBOUNCE_MS) as unknown as number;
  },

  clearKeyword() {
    this.setData({
      keyword: '',
      normalizedKeyword: '',
      searchMode: 'home',
      suggestions: [],
      brandSuggestions: [],
      skuSuggestions: [],
      items: [],
      sections: [],
      total: 0,
      hasResults: false,
      error: '',
    });
  },

  cancelSearch() {
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

  loadSuggestions(keyword: string, requestId: string) {
    const seq = ++this.suggestionSeq;
    this.setData({ suggesting: true });
    const params = [
      `keyword=${encodeURIComponent(keyword)}`,
      `scope=${encodeURIComponent(this.data.scope)}`,
      'limit=8',
      `request_id=${encodeURIComponent(requestId)}`,
    ].join('&');
    request<{ suggestions: Suggestion[]; normalized_keyword: string; request_id: string }>(
      `/api/v1/miniapp/search/suggestions?${params}`,
    )
      .then((data) => {
        if (seq !== this.suggestionSeq || data.request_id !== this.data.requestId) return;
        const suggestions = (data.suggestions || [])
          .filter((item) => item.entity_type === 'sku' || item.entity_type === 'brand')
          .map((item) => ({
            ...item,
            group_label: this.suggestionGroupLabel(item.entity_type),
          }));
        this.setData({
          suggestions,
          brandSuggestions: suggestions.filter((item) => item.entity_type === 'brand'),
          skuSuggestions: suggestions.filter((item) => item.entity_type === 'sku'),
          suggesting: false,
        });
        track('search_suggestion_exposure', this.trackBase({
          keyword,
          normalizedKeyword: data.normalized_keyword,
          resultCount: suggestions.length,
        }));
      })
      .catch(() => {
        if (seq !== this.suggestionSeq) return;
        this.setData({ suggestions: [], brandSuggestions: [], skuSuggestions: [], suggesting: false });
      });
  },

  submitSearch() {
    const keyword = normalizeKeyword(this.data.keyword);
    if (!keyword) return;
    const history = [keyword].concat(this.data.recentSearches.filter((item) => item !== keyword)).slice(0, 20);
    writeStringList(HISTORY_KEY, history);
    this.setData({
      keyword,
      normalizedKeyword: keyword,
      searchMode: 'result',
      recentSearches: history,
      suggestions: [],
      brandSuggestions: [],
      skuSuggestions: [],
      suggesting: false,
      page: 1,
      requestId: this.nextRequestId(keyword),
    });
    track('search_submit', this.trackBase({ module: 'miniapp_search', keyword, normalizedKeyword: keyword }));
    this.loadResults(true);
  },

  loadResults(reset: boolean) {
    const seq = ++this.searchSeq;
    const keyword = this.data.normalizedKeyword;
    if (!keyword) return;
    const page = reset ? 1 : this.data.page + 1;
    const params = [
      `keyword=${encodeURIComponent(keyword)}`,
      `tab=${this.data.activeTab}`,
      `page=${page}`,
      `page_size=${this.data.pageSize}`,
      `request_id=${encodeURIComponent(this.data.requestId)}`,
      this.data.filterSnapshot.brand ? `brand=${encodeURIComponent(this.data.filterSnapshot.brand)}` : '',
      this.data.filterSnapshot.category ? `category=${encodeURIComponent(this.data.filterSnapshot.category)}` : '',
      this.data.filterSnapshot.spec ? `spec=${encodeURIComponent(this.data.filterSnapshot.spec)}` : '',
      this.data.filterSnapshot.priceMin ? `price_min=${this.data.filterSnapshot.priceMin}` : '',
      this.data.filterSnapshot.priceMax ? `price_max=${this.data.filterSnapshot.priceMax}` : '',
    ].filter(Boolean).join('&');
    this.setData({ loading: true, error: '' });
    request<SearchResponse>(`/api/v1/miniapp/search?${params}`)
      .then((data) => {
        if (seq !== this.searchSeq) return;
        const items = reset ? data.items || [] : this.data.items.concat(data.items || []);
        const facets = this.markSelectedFacets(data.facets || this.data.facets, this.data.filterSnapshot);
        const resultCount = this.searchResultCount(data);
        const displaySections = this.orderDisplaySections(data.sections || []);
        this.setData({
          items,
          sections: data.sections || [],
          displaySections,
          activeDisplaySection: this.activeDisplaySection(displaySections, data.active_tab || this.data.activeTab),
          tabs: this.normalizeTabs(data.tabs || DEFAULT_TABS),
          facets,
          bestMatch: data.best_match || null,
          total: data.total || 0,
          hasResults: resultCount > 0,
          page: data.page || page,
          hasMore: Boolean(data.has_more),
          recommendedKeywords: data.recommended_keywords || [],
          loading: false,
        });
        track(resultCount ? 'search_result_exposure' : 'search_no_result', this.trackBase({
          keyword,
          normalizedKeyword: data.normalized_keyword,
          entityType: data.active_tab,
          resultCount,
          filterSnapshot: this.data.filterSnapshot,
        }));
      })
      .catch(() => {
        if (seq !== this.searchSeq) return;
        this.setData({ error: '搜索失败，请重试', loading: false });
      });
  },

  switchTab(event: WechatMiniprogram.TouchEvent) {
    const tab = event.currentTarget.dataset.tab;
    this.setData({ activeTab: tab || 'all' });
    this.loadResults(true);
  },

  openSuggestion(event: WechatMiniprogram.TouchEvent) {
    const item = event.currentTarget.dataset.item as Suggestion;
    if (!item) return;
    track('search_suggestion_click', this.trackBase({
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      entityType: item.entity_type,
    }));
    if (item.target_path) {
      wx.navigateTo({ url: item.target_path });
      return;
    }
    this.setData({ keyword: item.text, normalizedKeyword: item.text, searchMode: 'result' });
    this.submitSearch();
  },

  openProduct(event: WechatMiniprogram.TouchEvent) {
    const item = event.currentTarget.dataset.item as ProductCard;
    if (!item) return;
    this.saveRecentBrowsing(item);
    track('search_result_click', this.trackBase({
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      entityType: 'sku',
    }));
    wx.navigateTo({ url: `/pages/tile-detail/index?skuId=${item.product_id}` });
  },

  rememberProduct(event: WechatMiniprogram.CustomEvent<{ product: ProductCard }>) {
    if (event.detail?.product) {
      this.saveRecentBrowsing(event.detail.product);
    }
  },

  openSectionItem(event: WechatMiniprogram.TouchEvent) {
    const item = event.currentTarget.dataset.item as Record<string, unknown>;
    if (!item) return;
    if (typeof item.target_path === 'string') {
      wx.navigateTo({ url: item.target_path });
      return;
    }
    if (typeof item.product_id === 'number') {
      wx.navigateTo({ url: `/pages/tile-detail/index?skuId=${item.product_id}` });
    }
  },

  openFilterDrawer() {
    this.setData({ filterDrawerOpen: true });
  },

  closeFilterDrawer() {
    this.setData({ filterDrawerOpen: false });
  },

  selectFacet(event: WechatMiniprogram.TouchEvent) {
    const type = event.currentTarget.dataset.type;
    const value = event.currentTarget.dataset.value;
    const filterSnapshot = {
      ...this.data.filterSnapshot,
      [type]: this.data.filterSnapshot[type] === value ? '' : value,
    };
    this.setData({
      filterSnapshot,
      facets: this.markSelectedFacets(this.data.facets, filterSnapshot),
    });
  },

  selectPriceRange(event: WechatMiniprogram.TouchEvent) {
    const value = String(event.currentTarget.dataset.value || '');
    const [priceMin = '', priceMax = ''] = value.split('-');
    const selected = this.data.filterSnapshot.priceRange === value;
    const filterSnapshot = {
      ...this.data.filterSnapshot,
      priceRange: selected ? '' : value,
      priceMin: selected ? '' : priceMin,
      priceMax: selected ? '' : priceMax,
    };
    this.setData({
      filterSnapshot,
      facets: this.markSelectedFacets(this.data.facets, filterSnapshot),
    });
  },

  onPriceMinInput(event: WechatMiniprogram.Input) {
    const filterSnapshot = {
      ...this.data.filterSnapshot,
      priceRange: '',
      priceMin: event.detail.value,
    };
    this.setData({
      filterSnapshot,
      facets: this.markSelectedFacets(this.data.facets, filterSnapshot),
    });
  },

  onPriceMaxInput(event: WechatMiniprogram.Input) {
    const filterSnapshot = {
      ...this.data.filterSnapshot,
      priceRange: '',
      priceMax: event.detail.value,
    };
    this.setData({
      filterSnapshot,
      facets: this.markSelectedFacets(this.data.facets, filterSnapshot),
    });
  },

  resetFilters() {
    this.setData({
      filterSnapshot: {},
      facets: this.markSelectedFacets(this.data.facets, {}),
    });
  },

  applyFilters() {
    this.setData({ filterDrawerOpen: false });
    track('search_filter_apply', this.trackBase({
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      filterSnapshot: this.data.filterSnapshot,
      resultCount: this.data.total,
    }));
    this.loadResults(true);
  },

  useKeyword(event: WechatMiniprogram.TouchEvent) {
    const keyword = event.currentTarget.dataset.keyword;
    if (!keyword) return;
    track('search_history_click', this.trackBase({ keyword, normalizedKeyword: normalizeKeyword(keyword) }));
    this.setData({ keyword, normalizedKeyword: normalizeKeyword(keyword), searchMode: 'result' });
    this.submitSearch();
  },

  deleteHistory(event: WechatMiniprogram.TouchEvent) {
    const keyword = event.currentTarget.dataset.keyword;
    const recentSearches = this.data.recentSearches.filter((item) => item !== keyword);
    writeStringList(HISTORY_KEY, recentSearches);
    this.setData({ recentSearches });
    track('search_history_delete', this.trackBase({ keyword, normalizedKeyword: normalizeKeyword(keyword || '') }));
  },

  clearHistory() {
    writeStringList(HISTORY_KEY, []);
    this.setData({ recentSearches: [] });
    track('search_history_clear', this.trackBase({}));
  },

  retrySearch() {
    this.loadResults(true);
  },

  loadMore() {
    this.loadResults(false);
  },

  readRecentBrowsing(): ProductCard[] {
    try {
      const value = wx.getStorageSync(BROWSING_KEY);
      return Array.isArray(value) ? value.slice(0, 10) : [];
    } catch {
      return [];
    }
  },

  saveRecentBrowsing(item: ProductCard) {
    const next = [item].concat(this.readRecentBrowsing().filter((value) => value.product_id !== item.product_id)).slice(0, 10);
    wx.setStorage({ key: BROWSING_KEY, data: next });
  },

  nextRequestId(keyword: string): string {
    return `search-${Date.now()}-${Math.abs(keyword.length * 97 + this.searchSeq)}`;
  },

  suggestionGroupLabel(entityType: Suggestion['entity_type']): string {
    const labels: Record<Suggestion['entity_type'], string> = {
      keyword: '建议',
      sku: 'SKU',
      brand: '品牌',
      category: '类目',
      spec: '规格',
    };
    return labels[entityType] || '建议';
  },

  markSelectedFacets(
    facets: SearchResponse['facets'],
    filterSnapshot: Record<string, string>,
  ): SearchResponse['facets'] {
    const mark = (items: FacetOption[], key: string) => (items || []).map((item) => ({
      ...item,
      selected: Boolean(filterSnapshot[key]) && filterSnapshot[key] === item.value,
    }));
    return {
      brands: mark(facets.brands, 'brand'),
      categories: mark(facets.categories, 'category'),
      specs: mark(facets.specs, 'spec'),
      price_ranges: mark(facets.price_ranges, 'priceRange'),
    };
  },

  searchResultCount(data: SearchResponse): number {
    const sectionCount = (data.sections || []).reduce((sum, section) => sum + (section.count || 0), 0);
    return Math.max(data.total || 0, sectionCount, (data.items || []).length, data.best_match ? 1 : 0);
  },

  normalizeTabs(tabs: FacetOption[]): FacetOption[] {
    const order = ['all', 'brand', 'sku', 'certificate'];
    return order
      .map((value) => (tabs || DEFAULT_TABS).find((item) => item.value === value))
      .filter((item): item is FacetOption => Boolean(item));
  },

  orderDisplaySections(sections: SearchSection[]): Array<SearchSection & { card_label: string }> {
    const labels: Record<string, string> = {
      brand: '品牌',
      sku: 'SKU',
      certificate: '证书',
    };
    return ['brand', 'sku', 'certificate']
      .map((entityType) => sections.find((section) => section.entity_type === entityType))
      .filter((section): section is SearchSection => Boolean(section))
      .filter((section) => (section.count || 0) > 0 && (section.items || []).length > 0)
      .map((section) => ({ ...section, card_label: labels[section.entity_type] || section.title }));
  },

  activeDisplaySection(
    sections: Array<SearchSection & { card_label: string }>,
    activeTab: string,
  ): (SearchSection & { card_label: string }) | null {
    if (activeTab === 'all') return null;
    return sections.find((section) => section.entity_type === activeTab) || null;
  },

  trackBase(extra: Record<string, unknown>) {
    return {
      page_path: '/pages/search/index',
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      scope: this.data.scope,
      sourcePage: this.data.sourcePage,
      requestId: this.data.requestId,
      client_type: 'wechat_miniapp',
      ...extra,
    };
  },
});
