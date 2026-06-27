import { useCallback, useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';

import { useAuth } from '../../features/auth/hooks/useAuth';
import { AdminSidebar } from '../../features/admin/components/AdminSidebar';
import {
  readAdminSidebarCollapsed,
  writeAdminSidebarCollapsed,
} from '../../features/admin/lib/admin-sidebar-preference';
import '../../features/admin/styles/admin-home.css';

const PLACEHOLDER_MESSAGE = '功能建设中，将在后续迭代开放。';

export function AdminLayout() {
  const { user, logout } = useAuth();
  const [notice, setNotice] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => readAdminSidebarCollapsed());

  const showPlaceholder = useCallback(() => {
    setNotice(PLACEHOLDER_MESSAGE);
  }, []);

  const toggleSidebarCollapsed = useCallback(() => {
    setSidebarCollapsed((previous) => {
      const next = !previous;
      writeAdminSidebarCollapsed(next);
      return next;
    });
  }, []);

  useEffect(() => {
    if (!notice) {
      return;
    }

    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  return (
    <div
      className="admin-shell"
      data-sidebar-state={sidebarCollapsed ? 'collapsed' : 'expanded'}
    >
      <AdminSidebar
        user={user}
        onLogout={logout}
        onPlaceholder={showPlaceholder}
        collapsed={sidebarCollapsed}
        onToggleCollapsed={toggleSidebarCollapsed}
      />
      <main className="main-content" aria-label="首页内容">
        <div className="content-inner">
          {notice ? (
            <p className="admin-notice" role="status" aria-live="polite">
              {notice}
            </p>
          ) : null}
          <Outlet context={{ onPlaceholder: showPlaceholder }} />
        </div>
      </main>
    </div>
  );
}
