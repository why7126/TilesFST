import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { AdminUserMenu } from './AdminUserMenu';

describe('AdminUserMenu', () => {
  const user = {
    id: '1',
    username: 'admin',
    display_name: 'Admin User',
    role: 'admin',
    status: 'active',
  };

  it('renders user initials and email fallback', () => {
    render(
      <MemoryRouter>
        <AdminUserMenu user={user} onLogout={vi.fn()} onPlaceholder={vi.fn()} />
      </MemoryRouter>,
    );

    expect(screen.getByText('AU')).toBeInTheDocument();
    expect(screen.getByText('Admin User')).toBeInTheDocument();
    expect(screen.getByText('admin@tilesfst.com')).toBeInTheDocument();
  });

  it('opens dropdown and calls logout', async () => {
    const onLogout = vi.fn().mockResolvedValue(undefined);

    render(
      <MemoryRouter>
        <AdminUserMenu user={user} onLogout={onLogout} onPlaceholder={vi.fn()} />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByText('Admin User'));

    expect(screen.getByRole('menu')).toBeVisible();

    fireEvent.click(screen.getByRole('menuitem', { name: '退出登录' }));

    expect(onLogout).toHaveBeenCalled();
  });

  it('does not render standalone logout below trigger', () => {
    render(
      <MemoryRouter>
        <AdminUserMenu user={user} onLogout={vi.fn()} onPlaceholder={vi.fn()} />
      </MemoryRouter>,
    );

    const triggers = screen.getAllByRole('button');
    expect(triggers).toHaveLength(1);
  });
});
