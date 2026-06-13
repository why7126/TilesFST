import { Outlet, useNavigate } from 'react-router-dom';

import { useAuth } from '../../features/auth/hooks/useAuth';

export function AdminLayout() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login', { replace: true });
  };

  return (
    <div className="min-h-screen bg-[#18160F] text-[#EDE8DF]">
      <header className="flex items-center justify-between border-b border-white/10 px-6 py-4">
        <div>
          <p className="text-sm tracking-[0.16em] text-[#C8A055]">STONEX</p>
          <p className="text-xs text-[#EDE8DF]/50">瓷砖信息管理 · 管理端</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-[#EDE8DF]/70">{user?.display_name ?? user?.username}</span>
          <button
            type="button"
            onClick={() => {
              void handleLogout();
            }}
            className="rounded-[2px] border border-white/15 px-4 py-2 transition hover:border-[#C8A055]/50"
          >
            退出登录
          </button>
        </div>
      </header>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
