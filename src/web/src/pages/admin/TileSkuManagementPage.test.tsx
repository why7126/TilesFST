import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const fetchTileSkusMock = vi.fn();
const fetchBrandsMock = vi.fn();
const fetchCategoryTreeMock = vi.fn();
const publishTileSkuMock = vi.fn();
const unpublishTileSkuMock = vi.fn();

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/admin/api/brands-api', () => ({
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('@/features/admin/api/tile-categories-api', () => ({
  buildParentOptions: () => [],
  fetchCategoryTree: (...args: unknown[]) => fetchCategoryTreeMock(...args),
}));

vi.mock('@/features/admin/api/tile-skus-api', () => ({
  canDeleteTileSku: (sku: { status: string }) => sku.status !== 'PUBLISHED',
  deleteTileSku: vi.fn(),
  fetchTileSku: vi.fn(),
  fetchTileSkus: (...args: unknown[]) => fetchTileSkusMock(...args),
  formatReferencePrice: (price: number | null | undefined) =>
    price == null ? '—' : `¥ ${price.toFixed(2)}`,
  publishTileSku: (...args: unknown[]) => publishTileSkuMock(...args),
  unpublishTileSku: (...args: unknown[]) => unpublishTileSkuMock(...args),
}));

vi.mock('@/features/admin/components/TileSkuFormModal', () => ({
  TileSkuFormModal: () => null,
}));

import { TileSkuManagementPage } from './TileSkuManagementPage';

const listPayload = {
  items: [
    {
      id: 1,
      name: '测试 SKU',
      sku_code: 'SKU-001',
      brand_name: '测试品牌',
      category_name: '墙砖',
      size: '600×600',
      surface_finish: '哑光',
      reference_price: 268,
      has_main_image: true,
      image_count: 2,
      video_count: 1,
      status: 'DRAFT',
      updated_at: '2026-06-20T00:00:00Z',
      main_image_url: null,
    },
  ],
  total: 1,
  page: 1,
  page_size: 20,
  summary: {
    total: 1,
    published_count: 0,
    needs_completion_count: 0,
    draft_count: 1,
  },
};

describe('TileSkuManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchBrandsMock.mockResolvedValue({ items: [] });
    fetchCategoryTreeMock.mockResolvedValue([]);
    fetchTileSkusMock.mockResolvedValue(listPayload);
  });

  it('renders pagination aligned with user management and no table-head', async () => {
    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchTileSkusMock).toHaveBeenCalled();
    });

    expect(screen.queryByText('SKU 列表')).not.toBeInTheDocument();
    expect(document.querySelector('.table-head')).not.toBeInTheDocument();

    expect(screen.getByText('共 1 条')).toBeInTheDocument();
    expect(screen.getByText('每页显示')).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: '每页显示条数' })).toBeInTheDocument();

    const pagination = screen.getByText('共 1 条').closest('.pagination');
    expect(pagination?.querySelector('.page-summary')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-buttons')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-left')).not.toBeInTheDocument();
    expect(pagination?.querySelector('.brand-pagination-right')).not.toBeInTheDocument();
  });

  it('shows restore action for disabled SKU rows', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 2,
          sku_code: 'SKU-DISABLED-001',
          status: 'DISABLED',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '恢复' })).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: '编辑' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '删除' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '上架' })).not.toBeInTheDocument();
  });

  it('shows unpublish action for published SKU rows', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 3,
          sku_code: 'SKU-PUBLISHED-001',
          status: 'PUBLISHED',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '下架' })).toBeInTheDocument();
    });

    expect(screen.queryByRole('button', { name: '恢复' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '上架' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '删除' })).toBeDisabled();
  });

  it('opens publish confirm dialog before calling publishTileSku on restore', async () => {
    publishTileSkuMock.mockResolvedValue({});
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 4,
          name: '已下架 SKU',
          sku_code: 'SKU-DISABLED-002',
          status: 'DISABLED',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '恢复' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '恢复' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('上架 SKU')).toBeInTheDocument();
    expect(within(dialog).getByText('确认上架 SKU「已下架 SKU」？')).toBeInTheDocument();
    expect(publishTileSkuMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认上架' }));

    await waitFor(() => {
      expect(publishTileSkuMock).toHaveBeenCalledWith(4);
    });

    expect(document.querySelector('.admin-toast-region')).toBeInTheDocument();
    expect(document.querySelector('.admin-toast')).toHaveTextContent('SKU 已上架');
    expect(document.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('opens unpublish confirm dialog before calling unpublishTileSku', async () => {
    unpublishTileSkuMock.mockResolvedValue({});
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 5,
          name: '已上架 SKU',
          sku_code: 'SKU-PUBLISHED-002',
          status: 'PUBLISHED',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '下架' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '下架' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('下架 SKU')).toBeInTheDocument();
    expect(
      within(dialog).getByText('确认下架 SKU「已上架 SKU」？下架后前台将不再展示该商品。'),
    ).toBeInTheDocument();
    expect(unpublishTileSkuMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认下架' }));

    await waitFor(() => {
      expect(unpublishTileSkuMock).toHaveBeenCalledWith(5);
    });
  });

  it('does not call publishTileSku when status confirm is cancelled', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 6,
          status: 'DISABLED',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '恢复' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '恢复' }));

    const dialog = screen.getByRole('dialog');
    fireEvent.click(within(dialog).getByRole('button', { name: '取消' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(publishTileSkuMock).not.toHaveBeenCalled();
  });
});
