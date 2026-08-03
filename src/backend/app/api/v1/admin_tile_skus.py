"""Admin tile SKU management API routes."""

from __future__ import annotations

from collections.abc import Callable
from time import perf_counter
from typing import Annotated, TypeVar

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import get_tile_sku_repository, get_tile_spec_repository, require_admin_user
from app.core.exceptions import AppError
from app.db.session import get_db
from app.repositories.tile_sku_repository import TileSkuRepository
from app.repositories.tile_spec_repository import TileSpecRepository
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse
from app.schemas.tile_sku_admin import (
    MaterialCompleteness,
    TileSkuAdminItem,
    TileSkuAdminListData,
    TileSkuCreateRequest,
    TileSkuUpdateRequest,
)
from app.services.tile_sku_admin_service import TileSkuAdminService
from app.services.task_trace_service import TaskTraceContext, TaskTraceService, elapsed_ms

router = APIRouter(dependencies=[Depends(require_admin_user)])
T = TypeVar("T", bound=TileSkuAdminItem)


def get_tile_sku_admin_service(
    repo: Annotated[TileSkuRepository, Depends(get_tile_sku_repository)],
    spec_repo: Annotated[TileSpecRepository, Depends(get_tile_spec_repository)],
) -> TileSkuAdminService:
    return TileSkuAdminService(repo, spec_repo)


def _request_id(request: Request) -> str | None:
    value = getattr(request.state, "request_id", None)
    return str(value) if value else None


def _record_sku_span(
    trace_service: TaskTraceService,
    context: TaskTraceContext,
    *,
    span_name: str,
    sequence: int,
    status: str = "success",
    started_at: float | None = None,
    resource_id: str | None = None,
    error_code: str | None = None,
    summary: str | None = None,
    metadata: dict | None = None,
) -> None:
    trace_service.record_context_span_safe(
        context,
        span_name=span_name,
        status=status,
        sequence=sequence,
        duration_ms=elapsed_ms(started_at) if started_at is not None else None,
        resource_id=resource_id,
        error_code=error_code,
        summary=summary,
        metadata=metadata,
    )


def _run_sku_trace(
    *,
    request: Request,
    db: Session,
    current_user: UserRecord,
    task_type: str,
    operation: Callable[[], T],
    payload_summary: dict,
) -> T:
    trace_service = TaskTraceService(TaskTraceRepository(db))
    context = trace_service.build_context(
        task_type=task_type,
        task_trace_id=request.headers.get("x-task-trace-id"),
        request_id=_request_id(request),
        actor_user_id=current_user.id,
        client_type="web_admin",
        resource_type="tile_sku",
    )
    request.state.task_trace_id = context.task_trace_id
    request.state.task_type = context.task_type

    _record_sku_span(
        trace_service,
        context,
        span_name="api_receive",
        sequence=10,
        summary="接收 SKU 任务型请求",
        metadata=payload_summary,
    )
    _record_sku_span(
        trace_service,
        context,
        span_name="input_validate",
        sequence=20,
        summary="进入 SKU 业务校验",
        metadata={"task_context": TaskTraceService.serialize_async_context(context)},
    )

    operation_started = perf_counter()
    try:
        result = operation()
    except AppError as exc:
        _record_sku_span(
            trace_service,
            context,
            span_name="business_process",
            sequence=40,
            status="failed",
            started_at=operation_started,
            error_code=str(exc.code),
            summary=exc.message,
            metadata={"error_code": exc.code, "error_message": exc.message},
        )
        raise
    except Exception:
        _record_sku_span(
            trace_service,
            context,
            span_name="business_process",
            sequence=40,
            status="failed",
            started_at=operation_started,
            error_code="10001",
            summary="SKU 任务处理失败",
        )
        raise

    resource_id = str(result.id)
    _record_sku_span(
        trace_service,
        context,
        span_name="business_persist",
        sequence=40,
        started_at=operation_started,
        resource_id=resource_id,
        summary="SKU 数据与关联媒体已保存",
        metadata={
            "status": result.status,
            "image_count": result.image_count,
            "video_count": result.video_count,
            "material_completeness": result.material_completeness,
        },
    )
    _record_sku_span(
        trace_service,
        context,
        span_name="api_response",
        sequence=90,
        resource_id=resource_id,
        summary="SKU 任务响应已返回",
    )
    result.task_trace_id = context.task_trace_id
    result.task_type = context.task_type
    return result


