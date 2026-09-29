"""Admin-only control plane for authorized uploads; no media bytes pass here."""
from time import perf_counter
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request, Response
from sqlalchemy.orm import Session

from app.core import error_codes as codes
from app.core.deps import get_effective_settings_service, require_admin_access
from app.core.exceptions import AppError
from app.db.session import get_db
from app.modules.media.cos_upload import UploadObjectMismatch
from app.modules.media.upload_sessions import UploadSessionConflict, UploadSessionNotFound
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRecord
from app.schemas.common import ApiResponse, VALIDATION_ERROR_RESPONSE
from app.schemas.upload_session import (
    UploadAuthorization, UploadSessionCreate, UploadSessionCreated, UploadSessionRenewed, UploadSessionStatus,
)
from app.services.effective_settings_service import EffectiveSettingsService
from app.services.task_trace_service import TaskTraceService, elapsed_ms
from app.services.upload_session_service import UploadSessionService

router = APIRouter()
Actor = Annotated[UserRecord, Depends(require_admin_access)]


def get_service(db: Annotated[Session, Depends(get_db)],
                effective: Annotated[EffectiveSettingsService, Depends(get_effective_settings_service)]):
    return UploadSessionService(db, effective)


Service = Annotated[UploadSessionService, Depends(get_service)]


def _run(service, actor, request, response, operation, action):
    response.headers["Cache-Control"] = "no-store"
    started = perf_counter()
    result = None
    failure = None
    try:
        result = operation()
        return ApiResponse(data=result)
    except UploadSessionNotFound:
        failure = AppError(status_code=404, code=codes.UPLOAD_SESSION_NOT_FOUND, message="上传会话不存在或不可访问")
        raise failure from None
    except UploadSessionConflict:
        failure = AppError(status_code=409, code=codes.UPLOAD_SESSION_CONFLICT, message="上传状态已变化，请刷新后重试")
        raise failure from None
    except UploadObjectMismatch:
        failure = AppError(status_code=400, code=codes.UPLOAD_OBJECT_MISMATCH, message="上传对象与声明不符，请检查文件后重新上传")
        raise failure from None
    except AppError as exc:
        failure = exc
        raise
    except Exception:
        failure = AppError(status_code=500, code=codes.SYSTEM_ERROR, message="上传控制异常")
        raise
    finally:
        service.db.rollback()  # control methods commit durable changes themselves
        # Trace uses a separate transaction. Logging failure cannot undo upload state.
        try:
            status = getattr(result, "session", None) or (result if isinstance(result, UploadSessionStatus) else None)
            trace_id = status.task_trace_id if status else None
            if not trace_id and request.path_params.get("session_id"):
                try:
                    trace_id = service.repo.get(request.path_params["session_id"], actor.id)["task_trace_id"]
                except UploadSessionNotFound:
                    pass
                finally:
                    service.db.rollback()
            with Session(service.db.get_bind()) as trace_db:
                trace = TaskTraceService(TaskTraceRepository(trace_db))
                context = trace.build_context(task_type="media_direct_upload",
                    task_trace_id=trace_id,
                    request_id=getattr(request.state, "request_id", None),
                    behavior_trace_id=getattr(request.state, "behavior_trace_id", None),
                    actor_user_id=actor.id, client_type="web_admin")
                request.state.task_trace_id = context.task_trace_id
                request.state.task_type = context.task_type
                trace.record_context_span_safe(context, span_name=action, duration_ms=elapsed_ms(started),
                    status="failed" if failure else "success", error_code=str(failure.code) if failure else None,
                    metadata={"mode": getattr(result, "mode", "cos_direct"), "stage": action, "source":"backend", "duration_scope":"inclusive_control_request"})
        except Exception:
            pass  # no exception details: SDK exceptions can contain signed queries


@router.post("", response_model=ApiResponse[UploadSessionCreated], responses=VALIDATION_ERROR_RESPONSE, summary="申请媒体上传会话")
def create_upload_session(payload: UploadSessionCreate, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.create(payload, actor), "authorize")


@router.get("/{session_id}", response_model=ApiResponse[UploadSessionStatus], summary="查询媒体上传状态")
def query_upload_session(session_id: str, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.query(session_id, actor), "query")


@router.post("/{session_id}/renew", response_model=ApiResponse[UploadSessionRenewed], summary="续签媒体上传授权")
def renew_upload_session(session_id: str, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.renew(session_id, actor), "renew")


@router.post("/{session_id}/parts/{part_number}/authorize", response_model=ApiResponse[UploadAuthorization], responses=VALIDATION_ERROR_RESPONSE, summary="签发单片上传授权")
def authorize_upload_part(session_id: str, actor: Actor, service: Service, request: Request, response: Response,
                          part_number: int = Path(ge=1, le=10000)):
    return _run(service, actor, request, response, lambda: service.authorize(session_id, actor, part_number), "authorize_part")


@router.post("/{session_id}/confirm", response_model=ApiResponse[UploadSessionStatus], summary="校验并确认媒体上传")
def confirm_upload_session(session_id: str, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.confirm(session_id, actor), "confirm")


@router.post("/{session_id}/cancel", response_model=ApiResponse[UploadSessionStatus], summary="取消未绑定媒体上传")
def cancel_upload_session(session_id: str, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.cancel(session_id, actor), "cancel")


@router.post("/{session_id}/retry-processing", response_model=ApiResponse[UploadSessionStatus], summary="重试失败的图片派生")
def retry_upload_processing(session_id: str, actor: Actor, service: Service, request: Request, response: Response):
    return _run(service, actor, request, response, lambda: service.retry_processing(session_id, actor), "retry_processing")
