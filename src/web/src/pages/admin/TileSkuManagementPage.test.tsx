import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const tileSkuCss = readFileSync(
  join(process.cwd(), 'src/features/admin/styles/tile-sku-management.css'),
  'utf8',
);

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
import { formatSkuDateTime } from '@/features/admin/lib/tile-sku-display';

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
      published_at: null,
      updated_at: '2026-06-20T00:00:00Z',
      main_image_url: null,
      main_image_thumbnail_url: null,
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

const categoryTreePayload = [
  {
    id: 10,
    name: '亮光产品',
    level: 1,
    children: [
      {
        id: 11,
        name: '大理石瓷砖',
        level: 2,
        children: [
          {
            id: 12,
            name: '柔光灰砖',
            level: 3,
            children: [],
          },
        ],
      },
    ],
  },
  {
    id: 20,
    name: '木纹砖产品',
    level: 1,
    children: [],
  },
];

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

    const summary = screen.getByLabelText('SKU 统计');
    const cards = Array.from(summary.querySelectorAll('.metric-card'));
    expect(summary).toHaveClass('summary-grid');
    expect(cards).toHaveLength(4);
    cards.forEach((card) => {
      expect(card.tagName.toLowerCase()).toBe('article');
      expect(card.querySelector('.metric-label')).toBeInTheDocument();
      expect(card.querySelector('.metric-value')).toBeInTheDocument();
      expect(card.querySelector('.metric-desc')).toBeInTheDocument();
    });

    expect(screen.getByText('共 1 条')).toBeInTheDocument();
    expect(screen.getByText('每页显示')).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: '每页显示条数' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('商品名称 / SKU 编码')).toBeInTheDocument();
    expect(screen.queryByText('素材完整度')).not.toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: '操作' })).toHaveClass(
      'admin-sticky-action-cell',
    );
    const headers = screen.getAllByRole('columnheader').map((header) => header.textContent);
    expect(headers.indexOf('发布时间')).toBeGreaterThan(-1);
    expect(headers.indexOf('发布时间')).toBeLessThan(headers.indexOf('更新时间'));
    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[0]).not.toHaveClass('admin-sticky-action-cell');
    expect(row.cells[6]).toHaveTextContent('—');
    expect(row.cells[row.cells.length - 1]).toHaveClass('admin-sticky-action-cell');

    const pagination = screen.getByText('共 1 条').closest('.pagination');
    expect(pagination?.querySelector('.page-summary')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-buttons')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-left')).not.toBeInTheDocument();
    expect(pagination?.querySelector('.brand-pagination-right')).not.toBeInTheDocument();
  });

  it('keeps SKU table headers on one line with a stable wide table contract', async () => {
    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchTileSkusMock).toHaveBeenCalled();
    });

    const table = screen.getByRole('table');
    expect(table).toHaveClass('sku-mgmt-table');
    expect(tileSkuCss).toContain('width: max(100%, 1180px)');
    expect(tileSkuCss).toContain('min-width: 1180px');
    expect(tileSkuCss).toContain('overflow-x: auto');
    expect(tileSkuCss).toContain('white-space: nowrap');
    expect(tileSkuCss).toContain('.sku-mgmt-table th:nth-child(7)');
    expect(tileSkuCss).toContain('.sku-mgmt-table th:nth-child(8)');

    const headers = screen.getAllByRole('columnheader');
    expect(headers).toHaveLength(9);
    expect(headers.map((header) => header.textContent)).toEqual([
      'SKU 信息',
      '品牌 / 类目',
      '规格 / 工艺',
      '参考价格',
      '素材',
      '状态',
      '发布时间',
      '更新时间',
      '操作',
    ]);
  });

  it('formats published time and updated time with the same date formatter', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          status: 'PUBLISHED',
          published_at: '2026-06-19T16:30:00Z',
          updated_at: '2026-06-20T00:45:00Z',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('测试 SKU')).toBeInTheDocument();
    });

    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[6]).toHaveTextContent(formatSkuDateTime('2026-06-19T16:30:00Z'));
    expect(row.cells[7]).toHaveTextContent(formatSkuDateTime('2026-06-20T00:45:00Z'));
  });

  it('uses thumbnail image first and falls back to original image', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          main_image_url: '/media/tiles/1/images/main.jpg',
          main_image_thumbnail_url: '/media/tiles/1/images/main.thumb.jpg',
        },
      ],
    });

    const { container } = render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('测试 SKU')).toBeInTheDocument();
    });

    const image = container.querySelector('.sku-thumb img') as HTMLImageElement;
    expect(image).toHaveAttribute('src', '/media/tiles/1/images/main.thumb.jpg');

    fireEvent.error(image);

    await waitFor(() => {
      expect(container.querySelector('.sku-thumb img')).toHaveAttribute(
        'src',
        '/media/tiles/1/images/main.jpg',
      );
    });
  });

  it('renders category cascade in one dropdown with child panel opening to the right', async () => {
    fetchCategoryTreeMock.mockResolvedValue(categoryTreePayload);

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    const trigger = await screen.findByRole('button', { name: /全部类目/ });
    expect(screen.queryByLabelText('2级类目')).not.toBeInTheDocument();

    fireEvent.click(trigger);

    const menu = screen.getByRole('listbox', { name: '类目选项' });
    expect(within(menu).getAllByLabelText('1级类目')).toHaveLength(1);
    expect(within(menu).queryByLabelText('2级类目')).not.toBeInTheDocument();

    fireEvent.click(within(menu).getByRole('button', { name: '亮光产品' }));

    expect(within(menu).getByLabelText('2级类目')).toBeInTheDocument();
    expect(within(menu).getByRole('button', { name: '大理石瓷砖' })).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: '亮光产品' }).length).toBeGreaterThan(0);
    expect(screen.queryByText(/当前：/)).not.toBeInTheDocument();

    fireEvent.click(within(menu).getByRole('button', { name: '大理石瓷砖' }));

    expect(within(menu).getByLabelText('3级类目')).toBeInTheDocument();
    expect(within(menu).getByRole('button', { name: '柔光灰砖' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /亮光产品 \/ 大理石瓷砖/ })).toBeInTheDocument();
    expect(screen.queryByText(/当前：/)).not.toBeInTheDocument();
  });

  it('sends category id for parent and child cascade selection and clears it', async () => {
    fetchCategoryTreeMock.mockResolvedValue(categoryTreePayload);

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    fireEvent.click(await screen.findByRole('button', { name: /全部类目/ }));
    const menu = screen.getByRole('listbox', { name: '类目选项' });
    fireEvent.click(within(menu).getByRole('button', { name: '亮光产品' }));

    await waitFor(() => {
      expect(fetchTileSkusMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ category_id: 10 }),
      );
    });

    fireEvent.click(within(menu).getByRole('button', { name: '大理石瓷砖' }));

    await waitFor(() => {
      expect(fetchTileSkusMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ category_id: 11 }),
      );
    });

    fireEvent.click(within(menu).getByRole('button', { name: '全部类目' }));

    await waitFor(() => {
      expect(fetchTileSkusMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ category_id: undefined }),
      );
    });
  });

  it('keeps brand category and status dropdowns visually aligned', async () => {
    fetchBrandsMock.mockResolvedValue({ items: [{ id: 1, name: '尼卡瓷砖' }] });
    fetchCategoryTreeMock.mockResolvedValue(categoryTreePayload);

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    const brandTrigger = await screen.findByRole('button', { name: '全部品牌' });
    const categoryTrigger = screen.getByRole('button', { name: '全部类目' });
    const statusTrigger = screen.getByRole('button', { name: '全部状态' });

    [brandTrigger, categoryTrigger, statusTrigger].forEach((trigger) => {
      expect(trigger).toHaveClass('select');
      expect(
        trigger.classList.contains('sku-dropdown-trigger') ||
          trigger.classList.contains('category-cascade-trigger'),
      ).toBe(true);
    });

    fireEvent.click(brandTrigger);
    expect(screen.getByRole('listbox', { name: '品牌选项' })).toHaveClass('sku-dropdown-menu');

    fireEvent.click(categoryTrigger);
    expect(screen.getByRole('listbox', { name: '类目选项' })).toHaveClass('sku-dropdown-menu');

    fireEvent.click(statusTrigger);
    expect(screen.getByRole('listbox', { name: '状态选项' })).toHaveClass('sku-dropdown-menu');
  });

  it('keeps material count visible without showing redundant main image success tag', async () => {
    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('测试 SKU')).toBeInTheDocument();
    });

    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[4]).toHaveTextContent('2 图 / 1 视频');
    expect(row.cells[4]).not.toHaveTextContent('主图已设');
    expect(row.cells[4]).not.toHaveTextContent('缺主图');
  });

  it('keeps only material count visible for missing main image rows without material filter', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          has_main_image: false,
          image_count: 0,
          video_count: 0,
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('测试 SKU')).toBeInTheDocument();
    });

    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[4]).toHaveTextContent('0 图 / 0 视频');
    expect(row.cells[4]).not.toHaveTextContent('主图已设');
    expect(row.cells[4]).not.toHaveTextContent('缺主图');
    expect(screen.queryByText('素材完整度')).not.toBeInTheDocument();

    const [initialRequest] = fetchTileSkusMock.mock.calls[0];
    expect(initialRequest).not.toHaveProperty('material_completeness');
  });

  it('renders SKU rows in backend pagination order without local sorting params', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          id: 12,
          name: '未发布新建 SKU',
          status: 'DRAFT',
          published_at: null,
          updated_at: '2026-07-12T09:00:00Z',
        },
        {
          ...listPayload.items[0],
          id: 10,
          name: '发布时间更新的 SKU',
          status: 'PUBLISHED',
          published_at: '2026-07-03T09:00:00Z',
          updated_at: '2026-07-01T09:00:00Z',
        },
        {
          ...listPayload.items[0],
          id: 11,
          name: '更新时间更新的 SKU',
          status: 'PUBLISHED',
          published_at: '2026-07-01T09:00:00Z',
          updated_at: '2026-07-10T09:00:00Z',
        },
      ],
      total: 3,
      summary: {
        total: 3,
        published_count: 2,
        needs_completion_count: 0,
        draft_count: 1,
      },
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('发布时间更新的 SKU')).toBeInTheDocument();
    });

    const firstFetchParams = fetchTileSkusMock.mock.calls[0]?.[0] as Record<string, unknown>;
    const rows = screen
      .getAllByRole('row')
      .slice(1)
      .map((row) => row.querySelector('td')?.textContent ?? '');
    expect(rows).toEqual(['未发布新建 SKUSKU-001', '发布时间更新的 SKUSKU-001', '更新时间更新的 SKUSKU-001']);
    expect(firstFetchParams.sort).toBeUndefined();
    expect(firstFetchParams.order_by).toBeUndefined();
  });

  it('shows placeholder for invalid published time', async () => {
    fetchTileSkusMock.mockResolvedValue({
      ...listPayload,
      items: [
        {
          ...listPayload.items[0],
          published_at: 'not-a-date',
        },
      ],
    });

    render(
      <MemoryRouter>
        <TileSkuManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('测试 SKU')).toBeInTheDocument();
    });

    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[6]).toHaveTextContent('—');
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
          published_at: '2026-07-29T16:20:00Z',
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
    const row = screen.getByText('测试 SKU').closest('tr') as HTMLTableRowElement;
    expect(row.cells[6]).toHaveTextContent('2026-07-30 00:20');
  });

  it('uses the full filter-card width without an unused grid column', () => {
    expect(tileSkuCss).toContain('grid-template-columns: 1.35fr 1fr 1fr 1fr auto;');
    expect(tileSkuCss).not.toContain('grid-template-columns: 1.35fr repeat(4, 1fr) auto;');
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
    expect(within(dialog).getByText('上架商品')).toBeInTheDocument();
    expect(within(dialog).getByText('确认上架商品「已下架 SKU」？')).toBeInTheDocument();
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
    expect(within(dialog).getByText('下架商品')).toBeInTheDocument();
    expect(
      within(dialog).getByText('确认下架商品「已上架 SKU」？下架后前台将不再展示该商品。'),
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
