import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

describe('Design System components', () => {
  it('renders Button default variant', () => {
    render(<Button>登录</Button>);
    const button = screen.getByRole('button', { name: '登录' });
    expect(button).toBeInTheDocument();
    expect(button.className).toContain('bg-brand-gold');
    expect(button.className).toContain('text-page');
  });

  it('renders Input with placeholder', () => {
    render(<Input placeholder="请输入账号" />);
    expect(screen.getByPlaceholderText('请输入账号')).toBeInTheDocument();
  });
});
