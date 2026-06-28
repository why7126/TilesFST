import { describe, expect, it } from 'vitest';

import { canDeleteTileSpec } from '@/features/admin/api/tile-specs-api';

describe('canDeleteTileSpec', () => {
  it('allows delete only when disabled and unlinked', () => {
    expect(canDeleteTileSpec({ sku_count: 0, status: 'DISABLED' })).toBe(true);
    expect(canDeleteTileSpec({ sku_count: 0, status: 'ENABLED' })).toBe(false);
    expect(canDeleteTileSpec({ sku_count: 2, status: 'DISABLED' })).toBe(false);
    expect(canDeleteTileSpec({ sku_count: 1, status: 'ENABLED' })).toBe(false);
  });
});
