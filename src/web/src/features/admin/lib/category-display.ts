export const CATEGORY_STATUS_OPTIONS = [
  { label: '全部状态', value: '' },
  { label: '启用', value: 'ENABLED' },
  { label: '停用', value: 'DISABLED' },
] as const;

export const CATEGORY_LEVEL_OPTIONS = [
  { label: '全部层级', value: '' },
  { label: '一级类目', value: '1' },
  { label: '二级类目', value: '2' },
  { label: '三级类目', value: '3' },
] as const;

export function categoryLevelLabel(level: number): string {
  if (level === 1) return '一级';
  if (level === 2) return '二级';
  return '三级';
}

export function categoryStatusLabel(status: string): string {
  return status === 'ENABLED' ? '启用' : '停用';
}

export function categoryStatusBadgeClass(status: string): string {
  return status === 'ENABLED' ? 'cat-badge ok' : 'cat-badge off';
}

export function formatCategoryDateTime(value: string): string {
  return value.replace('T', ' ').slice(0, 16);
}

export function formatSkuCount(value: number): string {
  return value.toLocaleString('zh-CN');
}
