import type { TileSkuAdminItemStatus } from '@/shared/api/generated';

export const TILE_SKU_STATUS_OPTIONS = [
  { label: '全部状态', value: '' },
  { label: '已上架', value: 'PUBLISHED' },
  { label: '草稿', value: 'DRAFT' },
  { label: '待完善', value: 'NEEDS_COMPLETION' },
  { label: '已下架', value: 'DISABLED' },
] as const;

export const MATERIAL_COMPLETENESS_OPTIONS = [
  { label: '全部', value: '' },
  { label: '已完整', value: 'complete' },
  { label: '缺主图', value: 'missing_main_image' },
  { label: '缺图片', value: 'missing_images' },
  { label: '缺视频', value: 'missing_videos' },
] as const;

export function tileSkuStatusLabel(status: TileSkuAdminItemStatus): string {
  switch (status) {
    case 'PUBLISHED':
      return '已上架';
    case 'DRAFT':
      return '草稿';
    case 'NEEDS_COMPLETION':
      return '待完善';
    case 'DISABLED':
      return '已下架';
    default:
      return status;
  }
}

export function tileSkuStatusBadgeClass(status: TileSkuAdminItemStatus): string {
  switch (status) {
    case 'PUBLISHED':
      return 'sku-status on';
    case 'DRAFT':
      return 'sku-status draft';
    case 'NEEDS_COMPLETION':
      return 'sku-status warn';
    default:
      return 'sku-status draft';
  }
}

export function formatSkuDateTime(value: string | null | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value.slice(0, 16).replace('T', ' ');
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
