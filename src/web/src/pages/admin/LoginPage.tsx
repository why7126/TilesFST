import { Navigate, useNavigate } from 'react-router-dom';

import { AuthBrandPanel } from '../../features/auth/components/AuthBrandPanel';
import { LoginForm } from '../../features/auth/components/LoginForm';
import { LoginFormPanel } from '../../features/auth/components/LoginFormPanel';
import { LoginHeader } from '../../features/auth/components/LoginHeader';
import { LoginSecurityNotice } from '../../features/auth/components/LoginSecurityNotice';
import { LanguageSwitcher } from '../../features/auth/components/LanguageSwitcher';
import '../../features/auth/styles/login-page.css';
import { useAuth } from '../../features/auth/hooks/useAuth';
import { ThemeSwitcher } from '../../features/theme/ThemeSwitcher';

export function LoginPage() {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();

  if (isAuthenticated && user && user.role !== 'store_owner') {
    return <Navigate to="/admin/dashboard" replace />;
  }

  return (
    <main className="login-shell">
      <AuthBrandPanel />
      <LoginFormPanel>
        <div className="login-tools" aria-label="登录页辅助工具">
          <ThemeSwitcher compact />
          <LanguageSwitcher />
        </div>
        <div className="login-card">
          <LoginHeader />
          <LoginForm onSuccess={() => navigate('/admin/dashboard', { replace: true })} />
          <LoginSecurityNotice />
        </div>
      </LoginFormPanel>
    </main>
  );
}
