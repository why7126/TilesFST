import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { ThemeProvider } from '@/features/theme/ThemeContext';

vi.mock('../../hooks/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: false,
    user: null,
    login: vi.fn(),
    isLoading: false,
    error: null,
    clearError: vi.fn(),
  }),
}));

import { LoginPage } from '../../../pages/admin/LoginPage';

describe('LoginPage', () => {
  it('renders TilesFST logo and admin title on login page', () => {
    render(
      <MemoryRouter>
        <ThemeProvider>
          <LoginPage />
        </ThemeProvider>
      </MemoryRouter>,
    );
    expect(screen.getAllByText('TilesFST').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole('heading', { name: '瓷砖信息管理后台' })).toBeInTheDocument();
    expect(screen.getByLabelText('主题')).toBeInTheDocument();
  });

  it('does not render WeCom login entry', () => {
    render(
      <MemoryRouter>
        <ThemeProvider>
          <LoginPage />
        </ThemeProvider>
      </MemoryRouter>,
    );
    expect(screen.queryByRole('button', { name: '企业微信登录' })).not.toBeInTheDocument();
  });
});
