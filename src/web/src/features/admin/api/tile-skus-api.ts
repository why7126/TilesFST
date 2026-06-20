import { api } from '@/features/auth/api/auth-api';
import type {
  ListTileSkusApiV1AdminTileSkusGetParams,
  TileSkuAdminItem,
  TileSkuAdminListData,
  TileSkuCreateRequest,
  TileSkuUpdateRequest,
} from '@/shared/api/generated';

export type TileSkuListData = TileSkuAdminListData & {
  total: number;
  page: number;
  page_size: number;
};

export async function fetchTileSkus(
  params: ListTileSkusApiV1AdminTileSkusGetParams,
): Promise<TileSkuListData> {
  const response = await api.listTileSkusApiV1AdminTileSkusGet(params);
  const data = response.data.data!;
  return {
    ...data,
    total: data.pagination.total ?? 0,
    page: data.pagination.page ?? params.page ?? 1,
    page_size: data.pagination.page_size ?? params.page_size ?? 20,
  };
}

export async function fetchTileSku(tileId: number) {
  const response = await api.getTileSkuApiV1AdminTileSkusTileIdGet(tileId);
  return response.data.data!;
}

export async function createTileSku(payload: TileSkuCreateRequest) {
  const response = await api.createTileSkuApiV1AdminTileSkusPost(payload);
  return response.data.data!;
}

export async function updateTileSku(tileId: number, payload: TileSkuUpdateRequest) {
  const response = await api.updateTileSkuApiV1AdminTileSkusTileIdPut(tileId, payload);
  return response.data.data!;
}

export async function publishTileSku(tileId: number) {
  const response = await api.publishTileSkuApiV1AdminTileSkusTileIdPublishPost(tileId);
  return response.data.data!;
}

export async function unpublishTileSku(tileId: number) {
  const response = await api.unpublishTileSkuApiV1AdminTileSkusTileIdUnpublishPost(tileId);
  return response.data.data!;
}

export async function deleteTileSku(tileId: number) {
  await api.deleteTileSkuApiV1AdminTileSkusTileIdDelete(tileId);
}

export async function uploadTileImage(file: File, tileId?: number) {
  const response = await api.uploadTileImageApiV1AdminUploadsTileImagesPost(
    { file },
    tileId ? { tile_id: tileId } : undefined,
  );
  return response.data.data!;
}

export async function uploadTileVideo(file: File, tileId?: number) {
  const response = await api.uploadTileVideoApiV1AdminUploadsTileVideosPost(
    { file },
    tileId ? { tile_id: tileId } : undefined,
  );
  return response.data.data!;
}

export function canDeleteTileSku(sku: Pick<TileSkuAdminItem, 'status'>): boolean {
  return sku.status !== 'PUBLISHED';
}

export function formatReferencePrice(price: number | null | undefined): string {
  if (price == null || Number.isNaN(price)) {
    return '—';
  }
  return `¥ ${price.toFixed(2)}`;
}

export type { TileSkuAdminItem };
