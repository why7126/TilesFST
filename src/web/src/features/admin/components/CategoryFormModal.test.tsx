import { render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import type { TileCategoryTreeNode } from '@/shared/api/generated';

import { CategoryFormModal } from './CategoryFormModal';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('../api/tile-categories-api', async () => {
  const actual = await vi.importActual<typeof import('../api/tile-categories-api')>(
    '../api/tile-categories-api',
  );
  return {
    ...actual,
    createCategory: vi.fn(),
    updateCategory: vi.fn(),
  };
});

const tree: TileCategoryTreeNode[] = [
  {
    id: 1,
    name: '地面砖',
    code: 'CAT-FLOOR',
    level: 1,
    status: 'ENABLED',
    sku_count: 0,
    children: [
      {
        id: 2,
        name: '通体大理石',
        code: 'CAT-MARBLE',
        level: 2,
        status: 'ENABLED',
        sku_count: 0,
        children: [],
      },
    ],
  },
];

describe('CategoryFormModal', () => {
  it('only offers root and level-1 parents when creating categories', () => {
    render(
      <CategoryFormModal
        open
        mode="create"
        category={null}
        tree={tree}
        defaultParentId={2}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    const parentSelect = screen.getByLabelText('上级类目');
    const options = within(parentSelect).getAllByRole('option').map((option) => option.textContent);

    expect(options).toEqual(['无，创建一级类目', '地面砖']);
    expect(screen.getByText('选择上级类目后自动生成层级；当前最多支持二级类目。')).toBeInTheDocument();
  });
});
