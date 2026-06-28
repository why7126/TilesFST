import { api } from '@/features/auth/api/auth-api';
import type {
  BannerAdminItem,
  BannerCreateRequest,
  BannerUpdateRequest,
  ListBannersApiV1AdminBannersGetParams,
} from '@/shared/api/generated';

export type UploadProgressHandler = (progress: number) => void;

export async function fetchBanners(params: ListBannersApiV1AdminBannersGetParams) {
  const response = await api.listBannersApiV1AdminBannersGet(params);
  return response.data.data!;
}

export async function fetchBanner(bannerId: number) {
  const response = await api.getBannerApiV1AdminBannersBannerIdGet(bannerId);
  return response.data.data!;
}

export async function createBanner(payload: BannerCreateRequest) {
  const response = await api.createBannerApiV1AdminBannersPost(payload);
  return response.data.data!;
}

export async function updateBanner(bannerId: number, payload: BannerUpdateRequest) {
  const response = await api.updateBannerApiV1AdminBannersBannerIdPut(bannerId, payload);
  return response.data.data!;
}

export async function onlineBanner(bannerId: number) {
  const response = await api.onlineBannerApiV1AdminBannersBannerIdOnlinePost(bannerId);
  return response.data.data!;
}

export async function offlineBanner(bannerId: number) {
  const response = await api.offlineBannerApiV1AdminBannersBannerIdOfflinePost(bannerId);
  return response.data.data!;
}

export async function deleteBanner(bannerId: number) {
  await api.deleteBannerApiV1AdminBannersBannerIdDelete(bannerId);
}

export async function uploadBannerImage(file: File, onProgress?: UploadProgressHandler) {
  const response = await api.uploadBannerImageApiV1AdminUploadsBannerImagesPost(
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

export type { BannerAdminItem };

export { canDeleteBanner, canOnlineBanner } from '../lib/banner-display';
