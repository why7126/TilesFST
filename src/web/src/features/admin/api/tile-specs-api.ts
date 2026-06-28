import { api } from '@/features/auth/api/auth-api';
import type {
  ListTileSpecsApiV1AdminTileSpecsGetParams,
  TileSpecAdminItem,
  TileSpecCreateRequest,
  TileSpecUpdateRequest,
} from '@/shared/api/generated';

export async function fetchTileSpecs(params: ListTileSpecsApiV1AdminTileSpecsGetParams) {
  const response = await api.listTileSpecsApiV1AdminTileSpecsGet(params);
  return response.data.data!;
}

export async function createTileSpec(payload: TileSpecCreateRequest) {
  const response = await api.createTileSpecApiV1AdminTileSpecsPost(payload);
  return response.data.data!;
}

export async function updateTileSpec(specId: number, payload: TileSpecUpdateRequest) {
  const response = await api.updateTileSpecApiV1AdminTileSpecsSpecIdPut(specId, payload);
  return response.data.data!;
}

export async function enableTileSpec(specId: number) {
  const response = await api.enableTileSpecApiV1AdminTileSpecsSpecIdEnablePost(specId);
  return response.data.data!;
}

export async function disableTileSpec(specId: number) {
  const response = await api.disableTileSpecApiV1AdminTileSpecsSpecIdDisablePost(specId);
  return response.data.data!;
}

export async function deleteTileSpec(specId: number) {
  await api.deleteTileSpecApiV1AdminTileSpecsSpecIdDelete(specId);
}

export function canDeleteTileSpec(spec: Pick<TileSpecAdminItem, 'sku_count' | 'status'>): boolean {
  return spec.sku_count === 0 && spec.status === 'DISABLED';
}

export function buildDisplayName(widthMm: number, lengthMm: number): string {
  return `${widthMm}×${lengthMm}mm`;
}

export type { TileSpecAdminItem };
