import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi, beforeEach } from 'vitest';

const fetchBrandsMock = vi.fn();
const enableBrandMock = vi.hoisted(() => vi.fn());
const disableBrandMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/admin/api/brands-api', () => ({
  canDeleteBrand: (brand: { sku_count: number; status: string }) =>
    brand.sku_count === 0 && brand.status === 'DISABLED',
  deleteBrand: vi.fn(),
  disableBrand: (...args: unknown[]) => disableBrandMock(...args),
  enableBrand: (...args: unknown[]) => enableBrandMock(...args),
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('@/features/admin/components/BrandFormModal', () => ({
  BrandFormModal: () => null,
}));

import { BrandManagementPage } from './BrandManagementPage';

const listPayload = {
  items: [
    {
      id: 1,
      name: '岩板品牌',
      short_name: '岩板',
      english_name: 'STONE',
      description: '高端岩板',
      logo_url: '/media/original/default/brands/logos/demo.webp',
      logo_object_key: 'original/default/brands/logos/demo.webp',
      sort_order: 10,
      sku_count: 0,
      status: 'DISABLED',
      updated_at: '2026-06-20T00:00:00Z',
    },
    {
      id: 2,
      name: '无标品牌',
      short_name: null,
      english_name: null,
      description: null,
      logo_url: null,
      logo_object_key: null,
      sort_order: 20,
      sku_count: 0,
      status: 'ENABLED',
      updated_at: '2026-06-20T00:00:00Z',
    },
  ],
  total: 2,
  page: 1,
  page_size: 20,
  summary: {
    total: 2,
    enabled_count: 1,
    disabled_count: 1,
    unlinked_sku_count: 0,
  },
};

describe('BrandManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchBrandsMock.mockResolvedValue(listPayload);
  });

  it('renders pagination with the same structure as user management', async () => {
    fetchBrandsMock.mockResolvedValue(listPayload);

    render(
      <MemoryRouter>
        <BrandManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchBrandsMock).toHaveBeenCalled();
    });

    expect(screen.getByText('共 2 条品牌')).toBeInTheDocument();
    expect(screen.getByText('每页显示')).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: '每页显示条数' })).toBeInTheDocument();
    expect(screen.getByLabelText('关键词')).toHaveAttribute(
      'placeholder',
      '搜索品牌名称 / 简称 / 英文名称',
    );
    expect(screen.getByLabelText('状态')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '操作' })).toHaveClass(
      'admin-sticky-action-cell',
    );
    expect(document.querySelector('td.admin-sticky-action-cell')).toBeInTheDocument();
    expect(screen.queryByText('跳至')).not.toBeInTheDocument();

    const pagination = screen.getByText('共 2 条品牌').closest('.pagination');
    expect(pagination?.querySelector('.page-summary')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-buttons')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-left')).not.toBeInTheDocument();
    expect(pagination?.querySelector('.brand-pagination-right')).not.toBeInTheDocument();
    expect(pagination?.querySelector('.jump-input')).not.toBeInTheDocument();
  });

  it('renders logo_url images and stable placeholders for brands without logo', async () => {
    fetchBrandsMock.mockResolvedValue(listPayload);

    const { container } = render(
      <MemoryRouter>
        <BrandManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchBrandsMock).toHaveBeenCalled();
    });

    const logo = container.querySelector('.brand-logo img') as HTMLImageElement | null;
    expect(logo?.getAttribute('src')).toBe('/media/original/default/brands/logos/demo.webp');
    expect(screen.getByText('无标')).toBeInTheDocument();
  });

  it('opens enable confirm dialog before calling enableBrand', async () => {
    enableBrandMock.mockResolvedValue(undefined);
    fetchBrandsMock.mockResolvedValue(listPayload);

    const { container } = render(
      <MemoryRouter>
        <BrandManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '启用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '启用' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('启用品牌')).toBeInTheDocument();
    expect(within(dialog).getByText('确认启用品牌「岩板品牌」？')).toBeInTheDocument();
    expect(enableBrandMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认启用' }));

    await waitFor(() => {
      expect(enableBrandMock).toHaveBeenCalledWith(1);
    });
    expect(container.querySelector('.admin-toast-region')).toBeInTheDocument();
    expect(container.querySelector('.admin-toast')).toHaveTextContent('品牌已启用');
    expect(container.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('opens disable confirm dialog before calling disableBrand', async () => {
    disableBrandMock.mockResolvedValue(undefined);
    fetchBrandsMock.mockResolvedValue(listPayload);

    render(
      <MemoryRouter>
        <BrandManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '停用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '停用' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('停用品牌')).toBeInTheDocument();
    expect(
      within(dialog).getByText('确认停用品牌「无标品牌」？停用后前台将不再展示该品牌。'),
    ).toBeInTheDocument();
    expect(disableBrandMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认停用' }));

    await waitFor(() => {
      expect(disableBrandMock).toHaveBeenCalledWith(2);
    });
  });

  it('does not call enableBrand when status confirm is cancelled', async () => {
    fetchBrandsMock.mockResolvedValue(listPayload);

    render(
      <MemoryRouter>
        <BrandManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '启用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '启用' }));

    const dialog = screen.getByRole('dialog');
    fireEvent.click(within(dialog).getByRole('button', { name: '取消' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(enableBrandMock).not.toHaveBeenCalled();
  });
});
