import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { ThirdPartyLoginSection } from './ThirdPartyLoginSection';

describe('ThirdPartyLoginSection', () => {
  it('renders WeCom login entry with divider text', () => {
    render(
      <main className="login-shell">
        <ThirdPartyLoginSection />
      </main>,
    );
    expect(screen.getByRole('button', { name: '企业微信登录' })).toBeInTheDocument();
    expect(screen.getByText('或使用企业身份登录')).toBeInTheDocument();
  });
});
