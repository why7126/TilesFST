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

export async function uploadBrandLogo(file: File, onProgress?: UploadProgressHandler) {
  const response = await api.uploadBrandLogoApiV1AdminUploadsBrandLogosPost(
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

export function canDeleteBrand(brand: Pick<BrandAdminItem, 'sku_count' | 'status'>): boolean {
  return brand.sku_count === 0 && brand.status === 'DISABLED';
}

export type { BrandAdminItem };
