import { track } from '../../services/api';

type BrandCardInput = {
  brand_id?: number | string | null;
  brand_name?: string | null;
  brand_short_name?: string | null;
  brand_logo_url?: string | null;
  brand_entry_path?: string | null;
  available?: boolean;
};

type NormalizedBrandCard = {
  brandId: number | string;
  brandName: string;
  rawBrandName: string;
  hint: string;
  logoSrc: string;
  fallbackText: string;
  entryPath: string;
  available: boolean;
  unavailableReason: string;
};

const NAV_LOCK_MS = 800;
const MAX_PARAM_LENGTH = 80;

function safeText(value: unknown, fallback = ''): string {
  if (typeof value !== 'string') return fallback;
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : fallback;
}

function cleanParam(value: unknown): string {
  if (value === undefined || value === null) return '';
  return String(value).trim().slice(0, MAX_PARAM_LENGTH);
}

function firstBrandLetter(name: string): string {
  const text = safeText(name, '品牌');
  const compact = text.replace(/\s/g, '');
  return compact ? compact.slice(0, 2).toUpperCase() : '品牌';
}

function normalizeBrand(brand: BrandCardInput, hint: string): NormalizedBrandCard {
  const rawBrandName = safeText(brand.brand_name || brand.brand_short_name, '');
  const brandName = rawBrandName || '品牌信息待完善';
  const entryPath = safeText(brand.brand_entry_path, '');
  const logoSrc = safeText(brand.brand_logo_url, '');
  const available = Boolean(rawBrandName) && (Boolean(entryPath) || brand.available !== false);
  return {
    brandId: brand.brand_id || '',
    brandName,
    rawBrandName,
    hint: available ? safeText(hint, '查看品牌主页与同品牌产品') : '暂无内容',
    logoSrc,
    fallbackText: firstBrandLetter(brandName),
    entryPath,
    available,
    unavailableReason: rawBrandName ? 'entry_unavailable' : 'missing_brand_name',
  };
}

function fallbackSearchPath(brandName: string): string {
  return `/pages/search/index?keyword=${encodeURIComponent(cleanParam(brandName))}`;
}

Component({
  properties: {
    brand: { type: Object, value: {} },
    hint: { type: String, value: '查看品牌主页与同品牌产品' },
    sourcePage: { type: String, value: 'direct' },
    sourceModule: { type: String, value: 'brand-card' },
    density: { type: String, value: 'default' },
    skuId: { type: null, value: '' },
    listContext: { type: String, value: '' },
    index: { type: Number, value: 0 },
    requestId: { type: String, value: '' },
  },

  data: {
    normalized: normalizeBrand({}, '查看品牌主页与同品牌产品'),
    imageFailed: false,
    navigating: false,
  },

  observers: {
    'brand, hint': function observeBrand(brand: BrandCardInput, hint: string) {
      this.setData({
        normalized: normalizeBrand(brand || {}, hint),
        imageFailed: false,
        navigating: false,
      });
    },
  },

  methods: {
    openBrand() {
      const normalized = this.data.normalized as NormalizedBrandCard;
      if (!normalized.available) {
        wx.showToast({ title: '暂无内容', icon: 'none' });
        this.trackBrandCard('brand_card_unavailable_click', normalized);
        return;
      }
      if (this.data.navigating) return;

      this.setData({ navigating: true });
      const url = normalized.entryPath || fallbackSearchPath(normalized.rawBrandName);
      this.trackBrandCard('brand_card_click', normalized);
      wx.navigateTo({
        url,
        fail: () => {
          const fallbackUrl = fallbackSearchPath(normalized.rawBrandName);
          wx.navigateTo({
            url: fallbackUrl,
            fail: () => wx.showToast({ title: '暂无内容', icon: 'none' }),
          });
        },
        complete: () => {
          setTimeout(() => this.setData({ navigating: false }), NAV_LOCK_MS);
        },
      });
    },

    onImageError() {
      this.setData({ imageFailed: true });
      this.trackBrandCard('brand_card_image_failed', this.data.normalized as NormalizedBrandCard);
    },

    trackBrandCard(eventName: string, normalized: NormalizedBrandCard) {
      track(eventName, {
        page_path: '/components/brand-card/index',
        brandId: normalized.brandId || undefined,
        brandName: normalized.rawBrandName || normalized.brandName,
        sourcePage: this.properties.sourcePage,
        sourceModule: this.properties.sourceModule,
        skuId: this.properties.skuId || undefined,
        listContext: this.properties.listContext || undefined,
        index: this.properties.index,
        requestId: this.properties.requestId || undefined,
        unavailableReason: normalized.available ? undefined : normalized.unavailableReason,
      });
    },
  },
});
