"""Admin brand certificate API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin_user, require_system_admin
from app.db.session import get_db
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.brand_certificate_repository import BrandCertificateRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.user_repository import UserRecord
from app.schemas.brand_certificate_admin import (
    BrandCertificateCreateRequest,
    BrandCertificateItem,
    BrandCertificateListData,
    BrandCertificateUpdateRequest,
)
from app.schemas.common import ApiResponse
from app.services.brand_certificate_admin_service import BrandCertificateAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_brand_certificate_service(
    db: Annotated[Session, Depends(get_db)],
) -> BrandCertificateAdminService:
    return BrandCertificateAdminService(
        BrandCertificateRepository(db),
        BrandRepository(db),
        AuditLogRepository(db),
    )


@router.get("", response_model=ApiResponse[BrandCertificateListData], summary="品牌证书列表")
def list_brand_certificates(
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    brand_id: int | None = Query(None, ge=1),
    type: str | None = Query(None),
    validity_status: str | None = Query(None),
    display_status: str | None = Query(None),
) -> ApiResponse[BrandCertificateListData]:
    return ApiResponse(
        data=service.list_certificates(
            page=page,
            page_size=page_size,
            keyword=keyword,
            brand_id=brand_id,
            certificate_type=type,
            validity_status=validity_status,
            display_status=display_status,
        )
    )


@router.post("", response_model=ApiResponse[BrandCertificateItem], summary="创建品牌证书")
def create_brand_certificate(
    payload: BrandCertificateCreateRequest,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    current_user: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[BrandCertificateItem]:
    return ApiResponse(data=service.create_certificate(payload, actor_user_id=current_user.id))


@router.get(
    "/{certificate_id}",
    response_model=ApiResponse[BrandCertificateItem],
    summary="品牌证书详情",
)
def get_brand_certificate(
    certificate_id: int,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
) -> ApiResponse[BrandCertificateItem]:
    return ApiResponse(data=service.get_certificate(certificate_id))


@router.put(
    "/{certificate_id}",
    response_model=ApiResponse[BrandCertificateItem],
    summary="更新品牌证书",
)
def update_brand_certificate(
    certificate_id: int,
    payload: BrandCertificateUpdateRequest,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    current_user: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[BrandCertificateItem]:
    return ApiResponse(
        data=service.update_certificate(certificate_id, payload, actor_user_id=current_user.id)
    )


@router.post(
    "/{certificate_id}/show",
    response_model=ApiResponse[BrandCertificateItem],
    summary="显示品牌证书",
)
def show_brand_certificate(
    certificate_id: int,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    current_user: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[BrandCertificateItem]:
    return ApiResponse(data=service.show_certificate(certificate_id, actor_user_id=current_user.id))


@router.post(
    "/{certificate_id}/hide",
    response_model=ApiResponse[BrandCertificateItem],
    summary="隐藏品牌证书",
)
def hide_brand_certificate(
    certificate_id: int,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    current_user: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[BrandCertificateItem]:
    return ApiResponse(data=service.hide_certificate(certificate_id, actor_user_id=current_user.id))


@router.delete("/{certificate_id}", response_model=ApiResponse[None], summary="删除品牌证书")
def delete_brand_certificate(
    certificate_id: int,
    service: Annotated[BrandCertificateAdminService, Depends(get_brand_certificate_service)],
    current_user: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[None]:
    service.delete_certificate(certificate_id, actor_user_id=current_user.id)
    return ApiResponse(data=None)
