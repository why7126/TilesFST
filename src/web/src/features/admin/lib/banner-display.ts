import type { BannerAdminItem, TileSkuAdminItem } from '@/shared/api/generated';

export const BANNER_PAGE_SIZES = [10, 20, 50] as const;

export const DISPLAY_CLIENT_OPTIONS = [
  { label: '小程序', value: 'MINIAPP_HOME' },
] as const;

export const BANNER_STATUS_OPTIONS = [
  { label: '全部状态', value: '' },
  { label: '草稿', value: 'DRAFT' },
  { label: '已上线', value: 'ONLINE' },
  { label: '已下线', value: 'OFFLINE' },
  { label: '已过期', value: 'EXPIRED' },
] as const;

export const TIME_STATUS_OPTIONS = [
  { label: '全部', value: '' },
  { label: '当前生效', value: 'ACTIVE' },
  { label: '待生效', value: 'PENDING' },
  { label: '已过期', value: 'EXPIRED' },
] as const;

export const JUMP_TYPE_OPTIONS = [
  { label: 'SKU 详情', value: 'SKU_DETAIL' },
  { label: '品牌详情', value: 'BRAND_DETAIL' },
  { label: '外部链接', value: 'EXTERNAL_LINK' },
  { label: '专题页', value: 'TOPIC_PAGE' },
  { label: '无跳转', value: 'NO_JUMP' },
] as const;

export const POSITIONS_BY_CLIENT: Record<string, { value: string; label: string }[]> = {
  MINIAPP_HOME: [
    { value: 'MINIAPP_HOME_CAROUSEL', label: '首页轮播' },
    { value: 'MINIAPP_BRAND_LIST_CAROUSEL', label: '品牌列表页轮播' },
  ],
};

export const DEFAULT_POSITION: Record<string, string> = {
  MINIAPP_HOME: 'MINIAPP_HOME_CAROUSEL',
};

export function displayClientLabel(value: string): string {
  const map: Record<string, string> = {
    MINIAPP_HOME: '小程序',
  };
  return map[value] ?? value;
}

export function displayClientBadgeClass(value: string): string {
  if (value === 'MINIAPP_HOME') return 'badge mini';
  return 'badge mini';
}

export function positionLabel(value: string): string {
  for (const positions of Object.values(POSITIONS_BY_CLIENT)) {
    const found = positions.find((p) => p.value === value);
    if (found) return found.label;
  }
  return value;
}

export function jumpTypeLabel(value: string): string {
  const map: Record<string, string> = {
    SKU_DETAIL: 'SKU详情',
    BRAND_DETAIL: '品牌详情',
    EXTERNAL_LINK: '外部链接',
    TOPIC_PAGE: '专题页',
    NO_JUMP: '无跳转',
  };
  return map[value] ?? value;
}

export function jumpTypeBadgeClass(value: string): string {
  const map: Record<string, string> = {
    SKU_DETAIL: 'badge link-sku',
    BRAND_DETAIL: 'badge link-cat',
    EXTERNAL_LINK: 'badge link-url',
    TOPIC_PAGE: 'badge link-cat',
    NO_JUMP: 'badge link-none',
  };
  return map[value] ?? 'badge link-none';
}

export function formatBannerDateTime(value: string | null | undefined): string {
  if (!value) return '未设置';
  return value.replace('T', ' ').slice(0, 16);
}

export function bannerStatusDisplay(banner: Pick<BannerAdminItem, 'status' | 'time_status'>): {
  label: string;
  className: string;
} {
  if (banner.time_status === 'PENDING') {
    return { label: '待生效', className: 'badge pending' };
  }
  if (banner.time_status === 'EXPIRED' || banner.status === 'EXPIRED') {
    return { label: '已过期', className: 'badge off' };
  }
  if (banner.status === 'ONLINE') {
    return { label: '已上线', className: 'badge ok' };
  }
  if (banner.status === 'OFFLINE') {
    return { label: '已下线', className: 'badge off' };
  }
  return { label: '草稿', className: 'badge draft' };
}

export function canDeleteBanner(banner: Pick<BannerAdminItem, 'status'>): boolean {
  return banner.status !== 'ONLINE';
}

export function canOnlineBanner(banner: Pick<BannerAdminItem, 'time_status'>): boolean {
  return banner.time_status !== 'EXPIRED';
}

export function jumpTypeModalTitle(jumpType: string): string {
  return `新增 Banner · ${jumpTypeLabel(jumpType)}`;
}

export function clearJumpFieldsForType(jumpType: string): {
  sku_id: number | null;
  external_url: string | null;
  topic_id: number | null;
  brand_id: number | null;
  sku_gallery_asset_id: number | null;
  image_source: string;
} {
  if (jumpType === 'SKU_DETAIL') {
    return {
      sku_id: null,
      external_url: null,
      topic_id: null,
      brand_id: null,
      sku_gallery_asset_id: null,
      image_source: 'sku_main_image',
    };
  }
  if (jumpType === 'BRAND_DETAIL') {
    return {
      sku_id: null,
      external_url: null,
      topic_id: null,
      brand_id: null,
      sku_gallery_asset_id: null,
      image_source: 'brand_logo',
    };
  }
  if (jumpType === 'EXTERNAL_LINK') {
    return {
      sku_id: null,
      external_url: '',
      topic_id: null,
      brand_id: null,
      sku_gallery_asset_id: null,
      image_source: 'custom_upload',
    };
  }
  if (jumpType === 'TOPIC_PAGE') {
    return {
      sku_id: null,
      external_url: null,
      topic_id: null,
      brand_id: null,
      sku_gallery_asset_id: null,
      image_source: 'custom_upload',
    };
  }
  return {
    sku_id: null,
    external_url: null,
    topic_id: null,
    brand_id: null,
    sku_gallery_asset_id: null,
    image_source: 'custom_upload',
  };
}

export function extractSkuMainImage(
  sku: Pick<TileSkuAdminItem, 'images' | 'main_image_url'>,
): { objectKey: string | null; url: string | null } {
  const mainImage = sku.images?.find((img) => img.is_main) ?? sku.images?.[0];
  return {
    objectKey: mainImage?.object_key ?? null,
    url: mainImage?.url ?? sku.main_image_url ?? null,
  };
}