@router.get("", response_model=ApiResponse[TileSkuAdminListData], summary="SKU 列表")
def list_tile_skus(
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    brand_id: int | None = Query(None),
    category_id: int | None = Query(
        None,
        description="类目 ID；父类目筛选包含自身及所有子孙类目的 SKU",
    ),
    status: str | None = Query(None),
    material_completeness: MaterialCompleteness | None = Query(None),
) -> ApiResponse[TileSkuAdminListData]:
    data = service.list_skus(
        page=page,
        page_size=page_size,
        keyword=keyword,
        brand_id=brand_id,
        category_id=category_id,
        status=status,
        material_completeness=material_completeness,
    )
    return ApiResponse(data=data)


@router.post("", response_model=ApiResponse[TileSkuAdminItem], summary="创建 SKU")
def create_tile_sku(
    request: Request,
    payload: TileSkuCreateRequest,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    current_user: Annotated[UserRecord, Depends(require_admin_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiResponse[TileSkuAdminItem]:
    data = _run_sku_trace(
        request=request,
        db=db,
        current_user=current_user,
        task_type="sku_create",
        operation=lambda: service.create_sku(payload),
        payload_summary={
            "save_mode": payload.save_mode,
            "image_count": len(payload.images),
            "video_count": len(payload.videos),
        },
    )
    return ApiResponse(data=data)


@router.get(
    "/{tile_id}", response_model=ApiResponse[TileSkuAdminItem], summary="SKU 详情"
)
def get_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[TileSkuAdminItem]:
    return ApiResponse(data=service.get_sku(tile_id))


@router.put(
    "/{tile_id}", response_model=ApiResponse[TileSkuAdminItem], summary="更新 SKU"
)
def update_tile_sku(
    request: Request,
    tile_id: int,
    payload: TileSkuUpdateRequest,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    current_user: Annotated[UserRecord, Depends(require_admin_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiResponse[TileSkuAdminItem]:
    data = _run_sku_trace(
        request=request,
        db=db,
        current_user=current_user,
        task_type="sku_update",
        operation=lambda: service.update_sku(tile_id, payload),
        payload_summary={
            "tile_id": tile_id,
            "has_images": payload.images is not None,
            "has_videos": payload.videos is not None,
        },
    )
    return ApiResponse(data=data)


@router.post(
    "/{tile_id}/publish",
    response_model=ApiResponse[TileSkuAdminItem],
    summary="上架 SKU",
)
def publish_tile_sku(
    request: Request,
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    current_user: Annotated[UserRecord, Depends(require_admin_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiResponse[TileSkuAdminItem]:
    data = _run_sku_trace(
        request=request,
        db=db,
        current_user=current_user,
        task_type="sku_publish",
        operation=lambda: service.publish_sku(tile_id),
        payload_summary={"tile_id": tile_id},
    )
    return ApiResponse(data=data)


@router.post(
    "/{tile_id}/unpublish",
    response_model=ApiResponse[TileSkuAdminItem],
    summary="下架 SKU",
)
def unpublish_tile_sku(
    request: Request,
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
    current_user: Annotated[UserRecord, Depends(require_admin_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiResponse[TileSkuAdminItem]:
    data = _run_sku_trace(
        request=request,
        db=db,
        current_user=current_user,
        task_type="sku_unpublish",
        operation=lambda: service.unpublish_sku(tile_id),
        payload_summary={"tile_id": tile_id},
    )
    return ApiResponse(data=data)


@router.delete("/{tile_id}", response_model=ApiResponse[None], summary="删除 SKU")
def delete_tile_sku(
    tile_id: int,
    service: Annotated[TileSkuAdminService, Depends(get_tile_sku_admin_service)],
) -> ApiResponse[None]:
    service.delete_sku(tile_id)
    return ApiResponse(data=None)
