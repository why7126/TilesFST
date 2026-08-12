import { useEffect, useId, useRef, useState } from 'react';
import { KeyRound, LogOut, SunMoon, UserRound } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';

import { useTheme } from '@/features/theme/ThemeContext';
import type { UserProfile } from '@/shared/api/generated';

import { getUserDisplayName, getUserInitials } from '../lib/user-display';

interface AdminUserMenuProps {
  user: UserProfile | null;
  avatarUrl?: string | null;
  onLogout: () => Promise<void>;
  onOpenPasswordChange: () => void;
}

export function AdminUserMenu({
  user,
  avatarUrl,
  onLogout,
  onOpenPasswordChange,
}: AdminUserMenuProps) {
  const menuId = useId();
  const containerRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [avatarImageFailed, setAvatarImageFailed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { mode, setMode } = useTheme();

  const displayName = getUserDisplayName(user?.display_name, user?.username);
  const initials = getUserInitials(user?.display_name, user?.username);
  const isProfileActive = location.pathname.startsWith('/admin/profile');
  const showAvatarImage = Boolean(avatarUrl) && !avatarImageFailed;
  const nextThemeMode = mode === 'dark_flagship' ? 'system' : 'dark_flagship';
  const themeActionLabel =
    nextThemeMode === 'system' ? '切换到跟随系统' : '切换到暗色旗舰';

  useEffect(() => {
    setAvatarImageFailed(false);
  }, [avatarUrl]);

  useEffect(() => {
    if (!open) {
      return;
    }

    const handlePointerDown = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener('mousedown', handlePointerDown);
    return () => document.removeEventListener('mousedown', handlePointerDown);
  }, [open]);

  const handleLogout = () => {
    setOpen(false);
    void onLogout().then(() => {
      navigate('/admin/login', { replace: true });
    });
  };

  return (
    <div className="sidebar-user" ref={containerRef}>
      <div
        className="user-dropdown"
        role="menu"
        aria-label="用户菜单下拉框"
        id={menuId}
        hidden={!open}
      >
        <button
          type="button"
          className={`dropdown-item${isProfileActive ? ' active' : ''}`}
          role="menuitem"
          onClick={() => {
            setOpen(false);
            navigate('/admin/profile');
          }}
        >
          <UserRound className="dropdown-icon" size={15} strokeWidth={1.7} aria-hidden />
          <span className="dropdown-label">个人资料</span>
        </button>
        <button
          type="button"
          className="dropdown-item"
          role="menuitem"
          onClick={() => {
            setOpen(false);
            onOpenPasswordChange();
          }}
        >
          <KeyRound className="dropdown-icon" size={15} strokeWidth={1.7} aria-hidden />
          <span className="dropdown-label">密码修改</span>
        </button>
        <button
          type="button"
          className="dropdown-item theme-toggle"
          role="menuitem"
          aria-label={themeActionLabel}
          title={themeActionLabel}
          onClick={() => {
            void setMode(nextThemeMode);
          }}
        >
          <SunMoon className="dropdown-icon" size={15} strokeWidth={1.7} aria-hidden />
          <span className="dropdown-label">界面主题</span>
          <span className="theme-switch-track" aria-hidden>
            <span className="theme-switch-thumb" />
          </span>
        </button>
        <div className="dropdown-divider" role="separator" />
        <button type="button" className="dropdown-item logout" role="menuitem" onClick={handleLogout}>
          <LogOut className="dropdown-icon" size={15} strokeWidth={1.7} aria-hidden />
          <span className="dropdown-label">退出登录</span>
        </button>
      </div>
      <button
        type="button"
        className="user-trigger"
        aria-expanded={open}
        aria-haspopup="menu"
        aria-controls={menuId}
        onClick={() => setOpen((value) => !value)}
      >
        <span className={`avatar${showAvatarImage ? '' : ' is-fallback'}`}>
          {avatarUrl ? (
            <img
              src={avatarUrl}
              alt=""
              onError={() => {
                setAvatarImageFailed(true);
              }}
            />
          ) : null}
          <span className="avatar-fallback">{initials}</span>
        </span>
        <span>
          <span className="user-name">{displayName}</span>
        </span>
        <span className="chevron" aria-hidden>
          ⌃
        </span>
      </button>
    </div>
  );
}
