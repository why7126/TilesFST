"""Authentication API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_effective_settings_service, get_user_repository
from app.db.session import get_db
from app.repositories.profile_activity_repository import ProfileActivityRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.auth import LoginData, LoginRequest, LogoutData, ThemePreferenceUpdateRequest, UserProfile
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService
from app.services.effective_settings_service import EffectiveSettingsService

router = APIRouter()


def get_profile_activity_repository(
    db: Annotated[Session, Depends(get_db)],
) -> ProfileActivityRepository:
    return ProfileActivityRepository(db)


def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    activity_repo: Annotated[ProfileActivityRepository, Depends(get_profile_activity_repository)],
    effective: Annotated[EffectiveSettingsService, Depends(get_effective_settings_service)],
) -> AuthService:
    return AuthService(repo, activity_repo, effective)


@router.post(
    "/login",
    response_model=ApiResponse[LoginData],
    summary="用户登录",
)
def login(
    payload: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[LoginData]:
    data = service.login(
        username=payload.username,
        password=payload.password,
        remember_me=payload.remember_me,
    )
    return ApiResponse(data=data)


@router.get(
    "/me",
    response_model=ApiResponse[UserProfile],
    summary="获取当前用户",
)
def me(
    current_user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[UserProfile]:
    return ApiResponse(data=service.get_current_profile(current_user))


@router.patch(
    "/me/theme",
    response_model=ApiResponse[UserProfile],
    summary="更新当前用户主题偏好",
)
def update_theme_preference(
    payload: ThemePreferenceUpdateRequest,
    current_user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[UserProfile]:
    return ApiResponse(data=service.update_theme_mode(current_user, payload.theme_mode))


@router.post(
    "/logout",
    response_model=ApiResponse[LogoutData],
    summary="用户登出",
)
def logout(
    _: Annotated[UserRecord, Depends(get_current_user)],
) -> ApiResponse[LogoutData]:
    return ApiResponse(data=LogoutData(success=True))
