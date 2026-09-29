"""Public and administrative media authorization use separate identity dependencies."""

from typing import Annotated
from time import perf_counter

from fastapi import APIRouter, Depends, Request, Response, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin_user
from app.db.session import get_db
from app.repositories.media_read_repository import MediaReadRepository
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse, VALIDATION_ERROR_RESPONSE
from app.schemas.media_read import MediaReadData, MediaReadRequest
from app.services.media_read_service import MediaReadService
from app.services.task_trace_service import TaskTraceService, elapsed_ms

router = APIRouter()
admin_router = APIRouter()


def _authorize(payload: MediaReadRequest, request: Request, response: Response, db: Session, actor: UserRecord | None) -> ApiResponse[MediaReadData]:
    response.headers["Cache-Control"] = "no-store"
    started = perf_counter()
    client_type = request.headers.get("x-client-type", "unknown")
    if client_type not in {"web_admin", "web_catalog", "wechat_miniapp"}:
        client_type = "unknown"
    data = MediaReadService(MediaReadRepository(db)).authorize(payload, actor, client_type)
    trace = TaskTraceService(TaskTraceRepository(db))
    context = trace.build_context(
        task_type="media_read_authorization",
        request_id=getattr(request.state, "request_id", None),
        behavior_trace_id=getattr(request.state, "behavior_trace_id", None),
        actor_user_id=actor.id if actor else None,
        client_type=client_type,
    )
    request.state.task_trace_id = context.task_trace_id
    request.state.task_type = context.task_type
    trace.record_context_span_safe(
        context, span_name="authorize_and_probe", duration_ms=elapsed_ms(started),
        status="failed" if any(item.status != "ready" for item in data.items) else "success",
        metadata={"item_count": len(data.items), "ready_count": sum(item.status == "ready" for item in data.items),
                  "external_count": sum(bool(item.descriptor and item.descriptor.read_mode == "external") for item in data.items),
                  "proxy_count": sum(bool(item.descriptor and item.descriptor.read_mode == "proxy") for item in data.items),
                  "degraded_count": sum(bool(item.descriptor and item.descriptor.degraded) for item in data.items)},
    )
    return ApiResponse(data=data)


@router.post("/read-authorizations", response_model=ApiResponse[MediaReadData], responses=VALIDATION_ERROR_RESPONSE, summary="公开媒体读取授权")
def authorize_public_media(payload: MediaReadRequest, request: Request, response: Response, db: Annotated[Session, Depends(get_db)]) -> ApiResponse[MediaReadData]:
    return _authorize(payload, request, response, db, None)


@admin_router.post("/read-authorizations", response_model=ApiResponse[MediaReadData], responses=VALIDATION_ERROR_RESPONSE, summary="管理媒体读取授权")
def authorize_admin_media(payload: MediaReadRequest, request: Request, response: Response, db: Annotated[Session, Depends(get_db)], actor: Annotated[UserRecord, Depends(require_admin_user)]) -> ApiResponse[MediaReadData]:
    return _authorize(payload, request, response, db, actor)


@router.api_route("/read", methods=["GET", "HEAD"], include_in_schema=False)
def read_authorized_media(request: Request, db: Annotated[Session, Depends(get_db)], ticket: str = Query(min_length=1, max_length=4096)):
    from app.services.media_proxy_service import read_proxy
    return read_proxy(db, ticket, request.method, request.headers.get("range"))
