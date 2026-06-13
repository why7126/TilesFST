import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { LanguageSwitcher } from './LanguageSwitcher';

describe('LanguageSwitcher', () => {
  it('renders label with dropdown marker', () => {
    render(
      <main className="login-shell">
        <LanguageSwitcher />
      </main>,
    );
    expect(screen.getByRole('button', { name: '切换语言' })).toHaveTextContent('简体中文');
  });
});
