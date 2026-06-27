import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ADMIN_SIDEBAR_COLLAPSED_KEY } from '../lib/admin-sidebar-preference';
import { AdminLayout } from '../../../pages/admin/AdminLayout';
import { DashboardPage } from '../../../pages/admin/DashboardPage';

vi.mock('../../../features/auth/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

describe('AdminLayout', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders TILESFST sidebar shell without header logout', async () => {
    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: {
        id: '1',
        username: 'admin',
        display_name: 'Admin User',
        role: 'admin',
        status: 'active',
      },
      token: 'token',
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      restoreSession: vi.fn(),
      clearError: vi.fn(),
      isAdmin: true,
    });

    render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <Routes>
          <Route element={<AdminLayout />}>
            <Route path="/admin/dashboard" element={<DashboardPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('TILESFST')).toBeInTheDocument();
    expect(screen.getByLabelText('后台导航')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '退出登录' })).not.toBeInTheDocument();
    expect(screen.getByText('数据概览')).toBeInTheDocument();
  });

  it('persists sidebar collapse state on admin shell', async () => {
    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: {
        id: '1',
        username: 'admin',
        display_name: 'Admin User',
        role: 'admin',
        status: 'active',
      },
      token: 'token',
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      restoreSession: vi.fn(),
      clearError: vi.fn(),
      isAdmin: true,
    });

    const { container } = render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <Routes>
          <Route element={<AdminLayout />}>
            <Route path="/admin/dashboard" element={<DashboardPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    const shell = container.querySelector('.admin-shell');
    expect(shell).toHaveAttribute('data-sidebar-state', 'expanded');

    fireEvent.click(screen.getByRole('button', { name: '收起侧边栏' }));
    expect(shell).toHaveAttribute('data-sidebar-state', 'collapsed');
    expect(localStorage.getItem(ADMIN_SIDEBAR_COLLAPSED_KEY)).toBe('true');

    fireEvent.click(screen.getByRole('button', { name: '展开侧边栏' }));
    expect(shell).toHaveAttribute('data-sidebar-state', 'expanded');
    expect(localStorage.getItem(ADMIN_SIDEBAR_COLLAPSED_KEY)).toBe('false');
  });

  it('restores collapsed state from localStorage on mount', async () => {
    localStorage.setItem(ADMIN_SIDEBAR_COLLAPSED_KEY, 'true');

    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: {
        id: '1',
        username: 'admin',
        display_name: 'Admin User',
        role: 'admin',
        status: 'active',
      },
      token: 'token',
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      restoreSession: vi.fn(),
      clearError: vi.fn(),
      isAdmin: true,
    });

    const { container } = render(
      <MemoryRouter initialEntries={['/admin/dashboard']}>
        <Routes>
          <Route element={<AdminLayout />}>
            <Route path="/admin/dashboard" element={<DashboardPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(container.querySelector('.admin-shell')).toHaveAttribute(
      'data-sidebar-state',
      'collapsed',
    );
    expect(screen.getByRole('button', { name: '展开侧边栏' })).toBeInTheDocument();
  });
});
