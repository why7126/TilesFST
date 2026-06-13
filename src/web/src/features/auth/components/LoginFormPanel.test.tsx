import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: false,
    user: null,
  }),
}));

vi.mock('./LoginForm', () => ({
  LoginForm: () => <div data-testid="login-form" />,
}));

import { LoginFormPanel } from './LoginFormPanel';

describe('LoginFormPanel', () => {
  it('does not render notice banner', () => {
    render(
      <main className="login-shell">
        <LoginFormPanel>
          <div>content</div>
        </LoginFormPanel>
      </main>,
    );
    expect(screen.queryByText('功能建设中')).not.toBeInTheDocument();
  });

  it('renders language switcher in form panel', () => {
    render(
      <main className="login-shell">
        <LoginFormPanel>
          <div>content</div>
        </LoginFormPanel>
      </main>,
    );
    expect(screen.getByRole('button', { name: '切换语言' })).toBeInTheDocument();
  });

  it('uses port CSS form-panel class', () => {
    const { container } = render(
      <main className="login-shell">
        <LoginFormPanel>
          <div>content</div>
        </LoginFormPanel>
      </main>,
    );
    expect(container.querySelector('.form-panel')).toBeInTheDocument();
  });
});
