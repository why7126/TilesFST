import { describe, expect, it } from 'vitest';

import { canDeleteBrand } from '../api/brands-api';

describe('canDeleteBrand', () => {
  it('allows delete when disabled and no sku', () => {
    expect(canDeleteBrand({ sku_count: 0, status: 'DISABLED' })).toBe(true);
  });

  it('blocks delete when enabled', () => {
    expect(canDeleteBrand({ sku_count: 0, status: 'ENABLED' })).toBe(false);
  });

  it('blocks delete when sku_count > 0 even if disabled', () => {
    expect(canDeleteBrand({ sku_count: 3, status: 'DISABLED' })).toBe(false);
  });

  it('blocks delete when enabled with sku', () => {
    expect(canDeleteBrand({ sku_count: 5, status: 'ENABLED' })).toBe(false);
  });
});
