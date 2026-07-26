"""HTTP request logging middleware helpers."""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import Request
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_session_factory
from app.repositories.log_repository import LogRepository
from app.repositories.user_repository import UserRepository
from app.services.log_service import LogService, RequestLogContext
from app.services.task_trace_service import TaskTraceService

CLIENT_REQUEST_ID_HEADER = "x-client-request-id"
CLIENT_REQUEST_ID_MAX_LENGTH = 128
CLIENT_REQUEST_ID_ALLOWED_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-")
ALLOWED_CLIENT_TYPES = frozenset({"web_admin", "web_catalog", "wechat_miniapp"})

EXCLUDED_PREFIXES = (
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/media/",
    "/favicon",
    "/assets/",
)

MAX_BODY_SNAPSHOT_BYTES = 64 * 1024
QUERY_ALLOWLIST = {
    "page",
    "page_size",
    "keyword",
    "log_type",
    "actor_user_id",
    "client_type",
    "status_code",
    "result",
    "resource_id",
    "path_or_request_id",
    "task_trace_id",
    "start_time",
    "end_time",
    "brand_id",
    "category_id",
    "spec_id",
    "status",
    "sort",
    "order",
    "limit",
}
BODY_VALUE_ALLOWLIST = {
    "event_name",
    "page_path",
    "client_type",
    "request_id",
    "client_request_id",
    "task_trace_id",
    "task_type",
    "session_id",
    "duration_ms",
    "save_mode",
    "status",
    "result",
    "module",
    "entity_type",
    "entity_id",
    "resource_type",
    "resource_id",
}
SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "password",
    "passwd",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "secret_key",
    "access_key",
    "dsn",
    "database_url",
    "raw_payload",
    "raw_body",
    "raw_response",
    "raw_filename",
    "filename",
    "file_name",
    "internal_path",
    "object_key",
    "raw_object_key",
}


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = f"req_{uuid4().hex[:16]}"
        request.state.request_id = request_id
        client_request_id = _client_request_id_from_request(request)
        request.state.client_request_id = client_request_id
        started_at = datetime.now(UTC)
        body_schema_summary = await _body_schema_summary_from_request(request)
        started = time.perf_counter()
        status_code = 500
        response: Response | None = None
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = max(0, int((time.perf_counter() - started) * 1000))
            finished_at = datetime.now(UTC)
            if response is not None:
                response.headers["x-request-id"] = request_id
            if _should_log_request(request.url.path):
                _record_request_log(
                    request,
                    request_id,
                    status_code,
                    duration_ms,
                    started_at=started_at.isoformat(),
                    finished_at=finished_at.isoformat(),
                    body_schema_summary=body_schema_summary,
                    client_request_id=client_request_id,
                )


