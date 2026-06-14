import { Outlet, useNavigate } from 'react-router-dom';

import { Button } from '@/shared/ui/button';

import { useAuth } from '../../features/auth/hooks/useAuth';

export function AdminLayout() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login', { replace: true });
  };

  return (
    <div className="min-h-screen bg-page text-primary">
      <header className="flex items-center justify-between border-b border-border-emphasis px-6 py-4">
        <div>
          <p className="text-sm tracking-[0.16em] text-brand-gold">TilesFST</p>
          <p className="text-xs text-secondary">瓷砖信息管理 · 管理端</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-secondary">{user?.display_name ?? user?.username}</span>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => {
              void handleLogout();
            }}
          >
            退出登录
          </Button>
        </div>
      </header>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
