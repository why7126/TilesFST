const { track } = require('../services/api');

const LOGO = '/assets/logos/product-logo.png';
const QUERY_LIMIT = 2048;

let cachedLogo = '';
function packageLogo() {
  if (cachedLogo) return cachedLogo;
  // DevTools cannot render a package-relative URL in its native share preview.
  // Materialize the small public asset once; restricted modes keep the package fallback.
  try {
    const fs = wx.getFileSystemManager();
    const destination = `${wx.env.USER_DATA_PATH}/public-share-logo-v1.png`;
    fs.copyFileSync(LOGO, destination);
    cachedLogo = destination;
    return destination;
  } catch (_) {
    cachedLogo = '';
    return LOGO;
  }
}

const KEYS = {
  index: [], 'store-info': [], find: [],
  'tile-detail': ['skuId'], 'brand-detail': ['brandId'], 'certificate-detail': ['certificateId'],
  'product-list': ['categoryId', 'categoryLevel', 'categoryName', 'brandId', 'keyword', 'section', 'spec', 'priceRange', 'sort'],
  'brand-list': ['keyword'], certificates: ['keyword'], category: ['categoryId'], search: ['keyword', 'scope', 'tab'],
};
const TITLES = {
  index: '菲尚特瓷砖馆', 'store-info': '门店信息', find: '菲尚特找砖',
  'tile-detail': '菲尚特瓷砖', 'brand-detail': '品牌主页', 'certificate-detail': '菲尚特证书',
  'product-list': '全部商品', 'brand-list': '菲尚特品牌列表', certificates: '菲尚特证书列表',
  category: '全部分类', search: '菲尚特搜索',
};
const EVENTS = {
  index: 'home_share', 'tile-detail': 'sku_share_click', 'product-list': 'product_list_share_click',
  'brand-detail': 'brand_detail_share_click', 'certificate-detail': 'certificate_detail_share_click',
  'brand-list': 'brand_list_share_click', certificates: 'certificate_list_share_click',
  'store-info': 'store_info_share_click', category: 'category_share_click', search: 'search_share_click', find: 'find_share_click',
};
const ENUMS = {
  categoryLevel: ['primary', 'secondary'], section: ['new', 'hot'],
  sort: ['default', 'latest', 'price_asc', 'price_desc'], tab: ['all', 'brand', 'sku', 'certificate'],
};

function text(value) {
  if (typeof value !== 'string' && typeof value !== 'number') return '';
  const result = String(value).trim();
  return /[\u0000-\u001f\u007f\ud800-\udfff]/u.test(result) || ['null', 'undefined'].includes(result) ? '' : result;
}

// Existing navigation constructs encoded query values. Decode once, never recursively.
function decode(value) {
  const raw = text(value);
  try { return decodeURIComponent(raw); } catch (_) { return raw; }
}

function valid(key, value) {
  const raw = text(value);
  if (/Id$/.test(key)) return /^\d+$/.test(raw) && Number.isSafeInteger(Number(raw)) && Number(raw) > 0 ? String(Number(raw)) : '';
  if (ENUMS[key]) return ENUMS[key].includes(raw) ? raw : '';
  const max = key === 'priceRange' ? 40 : 80;
  if (Array.from(raw).length > max) return '';
  if (key === 'priceRange' && raw) {
    if (!/^(?:\d+(?:\.\d+)?)?-(?:\d+(?:\.\d+)?)?$/.test(raw) || raw === '-') return '';
    const [min, maxValue] = raw.split('-');
    if ((min && !Number.isFinite(Number(min))) || (maxValue && !Number.isFinite(Number(maxValue)))) return '';
    if (min && maxValue && Number(min) > Number(maxValue)) return '';
  }
  return raw;
}

function sanitize(page, input, encoded = false) {
  const result = {};
  for (const key of KEYS[page] || []) {
    const value = valid(key, encoded ? decode(input[key]) : input[key]);
    if (value) result[key] = value;
  }
  if (page === 'search' && !result.keyword) { delete result.scope; delete result.tab; }
  if (page === 'product-list' && !result.categoryId) delete result.categoryLevel;
  return result;
}

function safeTrack(event, properties) {
  try {
    const pending = track(event, properties);
    if (pending && typeof pending.catch === 'function') pending.catch(() => {});
  } catch (_) { /* Sharing must remain available when collection fails. */ }
}

function summary(page, values, channel, localRequestId = '') {
  return {
    page_path: `/pages/${page}/index`, share_channel: channel,
    sku_id: values.skuId || 0, brand_id: values.brandId, certificate_id: values.certificateId,
    brandId: values.brandId || 0, certificateId: values.certificateId || 0,
    sourcePage: 'share', share_path: `/pages/${page}/index`,
    requestId: /^[a-zA-Z0-9._:-]{1,128}$/.test(localRequestId) ? localRequestId : `share-${Date.now()}`,
    category_id: values.categoryId, has_keyword: Boolean(values.keyword),
    keyword_length: Array.from(values.keyword || '').length, filter_count: Object.keys(values).length,
  };
}

