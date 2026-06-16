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

describe('AdminSidebar', () => {
  it('shows 用户管理 for admin', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={adminUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} />
      </MemoryRouter>,
    );
    expect(screen.getByRole('button', { name: '用户管理' })).toBeInTheDocument();
  });

  it('hides 用户管理 for employee', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <AdminSidebar user={employeeUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} />
      </MemoryRouter>,
    );
    expect(screen.queryByRole('button', { name: '用户管理' })).not.toBeInTheDocument();
  });
});
