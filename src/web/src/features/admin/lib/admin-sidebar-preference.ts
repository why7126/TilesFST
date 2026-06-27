export const ADMIN_SIDEBAR_COLLAPSED_KEY = 'admin-sidebar-collapsed';

export function readAdminSidebarCollapsed(): boolean {
  try {
    return localStorage.getItem(ADMIN_SIDEBAR_COLLAPSED_KEY) === 'true';
  } catch {
    return false;
  }
}

export function writeAdminSidebarCollapsed(collapsed: boolean): void {
  try {
    localStorage.setItem(ADMIN_SIDEBAR_COLLAPSED_KEY, collapsed ? 'true' : 'false');
  } catch {
    // localStorage unavailable — silent degrade
  }
}
