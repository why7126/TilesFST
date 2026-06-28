import { useCallback, useEffect, useMemo, useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

import { fetchProfileMe } from '../../features/admin/api/profile-api';
import { AdminSidebar } from '../../features/admin/components/AdminSidebar';
import { AdminToast } from '../../features/admin/components/AdminToast';
import { ChangePasswordModal } from '../../features/admin/components/ChangePasswordModal';
import { ChangePasswordModalContext } from '../../features/admin/context/ChangePasswordModalContext';
import {
  readAdminSidebarCollapsed,
  writeAdminSidebarCollapsed,
} from '../../features/admin/lib/admin-sidebar-preference';
import { useAuth } from '../../features/auth/hooks/useAuth';
import '../../features/admin/styles/admin-home.css';
import '../../features/admin/styles/password-change-modal.css';

const PLACEHOLDER_MESSAGE = '功能建设中，将在后续迭代开放。';
const PASSWORD_CHANGE_SUCCESS_MESSAGE = '密码修改成功，请使用新密码重新登录。';

export function AdminLayout() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [notice, setNotice] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [passwordModalOpen, setPasswordModalOpen] = useState(false);
  const [profileEmail, setProfileEmail] = useState<string | null>(null);
  const [profileAvatarUrl, setProfileAvatarUrl] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => readAdminSidebarCollapsed());

  const showPlaceholder = useCallback(() => {
    setNotice(PLACEHOLDER_MESSAGE);
  }, []);

  const openPasswordChange = useCallback(() => {
    setPasswordModalOpen(true);
  }, []);

  const handlePasswordChangeSuccess = useCallback(async () => {
    setToast(PASSWORD_CHANGE_SUCCESS_MESSAGE);
    await logout();
    window.setTimeout(() => {
      navigate('/admin/login', { replace: true });
    }, 800);
  }, [logout, navigate]);

  const changePasswordContextValue = useMemo(
    () => ({ openChangePasswordModal: openPasswordChange }),
    [openPasswordChange],
  );

  const passwordDisplayName =
    user?.display_name?.trim() || user?.username?.trim() || '当前账号';

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

  const loadProfileShell = useCallback(async () => {
    if (!user || (user.role !== 'admin' && user.role !== 'employee')) {
      setProfileEmail(null);
      setProfileAvatarUrl(null);
      return;
    }

    try {
      const profile = await fetchProfileMe();
      setProfileEmail(profile.email ?? null);
      setProfileAvatarUrl(profile.avatar_url ?? null);
    } catch {
      setProfileEmail(null);
      setProfileAvatarUrl(null);
    }
  }, [user]);

  useEffect(() => {
    void loadProfileShell();
  }, [loadProfileShell]);

  return (
    <ChangePasswordModalContext.Provider value={changePasswordContextValue}>
      <div
        className={`admin-shell${passwordModalOpen ? ' is-modal-open' : ''}`}
        data-sidebar-state={sidebarCollapsed ? 'collapsed' : 'expanded'}
      >
        <AdminSidebar
          user={user}
          profileEmail={profileEmail}
          profileAvatarUrl={profileAvatarUrl}
          onLogout={logout}
          onPlaceholder={showPlaceholder}
          onOpenPasswordChange={openPasswordChange}
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
            <Outlet
              context={{
                onPlaceholder: showPlaceholder,
                onOpenPasswordChange: openPasswordChange,
                refetchProfileShell: loadProfileShell,
              }}
            />
          </div>
        </main>
        <ChangePasswordModal
          open={passwordModalOpen}
          displayName={passwordDisplayName}
          onClose={() => setPasswordModalOpen(false)}
          onSuccess={() => void handlePasswordChangeSuccess()}
        />
        <AdminToast message={toast} />
      </div>
    </ChangePasswordModalContext.Provider>
  );
}
