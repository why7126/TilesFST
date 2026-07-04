import type { LucideIcon } from 'lucide-react';
import {
  Building2,
  BookOpen,
  FolderTree,
  Image,
  LayoutDashboard,
  ListTree,
  Package,
  Ruler,
  Settings,
  Users,
} from 'lucide-react';

export interface AdminNavItem {
  id: string;
  label: string;
  path?: string;
  icon: LucideIcon;
}

export interface AdminNavSection {
  id: string;
  title: string;
  ariaLabel: string;
  items: AdminNavItem[];
}

export const adminNavSections: AdminNavSection[] = [
  {
    id: 'operations',
    title: 'OPERATIONS',
    ariaLabel: 'Operations',
    items: [
      { id: 'home', label: '首页', path: '/admin/dashboard', icon: LayoutDashboard },
      { id: 'sku', label: '瓷砖 SKU', path: '/admin/tile-skus', icon: Package },
      { id: 'brand', label: '瓷砖品牌', path: '/admin/brands', icon: Building2 },
      { id: 'category', label: '瓷砖类目', path: '/admin/tile-categories', icon: FolderTree },
      { id: 'tile-spec', label: '瓷砖规格', path: '/admin/tile-specs', icon: Ruler },
      { id: 'banner', label: 'Banner 管理', path: '/admin/banners', icon: Image },
    ],
  },
  {
    id: 'system',
    title: 'SYSTEM',
    ariaLabel: 'System',
    items: [
      { id: 'users', label: '用户管理', path: '/admin/users', icon: Users },
      { id: 'settings', label: '系统设置', path: '/admin/settings', icon: Settings },
      { id: 'logs', label: '日志审计', path: '/admin/logs', icon: ListTree },
      { id: 'api-docs', label: '接口文档', path: '/admin/api-docs', icon: BookOpen },
    ],
  },
];

export function isAdminNavItemActive(pathname: string, item: AdminNavItem): boolean {
  if (!item.path) {
    return false;
  }

  if (item.id === 'settings') {
    return pathname === item.path || pathname.startsWith(`${item.path}/`);
  }

  return pathname === item.path;
}
