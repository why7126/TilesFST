"""Admin user management API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_user_repository, require_system_admin
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.common import ApiResponse
from app.schemas.user_admin import (
    ResetPasswordData,
    UserAdminItem,
    UserAdminListData,
    UserCreateData,
    UserCreateRequest,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
from app.services.user_admin_service import UserAdminService

router = APIRouter(dependencies=[Depends(require_system_admin)])


def get_user_admin_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserAdminService:
    return UserAdminService(repo)


@router.get("", response_model=ApiResponse[UserAdminListData], summary="用户列表")
def list_users(
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    keyword: str | None = Query(None),
    role: str | None = Query(None),
    status: str | None = Query(None),
    login_filter: str | None = Query(None),
) -> ApiResponse[UserAdminListData]:
    data = service.list_users(
        page=page,
        page_size=page_size,
        keyword=keyword,
        role=role,
        status=status,
        login_filter=login_filter,
    )
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[UserCreateData], summary="创建用户")
def create_user(
    payload: UserCreateRequest,
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
) -> ApiResponse[UserCreateData]:
    return ApiResponse(data=service.create_user(payload))


@router.get("/{user_id}", response_model=ApiResponse[UserAdminItem], summary="用户详情")
def get_user(
    user_id: str,
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
) -> ApiResponse[UserAdminItem]:
    return ApiResponse(data=service.get_user(user_id))


@router.patch("/{user_id}", response_model=ApiResponse[UserAdminItem], summary="更新用户")
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
) -> ApiResponse[UserAdminItem]:
    return ApiResponse(data=service.update_user(user_id, payload))


@router.post(
    "/{user_id}/reset-password",
    response_model=ApiResponse[ResetPasswordData],
    summary="重置密码",
)
def reset_password(
    user_id: str,
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
    _: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[ResetPasswordData]:
    password = service.reset_password(user_id)
    return ApiResponse(data=ResetPasswordData(password=password))


@router.patch(
    "/{user_id}/status",
    response_model=ApiResponse[UserAdminItem],
    summary="更新用户状态",
)
def update_user_status(
    user_id: str,
    payload: UserStatusUpdateRequest,
    service: Annotated[UserAdminService, Depends(get_user_admin_service)],
) -> ApiResponse[UserAdminItem]:
    return ApiResponse(data=service.update_status(user_id, payload.status))
