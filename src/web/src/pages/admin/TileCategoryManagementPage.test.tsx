import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return {
    ...actual,
    useSearchParams: () => [new URLSearchParams(), vi.fn()] as const,
  };
});

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

const fetchCategoriesMock = vi.fn();
const fetchCategoryTreeMock = vi.fn();
const enableCategoryMock = vi.fn();
const disableCategoryMock = vi.fn();

vi.mock('@/features/admin/api/tile-categories-api', async () => {
  const actual = await vi.importActual<
    typeof import('@/features/admin/api/tile-categories-api')
  >('@/features/admin/api/tile-categories-api');
  return {
    ...actual,
    fetchCategories: (...args: unknown[]) => fetchCategoriesMock(...args),
    fetchCategoryTree: (...args: unknown[]) => fetchCategoryTreeMock(...args),
    enableCategory: (...args: unknown[]) => enableCategoryMock(...args),
    disableCategory: (...args: unknown[]) => disableCategoryMock(...args),
    deleteCategory: vi.fn(),
  };
});

vi.mock('@/features/admin/components/CategoryFormModal', () => ({
  CategoryFormModal: () => null,
}));

vi.mock('@/features/admin/components/CategoryTree', () => ({
  CategoryTree: () => null,
}));

import { TileCategoryManagementPage } from './TileCategoryManagementPage';

const baseSummary = {
  total: 2,
  filtered: 2,
  enabled_count: 1,
  disabled_count: 1,
  sku_bound_count: 1,
};

const enabledCategory = {
  id: 1,
  name: '启用类目',
  code: 'EN',
  path: '启用类目',
  level: 1,
  sort_order: 1,
  sku_count: 3,
  status: 'ENABLED' as const,
  parent_id: null,
  updated_at: '2026-06-01T00:00:00Z',
};

const disabledDeletableCategory = {
  id: 2,
  name: '停用类目',
  code: 'DIS',
  path: '停用类目',
  level: 1,
  sort_order: 2,
  sku_count: 0,
  status: 'DISABLED' as const,
  parent_id: null,
  updated_at: '2026-06-02T00:00:00Z',
};

function mockListResponse(items: typeof enabledCategory[], total: number) {
  fetchCategoriesMock.mockResolvedValue({
    items,
    total,
    page: 1,
    page_size: 10,
    summary: { ...baseSummary, total, filtered: total },
  });
  fetchCategoryTreeMock.mockResolvedValue([]);
}

describe('TileCategoryManagementPage', () => {
  it('shows enable and delete on disabled row with sku_count=0 (AC-009)', async () => {
    mockListResponse([disabledDeletableCategory], 1);

    render(<TileCategoryManagementPage />);

    await waitFor(() => {
      expect(fetchCategoriesMock).toHaveBeenCalled();
    });

    expect(screen.getByRole('button', { name: '启用' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '删除' })).toBeEnabled();
  });

  it('shows disable without delete on enabled row (AC-010)', async () => {
    mockListResponse([enabledCategory], 1);

    render(<TileCategoryManagementPage />);

    await waitFor(() => {
      expect(fetchCategoriesMock).toHaveBeenCalled();
    });

    expect(screen.getByRole('button', { name: '停用' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '删除' })).not.toBeInTheDocument();
  });

  it('opens enable confirm dialog before calling enableCategory', async () => {
    enableCategoryMock.mockResolvedValue(undefined);
    fetchCategoriesMock
      .mockResolvedValueOnce({
        items: [disabledDeletableCategory],
        total: 1,
        page: 1,
        page_size: 10,
        summary: { ...baseSummary, total: 1, filtered: 1, disabled_count: 1 },
      })
      .mockResolvedValueOnce({
        items: [{ ...disabledDeletableCategory, status: 'ENABLED' }],
        total: 1,
        page: 1,
        page_size: 10,
        summary: { ...baseSummary, total: 1, filtered: 1, enabled_count: 1 },
      });
    fetchCategoryTreeMock.mockResolvedValue([]);

    render(<TileCategoryManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '启用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '启用' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('启用类目')).toBeInTheDocument();
    expect(within(dialog).getByText('确认启用类目「停用类目」？')).toBeInTheDocument();
    expect(enableCategoryMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认启用' }));

    await waitFor(() => {
      expect(enableCategoryMock).toHaveBeenCalledWith(2);
    });

    expect(document.querySelector('.admin-toast-region')).toBeInTheDocument();
    expect(document.querySelector('.admin-toast')).toHaveTextContent('类目已启用');
    expect(document.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('opens disable confirm dialog before calling disableCategory', async () => {
    disableCategoryMock.mockResolvedValue(undefined);
    fetchCategoriesMock
      .mockResolvedValueOnce({
        items: [enabledCategory],
        total: 1,
        page: 1,
        page_size: 10,
        summary: { ...baseSummary, total: 1, filtered: 1, enabled_count: 1 },
      })
      .mockResolvedValueOnce({
        items: [{ ...enabledCategory, status: 'DISABLED' }],
        total: 1,
        page: 1,
        page_size: 10,
        summary: { ...baseSummary, total: 1, filtered: 1, disabled_count: 1 },
      });
    fetchCategoryTreeMock.mockResolvedValue([]);

    render(<TileCategoryManagementPage />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '停用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '停用' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('停用类目')).toBeInTheDocument();
    expect(
      within(dialog).getByText('确认停用类目「启用类目」？停用后前台将不再展示该类目。'),
    ).toBeInTheDocument();
    expect(disableCategoryMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认停用' }));

    await waitFor(() => {
      expect(disableCategoryMock).toHaveBeenCalledWith(1);
    });
  });

  it('does not show section titles and uses pagination v2 summary (REQ-0007)', async () => {
    mockListResponse([enabledCategory, disabledDeletableCategory], 2);

    render(<TileCategoryManagementPage />);

    await waitFor(() => {
      expect(fetchCategoriesMock).toHaveBeenCalled();
    });

    expect(screen.queryByText('类目检索')).not.toBeInTheDocument();
    expect(screen.queryByText('类目列表')).not.toBeInTheDocument();
    expect(screen.queryByText(/当前显示/)).not.toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/共 2 个类目/)).toBeInTheDocument();
    });
    expect(screen.getByText('每页显示')).toBeInTheDocument();
  });
});
