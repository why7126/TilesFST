const { request, track } = require('../../services/api');

const HISTORY_KEY = 'miniapp_search_recent_keywords_v1';
const BROWSING_KEY = 'miniapp_recent_browsing_v1';
const DEBOUNCE_MS = 300;
const DEFAULT_SCOPE = 'all';
const DEFAULT_TABS = [
  { value: 'all', label: '综合', count: 0, selected: true },
  { value: 'sku', label: 'SKU', count: 0 },
  { value: 'brand', label: '品牌', count: 0 },
  { value: 'category', label: '类目', count: 0 },
  { value: 'certificate', label: '证书', count: 0 },
];

function normalizeKeyword(value) {
  return String(value || '').trim().replace(/\s+/g, ' ');
}

function meetsSuggestThreshold(value) {
  if (!value) return false;
  return /[\u4e00-\u9fa5]/.test(value) ? value.length >= 1 : value.length >= 2;
}

function readStringList(key) {
  try {
    const value = wx.getStorageSync(key);
    return Array.isArray(value) ? value.filter((item) => typeof item === 'string') : [];
  } catch (error) {
    return [];
  }
}

function writeStringList(key, values) {
  wx.setStorage({ key, data: values });
}

Page({
  suggestionTimer: 0,
  suggestionSeq: 0,
  searchSeq: 0,

  data: {
    keyword: '',
    normalizedKeyword: '',
    scope: DEFAULT_SCOPE,
    sourcePage: 'direct',
    requestId: '',
    activeTab: 'all',
    loading: false,
    suggesting: false,
    error: '',
    suggestions: [],
    recentSearches: [],
    hotKeywords: [],
    recentBrowsing: [],
    recommendedKeywords: [],
    tabs: DEFAULT_TABS,
    sections: [],
    items: [],
    bestMatch: null,
    total: 0,
    page: 1,
    pageSize: 20,
    hasMore: false,
    filterDrawerOpen: false,
    filterSnapshot: {},
    facets: {
      brands: [],
      categories: [],
      specs: [],
      price_ranges: [],
    },
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query) {
    const keyword = normalizeKeyword(decodeURIComponent(query.keyword || ''));
    const scope = decodeURIComponent(query.scope || query.categoryName || DEFAULT_SCOPE);
    const sourcePage = decodeURIComponent(query.sourcePage || 'direct');
    this.setData({
      keyword,
      normalizedKeyword: keyword,
      scope: scope || DEFAULT_SCOPE,
      sourcePage,
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

  onUnload() {
    if (this.suggestionTimer) {
      clearTimeout(this.suggestionTimer);
    }
  },

  loadSearchHome() {
    request('/api/v1/miniapp/search/home')
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

  onInput(event) {
    const keyword = event.detail.value;
    const normalized = normalizeKeyword(keyword);
    const requestId = this.nextRequestId(normalized);
    this.setData({ keyword, normalizedKeyword: normalized, requestId, error: '' });
    track('search_input', this.trackBase({ keyword, normalizedKeyword: normalized }));
    if (this.suggestionTimer) {
      clearTimeout(this.suggestionTimer);
    }
    if (!meetsSuggestThreshold(normalized)) {
      this.setData({ suggestions: [], suggesting: false });
      return;
    }
    this.suggestionTimer = setTimeout(() => this.loadSuggestions(normalized, requestId), DEBOUNCE_MS);
  },

  clearKeyword() {
    this.setData({ keyword: '', normalizedKeyword: '', suggestions: [], items: [], sections: [], total: 0, error: '' });
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

  loadSuggestions(keyword, requestId) {
    const seq = ++this.suggestionSeq;
    this.setData({ suggesting: true });
    const params = [
      `keyword=${encodeURIComponent(keyword)}`,
      `scope=${encodeURIComponent(this.data.scope)}`,
      'limit=8',
      `request_id=${encodeURIComponent(requestId)}`,
    ].join('&');
    request(`/api/v1/miniapp/search/suggestions?${params}`)
      .then((data) => {
        if (seq !== this.suggestionSeq || data.request_id !== this.data.requestId) return;
        this.setData({ suggestions: data.suggestions || [], suggesting: false });
        track('search_suggestion_exposure', this.trackBase({
          keyword,
          normalizedKeyword: data.normalized_keyword,
          resultCount: (data.suggestions || []).length,
        }));
      })
      .catch(() => {
        if (seq !== this.suggestionSeq) return;
        this.setData({ suggestions: [], suggesting: false });
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
      recentSearches: history,
      suggestions: [],
      page: 1,
      requestId: this.nextRequestId(keyword),
    });
    track('search_submit', this.trackBase({ module: 'miniapp_search', keyword, normalizedKeyword: keyword }));
    this.loadResults(true);
  },

  loadResults(reset) {
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
    request(`/api/v1/miniapp/search?${params}`)
      .then((data) => {
        if (seq !== this.searchSeq) return;
        const items = reset ? data.items || [] : this.data.items.concat(data.items || []);
        this.setData({
          items,
          sections: data.sections || [],
          tabs: data.tabs || DEFAULT_TABS,
          facets: data.facets,
          bestMatch: data.best_match || null,
          total: data.total || 0,
          page: data.page || page,
          hasMore: Boolean(data.has_more),
          recommendedKeywords: data.recommended_keywords || [],
          loading: false,
        });
        const resultCount = data.total || 0;
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

  switchTab(event) {
    const tab = event.currentTarget.dataset.tab;
    this.setData({ activeTab: tab || 'all' });
    this.loadResults(true);
  },

  openSuggestion(event) {
    const item = event.currentTarget.dataset.item;
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
    this.setData({ keyword: item.text, normalizedKeyword: item.text });
    this.submitSearch();
  },

  openProduct(event) {
    const item = event.currentTarget.dataset.item;
    if (!item) return;
    this.saveRecentBrowsing(item);
    track('search_result_click', this.trackBase({
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      entityType: 'sku',
    }));
    wx.navigateTo({ url: `/pages/tile-detail/index?skuId=${item.product_id}` });
  },

  openFilterDrawer() {
    this.setData({ filterDrawerOpen: true });
  },

  closeFilterDrawer() {
    this.setData({ filterDrawerOpen: false });
  },

  selectFacet(event) {
    const type = event.currentTarget.dataset.type;
    const value = event.currentTarget.dataset.value;
    this.setData({ [`filterSnapshot.${type}`]: value });
  },

  resetFilters() {
    this.setData({ filterSnapshot: {} });
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

  useKeyword(event) {
    const keyword = event.currentTarget.dataset.keyword;
    if (!keyword) return;
    track('search_history_click', this.trackBase({ keyword, normalizedKeyword: normalizeKeyword(keyword) }));
    this.setData({ keyword, normalizedKeyword: normalizeKeyword(keyword) });
    this.submitSearch();
  },

  deleteHistory(event) {
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

  readRecentBrowsing() {
    try {
      const value = wx.getStorageSync(BROWSING_KEY);
      return Array.isArray(value) ? value.slice(0, 10) : [];
    } catch (error) {
      return [];
    }
  },

  saveRecentBrowsing(item) {
    const next = [item].concat(this.readRecentBrowsing().filter((value) => value.product_id !== item.product_id)).slice(0, 10);
    wx.setStorage({ key: BROWSING_KEY, data: next });
  },

  nextRequestId(keyword) {
    return `search-${Date.now()}-${Math.abs(keyword.length * 97 + this.searchSeq)}`;
  },

  trackBase(extra) {
    return Object.assign({
      page_path: '/pages/search/index',
      keyword: this.data.keyword,
      normalizedKeyword: this.data.normalizedKeyword,
      scope: this.data.scope,
      sourcePage: this.data.sourcePage,
      requestId: this.data.requestId,
      client_type: 'wechat_miniapp',
    }, extra);
  },
});
