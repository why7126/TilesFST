"""Admin tile SKU management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_tile_sku_repository, require_admin_user
from app.repositories.tile_sku_repository import TileSkuRepository
from app.schemas.common import ApiResponse
from app.schemas.tile_sku_admin import (
    MaterialCompleteness,
    TileSkuAdminItem,
    TileSkuAdminListData,
    TileSkuCreateRequest,
    TileSkuUpdateRequest,
)
from app.services.tile_sku_admin_service import TileSkuAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_tile_sku_admin_service(
    repo: Annotated[TileSkuRepository, Depends(get_tile_sku_repository)],
) -> TileSkuAdminService:
    return TileSkuAdminService(repo)


@router.get("", response_model=ApiResponse[TileSkuAdminListData], summary="SKU 列表")
def list_tile_skus(
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    brand_id: int | None = Query(None),
    category_id: int | None = Query(None),
    status: str | None = Query(None),
    material_completeness: MaterialCompleteness | None = Query(None),
) -> ApiResponse[TileSkuAdminListData]:
    data = service.list_skus(
        page=page,
        page_size=page_size,
        keyword=keyword,
        brand_id=brand_id,
        category_id=category_id,
        status=status,
        material_completeness=material_completeness,
    )
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[TileSkuAdminItem], summary="创建 SKU")
def create_tile_sku(
    payload: TileSkuCreateRequest,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.create_sku(payload))


@router.get("/{tile_id}", response_model=ApiResponse[TileSkuAdminItem], summary="SKU 详情")
def get_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.get_sku(tile_id))


@router.put("/{tile_id}", response_model=ApiResponse[TileSkuAdminItem], summary="更新 SKU")
def update_tile_sku(
    tile_id: int,
    payload: TileSkuUpdateRequest,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.update_sku(tile_id, payload))


@router.post("/{tile_id}/publish", response_model=ApiResponse[TileSkuAdminItem], summary="上架 SKU")
def publish_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.publish_sku(tile_id))


@router.post(
    "/{tile_id}/unpublish", response_model=ApiResponse[TileSkuAdminItem], summary="下架 SKU"
)
def unpublish_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.unpublish_sku(tile_id))


@router.delete("/{tile_id}", response_model=ApiResponse[None], summary="删除 SKU")
def delete_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[None]:
    service.delete_sku(tile_id)
    return ApiResponse(data=None)
