"""HTTP request logging middleware helpers."""

from __future__ import annotations

import time
from uuid import uuid4

from fastapi import Request
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.security import decode_access_token
from app.db.session import get_session_factory
from app.repositories.log_repository import LogRepository
from app.repositories.user_repository import UserRepository
from app.services.log_service import LogService, RequestLogContext

EXCLUDED_PREFIXES = (
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/media/",
    "/favicon",
    "/assets/",
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or f"req_{uuid4().hex[:16]}"
        request.state.request_id = request_id
        started = time.perf_counter()
        status_code = 500
        response: Response | None = None
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = max(0, int((time.perf_counter() - started) * 1000))
            if response is not None:
                response.headers["x-request-id"] = request_id
            if _should_log_request(request.url.path):
                _record_request_log(request, request_id, status_code, duration_ms)


def _should_log_request(path: str) -> bool:
    if any(path == prefix or path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return path.startswith("/api/v1")


def _record_request_log(
    request: Request,
    request_id: str,
    status_code: int,
    duration_ms: int,
) -> None:
    session = get_session_factory()()
    try:
        actor_user_id, actor_role = _resolve_actor(request, session)
        service = LogService(LogRepository(session))
        service.record_request(
            RequestLogContext(
                request_id=request_id,
                actor_user_id=actor_user_id,
                actor_role=actor_role,
                client_type=_client_type_from_request(request),
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                error_code=str(status_code) if status_code >= 400 else None,
                metadata={
                    "query_params": dict(request.query_params),
                    "path": request.url.path,
                },
            )
        )
    except Exception:
        session.rollback()
    finally:
        session.close()


def _resolve_actor(request: Request, session) -> tuple[str | None, str | None]:
    header = request.headers.get("authorization", "")
    prefix = "Bearer "
    if not header.startswith(prefix):
        return None, "anonymous"
    try:
        payload = decode_access_token(header[len(prefix) :])
    except JWTError:
        return None, "anonymous"
    user_id = payload.get("sub")
    if not user_id:
        return None, "anonymous"
    user = UserRepository(session).get_by_id(str(user_id))
    if user is None or user.status != "active":
        return None, "anonymous"
    return user.id, user.role


def _client_type_from_request(request: Request) -> str:
    explicit = request.headers.get("x-client-type")
    if explicit:
        return explicit[:32]
    if request.url.path.startswith("/api/v1/admin"):
        return "web_admin"
    return "web_catalog"
