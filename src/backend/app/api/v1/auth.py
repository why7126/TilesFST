"""Authentication API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user, get_user_repository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.auth import LoginData, LoginRequest, LogoutData, UserProfile
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(repo)


@router.post(
    "/login",
    response_model=ApiResponse[LoginData],
    summary="用户登录",
    tags=["auth"],
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
    tags=["auth"],
)
def me(
    current_user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[UserProfile]:
    return ApiResponse(data=service.get_current_profile(current_user))


@router.post(
    "/logout",
    response_model=ApiResponse[LogoutData],
    summary="用户登出",
    tags=["auth"],
)
def logout(
    _: Annotated[UserRecord, Depends(get_current_user)],
) -> ApiResponse[LogoutData]:
    return ApiResponse(data=LogoutData(success=True))
