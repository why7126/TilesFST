"""Admin system settings API routes."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.deps import require_system_admin
from app.db.session import get_db
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse
from app.schemas.system_settings import (
    AuditSettingsPatch,
    BasicSettingsPatch,
    MediaSettingsPatch,
    NotificationSettingsPatch,
    SecuritySettingsPatch,
    SystemSettingsAuditRecentData,
    SystemSettingsAuditItem,
    SystemSettingsGroupResponse,
)
from app.services.system_settings_service import SystemSettingsService
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(require_system_admin)])
TAGS = ["Admin System Settings"]

PATCH_MODELS: dict[str, type] = {
    "basic": BasicSettingsPatch,
    "media": MediaSettingsPatch,
    "security": SecuritySettingsPatch,
    "notification": NotificationSettingsPatch,
    "audit": AuditSettingsPatch,
}


def get_system_settings_service(db: Session = Depends(get_db)) -> SystemSettingsService:
    return SystemSettingsService(
        SystemSettingsRepository(db),
        AuditLogRepository(db),
    )


@router.get(
    "/audit/recent",
    response_model=ApiResponse[SystemSettingsAuditRecentData],
    tags=TAGS,
    summary="最近系统设置变更",
)
def get_recent_audit(
    service: Annotated[SystemSettingsService, Depends(get_system_settings_service)],
    limit: int = Query(10, ge=1, le=50),
) -> ApiResponse[SystemSettingsAuditRecentData]:
    items = [
        SystemSettingsAuditItem(**item) for item in service.list_recent_audit(limit=limit)
    ]
    return ApiResponse(data=SystemSettingsAuditRecentData(items=items))


@router.get(
    "/{group}",
    response_model=ApiResponse[SystemSettingsGroupResponse],
    tags=TAGS,
    summary="读取设置分组",
)
def get_settings_group(
    group: str,
    service: Annotated[SystemSettingsService, Depends(get_system_settings_service)],
) -> ApiResponse[SystemSettingsGroupResponse]:
    data = service.get_group(group)
    return ApiResponse(data=SystemSettingsGroupResponse(group=group, data=data))


@router.patch(
    "/{group}",
    response_model=ApiResponse[SystemSettingsGroupResponse],
    tags=TAGS,
    summary="更新设置分组",
)
def patch_settings_group(
    group: str,
    payload: dict[str, Any],
    service: Annotated[SystemSettingsService, Depends(get_system_settings_service)],
    actor: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[SystemSettingsGroupResponse]:
    model_cls = PATCH_MODELS.get(group)
    if model_cls is None:
        from app.core.exceptions import AppError

        raise AppError(status_code=404, code=40400, message="未知的设置分组")
    validated = model_cls.model_validate(payload)
    patch_dict = validated.model_dump(exclude_unset=True)
    data = service.patch_group(group, patch_dict, actor.id)
    return ApiResponse(data=SystemSettingsGroupResponse(group=group, data=data))


@router.post(
    "/{group}/reset",
    response_model=ApiResponse[SystemSettingsGroupResponse],
    tags=TAGS,
    summary="恢复设置分组默认",
)
def reset_settings_group(
    group: str,
    service: Annotated[SystemSettingsService, Depends(get_system_settings_service)],
    actor: Annotated[UserRecord, Depends(require_system_admin)],
) -> ApiResponse[SystemSettingsGroupResponse]:
    data = service.reset_group(group, actor.id)
    return ApiResponse(data=SystemSettingsGroupResponse(group=group, data=data))
