import { fireEvent, render, screen } from '@testing-library/react';
import type { ReactElement } from 'react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import {
  ADMIN_SIDEBAR_COLLAPSED_KEY,
  readAdminSidebarCollapsed,
  writeAdminSidebarCollapsed,
} from '../lib/admin-sidebar-preference';
import { ThemeProvider } from '@/features/theme/ThemeContext';
import { AdminSidebar } from './AdminSidebar';

const adminUser = {
  id: '1',
  username: 'admin',
  display_name: 'Admin',
  role: 'admin',
  status: 'active',
};

function renderWithTheme(ui: ReactElement) {
  return render(
    <ThemeProvider>
      <MemoryRouter initialEntries={['/admin/dashboard']}>{ui}</MemoryRouter>
    </ThemeProvider>,
  );
}

describe('admin-sidebar-preference', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('defaults to expanded when storage is empty', () => {
    expect(readAdminSidebarCollapsed()).toBe(false);
  });

  it('persists collapsed preference', () => {
    writeAdminSidebarCollapsed(true);
    expect(localStorage.getItem(ADMIN_SIDEBAR_COLLAPSED_KEY)).toBe('true');
    expect(readAdminSidebarCollapsed()).toBe(true);
  });
});

describe('AdminSidebar collapse', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('toggles chevron, aria-expanded, and localStorage via layout handler', () => {
    const onToggleCollapsed = vi.fn();

    renderWithTheme(
      <AdminSidebar
        user={adminUser}
        onLogout={vi.fn()}
        onPlaceholder={vi.fn()}
        onOpenPasswordChange={vi.fn()}
        collapsed={false}
        onToggleCollapsed={onToggleCollapsed}
      />,
    );

    const toggle = screen.getByRole('button', { name: '收起侧边栏' });
    expect(toggle).toHaveAttribute('aria-expanded', 'true');
    expect(toggle).toHaveTextContent('‹');

    fireEvent.click(toggle);
    expect(onToggleCollapsed).toHaveBeenCalledTimes(1);
  });

  it('shows expand chevron and aria state when collapsed', () => {
    renderWithTheme(
      <AdminSidebar
        user={adminUser}
        onLogout={vi.fn()}
        onPlaceholder={vi.fn()}
        onOpenPasswordChange={vi.fn()}
        collapsed
        onToggleCollapsed={vi.fn()}
      />,
    );

    const toggle = screen.getByRole('button', { name: '展开侧边栏' });
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect(toggle).toHaveTextContent('›');
    expect(screen.getByAltText('菲尚特家居建材 Logo')).toHaveAttribute(
      'src',
      '/logos/64x64.png',
    );
    expect(screen.getByLabelText('主题')).toBeInTheDocument();
  });

  it('keeps active nav item class when collapsed', () => {
    renderWithTheme(
      <AdminSidebar
        user={adminUser}
        onLogout={vi.fn()}
        onPlaceholder={vi.fn()}
        onOpenPasswordChange={vi.fn()}
        collapsed
        onToggleCollapsed={vi.fn()}
      />,
    );

    expect(screen.getByRole('button', { name: '首页' })).toHaveClass('active');
  });

  it('uses native button semantics for keyboard activation', () => {
    renderWithTheme(
      <AdminSidebar
        user={adminUser}
        onLogout={vi.fn()}
        onPlaceholder={vi.fn()}
        onOpenPasswordChange={vi.fn()}
        collapsed={false}
        onToggleCollapsed={vi.fn()}
      />,
    );

    const toggle = screen.getByRole('button', { name: '收起侧边栏' });
    expect(toggle.tagName).toBe('BUTTON');
    expect(toggle).toHaveAttribute('type', 'button');
  });
});
