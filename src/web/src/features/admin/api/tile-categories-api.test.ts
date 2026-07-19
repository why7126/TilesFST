import { describe, expect, it } from 'vitest';

import {
  buildParentOptions,
  canDeleteCategory,
} from '../api/tile-categories-api';
import type { TileCategoryTreeNode } from '@/shared/api/generated';

const sampleTree: TileCategoryTreeNode[] = [
  {
    id: 1,
    name: '按材质',
    code: 'CAT-MAT',
    level: 1,
    status: 'ENABLED',
    sku_count: 10,
    children: [
      {
        id: 2,
        name: '大理石',
        code: 'CAT-MARBLE',
        level: 2,
        status: 'ENABLED',
        sku_count: 5,
        children: [
          {
            id: 3,
            name: '卡拉拉白',
            code: 'CAT-CAL',
            level: 3,
            status: 'ENABLED',
            sku_count: 2,
            children: [],
          },
        ],
      },
    ],
  },
];

describe('canDeleteCategory', () => {
  it('allows delete when disabled and no sku', () => {
    expect(canDeleteCategory({ sku_count: 0, status: 'DISABLED' })).toBe(true);
  });

  it('blocks delete when enabled', () => {
    expect(canDeleteCategory({ sku_count: 0, status: 'ENABLED' })).toBe(false);
  });

  it('blocks delete when sku bound', () => {
    expect(canDeleteCategory({ sku_count: 2, status: 'DISABLED' })).toBe(false);
  });
});

describe('buildParentOptions', () => {
  it('only allows root and level-1 nodes as parent candidates', () => {
    const options = buildParentOptions(sampleTree);
    const ids = options.map((o) => o.id);
    expect(ids).toContain(null);
    expect(ids).toContain(1);
    expect(ids).not.toContain(2);
    expect(ids).not.toContain(3);
  });
});
