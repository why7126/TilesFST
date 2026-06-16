export const ROLE_OPTIONS = [
  { value: '', label: '全部角色' },
  { value: 'store_owner', label: '前台用户' },
  { value: 'employee', label: '后台运营' },
  { value: 'admin', label: '后台管理员' },
] as const;

export const STATUS_OPTIONS = [
  { value: '', label: '全部状态' },
  { value: 'active', label: '正常' },
  { value: 'disabled', label: '已冻结' },
  { value: 'deleted', label: '已删除' },
] as const;

export const LOGIN_FILTER_OPTIONS = [
  { value: '', label: '全部' },
  { value: 'never_logged', label: '从未登录' },
  { value: 'recent_7_days', label: '最近 7 天登录' },
  { value: 'inactive_30_days', label: '超过 30 天未登录' },
] as const;

export const ROLE_FORM_OPTIONS = ROLE_OPTIONS.filter((o) => o.value !== '');

export function roleLabel(role: string): string {
  return ROLE_OPTIONS.find((o) => o.value === role)?.label ?? role;
}

export function statusLabel(status: string): string {
  return STATUS_OPTIONS.find((o) => o.value === status)?.label ?? status;
}

export function roleBadgeClass(role: string): string {
  if (role === 'admin') return 'badge admin';
  if (role === 'employee') return 'badge ops';
  return 'badge front';
}

export function statusBadgeClass(status: string): string {
  if (status === 'active') return 'badge ok';
  if (status === 'disabled') return 'badge frozen';
  return 'badge deleted';
}
