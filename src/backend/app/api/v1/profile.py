"""Profile self-service API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_user_repository, require_admin_access
from app.db.session import get_db
from app.repositories.profile_activity_repository import ProfileActivityRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.common import ApiResponse
from app.schemas.profile import ProfileActivityItem, ProfileMe, ProfilePatchRequest
from app.services.profile_service import ProfileService

router = APIRouter(dependencies=[Depends(require_admin_access)])


def get_profile_activity_repository(
    db: Annotated[Session, Depends(get_db)],
) -> ProfileActivityRepository:
    return ProfileActivityRepository(db)


def get_profile_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    activity_repo: Annotated[ProfileActivityRepository, Depends(get_profile_activity_repository)],
) -> ProfileService:
    return ProfileService(user_repo, activity_repo)


@router.get(
    "/me",
    response_model=ApiResponse[ProfileMe],
    summary="获取当前用户个人资料",
)
def get_profile_me(
    current_user: Annotated[UserRecord, Depends(require_admin_access)],
    service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ApiResponse[ProfileMe]:
    return ApiResponse(data=service.get_me(current_user))


@router.patch(
    "/me",
    response_model=ApiResponse[ProfileMe],
    summary="更新当前用户个人资料",
)
def patch_profile_me(
    payload: ProfilePatchRequest,
    current_user: Annotated[UserRecord, Depends(require_admin_access)],
    service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ApiResponse[ProfileMe]:
    return ApiResponse(data=service.patch_me(current_user, payload))


@router.get(
    "/me/activities",
    response_model=ApiResponse[list[ProfileActivityItem]],
    summary="获取个人资料操作记录",
)
def get_profile_activities(
    current_user: Annotated[UserRecord, Depends(require_admin_access)],
    service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ApiResponse[list[ProfileActivityItem]]:
    return ApiResponse(data=service.list_activities(current_user))
