import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import { render, screen } from '@testing-library/react';
import type { ReactElement } from 'react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { PRODUCT_VERSION } from '@shared/product-version';
import { ThemeProvider } from '@/features/theme/ThemeContext';

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

function renderWithTheme(ui: ReactElement) {
  return render(
    <ThemeProvider>
      <MemoryRouter initialEntries={['/admin/dashboard']}>{ui}</MemoryRouter>
    </ThemeProvider>,
  );
}

describe('AdminSidebar', () => {
  it('shows 用户管理 for admin', () => {
    renderWithTheme(
      <AdminSidebar user={adminUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );
    expect(screen.getByRole('button', { name: '用户管理' })).toBeInTheDocument();
  });

  it('hides 用户管理 for employee', () => {
    renderWithTheme(
      <AdminSidebar user={employeeUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );
    expect(screen.queryByRole('button', { name: '用户管理' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '系统设置' })).not.toBeInTheDocument();
  });

  it('shows product logo, brand copy, and version badge in brand head', () => {
    renderWithTheme(
      <AdminSidebar user={adminUser} onLogout={vi.fn()} onPlaceholder={vi.fn()} onOpenPasswordChange={vi.fn()} />,
    );
    expect(screen.getByText('菲尚特FST')).toBeInTheDocument();
    expect(screen.getByText('家居建材资料库')).toBeInTheDocument();
    expect(screen.getByAltText('菲尚特家居建材 Logo')).toHaveAttribute(
      'src',
      '/logos/64x64.png',
    );
    const pill = screen.getByLabelText(`产品版本 ${PRODUCT_VERSION}`);
    expect(pill).toHaveTextContent(PRODUCT_VERSION);
    expect(pill).toHaveClass('version-pill');
    expect(pill.className).toMatch(/text-muted/);
  });

  it('declares FST logo favicon and apple touch icon in web entry html', () => {
    const html = readFileSync(resolve(process.cwd(), 'index.html'), 'utf8');

    expect(html).toContain(
      '<link rel="icon" type="image/png" sizes="64x64" href="/logos/64x64.png" />',
    );
    expect(html).toContain(
      '<link rel="icon" type="image/png" sizes="128x128" href="/logos/128x128.png" />',
    );
    expect(html).toContain(
      '<link rel="apple-touch-icon" sizes="256x256" href="/logos/256x256.png" />',
    );
    expect(html).not.toContain('/vite.svg');
    expect(html).not.toContain('/react.svg');
  });
});
