import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { AdminFilterSelect } from './admin-filter-select';

const options = [
  { value: '', label: '全部状态' },
  { value: 'ENABLED', label: '启用' },
  { value: 'DISABLED', label: '停用', disabled: true },
] as const;

describe('AdminFilterSelect', () => {
  it('renders the shared admin filter dropdown and selects options', () => {
    const onChange = vi.fn();

    render(
      <AdminFilterSelect
        id="brand-filter-status"
        value=""
        options={options}
        listLabel="品牌状态选项"
        onChange={onChange}
      />,
    );

    const trigger = screen.getByRole('button', { name: '全部状态' });
    expect(trigger).toHaveClass('admin-filter-dropdown-trigger');
    expect(trigger).toHaveAttribute('aria-haspopup', 'listbox');

    fireEvent.click(trigger);

    expect(screen.getByRole('listbox', { name: '品牌状态选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );
    expect(screen.getByRole('option', { name: '全部状态' })).toHaveClass(
      'admin-filter-dropdown-option',
      'is-selected',
    );
    expect(screen.getByRole('option', { name: '停用' })).toBeDisabled();

    fireEvent.click(screen.getByRole('option', { name: '启用' }));
    expect(onChange).toHaveBeenCalledWith('ENABLED');
  });

  it('does not open while disabled', () => {
    render(
      <AdminFilterSelect
        value=""
        options={options}
        listLabel="品牌状态选项"
        onChange={vi.fn()}
        disabled
      />,
    );

    const trigger = screen.getByRole('button', { name: '全部状态' });
    expect(trigger).toBeDisabled();

    fireEvent.click(trigger);
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
  });

  it('closes the shared overlay on escape and outside pointer down', () => {
    render(
      <div>
        <button type="button">外部按钮</button>
        <AdminFilterSelect
          id="category-filter-status"
          value="ENABLED"
          options={options}
          listLabel="类目状态选项"
          onChange={vi.fn()}
        />
      </div>,
    );

    const trigger = screen.getByRole('button', { name: '启用' });
    fireEvent.click(trigger);
    expect(screen.getByRole('listbox', { name: '类目状态选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );

    fireEvent.keyDown(trigger, { key: 'Escape' });
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument();

    fireEvent.click(trigger);
    expect(screen.getByRole('listbox', { name: '类目状态选项' })).toBeInTheDocument();

    fireEvent.mouseDown(screen.getByRole('button', { name: '外部按钮' }));
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
  });
});
