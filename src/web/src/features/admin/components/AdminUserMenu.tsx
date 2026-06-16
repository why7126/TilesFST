import { useEffect, useId, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import type { UserProfile } from '@/shared/api/generated';

import { getUserDisplayName, getUserEmail, getUserInitials } from '../lib/user-display';

interface AdminUserMenuProps {
  user: UserProfile | null;
  onLogout: () => Promise<void>;
  onPlaceholder: () => void;
}

export function AdminUserMenu({ user, onLogout, onPlaceholder }: AdminUserMenuProps) {
  const menuId = useId();
  const containerRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const displayName = getUserDisplayName(user?.display_name, user?.username);
  const email = getUserEmail(user?.username);
  const initials = getUserInitials(user?.display_name, user?.username);

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
          className="dropdown-item"
          role="menuitem"
          onClick={() => {
            setOpen(false);
            onPlaceholder();
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
            onPlaceholder();
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
        <span className="avatar">{initials}</span>
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
