import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

const login = vi.fn().mockResolvedValue(undefined);
const clearError = vi.fn();

vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    login,
    isLoading: false,
    error: null,
    clearError,
    user: null,
    token: null,
    isAuthenticated: false,
    logout: vi.fn(),
    restoreSession: vi.fn(),
    isAdmin: false,
  }),
}));

import { LoginForm } from '../components/LoginForm';

describe('LoginForm', () => {
  it('shows validation errors when fields are empty', async () => {
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginForm onSuccess={() => undefined} />
        </div>
      </main>,
    );
    fireEvent.click(screen.getByRole('button', { name: '登录' }));
    expect(await screen.findByText('请输入账号')).toBeInTheDocument();
    expect(screen.getByText('请输入密码')).toBeInTheDocument();
  });

  it('calls login when form is valid', async () => {
    login.mockClear();
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginForm onSuccess={() => undefined} />
        </div>
      </main>,
    );
    fireEvent.change(screen.getByPlaceholderText('请输入手机号 / 邮箱 / 员工账号'), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByPlaceholderText('请输入登录密码'), { target: { value: 'secret' } });
    fireEvent.click(screen.getByRole('button', { name: '登录' }));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith('admin', 'secret', false);
    });
  });

  it('uses port CSS classes on native inputs', () => {
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginForm onSuccess={() => undefined} />
        </div>
      </main>,
    );
    expect(document.querySelector('.field-input')).toBeInTheDocument();
    expect(document.querySelector('.primary')).toBeInTheDocument();
  });

  it('does not render third-party login options', () => {
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginForm onSuccess={() => undefined} />
        </div>
      </main>,
    );
    expect(screen.queryByRole('button', { name: '企业微信登录' })).not.toBeInTheDocument();
    expect(screen.queryByText('或使用企业身份登录')).not.toBeInTheDocument();
  });

  it('does not render forgot password entry', () => {
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginForm onSuccess={() => undefined} />
        </div>
      </main>,
    );
    expect(screen.queryByText('忘记密码？')).not.toBeInTheDocument();
  });
});
