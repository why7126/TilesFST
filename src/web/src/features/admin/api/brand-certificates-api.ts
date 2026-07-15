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
  file: File,
  onProgress?: UploadProgressHandler,
): Promise<UploadResult> {
  const response = await api.uploadBrandCertificateApiV1AdminUploadsBrandCertificatesPost(
    { file },
    {
      onUploadProgress: (event) => {
        if (!onProgress) return;
        const total = event.total ?? 0;
        if (total <= 0) {
          onProgress(50);
          return;
        }
        onProgress(Math.min(99, Math.max(1, Math.round((event.loaded / total) * 100))));
      },
    },
  );
  return response.data.data!;
}

export type { BrandCertificateCreateRequest, BrandCertificateItem, BrandCertificateUpdateRequest };