function receiveShare(page, query = {}) {
  packageLogo();
  const shared = query.source === 'share' || query.sourcePage === 'share';
  const aliases = { ...query };
  if (page === 'tile-detail') aliases.skuId = query.skuId || query.id;
  if (page === 'brand-detail') aliases.brandId = query.brandId || query.brand_id;
  if (page === 'certificate-detail') aliases.certificateId = query.certificateId || query.certificate_id;
  const values = sanitize(page, aliases, true);
  const result = shared ? { ...values, source: 'share', sourcePage: 'share' } : { ...query, ...values };
  // Replace rejected known values too, so they cannot reach Number()/API through the original query.
  for (const key of KEYS[page] || []) result[key] = values[key] || '';
  if (page === 'tile-detail') delete result.id;
  if (page === 'brand-detail') delete result.brand_id;
  if (page === 'certificate-detail') delete result.certificate_id;
  if (shared) {
    const channel = ['wechat_friend', 'wechat_timeline'].includes(query.shareChannel) ? query.shareChannel : 'unknown';
    safeTrack('share_page_open', summary(page, values, channel));
  }
  return result;
}

function context(page, instance) {
  const d = instance.data;
  if (page === 'tile-detail') return { skuId: d.id };
  if (page === 'category') return { categoryId: d.currentPrimaryId };
  if (page === 'search') return d.searchMode === 'result' ? { keyword: d.normalizedKeyword, scope: d.scope, tab: d.activeTab } : {};
  if (page === 'brand-list' || page === 'certificates') return { keyword: d.shareKeyword || '' };
  return d;
}

function serialize(values, channel) {
  return Object.keys(values).map((key) => `${key}=${encodeURIComponent(values[key])}`)
    .concat(['source=share', `shareChannel=${channel}`]).join('&');
}

function shareTitle(page, d, values, fallback) {
  if (fallback) return TITLES[page];
  if (page === 'tile-detail') return text(d.product && d.product.share && d.product.share.title) || text(d.product && d.product.product_name) || TITLES[page];
  if (page === 'brand-detail') return text(d.brand && d.brand.brand_name) || TITLES[page];
  if (page === 'certificate-detail') return text(d.detail && d.detail.certificate_name) || TITLES[page];
  if (page === 'index') return text(d.home && d.home.store && d.home.store.name) || TITLES[page];
  if (page === 'store-info') return text(d.store && d.store.name) || TITLES[page];
  if (values.keyword) return `${TITLES[page]}：${values.keyword}`;
  if (page === 'category') return text(d.currentPrimaryName) || TITLES[page];
  if (page === 'product-list') return values.categoryName || (values.brandId ? '品牌商品' : values.section === 'new' ? '新品榜' : values.section === 'hot' ? '热销榜' : TITLES[page]);
  return TITLES[page];
}

// Only an already validated lightweight candidate may be used; otherwise use the local logo.
function shareImage(page, instance) {
  const d = instance.data;
  let candidate = '';
  if (page === 'tile-detail') candidate = d.product && d.product.share && d.product.share.image_url || d.product && d.product.cover_image;
  if (page === 'brand-detail') candidate = d.brand && d.brand.brand_logo_thumbnail_url;
  if (page === 'certificate-detail') candidate = d.detail && d.detail.share && d.detail.share.image_url;
  if (page === 'product-list') candidate = d.items && d.items[0] && d.items[0].cover_image;
  candidate = text(candidate);
  if (!/^https:\/\//.test(candidate)) return packageLogo();
  const cache = instance.publicShareImage;
  if (cache && cache.url === candidate) return cache.ready ? cache.localPath : packageLogo();
  const state = { url: candidate, ready: false, localPath: '' };
  instance.publicShareImage = state;
  try {
    wx.getImageInfo({
      src: candidate,
      success: (result) => {
        // Keep decoded bytes locally: a previously valid signed URL may expire before sharing.
        const localPath = text(result && result.path);
        if (/^(?:wxfile:\/\/|https?:\/\/(?:tmp|usr)\/|\/(?!\/))/.test(localPath)) {
          state.localPath = localPath;
          state.ready = true;
        }
      },
      fail: () => { state.ready = false; },
    });
  } catch (_) { /* Package logo works without network APIs, including restricted entry modes. */ }
  return packageLogo();
}

function sharePage(page, instance, channel) {
  const input = context(page, instance);
  let values = sanitize(page, input);
  let fallback = (KEYS[page] || []).some((key) => input[key] !== 0 && text(input[key]) && !valid(key, input[key]));
  let query = serialize(values, channel);
  if (query.length > QUERY_LIMIT) { delete values.categoryName; query = serialize(values, channel); }
  if (query.length > QUERY_LIMIT || fallback) { values = {}; query = serialize(values, channel); fallback = true; }
  safeTrack(EVENTS[page], summary(page, values, channel, instance.data.requestId));
  const common = { title: shareTitle(page, instance.data, values, fallback), imageUrl: fallback ? packageLogo() : shareImage(page, instance) };
  return channel === 'wechat_timeline' ? { ...common, query } : { ...common, path: `/pages/${page}/index?${query}` };
}

module.exports = { sharePage, receiveShare, sanitize, serialize, QUERY_LIMIT, LOGO };
