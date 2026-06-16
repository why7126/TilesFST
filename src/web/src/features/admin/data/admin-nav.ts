export interface AdminNavItem {
  id: string;
  label: string;
  path?: string;
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
      { id: 'home', label: '首页', path: '/admin/dashboard' },
      { id: 'sku', label: '瓷砖 SKU' },
      { id: 'brand', label: '瓷砖品牌' },
      { id: 'category', label: '瓷砖类目' },
      { id: 'banner', label: 'Banner 管理' },
    ],
  },
  {
    id: 'system',
    title: 'SYSTEM',
    ariaLabel: 'System',
    items: [
      { id: 'users', label: '用户管理', path: '/admin/users' },
      { id: 'settings', label: '系统设置' },
    ],
  },
];

export function isAdminNavItemActive(pathname: string, item: AdminNavItem): boolean {
  if (!item.path) {
    return false;
  }

  return pathname === item.path;
}
