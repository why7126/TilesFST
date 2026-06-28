import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/tile-spec-management.css';
import '../styles/brand-management.css';

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

const createTileSpecMock = vi.fn();
const updateTileSpecMock = vi.fn();

vi.mock('../api/tile-specs-api', () => ({
  buildDisplayName: (width: number, length: number) => `${width}×${length}mm`,
  createTileSpec: (...args: unknown[]) => createTileSpecMock(...args),
  updateTileSpec: (...args: unknown[]) => updateTileSpecMock(...args),
}));

import { TileSpecFormModal } from './TileSpecFormModal';

function renderModal(
  props: Partial<React.ComponentProps<typeof TileSpecFormModal>> = {},
) {
  const defaultProps = {
    open: true,
    mode: 'create' as const,
    spec: null,
    onClose: vi.fn(),
    onSuccess: vi.fn(),
  };
  return render(
    <div className="admin-shell">
      <TileSpecFormModal {...defaultProps} {...props} />
    </div>,
  );
}

describe('TileSpecFormModal', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    createTileSpecMock.mockResolvedValue({ id: 2 });
    updateTileSpecMock.mockResolvedValue({ id: 1 });
  });

  it('orders fields as width/length, readonly name, thickness/sort, remark', () => {
    const { container } = renderModal();

    const labels = Array.from(
      container.querySelectorAll('.tile-spec-form-grid label'),
    ).map((node) => node.textContent?.replace(/\s+/g, ' ').trim());

    expect(labels).toEqual([
      '宽度 (mm) *',
      '长度 (mm) *',
      '尺寸名称（只读）',
      '厚度 (mm)',
      '排序 *',
      '备注',
    ]);

    const remarkField = container.querySelector('.brand-form-item.form-full:has(textarea)');
    expect(remarkField).not.toBeNull();
    expect(container.querySelector('.tile-spec-readonly')).toHaveTextContent('600×1200mm');
  });

  it('calls onSuccess after create', async () => {
    const onSuccess = vi.fn();
    renderModal({ onSuccess });

    fireEvent.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(createTileSpecMock).toHaveBeenCalled();
      expect(onSuccess).toHaveBeenCalledWith('规格已创建');
    });
  });
});
