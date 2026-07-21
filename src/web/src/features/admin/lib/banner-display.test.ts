import { describe, expect, it } from 'vitest';

import type { BannerAdminItem } from '@/shared/api/generated';

import {
  DEFAULT_POSITION,
  DISPLAY_CLIENT_OPTIONS,
  POSITIONS_BY_CLIENT,
  canDeleteBanner,
  canOnlineBanner,
  clearJumpFieldsForType,
  extractSkuMainImage,
} from './banner-display';

describe('banner-display helpers', () => {
  it('scopes display client and positions to miniapp carousels', () => {
    expect(DISPLAY_CLIENT_OPTIONS).toEqual([{ label: '小程序', value: 'MINIAPP_HOME' }]);
    expect(POSITIONS_BY_CLIENT.MINIAPP_HOME).toEqual([
      { value: 'MINIAPP_HOME_CAROUSEL', label: '首页轮播' },
      { value: 'MINIAPP_BRAND_LIST_CAROUSEL', label: '品牌列表页轮播' },
    ]);
    expect(Object.keys(POSITIONS_BY_CLIENT)).toEqual(['MINIAPP_HOME']);
    expect(DEFAULT_POSITION.MINIAPP_HOME).toBe('MINIAPP_HOME_CAROUSEL');
  });

  it('disables delete when banner is ONLINE', () => {
    const online = { status: 'ONLINE' } as Pick<BannerAdminItem, 'status'>;
    const draft = { status: 'DRAFT' } as Pick<BannerAdminItem, 'status'>;
    expect(canDeleteBanner(online)).toBe(false);
    expect(canDeleteBanner(draft)).toBe(true);
  });

  it('clears incompatible fields when jump_type changes', () => {
    const sku = clearJumpFieldsForType('SKU_DETAIL');
    expect(sku.sku_id).toBeNull();
    expect(sku.external_url).toBeNull();
    expect(sku.topic_id).toBeNull();
    expect(sku.brand_id).toBeNull();
    expect(sku.image_source).toBe('sku_main_image');

    const brand = clearJumpFieldsForType('BRAND_DETAIL');
    expect(brand.brand_id).toBeNull();
    expect(brand.sku_id).toBeNull();
    expect(brand.topic_id).toBeNull();
    expect(brand.external_url).toBeNull();
    expect(brand.image_source).toBe('brand_logo');

    const external = clearJumpFieldsForType('EXTERNAL_LINK');
    expect(external.external_url).toBe('');
    expect(external.image_source).toBe('custom_upload');
    expect(external.sku_id).toBeNull();
    expect(external.brand_id).toBeNull();

    const topic = clearJumpFieldsForType('TOPIC_PAGE');
    expect(topic.topic_id).toBeNull();
    expect(topic.image_source).toBe('custom_upload');

    const none = clearJumpFieldsForType('NO_JUMP');
    expect(none.sku_id).toBeNull();
    expect(none.external_url).toBeNull();
    expect(none.topic_id).toBeNull();
  });

  it('blocks online when time_status is EXPIRED', () => {
    expect(canOnlineBanner({ time_status: 'EXPIRED' })).toBe(false);
    expect(canOnlineBanner({ time_status: 'ACTIVE' })).toBe(true);
    expect(canOnlineBanner({ time_status: null })).toBe(true);
  });

  it('extracts main image from sku detail when list item has empty images', () => {
    const result = extractSkuMainImage({
      images: [{ id: 1, object_key: 'images/default/sku/main.webp', url: '/media/main.webp', is_main: true }],
      main_image_url: '/media/fallback.webp',
    });
    expect(result.objectKey).toBe('images/default/sku/main.webp');
    expect(result.url).toBe('/media/main.webp');
  });
});
