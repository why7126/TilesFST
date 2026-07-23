import { ReactNode } from 'react';

interface LoginFormPanelProps {
  children: ReactNode;
}

export function LoginFormPanel({ children }: LoginFormPanelProps) {
  return (
    <section className="form-panel" aria-label="登录表单区">
      {children}
    </section>
  );
}
