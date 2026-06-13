import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { LoginHeader } from './LoginHeader';

describe('LoginHeader', () => {
  it('renders admin portal eyebrow and title', () => {
    render(
      <main className="login-shell">
        <div className="login-card">
          <LoginHeader />
        </div>
      </main>,
    );
    expect(screen.getByText('ADMIN PORTAL')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: '登录管理端' })).toBeInTheDocument();
  });
});
