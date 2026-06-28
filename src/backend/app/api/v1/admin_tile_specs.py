"""Admin tile spec management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_tile_spec_repository, require_admin_user
from app.repositories.tile_spec_repository import TileSpecRepository
from app.schemas.common import ApiResponse
from app.schemas.tile_spec_admin import (
    TileSpecAdminItem,
    TileSpecAdminListData,
    TileSpecCreateRequest,
    TileSpecUpdateRequest,
)
from app.services.tile_spec_admin_service import TileSpecAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_tile_spec_admin_service(
    repo: Annotated[TileSpecRepository, Depends(get_tile_spec_repository)],
) -> TileSpecAdminService:
    return TileSpecAdminService(repo)


@router.get("", response_model=ApiResponse[TileSpecAdminListData], summary="瓷砖规格列表")
def list_tile_specs(
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
) -> ApiResponse[TileSpecAdminListData]:
    return ApiResponse(
        data=service.list_specs(
            page=page,
            page_size=page_size,
            keyword=keyword,
            status=status,
        )
    )


@router.post("", response_model=ApiResponse[TileSpecAdminItem], summary="创建瓷砖规格")
def create_tile_spec(
    payload: TileSpecCreateRequest,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[TileSpecAdminItem]:
    return ApiResponse(data=service.create_spec(payload))


@router.get("/{spec_id}", response_model=ApiResponse[TileSpecAdminItem], summary="瓷砖规格详情")
def get_tile_spec(
    spec_id: int,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[TileSpecAdminItem]:
    return ApiResponse(data=service.get_spec(spec_id))


@router.put("/{spec_id}", response_model=ApiResponse[TileSpecAdminItem], summary="更新瓷砖规格")
def update_tile_spec(
    spec_id: int,
    payload: TileSpecUpdateRequest,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[TileSpecAdminItem]:
    return ApiResponse(data=service.update_spec(spec_id, payload))


@router.post(
    "/{spec_id}/enable",
    response_model=ApiResponse[TileSpecAdminItem],
    summary="启用瓷砖规格",
)
def enable_tile_spec(
    spec_id: int,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[TileSpecAdminItem]:
    return ApiResponse(data=service.enable_spec(spec_id))


@router.post(
    "/{spec_id}/disable",
    response_model=ApiResponse[TileSpecAdminItem],
    summary="停用瓷砖规格",
)
def disable_tile_spec(
    spec_id: int,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[TileSpecAdminItem]:
    return ApiResponse(data=service.disable_spec(spec_id))


@router.delete("/{spec_id}", response_model=ApiResponse[dict[str, bool]], summary="删除瓷砖规格")
def delete_tile_spec(
    spec_id: int,
    service: Annotated[TileSpecAdminService, Depends(get_tile_spec_admin_service)],
) -> ApiResponse[dict[str, bool]]:
    service.delete_spec(spec_id)
    return ApiResponse(data={"success": True})
