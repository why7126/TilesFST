import type { BrandCertificateItem } from '@/shared/api/generated';

export const CERTIFICATE_TYPE_OPTIONS = [
  { label: '全部类型', value: '' },
  { label: '质量体系', value: 'QUALITY' },
  { label: '检测报告', value: 'INSPECTION' },
  { label: '绿色建材', value: 'GREEN_BUILDING' },
  { label: '荣誉资质', value: 'HONOR' },
  { label: '其他证书', value: 'OTHER' },
] as const;

export const CERTIFICATE_VALIDITY_OPTIONS = [
  { label: '全部有效状态', value: '' },
  { label: '长期有效', value: 'PERMANENT' },
  { label: '有效', value: 'VALID' },
  { label: '即将到期', value: 'EXPIRING_SOON' },
  { label: '已过期', value: 'EXPIRED' },
  { label: '未设置', value: 'UNSET' },
] as const;

export const CERTIFICATE_DISPLAY_OPTIONS = [
  { label: '全部展示状态', value: '' },
  { label: '前台展示', value: 'VISIBLE' },
  { label: '前台隐藏', value: 'HIDDEN' },
] as const;

const typeLabels: Record<string, string> = {
  QUALITY: '质量体系',
  INSPECTION: '检测报告',
  GREEN_BUILDING: '绿色建材',
  HONOR: '荣誉资质',
  OTHER: '其他证书',
};

const validityLabels: Record<string, string> = {
  PERMANENT: '长期有效',
  VALID: '有效',
  EXPIRING_SOON: '即将到期',
  EXPIRED: '已过期',
  UNSET: '未设置',
};

export function certificateTypeLabel(type: string): string {
  return typeLabels[type] ?? type;
}

export function validityStatusLabel(status: string): string {
  return validityLabels[status] ?? status;
}

export function validityBadgeClass(status: string): string {
  if (status === 'EXPIRED') return 'badge danger';
  if (status === 'EXPIRING_SOON') return 'badge warning';
  if (status === 'UNSET') return 'badge disabled';
  return 'badge enabled';
}

export function displayStatusLabel(item: Pick<BrandCertificateItem, 'is_visible'>): string {
  return item.is_visible ? '展示' : '隐藏';
}

export function formatCertificateDateTime(value: string): string {
  return value.replace('T', ' ').slice(0, 16);
}

export function formatValidityRange(item: BrandCertificateItem): string {
  if (item.is_permanent) return '长期有效';
  if (!item.effective_date && !item.expiry_date) return '未设置';
  if (!item.effective_date) return `至 ${item.expiry_date ?? '-'}`;
  return `${item.effective_date} 至 ${item.expiry_date ?? '-'}`;
}

export function isPdfCertificate(item: Pick<BrandCertificateItem, 'file_mime_type' | 'file_name'>) {
  return item.file_mime_type === 'application/pdf' || item.file_name.toLowerCase().endsWith('.pdf');
}
