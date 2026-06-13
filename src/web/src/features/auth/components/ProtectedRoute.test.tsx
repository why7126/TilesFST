import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { ProtectedRoute } from '../../../app/router/ProtectedRoute';

vi.mock('../../../features/auth/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

describe('ProtectedRoute', () => {
  it('redirects unauthenticated users to login', async () => {
    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: false,
      isLoading: false,
      user: null,
      token: null,
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
          <Route path="/admin/login" element={<div>Login Page</div>} />
          <Route element={<ProtectedRoute />}>
            <Route path="/admin/dashboard" element={<div>Dashboard</div>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('renders protected content for authenticated admin users', async () => {
    const { useAuth } = await import('../../../features/auth/hooks/useAuth');
    vi.mocked(useAuth).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: {
        id: '1',
        username: 'admin',
        display_name: 'Admin',
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
          <Route element={<ProtectedRoute />}>
            <Route path="/admin/dashboard" element={<div>Dashboard</div>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });
});
