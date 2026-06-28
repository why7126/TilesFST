import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

const fetchTileSpecsMock = vi.fn();
const disableTileSpecMock = vi.fn();

vi.mock('@/features/admin/api/tile-specs-api', () => ({
  canDeleteTileSpec: (spec: { sku_count: number; status: string }) =>
    spec.sku_count === 0 && spec.status === 'DISABLED',
  deleteTileSpec: vi.fn(),
  disableTileSpec: (...args: unknown[]) => disableTileSpecMock(...args),
  enableTileSpec: vi.fn(),
  fetchTileSpecs: (...args: unknown[]) => fetchTileSpecsMock(...args),
}));

vi.mock('@/features/admin/components/TileSpecFormModal', () => ({
  TileSpecFormModal: ({
    onSuccess,
  }: {
    onSuccess: (message: string) => void;
  }) => (
    <button type="button" onClick={() => onSuccess('规格已创建')}>
      trigger-save-success
    </button>
  ),
}));

import { TileSpecManagementPage } from './TileSpecManagementPage';

const listPayload = {
  items: [
    {
      id: 1,
      display_name: '600×1200mm',
      width_mm: 600,
      length_mm: 1200,
      thickness_mm: null,
      sku_count: 0,
      sort_order: 10,
      status: 'ENABLED',
      remark: null,
      updated_at: '2026-06-28T00:00:00Z',
    },
  ],
  total: 1,
  page: 1,
  page_size: 20,
  summary: {
    total: 1,
    enabled_count: 1,
    disabled_count: 0,
    unlinked_sku_count: 1,
  },
};

describe('TileSpecManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchTileSpecsMock.mockResolvedValue(listPayload);
  });

  it('uses standard pagination DOM aligned with user management page', async () => {
    const { container } = render(
      <div className="admin-shell">
        <TileSpecManagementPage />
      </div>,
    );

    await waitFor(() => {
      expect(fetchTileSpecsMock).toHaveBeenCalled();
    });

    expect(container.querySelector('.pagination')).toBeInTheDocument();
    expect(container.querySelector('.page-summary')).toHaveTextContent('共 1 条');
    expect(container.querySelector('.page-buttons')).toBeInTheDocument();
    expect(container.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(screen.getByLabelText('每页显示条数')).toBeInTheDocument();
    expect(screen.getByText('每页显示')).toBeInTheDocument();
    expect(container.querySelector('.pagination-bar')).toBeNull();
    expect(container.querySelector('.page-indicator')).toBeNull();
  });

  it('reloads list after form save success', async () => {
    render(
      <div className="admin-shell">
        <TileSpecManagementPage />
      </div>,
    );

    await waitFor(() => {
      expect(fetchTileSpecsMock).toHaveBeenCalledTimes(1);
    });

    fireEvent.click(screen.getByRole('button', { name: 'trigger-save-success' }));

    await waitFor(() => {
      expect(fetchTileSpecsMock).toHaveBeenCalledTimes(2);
    });
  });

  it('opens disable confirm dialog before calling disableTileSpec', async () => {
    disableTileSpecMock.mockResolvedValue(undefined);
    fetchTileSpecsMock
      .mockResolvedValueOnce(listPayload)
      .mockResolvedValueOnce({
        ...listPayload,
        items: [{ ...listPayload.items[0], status: 'DISABLED' }],
        summary: { ...listPayload.summary, enabled_count: 0, disabled_count: 1 },
      });

    render(
      <div className="admin-shell">
        <TileSpecManagementPage />
      </div>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '停用' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '停用' }));

    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByText('停用规格')).toBeInTheDocument();
    expect(
      within(dialog).getByText(
        '确认停用规格「600×1200mm」？停用后前台将不再展示该规格。',
      ),
    ).toBeInTheDocument();
    expect(disableTileSpecMock).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认停用' }));

    await waitFor(() => {
      expect(disableTileSpecMock).toHaveBeenCalledWith(1);
    });
  });
});
