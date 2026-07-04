"""Admin banner management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_banner_repository, get_topic_repository, require_admin_user
from app.repositories.banner_repository import BannerRepository
from app.repositories.topic_repository import TopicRepository
from app.schemas.banner_admin import (
    BannerAdminItem,
    BannerAdminListData,
    BannerCreateRequest,
    BannerUpdateRequest,
)
from app.schemas.common import ApiResponse
from app.services.banner_admin_service import BannerAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])
TAGS = ["Admin Banners"]


def get_banner_admin_service(
    banner_repo: Annotated[BannerRepository, Depends(get_banner_repository)],
    topic_repo: Annotated[TopicRepository, Depends(get_topic_repository)],
) -> BannerAdminService:
    return BannerAdminService(banner_repo, topic_repo)


@router.get("", response_model=ApiResponse[BannerAdminListData], tags=TAGS, summary="Banner 列表")
def list_banners(
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None),
    display_client: str | None = Query(None),
    status: str | None = Query(None),
    time_status: str | None = Query(None),
) -> ApiResponse[BannerAdminListData]:
    data = service.list_banners(
        page=page,
        page_size=page_size,
        keyword=keyword,
        display_client=display_client,
        status=status,
        time_status=time_status,
    )
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[BannerAdminItem], tags=TAGS, summary="创建 Banner")
def create_banner(
    payload: BannerCreateRequest,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[BannerAdminItem]:
    return ApiResponse(data=service.create_banner(payload))


@router.get(
    "/{banner_id}", response_model=ApiResponse[BannerAdminItem], tags=TAGS, summary="Banner 详情"
)
def get_banner(
    banner_id: int,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[BannerAdminItem]:
    return ApiResponse(data=service.get_banner(banner_id))


@router.put(
    "/{banner_id}", response_model=ApiResponse[BannerAdminItem], tags=TAGS, summary="更新 Banner"
)
def update_banner(
    banner_id: int,
    payload: BannerUpdateRequest,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[BannerAdminItem]:
    return ApiResponse(data=service.update_banner(banner_id, payload))


@router.post(
    "/{banner_id}/online",
    response_model=ApiResponse[BannerAdminItem],
    tags=TAGS,
    summary="上线 Banner",
)
def online_banner(
    banner_id: int,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[BannerAdminItem]:
    return ApiResponse(data=service.online_banner(banner_id))


@router.post(
    "/{banner_id}/offline",
    response_model=ApiResponse[BannerAdminItem],
    tags=TAGS,
    summary="下线 Banner",
)
def offline_banner(
    banner_id: int,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[BannerAdminItem]:
    return ApiResponse(data=service.offline_banner(banner_id))


@router.delete("/{banner_id}", response_model=ApiResponse[None], tags=TAGS, summary="删除 Banner")
def delete_banner(
    banner_id: int,
    service: Annotated[BannerAdminService, Depends(get_banner_admin_service)],
) -> ApiResponse[None]:
    service.delete_banner(banner_id)
    return ApiResponse(data=None)
