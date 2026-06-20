import { describe, expect, it } from 'vitest';

import { canDeleteTileSku, formatReferencePrice } from './tile-skus-api';

describe('tile-skus-api helpers', () => {
  it('formats reference price', () => {
    expect(formatReferencePrice(268)).toBe('¥ 268.00');
    expect(formatReferencePrice(null)).toBe('—');
  });

  it('blocks delete for published sku', () => {
    expect(canDeleteTileSku({ status: 'PUBLISHED' })).toBe(false);
    expect(canDeleteTileSku({ status: 'DRAFT' })).toBe(true);
  });
});
