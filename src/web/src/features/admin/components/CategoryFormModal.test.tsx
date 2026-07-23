import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/tile-category-management.css';
import '../styles/user-management.css';

import type { TileCategoryAdminItem, TileCategoryTreeNode } from '@/shared/api/generated';

import { createCategory } from '../api/tile-categories-api';
import { CategoryFormModal } from './CategoryFormModal';

const cssPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '../styles/tile-category-management.css',
);
const tileCategoryCss = readFileSync(cssPath, 'utf8');
const userManagementCssPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '../styles/user-management.css',
);
const userManagementCss = readFileSync(userManagementCssPath, 'utf8');

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
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(createCategory).mockResolvedValue({} as TileCategoryAdminItem);
  });

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

    const parentSelect = screen.getByLabelText(/上级类目/);
    const options = within(parentSelect).getAllByRole('option').map((option) => option.textContent);

    expect(options).toEqual(['无，创建一级类目', '地面砖']);
    expect(
      screen.getByText('选择上级类目后自动生成层级；当前最多支持二级类目。类目编码由系统自动生成。'),
    ).toBeInTheDocument();
  });

  it('hides category code and marks required create fields', () => {
    const { container } = render(
      <CategoryFormModal
        open
        mode="create"
        category={null}
        tree={tree}
        defaultParentId={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(screen.queryByLabelText(/类目编码/)).not.toBeInTheDocument();
    expect(screen.getByLabelText(/上级类目/)).toBeInTheDocument();
    expect(screen.getByLabelText(/类目名称/)).toBeInTheDocument();
    expect(screen.getByLabelText(/排序权重/)).toBeInTheDocument();
    expect(container.querySelectorAll('.required-mark')).toHaveLength(3);
    expect(container.querySelector('.category-modal')).toBeTruthy();
    expect(container.querySelector('.modal-card')).toBeNull();
  });

  it('keeps the dedicated category modal CSS contract', () => {
    expect(tileCategoryCss).toContain('.admin-shell .category-modal');
    expect(tileCategoryCss).toContain('width: 560px');
    expect(tileCategoryCss).not.toContain('.category-modal.modal-card');
    expect(tileCategoryCss).not.toContain('.modal-card.category-modal');
    expect(userManagementCss).toContain('.admin-shell .modal-body');
    expect(userManagementCss).toContain('overflow-y: auto');
    expect(userManagementCss).toContain('.admin-shell .modal-footer');
  });

  it('does not show editable category code when editing', () => {
    render(
      <CategoryFormModal
        open
        mode="edit"
        category={{
          id: 1,
          parent_id: null,
          name: '地面砖',
          code: 'CAT-FLOOR',
          sort_order: 10,
          level: 1,
          description: null,
          status: 'ENABLED',
          sku_count: 0,
          path: '地面砖',
          created_at: '2026-07-22T00:00:00Z',
          updated_at: '2026-07-22T00:00:00Z',
        }}
        tree={tree}
        defaultParentId={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(screen.queryByLabelText(/类目编码/)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/上级类目/)).not.toBeInTheDocument();
  });

  it('shows field-level validation errors before submit', () => {
    render(
      <CategoryFormModal
        open
        mode="create"
        category={null}
        tree={tree}
        defaultParentId={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    fireEvent.change(screen.getByLabelText(/类目名称/), { target: { value: 'bad-name' } });
    fireEvent.change(screen.getByLabelText(/排序权重/), { target: { value: '1.5' } });
    fireEvent.click(screen.getByRole('button', { name: '保存类目' }));

    expect(screen.getByText('类目名称只能包含中文、英文和数字')).toBeInTheDocument();
    expect(screen.getByText('排序权重必须为正整数')).toBeInTheDocument();
    expect(createCategory).not.toHaveBeenCalled();
  });

  it('submits create payload without code', async () => {
    const onSuccess = vi.fn();
    const onClose = vi.fn();
    render(
      <CategoryFormModal
        open
        mode="create"
        category={null}
        tree={tree}
        defaultParentId={1}
        onClose={onClose}
        onSuccess={onSuccess}
      />,
    );

    fireEvent.change(screen.getByLabelText(/类目名称/), { target: { value: '岩板A1' } });
    fireEvent.change(screen.getByLabelText(/排序权重/), { target: { value: '12' } });
    fireEvent.click(screen.getByRole('button', { name: '保存类目' }));

    await waitFor(() => expect(createCategory).toHaveBeenCalled());
    expect(createCategory).toHaveBeenCalledWith({
      parent_id: 1,
      name: '岩板A1',
      sort_order: 12,
      description: null,
      status: 'ENABLED',
    });
    expect(onSuccess).toHaveBeenCalledWith('类目已创建');
    expect(onClose).toHaveBeenCalled();
  });
});
