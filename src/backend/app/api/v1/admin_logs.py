"""Admin log audit APIs."""

from __future__ import annotations

from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_system_admin
from app.db.session import get_db
from app.repositories.log_repository import LogRepository
from app.schemas.common import ApiResponse
from app.schemas.logs import LogDetailData, LogListData, LogQueryParams
from app.services.log_service import LogService

router = APIRouter(dependencies=[Depends(require_system_admin)])


def get_log_service(db: Session = Depends(get_db)) -> LogService:
    return LogService(LogRepository(db))


@router.get(
    "",
    response_model=ApiResponse[LogListData],
    summary="日志审计列表",
    description="系统管理员分页查询 API 请求日志、产品行为事件和审计操作。",
)
def list_logs(
    service: Annotated[LogService, Depends(get_log_service)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    log_type: Literal["request", "usage_event", "audit"] | None = Query(default=None),
    keyword: str | None = Query(default=None, max_length=120),
    actor_user_id: str | None = Query(default=None, max_length=64),
    client_type: str | None = Query(default=None, max_length=32),
    status_code: int | None = Query(default=None, ge=100, le=599),
    result: str | None = Query(default=None, pattern="^(success|failed)$"),
    resource_id: str | None = Query(default=None, max_length=128),
    path_or_request_id: str | None = Query(default=None, max_length=180),
    start_time: str | None = Query(default=None, max_length=64),
    end_time: str | None = Query(default=None, max_length=64),
) -> ApiResponse[LogListData]:
    params = LogQueryParams(
        page=page,
        page_size=page_size,
        log_type=log_type,
        keyword=keyword,
        actor_user_id=actor_user_id,
        client_type=client_type,
        status_code=status_code,
        result=cast("Literal['success', 'failed'] | None", result),
        resource_id=resource_id,
        path_or_request_id=path_or_request_id,
        start_time=start_time,
        end_time=end_time,
    )
    return ApiResponse(data=service.list_logs(params))


@router.get(
    "/{log_id}",
    response_model=ApiResponse[LogDetailData],
    summary="日志审计详情",
    description="系统管理员查询单条日志的详情抽屉数据。",
)
def get_log_detail(
    log_id: str,
    service: Annotated[LogService, Depends(get_log_service)],
) -> ApiResponse[LogDetailData]:
    return ApiResponse(data=service.get_log_detail(log_id))
