import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { SearchableSelect } from './searchable-select';

const options = [
  { value: 'admin', label: '管理员', description: 'admin@example.com' },
  { value: 'editor', label: '编辑员', description: 'editor@example.com' },
];

describe('SearchableSelect', () => {
  it('uses the shared admin filter dropdown classes across states', () => {
    const onChange = vi.fn();
    render(
      <SearchableSelect
        aria-label="操作人"
        value="admin"
        options={options}
        onChange={onChange}
        onSearch={vi.fn()}
        clearable
      />,
    );

    const combobox = screen.getByRole('combobox', { name: '操作人' });
    expect(combobox).toHaveClass('admin-filter-dropdown-trigger');
    expect(combobox).toHaveValue('管理员');

    fireEvent.focus(combobox);

    expect(screen.getByRole('listbox')).toHaveClass('admin-filter-dropdown-menu');
    const selectedOption = screen.getByRole('option', { name: /管理员/ });
    expect(selectedOption).toHaveClass('admin-filter-dropdown-option');
    expect(selectedOption).toHaveClass('is-selected');

    fireEvent.click(screen.getByRole('button', { name: '清空选择' }));
    expect(onChange).toHaveBeenCalledWith(null);
  });

  it('keeps loading empty and disabled presentations on the unified classes', () => {
    const { rerender } = render(
      <SearchableSelect
        aria-label="品牌"
        value={null}
        options={[]}
        onChange={vi.fn()}
        onSearch={vi.fn()}
        loading
      />,
    );

    const loadingInput = screen.getByRole('combobox', { name: '品牌' });
    fireEvent.focus(loadingInput);
    expect(screen.getByText('加载中...')).toHaveClass('admin-filter-dropdown-empty');

    rerender(
      <SearchableSelect
        aria-label="品牌"
        value={null}
        options={[]}
        onChange={vi.fn()}
        onSearch={vi.fn()}
      />,
    );
    fireEvent.focus(screen.getByRole('combobox', { name: '品牌' }));
    expect(screen.getByText('无匹配结果')).toHaveClass('admin-filter-dropdown-empty');

    rerender(
      <SearchableSelect
        aria-label="品牌"
        value={null}
        options={options}
        onChange={vi.fn()}
        onSearch={vi.fn()}
        disabled
      />,
    );
    const disabledInput = screen.getByRole('combobox', { name: '品牌' });
    expect(disabledInput).toBeDisabled();
    fireEvent.focus(disabledInput);
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
  });

  it('keeps query reset selected and error states on the shared dropdown contract', () => {
    const onSearch = vi.fn();
    const onChange = vi.fn();
    const { rerender } = render(
      <div>
        <button type="button">外部按钮</button>
        <SearchableSelect
          aria-label="操作人"
          value="editor"
          options={options}
          onChange={onChange}
          onSearch={onSearch}
        />
      </div>,
    );

    const combobox = screen.getByRole('combobox', { name: '操作人' });
    expect(combobox).toHaveValue('编辑员');

    fireEvent.focus(combobox);
    fireEvent.change(combobox, { target: { value: 'adm' } });
    expect(combobox).toHaveValue('adm');

    fireEvent.mouseDown(screen.getByRole('button', { name: '外部按钮' }));
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
    expect(combobox).toHaveValue('编辑员');

    fireEvent.focus(combobox);
    fireEvent.click(screen.getByRole('option', { name: /管理员/ }));
    expect(onChange).toHaveBeenCalledWith('admin');

    rerender(
      <SearchableSelect
        aria-label="操作人"
        value={null}
        options={[]}
        onChange={onChange}
        onSearch={onSearch}
        error="加载失败"
      />,
    );

    fireEvent.focus(screen.getByRole('combobox', { name: '操作人' }));
    expect(screen.getByText('加载失败')).toHaveClass('admin-filter-dropdown-empty');
  });
});
