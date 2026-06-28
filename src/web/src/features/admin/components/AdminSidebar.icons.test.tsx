import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { AdminSidebar } from './AdminSidebar';

const adminUser = {
  id: '1',
  username: 'admin',
  display_name: 'Admin',
  role: 'admin',
  status: 'active',
};

const employeeUser = {
  ...adminUser,
  username: 'operator01',
  role: 'employee',
};

function iconMarkup(buttonName: string): string {
  const button = screen.getByRole('button', { name: buttonName });
  return button.querySelector('svg')?.innerHTML ?? '';
}

describe('AdminSidebar icons', () => {
  it('renders distinct lucide icons for collapsed navigation items', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar
          user={adminUser}
          onLogout={vi.fn()}
          onPlaceholder={vi.fn()}
          onOpenPasswordChange={vi.fn()}
          collapsed
          onToggleCollapsed={vi.fn()}
        />
      </MemoryRouter>,
    );

    const homeIcon = iconMarkup('首页');
    const skuIcon = iconMarkup('瓷砖 SKU');
    const brandIcon = iconMarkup('瓷砖品牌');

    expect(homeIcon).not.toBe('');
    expect(skuIcon).not.toBe('');
    expect(homeIcon).not.toBe(skuIcon);
    expect(homeIcon).not.toBe(brandIcon);
  });

  it('keeps distinct icons for employee when 用户管理 is hidden', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={employeeUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} collapsed />
      </MemoryRouter>,
    );

    expect(screen.queryByRole('button', { name: '用户管理' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '系统设置' })).not.toBeInTheDocument();

    const homeIcon = iconMarkup('首页');
    const skuIcon = iconMarkup('瓷砖 SKU');
    expect(homeIcon).not.toBe('');
    expect(skuIcon).not.toBe('');
    expect(homeIcon).not.toBe(skuIcon);
  });
});
