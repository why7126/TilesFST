"""Real-user performance monitoring APIs."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import require_system_admin
from app.db.session import get_db
from app.repositories.performance_repository import PerformanceRepository
from app.schemas.common import ApiResponse
from app.schemas.performance import (
    ClientType,
    PerformanceEventBatchCreate,
    PerformanceFilterOptionsData,
    PerformanceFilterOptionsQueryParams,
    PerformanceEventIngestData,
    PerformanceSampleData,
    PerformanceSampleQueryParams,
    PerformanceSummaryData,
    PerformanceSummaryQueryParams,
)
from app.services.performance_service import PerformanceService

router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_system_admin)])


def get_performance_service(db: Session = Depends(get_db)) -> PerformanceService:
    return PerformanceService(PerformanceRepository(db))


@router.post(
    "",
    response_model=ApiResponse[PerformanceEventIngestData],
    summary="上报真实用户页面性能事件",
    description="匿名上报 Web 与微信小程序 RUM 性能事件；失败不得阻断主业务流程。",
)
def ingest_performance_events(
    payload: PerformanceEventBatchCreate,
    request: Request,
    service: Annotated[PerformanceService, Depends(get_performance_service)],
) -> ApiResponse[PerformanceEventIngestData]:
    client_host = request.client.host if request.client else None
    ip_family = "unknown"
    if client_host:
        ip_family = "ipv6" if ":" in client_host else "ipv4"
    return ApiResponse(
        data=service.ingest(
            payload,
            user_agent=request.headers.get("user-agent"),
            ip_family=ip_family,
        )
    )


@admin_router.get(
    "/filter-options",
    response_model=ApiResponse[PerformanceFilterOptionsData],
    summary="真实用户页面性能筛选候选值",
    description="系统管理员按时间范围查询 RUM 筛选维度候选值；候选值不随其他筛选项级联收敛。",
)
def list_performance_filter_options(
    service: Annotated[PerformanceService, Depends(get_performance_service)],
    start_time: str | None = Query(default=None, max_length=64),
    end_time: str | None = Query(default=None, max_length=64),
) -> ApiResponse[PerformanceFilterOptionsData]:
    params = PerformanceFilterOptionsQueryParams(start_time=start_time, end_time=end_time)
    return ApiResponse(data=service.filter_options(params))


@admin_router.get(
    "/summary",
    response_model=ApiResponse[PerformanceSummaryData],
    summary="真实用户页面性能聚合",
    description="系统管理员按端、页面、版本、网络和时间范围查询 RUM 聚合指标。",
)
def summarize_performance_events(
    service: Annotated[PerformanceService, Depends(get_performance_service)],
    client_type: ClientType | None = Query(default=None),
    page_key: str | None = Query(default=None, max_length=120),
    app_version: str | None = Query(default=None, max_length=64),
    network_type: str | None = Query(default=None, max_length=32),
    device_class: str | None = Query(default=None, max_length=32),
    metric_name: str | None = Query(default=None, max_length=64),
    start_time: str | None = Query(default=None, max_length=64),
    end_time: str | None = Query(default=None, max_length=64),
    min_samples: int = Query(default=20, ge=1, le=10_000),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    limit: int | None = Query(default=None, ge=1, le=100),
) -> ApiResponse[PerformanceSummaryData]:
    params = PerformanceSummaryQueryParams(
        client_type=client_type,
        page_key=page_key,
        app_version=app_version,
        network_type=network_type,
        device_class=device_class,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        min_samples=min_samples,
        page=page,
        page_size=limit or page_size,
        limit=limit,
    )
    return ApiResponse(data=service.summarize(params))


@admin_router.get(
    "/samples",
    response_model=ApiResponse[PerformanceSampleData],
    summary="真实用户页面性能样本明细",
    description="系统管理员按聚合维度查看最近 RUM 受控样本；不返回完整 URL、Header、Cookie、签名 URL 或原始 payload。",
)
def list_performance_event_samples(
    service: Annotated[PerformanceService, Depends(get_performance_service)],
    client_type: ClientType | None = Query(default=None),
    page_key: str | None = Query(default=None, max_length=120),
    app_version: str | None = Query(default=None, max_length=64),
    network_type: str | None = Query(default=None, max_length=32),
    device_class: str | None = Query(default=None, max_length=32),
    metric_name: str | None = Query(default=None, max_length=64),
    start_time: str | None = Query(default=None, max_length=64),
    end_time: str | None = Query(default=None, max_length=64),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    limit: int | None = Query(default=None, ge=1, le=100),
) -> ApiResponse[PerformanceSampleData]:
    params = PerformanceSampleQueryParams(
        client_type=client_type,
        page_key=page_key,
        app_version=app_version,
        network_type=network_type,
        device_class=device_class,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        page=page,
        page_size=limit or page_size,
        limit=limit,
    )
    return ApiResponse(data=service.list_samples(params))
