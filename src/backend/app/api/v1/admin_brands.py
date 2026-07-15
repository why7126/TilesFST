"""Admin brand management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin_user
from app.db.session import get_db
from app.repositories.brand_certificate_repository import BrandCertificateRepository
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand_admin import (
    BrandAdminItem,
    BrandAdminListData,
    BrandCreateRequest,
    BrandUpdateRequest,
)
from app.schemas.common import ApiResponse
from app.services.brand_admin_service import BrandAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_brand_admin_service(
    db: Annotated[Session, Depends(get_db)],
) -> BrandAdminService:
    return BrandAdminService(BrandRepository(db), BrandCertificateRepository(db))


@router.get("", response_model=ApiResponse[BrandAdminListData], summary="品牌列表")
def list_brands(
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
) -> ApiResponse[BrandAdminListData]:
    data = service.list_brands(
        page=page,
        page_size=page_size,
        keyword=keyword,
        status=status,
    )
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[BrandAdminItem], summary="创建品牌")
def create_brand(
    payload: BrandCreateRequest,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[BrandAdminItem]:
    return ApiResponse(data=service.create_brand(payload))


@router.get(
    "/{brand_id}", response_model=ApiResponse[BrandAdminItem], summary="品牌详情"
)
def get_brand(
    brand_id: int,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[BrandAdminItem]:
    return ApiResponse(data=service.get_brand(brand_id))


@router.put(
    "/{brand_id}", response_model=ApiResponse[BrandAdminItem], summary="更新品牌"
)
def update_brand(
    brand_id: int,
    payload: BrandUpdateRequest,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[BrandAdminItem]:
    return ApiResponse(data=service.update_brand(brand_id, payload))


@router.post(
    "/{brand_id}/enable",
    response_model=ApiResponse[BrandAdminItem],
    summary="启用品牌",
)
def enable_brand(
    brand_id: int,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[BrandAdminItem]:
    return ApiResponse(data=service.enable_brand(brand_id))


@router.post(
    "/{brand_id}/disable",
    response_model=ApiResponse[BrandAdminItem],
    summary="停用品牌",
)
def disable_brand(
    brand_id: int,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[BrandAdminItem]:
    return ApiResponse(data=service.disable_brand(brand_id))


@router.delete("/{brand_id}", response_model=ApiResponse[None], summary="删除品牌")
def delete_brand(
    brand_id: int,
    service: Annotated[BrandAdminService, Depends(get_brand_admin_service)],
) -> ApiResponse[None]:
    service.delete_brand(brand_id)
    return ApiResponse(data=None)
