import type { SystemSettingsGroupResponseData } from '@/shared/api/generated';

export interface MediaUploadSettings {
  maxImageSizeMb: number;
  maxVideoSizeMb: number;
  maxFileSizeMb: number;
  allowedImageTypes: string;
  allowedVideoTypes: string;
}

export const DEFAULT_MEDIA_UPLOAD_SETTINGS: MediaUploadSettings = {
  maxImageSizeMb: 20,
  maxVideoSizeMb: 500,
  maxFileSizeMb: 25,
  allowedImageTypes: 'image/jpeg,image/jpg,image/png,image/webp',
  allowedVideoTypes: 'video/mp4',
};

const MIME_LABELS: Record<string, string> = {
  'image/jpeg': 'JPG',
  'image/jpg': 'JPG',
  'image/png': 'PNG',
  'image/webp': 'WebP',
  'image/gif': 'GIF',
  'image/svg+xml': 'SVG',
  'image/bmp': 'BMP',
  'image/tiff': 'TIFF',
  'image/heic': 'HEIC',
  'video/mp4': 'MP4',
  'video/quicktime': 'MOV',
  'video/x-msvideo': 'AVI',
  'video/webm': 'WebM',
  'video/x-matroska': 'MKV',
  'video/mpeg': 'MPEG',
  'video/3gpp': '3GP',
};

export function normalizeMimeList(value: unknown): string[] {
  return String(value ?? '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

export function buildAcceptValue(value: unknown): string {
  return normalizeMimeList(value).join(',');
}

export function formatMimeLabels(value: unknown): string {
  const labels = normalizeMimeList(value).map((mime) => MIME_LABELS[mime] ?? mime);
  return Array.from(new Set(labels)).join('、');
}

function numberFromSettings(value: unknown, fallback: number): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

export function mediaUploadSettingsFromResponse(
  data: SystemSettingsGroupResponseData,
): MediaUploadSettings {
  return {
    maxImageSizeMb: numberFromSettings(
      data.max_image_size_mb,
      DEFAULT_MEDIA_UPLOAD_SETTINGS.maxImageSizeMb,
    ),
    maxVideoSizeMb: numberFromSettings(
      data.max_video_size_mb,
      DEFAULT_MEDIA_UPLOAD_SETTINGS.maxVideoSizeMb,
    ),
    maxFileSizeMb: numberFromSettings(
      data.max_file_size_mb,
      DEFAULT_MEDIA_UPLOAD_SETTINGS.maxFileSizeMb,
    ),
    allowedImageTypes:
      String(data.allowed_image_types ?? '').trim() ||
      DEFAULT_MEDIA_UPLOAD_SETTINGS.allowedImageTypes,
    allowedVideoTypes:
      String(data.allowed_video_types ?? '').trim() ||
      DEFAULT_MEDIA_UPLOAD_SETTINGS.allowedVideoTypes,
  };
}
