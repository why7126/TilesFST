import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { ProtectedRoute } from './router/ProtectedRoute';
import { useAuthStore } from '../features/auth/store/auth-store';
import { AdminLayout } from '../pages/admin/AdminLayout';
import { DashboardPage } from '../pages/admin/DashboardPage';
import { ForbiddenPage } from '../pages/admin/ForbiddenPage';
import { LoginPage } from '../pages/admin/LoginPage';
import { DesignSystemPage } from '../pages/dev/DesignSystemPage';

function AuthBootstrap({ children }: { children: ReactNode }) {
  const restoreSession = useAuthStore((state) => state.restoreSession);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    void restoreSession().finally(() => setReady(true));
  }, [restoreSession]);

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#18160F] text-[#EDE8DF]">
        加载中...
      </div>
    );
  }

  return <>{children}</>;
}

function HomePage() {
  return (
    <main className="min-h-screen bg-[#18160F] p-6 text-[#EDE8DF]">
      <h1 className="text-2xl font-normal">瓷砖信息管理平台</h1>
      <p className="mt-2 text-sm text-[#EDE8DF]/50">Web 展示端入口</p>
      <a href="/admin/login" className="mt-6 inline-block text-[#C8A055]">
        进入管理端登录
      </a>
    </main>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <AuthBootstrap>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/design-system" element={<DesignSystemPage />} />
          <Route path="/admin/login" element={<LoginPage />} />
          <Route path="/admin/forbidden" element={<ForbiddenPage />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<AdminLayout />}>
              <Route path="/admin/dashboard" element={<DashboardPage />} />
            </Route>
          </Route>
          <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthBootstrap>
    </BrowserRouter>
  );
}
