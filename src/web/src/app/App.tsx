import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { ProtectedRoute } from './router/ProtectedRoute';
import { useAuthStore } from '../features/auth/store/auth-store';
import { ThemeProvider } from '../features/theme/ThemeContext';
import { AdminLayout } from '../pages/admin/AdminLayout';
import { ApiDocsPage } from '../pages/admin/ApiDocsPage';
import { BannerManagementPage } from '../pages/admin/BannerManagementPage';
import { BrandManagementPage } from '../pages/admin/BrandManagementPage';
import { DashboardPage } from '../pages/admin/DashboardPage';
import { LogAuditPage } from '../pages/admin/LogAuditPage';
import { ProfilePage } from '../pages/admin/ProfilePage';
import { TileCategoryManagementPage } from '../pages/admin/TileCategoryManagementPage';
import { TileSkuManagementPage } from '../pages/admin/TileSkuManagementPage';
import { TileSpecManagementPage } from '../pages/admin/TileSpecManagementPage';
import { SystemSettingsPage } from '../pages/admin/SystemSettingsPage';
import { UserManagementPage } from '../pages/admin/UserManagementPage';
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
      <div className="flex min-h-screen items-center justify-center bg-page text-primary">
        加载中...
      </div>
    );
  }

  return <>{children}</>;
}

function HomePage() {
  return (
    <main className="min-h-screen bg-page p-6 text-primary">
      <h1 className="text-2xl font-normal">TilesFST</h1>
      <p className="mt-2 text-sm text-secondary">Web 展示端入口</p>
      <a href="/admin/login" className="mt-6 inline-block text-brand-gold">
        进入管理端登录
      </a>
    </main>
  );
}

export function App() {
  return (
    <ThemeProvider>
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
                <Route path="/admin/brands" element={<BrandManagementPage />} />
                <Route path="/admin/banners" element={<BannerManagementPage />} />
                <Route path="/admin/tile-categories" element={<TileCategoryManagementPage />} />
                <Route path="/admin/tile-specs" element={<TileSpecManagementPage />} />
                <Route path="/admin/tile-skus" element={<TileSkuManagementPage />} />
                <Route path="/admin/profile" element={<ProfilePage />} />
                <Route element={<ProtectedRoute requireAdmin />}>
                  <Route path="/admin/users" element={<UserManagementPage />} />
                  <Route path="/admin/logs" element={<LogAuditPage />} />
                  <Route path="/admin/api-docs" element={<ApiDocsPage />} />
                  <Route path="/admin/settings" element={<Navigate to="/admin/settings/basic" replace />} />
                  <Route path="/admin/settings/:tab" element={<SystemSettingsPage />} />
                </Route>
              </Route>
            </Route>
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthBootstrap>
      </BrowserRouter>
    </ThemeProvider>
  );
}
