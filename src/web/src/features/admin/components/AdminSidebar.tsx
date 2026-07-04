import { useLocation, useNavigate } from 'react-router-dom';

import type { UserProfile } from '@/shared/api/generated';
import { ProductVersionBadge } from '@/shared/ui/product-version-badge';

import { adminNavSections, isAdminNavItemActive } from '../data/admin-nav';
import { AdminUserMenu } from './AdminUserMenu';

interface AdminSidebarProps {
  user: UserProfile | null;
  profileEmail?: string | null;
  profileAvatarUrl?: string | null;
  onLogout: () => Promise<void>;
  onPlaceholder: () => void;
  onOpenPasswordChange: () => void;
  collapsed?: boolean;
  onToggleCollapsed?: () => void;
}

export function AdminSidebar({
  user,
  profileEmail,
  profileAvatarUrl,
  onLogout,
  onPlaceholder,
  onOpenPasswordChange,
  collapsed = false,
  onToggleCollapsed,
}: AdminSidebarProps) {
  const location = useLocation();
  const navigate = useNavigate();

  const sections = adminNavSections.map((section) => {
    if (section.id === 'system' && user?.role !== 'admin') {
      return {
        ...section,
        items: section.items.filter(
          (item) =>
            item.id !== 'users' &&
            item.id !== 'settings' &&
            item.id !== 'logs' &&
            item.id !== 'api-docs',
        ),
      };
    }
    return section;
  });

  const handleNavClick = (path?: string) => {
    if (path) {
      navigate(path);
      return;
    }

    onPlaceholder();
  };

  return (
    <aside className="sidebar" aria-label="后台导航">
      <div className="sidebar-head">
        <div className="brand-block" aria-label="菲尚特FST 家居建材资料库">
          <img
            className="sidebar-brand-logo"
            src="/logos/64x64.png"
            alt="菲尚特家居建材 Logo"
          />
          <div className="brand-copy">
            <div className="brand-row">
              <span className="logo-text">菲尚特FST</span>
              <ProductVersionBadge className="shrink-0" />
            </div>
            <span className="brand-subtitle">家居建材资料库</span>
          </div>
        </div>
        <button
          type="button"
          className="sidebar-toggle"
          aria-expanded={!collapsed}
          aria-label={collapsed ? '展开侧边栏' : '收起侧边栏'}
          onClick={() => onToggleCollapsed?.()}
        >
          {collapsed ? '›' : '‹'}
        </button>
      </div>
      <div className="nav-scroll">
        {sections.map((section) => (
          <nav key={section.id} className="nav-section" aria-label={section.ariaLabel}>
            <p className="nav-title">{section.title}</p>
            {section.items.map((item) => {
              const active = isAdminNavItemActive(location.pathname, item);
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  type="button"
                  className={`nav-item${active ? ' active' : ''}`}
                  aria-label={item.label}
                  onClick={() => handleNavClick(item.path)}
                >
                  <Icon className="nav-icon" size={16} strokeWidth={1.5} aria-hidden />
                  <span className="nav-label">{item.label}</span>
                </button>
              );
            })}
          </nav>
        ))}
      </div>
      <AdminUserMenu
        user={user}
        profileEmail={profileEmail}
        avatarUrl={profileAvatarUrl}
        onLogout={onLogout}
        onOpenPasswordChange={onOpenPasswordChange}
      />
    </aside>
  );
}
