import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

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
        <LoginPage />
      </MemoryRouter>,
    );
    expect(screen.getAllByText('TilesFST').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole('heading', { name: '瓷砖信息管理后台' })).toBeInTheDocument();
  });

  it('does not render WeCom login entry', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    );
    expect(screen.queryByRole('button', { name: '企业微信登录' })).not.toBeInTheDocument();
  });
});
