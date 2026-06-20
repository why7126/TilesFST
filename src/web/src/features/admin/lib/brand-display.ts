export function getBrandInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length >= 2) {
    return `${parts[0]![0] ?? ''}${parts[1]![0] ?? ''}`.toUpperCase();
  }
  return name.trim().slice(0, 2).toUpperCase();
}

export function formatBrandDateTime(value: string): string {
  return value.replace('T', ' ').slice(0, 16);
}

export const BRAND_STATUS_OPTIONS = [
  { label: '全部状态', value: '' },
  { label: '启用', value: 'ENABLED' },
  { label: '停用', value: 'DISABLED' },
] as const;

export function brandStatusLabel(status: string): string {
  return status === 'ENABLED' ? '启用' : '停用';
}

export function brandStatusBadgeClass(status: string): string {
  return status === 'ENABLED' ? 'badge enabled' : 'badge disabled';
}
