import { useLocation, useNavigate } from 'react-router-dom';

import type { UserProfile } from '@/shared/api/generated';

import { adminNavSections, isAdminNavItemActive } from '../data/admin-nav';
import { AdminUserMenu } from './AdminUserMenu';

interface AdminSidebarProps {
  user: UserProfile | null;
  onLogout: () => Promise<void>;
  onPlaceholder: () => void;
}

export function AdminSidebar({ user, onLogout, onPlaceholder }: AdminSidebarProps) {
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
      <div className="logo">TILESFST</div>
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
                  onClick={() => handleNavClick(item.path)}
                >
                  <span className="nav-icon" aria-hidden />
                  {item.label}
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
