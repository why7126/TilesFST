import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { PRODUCT_VERSION } from '@shared/product-version';

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

describe('AdminSidebar', () => {
  it('shows 用户管理 for admin', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={adminUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />
      </MemoryRouter>,
    );
    expect(screen.getByRole('button', { name: '用户管理' })).toBeInTheDocument();
  });

  it('hides 用户管理 for employee', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={employeeUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />
      </MemoryRouter>,
    );
    expect(screen.queryByRole('button', { name: '用户管理' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '系统设置' })).not.toBeInTheDocument();
  });

  it('shows product version badge in brand head', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={adminUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />
      </MemoryRouter>,
    );
    expect(screen.getByText('TILESFST')).toBeInTheDocument();
    const pill = screen.getByLabelText(`产品版本 ${PRODUCT_VERSION}`);
    expect(pill).toHaveTextContent(PRODUCT_VERSION);
    expect(pill).toHaveClass('version-pill');
    expect(pill.className).toMatch(/text-muted/);
  });
});
