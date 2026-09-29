import { createImageUploadTask } from '@/features/media/media-upload-api';
import type { MediaUploadTask, UploadSnapshot } from '@/features/media/media-upload-controller';
import { api } from '@/features/auth/api/auth-api';
import type {
  BrandAdminItem,
  BrandCreateRequest,
  BrandUpdateRequest,
  ListBrandsApiV1AdminBrandsGetParams,
} from '@/shared/api/generated';

export type UploadProgressHandler = (progress: number) => void;

export async function fetchBrands(params: ListBrandsApiV1AdminBrandsGetParams) {
  const response = await api.listBrandsApiV1AdminBrandsGet(params);
  return response.data.data!;
}

export async function createBrand(payload: BrandCreateRequest) {
  const response = await api.createBrandApiV1AdminBrandsPost(payload);
  return response.data.data!;
}

export async function updateBrand(brandId: number, payload: BrandUpdateRequest) {
  const response = await api.updateBrandApiV1AdminBrandsBrandIdPut(brandId, payload);
  return response.data.data!;
}

export async function enableBrand(brandId: number) {
  const response = await api.enableBrandApiV1AdminBrandsBrandIdEnablePost(brandId);
  return response.data.data!;
}

export async function disableBrand(brandId: number) {
  const response = await api.disableBrandApiV1AdminBrandsBrandIdDisablePost(brandId);
  return response.data.data!;
}

export async function deleteBrand(brandId: number) {
  await api.deleteBrandApiV1AdminBrandsBrandIdDelete(brandId);
}

export async function uploadBrandLogo(file: File, onProgress?: UploadProgressHandler, options?: {
  brandId?: number; task?: MediaUploadTask; onTask?: (task: MediaUploadTask) => void;
  onUpdate?: (value: UploadSnapshot) => void;
}) {
  const update = (value: UploadSnapshot) => { onProgress?.(value.progress); options?.onUpdate?.(value); };
  const task = options?.task ?? createImageUploadTask(file, options?.brandId, update, async (signal, progress) => {
    const response = await api.uploadBrandLogoApiV1AdminUploadsBrandLogosPost({ file }, undefined, {
      signal, onUploadProgress: event => {
        if (event.total && event.total > 0) progress(Math.min(100, event.loaded / event.total * 100));
      },
    });
    return response.data.data!;
  }, 'brand_logo');
  task.setListener(update);
  options?.onTask?.(task);
  return task.run();
}

export function canDeleteBrand(brand: Pick<BrandAdminItem, 'sku_count' | 'status'>): boolean {
  return brand.sku_count === 0 && brand.status === 'DISABLED';
}

export type { BrandAdminItem };
