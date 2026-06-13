import { ReactNode } from 'react';

import { LanguageSwitcher } from './LanguageSwitcher';

interface LoginFormPanelProps {
  children: ReactNode;
}

export function LoginFormPanel({ children }: LoginFormPanelProps) {
  return (
    <section className="form-panel" aria-label="登录表单区">
      <LanguageSwitcher />
      {children}
    </section>
  );
}
