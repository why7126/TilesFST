import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const fetchBannersMock = vi.fn();

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/admin/api/banners-api', () => ({
  deleteBanner: vi.fn(),
  fetchBanners: (...args: unknown[]) => fetchBannersMock(...args),
  offlineBanner: vi.fn(),
  onlineBanner: vi.fn(),
}));

vi.mock('@/features/admin/components/BannerFormModal', () => ({
  BannerFormModal: () => null,
}));

import { BannerManagementPage } from './BannerManagementPage';

const listPayload = {
  items: [],
  total: 0,
  page: 1,
  page_size: 10,
  summary: {
    total: 0,
    filtered_count: 0,
    online_count: 0,
    pending_count: 0,
  },
};

const listWithItem = {
  ...listPayload,
  items: [
    {
      id: 1,
      title: '春季主推',
      position: 'MINIAPP_BRAND_LIST_CAROUSEL',
      display_client: 'MINIAPP_HOME',
      jump_type: 'NONE',
      status: 'ONLINE',
      image_url: null,
      valid_from: '2026-01-01T00:00:00',
      valid_to: '2026-12-31T23:59:59',
      sort_order: 10,
      updated_at: '2026-06-01T10:00:00',
    },
  ],
  total: 1,
  summary: {
    total: 1,
    filtered_count: 1,
    online_count: 1,
    pending_count: 0,
  },
};

describe('BannerManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchBannersMock.mockResolvedValue(listPayload);
  });

  it('requests and displays only miniapp banner scope options', async () => {
    render(
      <MemoryRouter>
        <BannerManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchBannersMock).toHaveBeenCalledWith(
        expect.objectContaining({ display_client: 'MINIAPP_HOME' }),
      );
    });

    const displayClientSelect = screen.getByLabelText('展示端') as HTMLSelectElement;
    expect(Array.from(displayClientSelect.options).map((option) => option.textContent)).toEqual([
      '小程序',
    ]);
    expect(displayClientSelect.value).toBe('MINIAPP_HOME');
    expect(screen.queryByText('Web 首页')).toBeNull();
    expect(screen.queryByText('专题页')).toBeNull();
  });

  it('renders standard pagination without section-head or banner-pagination', async () => {
    const { container } = render(
      <MemoryRouter>
        <BannerManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('共 0 个 Banner')).toBeInTheDocument();
    });

    expect(container.querySelector('.pagination')).toBeTruthy();
    expect(container.querySelector('.page-summary')).toBeTruthy();
    expect(container.querySelector('.page-size-wrap')).toBeTruthy();
    expect(container.querySelector('.section-head')).toBeNull();
    expect(container.querySelector('.banner-pagination')).toBeNull();
    expect(container.querySelector('.table-toolbar')).toBeNull();
    expect(screen.queryByRole('button', { name: '搜索' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();

    const hero = container.querySelector('.page-hero');
    const summary = container.querySelector('.summary-grid');
    const filter = container.querySelector('.filter-card');
    const table = container.querySelector('.table-card');
    expect(hero?.compareDocumentPosition(summary as Element)).toBeTruthy();
    expect(
      (hero?.compareDocumentPosition(summary as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      (summary?.compareDocumentPosition(filter as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      (filter?.compareDocumentPosition(table as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it('shows dedicated display position column without banner-sub in first column', async () => {
    fetchBannersMock.mockResolvedValue(listWithItem);

    const { container } = render(
      <MemoryRouter>
        <BannerManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('春季主推')).toBeInTheDocument();
    });

    expect(screen.getByRole('columnheader', { name: '展示位置' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '操作' })).toHaveClass(
      'admin-sticky-action-cell',
    );
    expect(container.querySelector('td.admin-sticky-action-cell')).toBeInTheDocument();
    expect(screen.getByText('品牌列表页轮播')).toBeInTheDocument();
    expect(container.querySelector('.banner-sub')).toBeNull();
    expect(container.querySelector('.banner-position')).toBeTruthy();
  });
});
