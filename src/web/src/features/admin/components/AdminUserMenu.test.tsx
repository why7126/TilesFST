import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
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

  it('renders avatar image when avatarUrl is provided', () => {
    render(
      <MemoryRouter>
        <AdminUserMenu
          user={user}
          avatarUrl="/media/images/default/user/avatars/demo.webp"
          onLogout={vi.fn()}
          onOpenPasswordChange={vi.fn()}
        />
      </MemoryRouter>,
    );

    const img = document.querySelector('.sidebar-user .avatar img') as HTMLImageElement;
    expect(img).toBeTruthy();
    expect(img).toHaveAttribute('src', '/media/images/default/user/avatars/demo.webp');
  });

  it('falls back to initials when avatar image fails to load', () => {
    render(
      <MemoryRouter>
        <AdminUserMenu
          user={user}
          avatarUrl="/media/broken.webp"
          onLogout={vi.fn()}
          onOpenPasswordChange={vi.fn()}
        />
      </MemoryRouter>,
    );

    const img = document.querySelector('.sidebar-user .avatar img') as HTMLImageElement;
    expect(img).toBeTruthy();
    fireEvent.error(img);
    expect(document.querySelector('.sidebar-user .avatar.is-fallback')).toBeTruthy();
    expect(screen.getByText('AU')).toBeInTheDocument();
  });

  it('renders user initials and email fallback', () => {
    render(
      <MemoryRouter>
        <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={vi.fn()} />
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
        <AdminUserMenu user={user} onLogout={onLogout} onOpenPasswordChange={vi.fn()} />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByText('Admin User'));

    expect(screen.getByRole('menu')).toBeVisible();

    fireEvent.click(screen.getByRole('menuitem', { name: '退出登录' }));

    expect(onLogout).toHaveBeenCalled();
  });

  it('navigates to profile page from user menu', () => {
    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <Routes>
          <Route
            path="/admin/dashboard"
            element={
              <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={vi.fn()} />
            }
          />
          <Route path="/admin/profile" element={<div>Profile Page</div>} />
        </Routes>
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByText('Admin User'));
    fireEvent.click(screen.getByRole('menuitem', { name: '个人资料' }));

    expect(screen.getByText('Profile Page')).toBeInTheDocument();
  });

  it('opens password change handler from user menu', () => {
    const onOpenPasswordChange = vi.fn();

    render(
      <MemoryRouter>
        <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={onOpenPasswordChange} />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByText('Admin User'));
    fireEvent.click(screen.getByRole('menuitem', { name: '密码修改' }));

    expect(onOpenPasswordChange).toHaveBeenCalled();
  });
});
