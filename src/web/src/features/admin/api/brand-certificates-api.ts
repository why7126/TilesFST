import { createImageUploadTask } from '@/features/media/media-upload-api';
import type { ImageTaskOptions } from '@/features/media/use-image-upload';
import { api } from '@/features/auth/api/auth-api';
import type {
  BrandCertificateCreateRequest,
  BrandCertificateItem,
  BrandCertificateListData,
  BrandCertificateUpdateRequest,
  ListBrandCertificatesApiV1AdminBrandCertificatesGetParams,
  UploadResult,
} from '@/shared/api/generated';

export type UploadProgressHandler = (progress: number) => void;

export async function fetchBrandCertificates(
  params: ListBrandCertificatesApiV1AdminBrandCertificatesGetParams,
): Promise<BrandCertificateListData> {
  const response = await api.listBrandCertificatesApiV1AdminBrandCertificatesGet(params);
  return response.data.data!;
}

export async function createBrandCertificate(payload: BrandCertificateCreateRequest) {
  const response = await api.createBrandCertificateApiV1AdminBrandCertificatesPost(payload);
  return response.data.data!;
}

export async function updateBrandCertificate(
  certificateId: number,
  payload: BrandCertificateUpdateRequest,
) {
  const response = await api.updateBrandCertificateApiV1AdminBrandCertificatesCertificateIdPut(
    certificateId,
    payload,
  );
  return response.data.data!;
}

export async function showBrandCertificate(certificateId: number) {
  const response =
    await api.showBrandCertificateApiV1AdminBrandCertificatesCertificateIdShowPost(certificateId);
  return response.data.data!;
}

export async function hideBrandCertificate(certificateId: number) {
  const response =
    await api.hideBrandCertificateApiV1AdminBrandCertificatesCertificateIdHidePost(certificateId);
  return response.data.data!;
}

export async function deleteBrandCertificate(certificateId: number) {
  await api.deleteBrandCertificateApiV1AdminBrandCertificatesCertificateIdDelete(certificateId);
}

export async function uploadBrandCertificateFile(
  file: File, onProgress?: UploadProgressHandler, options?: ImageTaskOptions,
): Promise<UploadResult> {
  const update = (value: import('@/features/media/media-upload-controller').UploadSnapshot) => {
    onProgress?.(value.progress); options?.onUpdate?.(value);
  };
  const task = options?.task ?? createImageUploadTask(file, undefined, update, async (signal, progress) => {
    const response = await api.uploadBrandCertificateApiV1AdminUploadsBrandCertificatesPost(
      {file}, undefined, {signal, onUploadProgress: event => {
        if (event.total && event.total > 0) progress(Math.min(100, event.loaded / event.total * 100));
      }},
    );
    return response.data.data!;
  }, 'certificate');
  task.setListener(update); options?.onTask?.(task);
  return task.run();
}

export type { BrandCertificateCreateRequest, BrandCertificateItem, BrandCertificateUpdateRequest };
