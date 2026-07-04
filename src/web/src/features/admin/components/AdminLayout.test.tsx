import { readFileSync } from 'node:fs';
import path from 'node:path';

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ADMIN_SIDEBAR_COLLAPSED_KEY } from '../lib/admin-sidebar-preference';
import { trackUsageEvent } from '../../../features/tracking/api/usage-tracking';
import { AdminLayout } from '../../../pages/admin/AdminLayout';
import { DashboardPage } from '../../../pages/admin/DashboardPage';

const adminStylesDir = path.resolve(process.cwd(), 'src/features/admin/styles');
const readAdminCss = (filename: string) =>
  readFileSync(path.join(adminStylesDir, filename), 'utf8');

vi.mock('../../../features/auth/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

vi.mock('../../../features/admin/api/profile-api', () => ({
  fetchProfileMe: vi.fn().mockResolvedValue({ email: 'admin@tilesfst.com' }),
}));

vi.mock('../../../features/tracking/api/usage-tracking', () => ({
  trackUsageEvent: vi.fn().mockResolvedValue(undefined),
}));

describe('AdminLayout', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.mocked(trackUsageEvent).mockClear();
  });

  it('renders FST brand sidebar shell without header logout', async () => {
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

    expect(screen.getByText('菲尚特FST')).toBeInTheDocument();
    expect(screen.getByText('家居建材资料库')).toBeInTheDocument();
    expect(container.querySelector('.main-content')).toBeInTheDocument();
    expect(container.querySelector('.content-inner')).toBeInTheDocument();
    expect(screen.getByAltText('菲尚特家居建材 Logo')).toHaveAttribute(
      'src',
      '/logos/64x64.png',
    );
    expect(screen.getByLabelText('后台导航')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '退出登录' })).not.toBeInTheDocument();
    expect(screen.getByText('数据概览')).toBeInTheDocument();
  });

  it('tracks page views for admin pages from the shared layout', async () => {
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
      <MemoryRouter initialEntries={['/admin/dashboard?from=nav']}>
        <Routes>
          <Route element={<AdminLayout />}>
            <Route path="/admin/dashboard" element={<DashboardPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(trackUsageEvent).toHaveBeenCalledWith('page_view', {
        module: 'dashboard',
        entity_type: 'admin_page',
        entity_id: 'admin_dashboard',
        page_title: '数据概览',
        route_pattern: '/admin/dashboard',
        page_path: '/admin/dashboard?from=nav',
      }, {
        pagePath: '/admin/dashboard?from=nav',
      });
    });
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

  it('keeps admin content padding and width strategy free of legacy max-width overrides', () => {
    const adminHomeCss = readAdminCss('admin-home.css');
    const tileSkuCss = readAdminCss('tile-sku-management.css');
    const systemSettingsCss = readAdminCss('system-settings.css');

    expect(adminHomeCss).toContain('padding: 24px 24px 48px;');
    expect(adminHomeCss).toContain('padding: 20px 16px 40px;');
    expect(adminHomeCss).toContain('padding: 16px 12px 32px;');
    expect(adminHomeCss).toContain('max-width: min(1440px, 100%);');
    expect(adminHomeCss).not.toContain('padding: 48px 56px 72px;');
    expect(adminHomeCss).not.toMatch(/\.content-inner\s*\{[^}]*max-width:\s*1080px/s);
    expect(tileSkuCss).not.toMatch(/content-inner\s*\{[^}]*max-width:\s*1120px/s);
    expect(systemSettingsCss).not.toMatch(
      /settings-content-inner\s*\{[^}]*max-width:\s*1080px/s,
    );
  });

  it('shows log audit and api docs below system settings for admin users', async () => {
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

    const buttons = screen.getAllByRole('button').map((button) => button.getAttribute('aria-label'));
    expect(buttons.indexOf('日志审计')).toBe(buttons.indexOf('系统设置') + 1);
    expect(buttons.indexOf('接口文档')).toBe(buttons.indexOf('日志审计') + 1);
  });

  it('hides admin-only system entries for employee users', async () => {
    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: {
        id: '2',
        username: 'employee',
        display_name: 'Employee User',
        role: 'employee',
        status: 'active',
      },
      token: 'token',
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      restoreSession: vi.fn(),
      clearError: vi.fn(),
      isAdmin: false,
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

    expect(screen.queryByRole('button', { name: '用户管理' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '系统设置' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '日志审计' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '接口文档' })).not.toBeInTheDocument();
  });
});
