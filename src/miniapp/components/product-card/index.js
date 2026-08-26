const { track } = require('../../services/api');

const FALLBACK_IMAGE = '';
const NAV_LOCK_MS = 800;
const MAX_PARAM_LENGTH = 80;
const EXPOSURE_FLUSH_DELAY_MS = 120;

const trackedExposureKeys = {};
const pendingExposureBatches = {};

function telemetryId() {
  return `product-card-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
}

function safeText(value, fallback) {
  if (typeof value !== 'string') return fallback;
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : fallback;
}

function priceText(value) {
  if (value === 0) return '暂无';
  const text = safeText(value, '暂无');
  const legacyNoPriceText = ['暂无', '参考价'].join('');
  const pendingPriceText = ['价格', '待维护'].join('');
  if (text === legacyNoPriceText || text === pendingPriceText) return '暂无';
  const numeric = Number(text.replace(/[¥￥,\s]/g, ''));
  return Number.isFinite(numeric) && numeric === 0 ? '暂无' : text;
}

function numberValue(value) {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) ? parsed : 0;
}

function cleanParam(value) {
  if (value === undefined || value === null) return '';
  return String(value).slice(0, MAX_PARAM_LENGTH);
}

function queryPair(key, value) {
  const cleaned = cleanParam(value);
  return cleaned ? `${key}=${encodeURIComponent(cleaned)}` : '';
}

function exposureKey(properties) {
  return [
    properties.page_path,
    properties.sourcePage,
    properties.sourceModule,
    properties.listContext,
    properties.keyword || 'no-keyword',
    properties.requestId || 'no-request',
    properties.skuId || 'missing-sku',
  ].join('|');
}

function batchKey(properties) {
  return [
    properties.page_path,
    properties.sourcePage,
    properties.sourceModule,
    properties.listContext,
    properties.keyword || 'no-keyword',
    properties.requestId || 'no-request',
  ].join('|');
}

function queueProductCardExposure(properties) {
  if (!properties.skuId) return;
  const uniqueKey = exposureKey(properties);
  if (trackedExposureKeys[uniqueKey]) return;
  trackedExposureKeys[uniqueKey] = true;

  const key = batchKey(properties);
  const batch = pendingExposureBatches[key] || { items: [] };
  batch.items.push(properties);
  pendingExposureBatches[key] = batch;
  if (batch.timer) return;

  batch.timer = setTimeout(() => {
    flushProductCardExposureBatch(key);
  }, EXPOSURE_FLUSH_DELAY_MS);
}

function flushProductCardExposureBatch(key) {
  const batch = pendingExposureBatches[key];
  if (!batch || batch.items.length === 0) return;
  delete pendingExposureBatches[key];

  const first = batch.items[0];
  track('product_card_exposure', {
    ...first,
    exposureCount: batch.items.length,
    exposureItems: batch.items.map((item) => ({
      skuId: item.skuId,
      skuCode: item.skuCode,
      index: item.index,
      requestId: item.requestId,
    })),
  });
}

function normalizeProduct(product) {
  const skuId = numberValue(product.sku_id || product.product_id || product.id);
  const badge = product.is_recall_pinned
    ? '置顶'
    : product.is_new
      ? '新品'
      : product.is_hot
        ? '热销'
        : product.status === 'offline'
          ? '下架'
          : '';
  const available = Boolean(skuId) && product.available !== false && product.is_public !== false && product.status !== 'offline';
  return {
    skuId,
    productName: safeText(product.sku_name || product.product_name, '未命名商品'),
    brandName: safeText(product.brand_name, '品牌待确认'),
    skuCode: safeText(product.sku_code, 'SKU 待补充'),
    specification: safeText(product.specification, '规格待补充'),
    priceText: priceText(product.price_display),
    imageSrc: safeText(product.thumbnail_url || product.cover_image, ''),
    badge,
    available,
  };
}

Component({
  properties: {
    product: { type: Object, value: {} },
    density: { type: String, value: 'list' },
    sourcePage: { type: String, value: 'direct' },
    sourceModule: { type: String, value: '' },
    categoryId: { type: String, value: '' },
    brandId: { type: String, value: '' },
    keyword: { type: String, value: '' },
    listContext: { type: String, value: '' },
    index: { type: Number, value: 0 },
    requestId: { type: String, value: '' },
    imageFallback: { type: String, value: FALLBACK_IMAGE },
    imageLazyLoad: { type: Boolean, value: true },
  },

  data: {
    normalized: normalizeProduct({}),
    imageFailed: false,
    navigating: false,
    telemetryRequestId: '',
  },

  observers: {
    'product, imageFallback': function observeProduct(product) {
      const normalized = normalizeProduct(product || {});
      this.setData({
        normalized,
        imageFailed: false,
      });
      this.trackCardExposure(normalized);
    },
  },

  methods: {
    openDetail() {
      const normalized = this.data.normalized;
      if (!normalized.available) {
        wx.showToast({ title: '商品暂不可查看', icon: 'none' });
        this.trackCard('product_card_unavailable_click', normalized);
        return;
      }
      if (this.data.navigating) return;
      this.setData({ navigating: true });
      this.trackCard('product_card_click', normalized);
      this.triggerEvent('cardtap', {
        product: this.properties.product,
        skuId: normalized.skuId,
        index: this.properties.index,
      });
      const params = [
        `skuId=${normalized.skuId}`,
        queryPair('source', this.properties.sourcePage || 'direct'),
        queryPair('sourcePage', this.properties.sourcePage),
        queryPair('sourceModule', this.properties.sourceModule),
        queryPair('categoryId', this.properties.categoryId),
        queryPair('brandId', this.properties.brandId),
        queryPair('keyword', this.properties.keyword),
        queryPair('listContext', this.properties.listContext),
        queryPair('index', this.properties.index),
        queryPair('requestId', this.resolveTelemetryRequestId()),
      ].filter(Boolean).join('&');
      wx.navigateTo({
        url: `/pages/tile-detail/index?${params}`,
        fail: () => wx.showToast({ title: '商品打开失败，请重试', icon: 'none' }),
        complete: () => {
          setTimeout(() => this.setData({ navigating: false }), NAV_LOCK_MS);
        },
      });
    },

    onImageError() {
      this.setData({ imageFailed: true });
      this.trackCard('product_card_image_failed', this.data.normalized);
    },

    resolveTelemetryRequestId() {
      if (this.properties.requestId) return this.properties.requestId;
      if (this.data.telemetryRequestId) return this.data.telemetryRequestId;
      const requestId = telemetryId();
      this.setData({ telemetryRequestId: requestId });
      return requestId;
    },

    cardTelemetryProperties(normalized) {
      return {
        page_path: '/components/product-card/index',
        skuId: normalized.skuId || undefined,
        skuCode: normalized.skuCode,
        sourcePage: this.properties.sourcePage,
        sourceModule: this.properties.sourceModule || 'product-card',
        listContext: this.properties.listContext || this.properties.sourceModule || 'product-card',
        index: this.properties.index,
        categoryId: this.properties.categoryId || undefined,
        brandId: this.properties.brandId || undefined,
        keyword: this.properties.keyword || undefined,
        requestId: this.resolveTelemetryRequestId(),
      };
    },

    trackCardExposure(normalized) {
      queueProductCardExposure(this.cardTelemetryProperties(normalized));
    },

    trackCard(eventName, normalized) {
      track(eventName, this.cardTelemetryProperties(normalized));
    },
  },
});
