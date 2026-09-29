"""Trace connector master-data writes without changing their HTTP contract."""

from __future__ import annotations

import logging
import re
from time import perf_counter
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.deps import require_admin_user
from app.core.exceptions import AppError
from app.db.session import get_db
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRecord
from app.services.task_trace_service import TaskTraceService, elapsed_ms

logger = logging.getLogger(__name__)
PATH = re.compile(r"^/api/v1/admin/(brands|tile-categories)(?:/([0-9]+)(?:/(enable|disable))?)?$")


def trace_workbuddy_maintenance(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[UserRecord, Depends(require_admin_user)],
):
    match = PATH.fullmatch(request.url.path)
    if (request.headers.get("x-client-type") != "workbuddy_connector"
            or request.method not in {"POST", "PUT"} or match is None):
        yield
        return
    resource, resource_id, action = match.groups()
    resource = "brand" if resource == "brands" else "category"
    action = action or ("update" if request.method == "PUT" else "create")
    context = TaskTraceService(TaskTraceRepository(db)).build_context(
        task_type=f"{resource}_{action}", request_id=getattr(request.state, "request_id", None),
        actor_user_id=user.id, client_type="workbuddy_connector",
        resource_type=resource, resource_id=resource_id,
    )
    request.state.task_trace_id = context.task_trace_id
    request.state.task_type = context.task_type
    started = perf_counter()

    def record(name: str, sequence: int, status: str = "success", error_code: str | None = None):
        try:
            # A separate session keeps telemetry commit/rollback away from business changes.
            with Session(bind=db.get_bind()) as trace_db:
                TaskTraceService(TaskTraceRepository(trace_db)).record_context_span(
                    context, span_name=name, sequence=sequence, status=status,
                    duration_ms=elapsed_ms(started), error_code=error_code,
                    summary="Connector master-data operation " + status,
                )
        except Exception:
            logger.warning("workbuddy_maintenance_trace_unavailable")

    record("api_receive", 10)
    try:
        yield
    except Exception as exc:
        code = str(exc.code) if isinstance(exc, AppError) else "10001"
        record("business_process", 40, "failed", code)
        raise
    else:
        record("business_persist", 40)
        record("api_response", 90)
