import { fireEvent, render, screen, waitFor } from '@testing-library/react';
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
  function renderLoginPage() {
    return render(
      <MemoryRouter>
        <ThemeProvider>
          <LoginPage />
        </ThemeProvider>
      </MemoryRouter>,
    );
  }

  it('renders TilesFST logo and admin title on login page', () => {
    renderLoginPage();
    expect(screen.getAllByText('TilesFST').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole('heading', { name: '瓷砖信息管理后台' })).toBeInTheDocument();
    expect(screen.getByLabelText('主题')).toBeInTheDocument();
  });

  it('renders theme and language controls in one login tools area', () => {
    const { container } = renderLoginPage();
    const tools = container.querySelector('.login-tools');

    expect(tools).toBeInTheDocument();
    expect(tools).toContainElement(screen.getByLabelText('主题'));
    expect(tools).toContainElement(screen.getByRole('button', { name: '切换语言' }));
    expect(screen.getByRole('button', { name: '切换语言' })).toHaveTextContent('简体中文⌄');
  });

  it('keeps theme switching available on the login page', async () => {
    renderLoginPage();

    fireEvent.change(screen.getByLabelText('主题'), { target: { value: 'light' } });

    await waitFor(() => {
      expect(document.documentElement).toHaveAttribute('data-theme-mode', 'light');
    });
    expect(localStorage.getItem('tilesfst.theme_mode')).toBe('light');
  });

  it('does not render WeCom login entry', () => {
    renderLoginPage();
    expect(screen.queryByRole('button', { name: '企业微信登录' })).not.toBeInTheDocument();
  });
});
