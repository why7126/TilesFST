import { useLocation, useNavigate } from 'react-router-dom';

import type { UserProfile } from '@/shared/api/generated';
import { ProductVersionBadge } from '@/shared/ui/product-version-badge';

import { adminNavSections, isAdminNavItemActive } from '../data/admin-nav';
import { AdminUserMenu } from './AdminUserMenu';

interface AdminSidebarProps {
  user: UserProfile | null;
  onLogout: () => Promise<void>;
  onPlaceholder: () => void;
  collapsed?: boolean;
  onToggleCollapsed?: () => void;
}

export function AdminSidebar({
  user,
  onLogout,
  onPlaceholder,
  collapsed = false,
  onToggleCollapsed,
}: AdminSidebarProps) {
  const location = useLocation();
  const navigate = useNavigate();

  const sections = adminNavSections.map((section) => {
    if (section.id === 'system' && user?.role !== 'admin') {
      return {
        ...section,
        items: section.items.filter((item) => item.id !== 'users'),
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
        <div className="brand-block">
          <span className="brand-mark" aria-hidden="true">
            TF
          </span>
          <div className="brand-row">
            <span className="logo-text">TILESFST</span>
            <ProductVersionBadge className="shrink-0" />
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

              return (
                <button
                  key={item.id}
                  type="button"
                  className={`nav-item${active ? ' active' : ''}`}
                  aria-label={item.label}
                  onClick={() => handleNavClick(item.path)}
                >
                  <span className="nav-icon" aria-hidden="true" />
                  <span className="nav-label">{item.label}</span>
                </button>
              );
            })}
          </nav>
        ))}
      </div>
      <AdminUserMenu user={user} onLogout={onLogout} onPlaceholder={onPlaceholder} />
    </aside>
  );
}
