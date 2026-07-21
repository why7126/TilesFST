import { track } from '../../services/api';

type ProductCardInput = {
  product_id?: number;
  sku_id?: number;
  id?: number;
  product_name?: string | null;
  sku_name?: string | null;
  sku_code?: string | null;
  cover_image?: string | null;
  specification?: string | null;
  material?: string | null;
  surface_finish?: string | null;
  style?: string | null;
  category_name?: string | null;
  brand_name?: string | null;
  color_family?: string | null;
  price_display?: string | null;
  is_new?: boolean;
  is_hot?: boolean;
  available?: boolean;
  is_public?: boolean;
  status?: string | null;
};

type NormalizedProductCard = {
  skuId: number;
  productName: string;
  brandName: string;
  skuCode: string;
  specification: string;
  priceText: string;
  imageSrc: string;
  badge: string;
  available: boolean;
};

const FALLBACK_IMAGE = '/assets/tile-placeholder.png';
const NAV_LOCK_MS = 800;
const MAX_PARAM_LENGTH = 80;

function safeText(value: unknown, fallback: string): string {
  if (typeof value !== 'string') return fallback;
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : fallback;
}

function priceText(value: unknown): string {
  if (value === 0) return '暂无';
  const text = safeText(value, '暂无');
  const legacyNoPriceText = ['暂无', '参考价'].join('');
  const pendingPriceText = ['价格', '待维护'].join('');
  if (text === legacyNoPriceText || text === pendingPriceText) return '暂无';
  const numeric = Number(text.replace(/[¥￥,\s]/g, ''));
  return Number.isFinite(numeric) && numeric === 0 ? '暂无' : text;
}

function numberValue(value: unknown): number {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) ? parsed : 0;
}

function cleanParam(value: unknown): string {
  if (value === undefined || value === null) return '';
  return String(value).slice(0, MAX_PARAM_LENGTH);
}

function queryPair(key: string, value: unknown): string {
  const cleaned = cleanParam(value);
  return cleaned ? `${key}=${encodeURIComponent(cleaned)}` : '';
}

function normalizeProduct(product: ProductCardInput): NormalizedProductCard {
  const skuId = numberValue(product.sku_id || product.product_id || product.id);
  const badge = product.is_new ? '新品' : product.is_hot ? '热销' : product.status === 'offline' ? '下架' : '';
  const available = Boolean(skuId) && product.available !== false && product.is_public !== false && product.status !== 'offline';
  return {
    skuId,
    productName: safeText(product.sku_name || product.product_name, '未命名商品'),
    brandName: safeText(product.brand_name, '品牌待确认'),
    skuCode: safeText(product.sku_code, 'SKU 待补充'),
    specification: safeText(product.specification, '规格待补充'),
    priceText: priceText(product.price_display),
    imageSrc: safeText(product.cover_image, ''),
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
  },

  data: {
    normalized: normalizeProduct({}),
    imageFailed: false,
    navigating: false,
  },

  observers: {
    'product, imageFallback': function observeProduct(product: ProductCardInput) {
      const normalized = normalizeProduct(product || {});
      this.setData({
        normalized,
        imageFailed: false,
      });
      this.trackCard('product_card_exposure', normalized);
    },
  },

  methods: {
    openDetail() {
      const normalized = this.data.normalized as NormalizedProductCard;
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
        queryPair('requestId', this.properties.requestId),
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
      this.trackCard('product_card_image_failed', this.data.normalized as NormalizedProductCard);
    },

    trackCard(eventName: string, normalized: NormalizedProductCard) {
      track(eventName, {
        page_path: '/components/product-card/index',
        skuId: normalized.skuId || undefined,
        skuCode: normalized.skuCode,
        sourcePage: this.properties.sourcePage,
        sourceModule: this.properties.sourceModule,
        listContext: this.properties.listContext,
        index: this.properties.index,
        categoryId: this.properties.categoryId || undefined,
        brandId: this.properties.brandId || undefined,
        keyword: this.properties.keyword || undefined,
        requestId: this.properties.requestId || undefined,
      });
    },
  },
});
