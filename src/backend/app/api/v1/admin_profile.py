"""Admin profile password change routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_effective_settings_service, get_user_repository, require_admin_access
from app.db.session import get_db
from app.repositories.password_change_repository import PasswordChangeRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.admin_password import ChangePasswordData, ChangePasswordRequest
from app.schemas.common import ApiResponse
from app.services.effective_settings_service import EffectiveSettingsService
from app.services.password_change_service import PasswordChangeService

router = APIRouter(dependencies=[Depends(require_admin_access)])


def get_password_change_repository(
    db: Annotated[Session, Depends(get_db)],
) -> PasswordChangeRepository:
    return PasswordChangeRepository(db)


def get_password_change_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    attempt_repo: Annotated[PasswordChangeRepository, Depends(get_password_change_repository)],
    effective: Annotated[EffectiveSettingsService, Depends(get_effective_settings_service)],
) -> PasswordChangeService:
    return PasswordChangeService(user_repo, attempt_repo, effective)


@router.post(
    "/password",
    response_model=ApiResponse[ChangePasswordData],
    summary="修改当前用户密码",
    tags=["admin-profile"],
)
def change_password(
    payload: ChangePasswordRequest,
    current_user: Annotated[UserRecord, Depends(require_admin_access)],
    service: Annotated[PasswordChangeService, Depends(get_password_change_service)],
) -> ApiResponse[ChangePasswordData]:
    data = service.change_password(
        current_user,
        old_password=payload.old_password,
        new_password=payload.new_password,
    )
    return ApiResponse(data=data)
