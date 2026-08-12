import { fireEvent, render, screen } from '@testing-library/react';
import type { ReactNode } from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ThemeProvider } from '@/features/theme/ThemeContext';
import { THEME_STORAGE_KEY } from '@/features/theme/theme';

import { AdminUserMenu } from './AdminUserMenu';

describe('AdminUserMenu', () => {
  const user = {
    id: '1',
    username: 'admin',
    display_name: 'Admin User',
    role: 'admin',
    status: 'active',
  };

  beforeEach(() => {
    localStorage.clear();
    document.documentElement.removeAttribute('data-theme-mode');
    document.documentElement.removeAttribute('data-theme');
  });

  function renderUserMenu(ui: ReactNode) {
    return render(
      <ThemeProvider>
        <MemoryRouter>{ui}</MemoryRouter>
      </ThemeProvider>,
    );
  }

  it('renders avatar image when avatarUrl is provided', () => {
    renderUserMenu(
      <AdminUserMenu
        user={user}
        avatarUrl="/media/images/default/user/avatars/demo.webp"
        onLogout={vi.fn()}
        onOpenPasswordChange={vi.fn()}
      />,
    );

    const img = document.querySelector('.sidebar-user .avatar img') as HTMLImageElement;
    expect(img).toBeTruthy();
    expect(img).toHaveAttribute('src', '/media/images/default/user/avatars/demo.webp');
  });

  it('falls back to initials when avatar image fails to load', () => {
    renderUserMenu(
      <AdminUserMenu
        user={user}
        avatarUrl="/media/broken.webp"
        onLogout={vi.fn()}
        onOpenPasswordChange={vi.fn()}
      />,
    );

    const img = document.querySelector('.sidebar-user .avatar img') as HTMLImageElement;
    expect(img).toBeTruthy();
    fireEvent.error(img);
    expect(document.querySelector('.sidebar-user .avatar.is-fallback')).toBeTruthy();
    expect(screen.getByText('AU')).toBeInTheDocument();
  });

  it('renders only nickname when display name is present', () => {
    renderUserMenu(
      <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );

    expect(screen.getByText('AU')).toBeInTheDocument();
    expect(screen.getByText('Admin User')).toBeInTheDocument();
    expect(screen.queryByText('admin@tilesfst.com')).not.toBeInTheDocument();
    expect(document.querySelector('.sidebar-user .user-email')).toBeNull();
  });

  it('falls back to username when display name is empty', () => {
    renderUserMenu(
      <AdminUserMenu
        user={{ ...user, display_name: '   ' }}
        onLogout={vi.fn()}
        onOpenPasswordChange={vi.fn()}
      />,
    );

    expect(screen.getByText('AD')).toBeInTheDocument();
    expect(screen.getByText('admin')).toBeInTheDocument();
    expect(screen.queryByText('admin@tilesfst.com')).not.toBeInTheDocument();
  });

  it('does not render real email or generated email as a subtitle', () => {
    renderUserMenu(
      <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );

    expect(screen.queryByText('owner@example.com')).not.toBeInTheDocument();
    expect(screen.queryByText(/@tilesfst\.com/)).not.toBeInTheDocument();
    expect(document.querySelector('.sidebar-user .user-trigger .user-name')).toBeTruthy();
    expect(document.querySelector('.sidebar-user .user-trigger .user-email')).toBeNull();
  });

  it('opens dropdown and calls logout', async () => {
    const onLogout = vi.fn().mockResolvedValue(undefined);

    renderUserMenu(
      <AdminUserMenu user={user} onLogout={onLogout} onOpenPasswordChange={vi.fn()} />,
    );

    fireEvent.click(screen.getByText('Admin User'));

    expect(screen.getByRole('menu')).toBeVisible();
    expect(screen.getByRole('menuitem', { name: '个人资料' }).querySelector('svg')).toBeTruthy();
    expect(screen.getByRole('menuitem', { name: '密码修改' }).querySelector('svg')).toBeTruthy();
    expect(screen.getByRole('menuitem', { name: '切换到暗色旗舰' }).querySelector('svg')).toBeTruthy();
    expect(screen.getByRole('menuitem', { name: '退出登录' }).querySelector('svg')).toBeTruthy();

    fireEvent.click(screen.getByRole('menuitem', { name: '退出登录' }));

    expect(onLogout).toHaveBeenCalled();
  });

  it('navigates to profile page from user menu', () => {
    render(
      <ThemeProvider>
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
        </MemoryRouter>
      </ThemeProvider>,
    );

    fireEvent.click(screen.getByText('Admin User'));
    fireEvent.click(screen.getByRole('menuitem', { name: '个人资料' }));

    expect(screen.getByText('Profile Page')).toBeInTheDocument();
  });

  it('opens password change handler from user menu', () => {
    const onOpenPasswordChange = vi.fn();

    renderUserMenu(
      <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={onOpenPasswordChange} />,
    );

    fireEvent.click(screen.getByText('Admin User'));
    fireEvent.click(screen.getByRole('menuitem', { name: '密码修改' }));

    expect(onOpenPasswordChange).toHaveBeenCalled();
  });

  it('switches theme through the icon-only user menu button', async () => {
    renderUserMenu(
      <AdminUserMenu user={user} onLogout={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );

    fireEvent.click(screen.getByText('Admin User'));
    fireEvent.click(screen.getByRole('menuitem', { name: '切换到暗色旗舰' }));

    expect(document.documentElement.dataset.themeMode).toBe('dark_flagship');
    expect(document.documentElement.dataset.theme).toBe('dark');
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe('dark_flagship');
    expect(screen.getByText('界面主题')).toBeInTheDocument();
    expect(document.querySelector('.theme-switch-track')).toBeTruthy();
    expect(screen.queryByText('暗色旗舰')).not.toBeInTheDocument();
  });
});