def _should_log_request(path: str) -> bool:
    if any(path == prefix or path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return path.startswith("/api/v1")


def _record_request_log(
    request: Request,
    request_id: str,
    status_code: int,
    duration_ms: int,
    *,
    started_at: str,
    finished_at: str,
    body_schema_summary: dict[str, Any],
    client_request_id: str | None,
) -> None:
    session = get_session_factory()()
    try:
        actor_user_id, actor_role, actor_username = _resolve_actor(request, session)
        client_type = _client_type_from_request(request)
        effective_client_request_id = client_request_id or _validate_client_request_id(
            _body_field_value(body_schema_summary, "client_request_id")
        )
        route_template, route_match_status = _route_template_from_request(request)
        query_summary = _query_summary_from_request(request)
        resource = _resource_from_request(request, route_template, body_schema_summary, query_summary)
        service = LogService(LogRepository(session))
        service.record_request(
            RequestLogContext(
                request_id=request_id,
                actor_user_id=actor_user_id,
                actor_role=actor_role,
                actor_username=actor_username,
                client_type=client_type,
                client_request_id=effective_client_request_id,
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                error_code=str(status_code) if status_code >= 400 else None,
                task_trace_id=_task_trace_id_from_request(request),
                task_type=_task_type_from_request(request),
                metadata={
                    "query_params": query_summary["allowed"],
                    "path": request.url.path,
                    "request_snapshot": {
                        "request": {
                            "method": request.method,
                            "path": request.url.path,
                            "route_template": route_template,
                            "route_match_status": route_match_status,
                            "request_id": request_id,
                            "client_request_id": effective_client_request_id,
                            "trusted_request_id_header": "x-request-id",
                            "client_request_id_header": CLIENT_REQUEST_ID_HEADER,
                        },
                        "input": {
                            "query": query_summary,
                            "body_schema_summary": body_schema_summary,
                            "redaction_summary": _redaction_summary(query_summary, body_schema_summary),
                        },
                        "resource": resource,
                        "response": {
                            "status_code": status_code,
                            "error_code": str(status_code) if status_code >= 400 else None,
                            "duration_ms": duration_ms,
                            "result": "failed" if status_code >= 400 else "success",
                            "error_summary": f"HTTP {status_code}" if status_code >= 400 else None,
                        },
                        "actor": {
                            "actor_user_id": actor_user_id,
                            "actor_username": actor_username,
                            "actor_role": actor_role,
                            "client_type": client_type,
                            "ip_summary": mask_ip_for_snapshot(request.client.host if request.client else None),
                            "user_agent_summary": _truncate_text(request.headers.get("user-agent"), 180),
                        },
                        "timing": {
                            "environment": settings.app_env,
                            "started_at": started_at,
                            "finished_at": finished_at,
                        },
                    },
                },
            )
        )
    except Exception:
        session.rollback()
    finally:
        session.close()


def _resolve_actor(request: Request, session) -> tuple[str | None, str | None, str | None]:
    header = request.headers.get("authorization", "")
    prefix = "Bearer "
    if not header.startswith(prefix):
        return None, "anonymous", None
    try:
        payload = decode_access_token(header[len(prefix) :])
    except JWTError:
        return None, "anonymous", None
    user_id = payload.get("sub")
    if not user_id:
        return None, "anonymous", None
    user = UserRepository(session).get_by_id(str(user_id))
    if user is None or user.status != "active":
        return None, "anonymous", None
    return user.id, user.role, user.username


def _client_type_from_request(request: Request) -> str:
    explicit = request.headers.get("x-client-type")
    if explicit:
        normalized = explicit.strip()[:32]
        return normalized if normalized in ALLOWED_CLIENT_TYPES else "unknown"
    if request.url.path.startswith("/api/v1/admin"):
        return "web_admin"
    if request.url.path.startswith("/api/v1/miniapp"):
        return "wechat_miniapp"
    return "web_catalog"


def _client_request_id_from_request(request: Request) -> str | None:
    header_value = request.headers.get(CLIENT_REQUEST_ID_HEADER)
    if header_value:
        return _validate_client_request_id(header_value)
    return None


def _validate_client_request_id(value: str | None) -> str | None:
    if not value:
        return None
    stripped = value.strip()
    if not stripped or len(stripped) > CLIENT_REQUEST_ID_MAX_LENGTH:
        return None
    if any(char not in CLIENT_REQUEST_ID_ALLOWED_CHARS for char in stripped):
        return None
    return stripped


def _task_trace_id_from_request(request: Request) -> str | None:
    state_value = getattr(request.state, "task_trace_id", None)
    if isinstance(state_value, str):
        valid = TaskTraceService.validate_task_trace_id(state_value)
        if valid:
            return valid
    header_value = request.headers.get("x-task-trace-id")
    return TaskTraceService.validate_task_trace_id(header_value)


def _task_type_from_request(request: Request) -> str | None:
    state_value = getattr(request.state, "task_type", None)
    if isinstance(state_value, str) and state_value:
        return state_value[:64]
    header_value = request.headers.get("x-task-type")
    if header_value:
        return header_value[:64]
    return None


def _route_template_from_request(request: Request) -> tuple[str, str]:
    route = request.scope.get("route")
    template = getattr(route, "path", None)
    if isinstance(template, str) and template:
        return template, "matched"
    return "unmatched", "unmatched"


def _query_summary_from_request(request: Request) -> dict[str, Any]:
    allowed: dict[str, str] = {}
    ignored: list[str] = []
    redacted: list[str] = []
    for key, value in request.query_params.multi_items():
        normalized = key.lower()
        if normalized in SENSITIVE_KEYS:
            redacted.append(key)
            continue
        if normalized not in QUERY_ALLOWLIST:
            ignored.append(key)
            continue
        allowed[key] = _truncate_text(value, 180) or ""
    return {
        "allowed": allowed,
        "ignored_keys": sorted(set(ignored))[:20],
        "redacted_keys": sorted(set(redacted))[:20],
        "policy": "allowlist",
    }


async def _body_schema_summary_from_request(request: Request) -> dict[str, Any]:
    content_type = (request.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
    content_length = _parse_int(request.headers.get("content-length"))
    base: dict[str, Any] = {
        "content_type": content_type or None,
        "content_length": content_length,
        "stored_raw_body": False,
    }
    if request.method.upper() not in {"POST", "PUT", "PATCH", "DELETE"}:
        return {**base, "body_type": "none", "field_count": 0, "fields": []}
    if "multipart/form-data" in content_type:
        return {**base, "body_type": "multipart", "field_count": None, "fields": [], "skip_reason": "multipart_body_not_read"}
    if "application/json" not in content_type:
        return {**base, "body_type": "unread", "field_count": None, "fields": [], "skip_reason": "non_json_body"}
    if content_length is not None and content_length > MAX_BODY_SNAPSHOT_BYTES:
        return {**base, "body_type": "json", "field_count": None, "fields": [], "skip_reason": "body_too_large"}
    try:
        raw_body = await request.body()
    except Exception:
        return {**base, "body_type": "json", "field_count": None, "fields": [], "skip_reason": "body_read_failed"}
    if not raw_body:
        return {**base, "body_type": "empty", "field_count": 0, "fields": []}
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError:
        return {**base, "body_type": "invalid_json", "field_count": None, "fields": [], "skip_reason": "json_parse_failed"}
    return {**base, **_summarize_json_body(parsed)}


def _summarize_json_body(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {
            "body_type": _value_type(value),
            "field_count": 0,
            "fields": [],
            "top_level_type": _value_type(value),
        }
    fields: list[dict[str, Any]] = []
    redacted: list[str] = []
    ignored: list[str] = []
    for key, item in value.items():
        normalized = str(key).lower()
        field: dict[str, Any] = {"name": str(key), "type": _value_type(item)}
        if normalized in SENSITIVE_KEYS:
            field["redaction"] = "redacted"
            redacted.append(str(key))
        elif normalized in BODY_VALUE_ALLOWLIST and _is_scalar(item):
            field["value"] = _truncate_text(str(item), 180)
        else:
            field["redaction"] = "value_not_stored"
            ignored.append(str(key))
        fields.append(field)
    return {
        "body_type": "json_object",
        "field_count": len(value),
        "fields": fields[:40],
        "redacted_keys": sorted(set(redacted))[:20],
        "ignored_value_keys": sorted(set(ignored))[:20],
    }


def _resource_from_request(
    request: Request,
    route_template: str,
    body_schema_summary: dict[str, Any],
    query_summary: dict[str, Any],
) -> dict[str, Any]:
    query_allowed = query_summary.get("allowed") if isinstance(query_summary.get("allowed"), dict) else {}
    for key in ("resource_id", "entity_id", "brand_id", "category_id", "spec_id"):
        value = query_allowed.get(key)
        if value:
            return {"resource_type": _resource_type_from_key(key), "resource_id": value, "id_source": f"query.{key}"}
    for field in body_schema_summary.get("fields") or []:
        if not isinstance(field, dict):
            continue
        name = str(field.get("name") or "")
        value = field.get("value")
        if name in {"resource_id", "entity_id"} and value:
            return {
                "resource_type": _body_field_value(body_schema_summary, "resource_type")
                or _body_field_value(body_schema_summary, "entity_type")
                or "unknown",
                "resource_id": str(value),
                "id_source": f"body.{name}",
            }
    if "{" in route_template and "}" in route_template:
        template_parts = route_template.strip("/").split("/")
        path_parts = request.url.path.strip("/").split("/")
        for index, part in enumerate(template_parts):
            if part.startswith("{") and part.endswith("}") and index < len(path_parts):
                resource_type = template_parts[index - 1] if index > 0 else "unknown"
                return {
                    "resource_type": resource_type,
                    "resource_id": path_parts[index],
                    "id_source": f"path.{part.strip('{}')}",
                }
    return {"resource_type": None, "resource_id": None, "id_source": "unidentified"}


def _body_field_value(summary: dict[str, Any], field_name: str) -> str | None:
    for field in summary.get("fields") or []:
        if isinstance(field, dict) and field.get("name") == field_name and field.get("value"):
            return str(field["value"])
    return None


def _redaction_summary(query_summary: dict[str, Any], body_schema_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy": "backend_allowlist_and_sensitive_blacklist",
        "query_redacted_keys": query_summary.get("redacted_keys", []),
        "query_ignored_keys": query_summary.get("ignored_keys", []),
        "body_redacted_keys": body_schema_summary.get("redacted_keys", []),
        "body_ignored_value_keys": body_schema_summary.get("ignored_value_keys", []),
        "stored_raw_body": False,
    }


def _resource_type_from_key(key: str) -> str:
    return key.removesuffix("_id") if key.endswith("_id") else "resource"


def _value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int | float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def _parse_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _truncate_text(value: str | None, limit: int) -> str | None:
    if value is None:
        return None
    return value if len(value) <= limit else value[: limit - 3] + "..."


def mask_ip_for_snapshot(value: str | None) -> str | None:
    if not value:
        return None
    if "." in value:
        parts = value.split(".")
        if len(parts) == 4:
            return ".".join(parts[:2] + ["*", "*"])
    if ":" in value:
        return value[:8] + "::****"
    return "******"
