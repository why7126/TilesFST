"""Admin tile category management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_tile_category_repository, require_admin_user
from app.repositories.tile_category_repository import TileCategoryRepository
from app.schemas.common import ApiResponse
from app.schemas.tile_category_admin import (
    TileCategoryAdminItem,
    TileCategoryAdminListData,
    TileCategoryCreateRequest,
    TileCategoryTreeNode,
    TileCategoryUpdateRequest,
)
from app.services.tile_category_admin_service import TileCategoryAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])
TAGS = ["Admin Tile Categories"]


def get_tile_category_admin_service(
    repo: Annotated[TileCategoryRepository, Depends(get_tile_category_repository)],
) -> TileCategoryAdminService:
    return TileCategoryAdminService(repo)


@router.get(
    "/tree", response_model=ApiResponse[list[TileCategoryTreeNode]], tags=TAGS, summary="类目树"
)
def get_category_tree(
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[list[TileCategoryTreeNode]]:
    return ApiResponse(data=service.get_category_tree())


@router.get(
    "", response_model=ApiResponse[TileCategoryAdminListData], tags=TAGS, summary="类目列表"
)
def list_categories(
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
    level: int | None = Query(None),
    parent_id: int | None = Query(None),
) -> ApiResponse[TileCategoryAdminListData]:
    data = service.list_categories(
        page=page,
        page_size=page_size,
        keyword=keyword,
        status=status,
        level=level,
        parent_id=parent_id,
    )
    return ApiResponse(data=data)


@router.post(
    "", response_model=ApiResponse[TileCategoryAdminItem], tags=TAGS, summary="创建类目"
)
def create_category(
    payload: TileCategoryCreateRequest,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[TileCategoryAdminItem]:
    return ApiResponse(data=service.create_category(payload))


@router.get(
    "/{category_id}",
    response_model=ApiResponse[TileCategoryAdminItem],
    tags=TAGS,
    summary="类目详情",
)
def get_category(
    category_id: int,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[TileCategoryAdminItem]:
    return ApiResponse(data=service.get_category(category_id))


@router.put(
    "/{category_id}",
    response_model=ApiResponse[TileCategoryAdminItem],
    tags=TAGS,
    summary="更新类目",
)
def update_category(
    category_id: int,
    payload: TileCategoryUpdateRequest,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[TileCategoryAdminItem]:
    return ApiResponse(data=service.update_category(category_id, payload))


@router.post(
    "/{category_id}/enable",
    response_model=ApiResponse[TileCategoryAdminItem],
    tags=TAGS,
    summary="启用类目",
)
def enable_category(
    category_id: int,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[TileCategoryAdminItem]:
    return ApiResponse(data=service.enable_category(category_id))


@router.post(
    "/{category_id}/disable",
    response_model=ApiResponse[TileCategoryAdminItem],
    tags=TAGS,
    summary="停用类目",
)
def disable_category(
    category_id: int,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[TileCategoryAdminItem]:
    return ApiResponse(data=service.disable_category(category_id))


@router.delete(
    "/{category_id}", response_model=ApiResponse[None], tags=TAGS, summary="删除类目"
)
def delete_category(
    category_id: int,
    service: Annotated[TileCategoryAdminService, Depends(get_tile_category_admin_service)],
) -> ApiResponse[None]:
    service.delete_category(category_id)
    return ApiResponse(data=None)
