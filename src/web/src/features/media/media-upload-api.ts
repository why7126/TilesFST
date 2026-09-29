import { trackUsageEvent } from '@/features/tracking/api/usage-tracking';
import { api } from '@/features/auth/api/auth-api';
import type { UploadResult, UploadSessionCreate } from '@/shared/api/generated';
import { MediaUploadTask, type UploadControlTransport, type UploadSnapshot, type UploadObservation } from './media-upload-controller';

const observe = (value: UploadObservation) => trackUsageEvent('media_upload', {
  action:value.action, stage:value.stage, mode:value.mode, media_kind:value.media_kind,
  media_type:value.media_kind === 'sku_video' ? 'video' : value.media_kind === 'certificate' ? 'attachment' : 'image',
  business_type:value.media_kind, file_size:value.file_size_bytes, result:value.stage === 'failed' ? 'failed' : 'success',
  file_size_bytes:value.file_size_bytes, source:'browser', duration_scope:'client_stage_wall_time',
}, {durationMs:value.duration_ms, taskTraceId:value.task_trace_id, taskType:'media_direct_upload', pagePath:window.location.pathname});

const transport: UploadControlTransport = {
  retryProcessing: async (id, signal) => (await api.retryUploadProcessingApiV1AdminUploadsSessionsSessionIdRetryProcessingPost(id, { signal, timeout: 10000 })).data.data!,
  create: async (input, signal) => (await api.createUploadSessionApiV1AdminUploadsSessionsPost(input, { signal, timeout: 10000 })).data.data!,
  query: async (id, signal) => (await api.queryUploadSessionApiV1AdminUploadsSessionsSessionIdGet(id, { signal, timeout: 10000 })).data.data!,
  renew: async (id, signal) => (await api.renewUploadSessionApiV1AdminUploadsSessionsSessionIdRenewPost(id, { signal, timeout: 10000 })).data.data!,
  authorizePart: async (id, part, signal) => (await api.authorizeUploadPartApiV1AdminUploadsSessionsSessionIdPartsPartNumberAuthorizePost(id, part, { signal, timeout: 10000 })).data.data!,
  confirm: async (id, signal) => (await api.confirmUploadSessionApiV1AdminUploadsSessionsSessionIdConfirmPost(id, { signal, timeout: 30000 })).data.data!,
  cancel: async id => (await api.cancelUploadSessionApiV1AdminUploadsSessionsSessionIdCancelPost(id, { timeout: 10000 })).data.data!,
};

export function createVideoUploadTask(file: File, tileId: number | undefined, onUpdate: (value: UploadSnapshot) => void,
  proxy: (signal: AbortSignal, onProgress: (progress: number) => void) => Promise<UploadResult>) {
  return new MediaUploadTask(file, tileId, transport, onUpdate, proxy, undefined, undefined, 'sku_video', observe);
}


export function createImageUploadTask(file: File, tileId: number | undefined, onUpdate: (value: UploadSnapshot) => void,
  proxy: (signal: AbortSignal, onProgress: (progress: number) => void) => Promise<UploadResult>,
  mediaKind: UploadSessionCreate['media_kind'] = 'sku_image') {
  return new MediaUploadTask(file, tileId, transport, onUpdate, proxy, undefined, undefined, mediaKind, observe);
}
