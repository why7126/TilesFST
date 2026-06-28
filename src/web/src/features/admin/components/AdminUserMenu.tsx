import { useEffect, useId, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import type { UserProfile } from '@/shared/api/generated';

import { getUserDisplayName, getUserEmail, getUserInitials } from '../lib/user-display';

interface AdminUserMenuProps {
  user: UserProfile | null;
  profileEmail?: string | null;
  avatarUrl?: string | null;
  onLogout: () => Promise<void>;
  onOpenPasswordChange: () => void;
}

export function AdminUserMenu({
  user,
  profileEmail,
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

  const displayName = getUserDisplayName(user?.display_name, user?.username);
  const email = getUserEmail(user?.username, profileEmail);
  const initials = getUserInitials(user?.display_name, user?.username);
  const isProfileActive = location.pathname.startsWith('/admin/profile');
  const showAvatarImage = Boolean(avatarUrl) && !avatarImageFailed;

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
          <span className="dropdown-icon" aria-hidden />
          个人资料
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
          <span className="dropdown-icon" aria-hidden />
          密码修改
        </button>
        <div className="dropdown-divider" role="separator" />
        <button type="button" className="dropdown-item logout" role="menuitem" onClick={handleLogout}>
          <span className="dropdown-icon" aria-hidden />
          退出登录
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
          <span className="user-email">{email}</span>
        </span>
        <span className="chevron" aria-hidden>
          ⌃
        </span>
      </button>
    </div>
  );
}
