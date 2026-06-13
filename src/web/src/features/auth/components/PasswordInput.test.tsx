import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { PasswordInput } from './PasswordInput';

describe('PasswordInput', () => {
  it('toggles password visibility', () => {
    render(<PasswordInput value="secret" onChange={vi.fn()} />);
    const input = screen.getByPlaceholderText('请输入密码');
    expect(input).toHaveAttribute('type', 'password');

    fireEvent.click(screen.getByRole('button', { name: '显示密码' }));
    expect(input).toHaveAttribute('type', 'text');

    fireEvent.click(screen.getByRole('button', { name: '隐藏密码' }));
    expect(input).toHaveAttribute('type', 'password');
  });

  it('shows error message', () => {
    render(<PasswordInput value="" onChange={vi.fn()} error="请输入密码" />);
    expect(screen.getByRole('alert')).toHaveTextContent('请输入密码');
  });
});
