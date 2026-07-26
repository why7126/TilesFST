"""Task Trace service helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

from app.repositories.task_trace_repository import TaskSpanRecord, TaskTraceRecord, TaskTraceRepository

TASK_TRACE_ID_PATTERN = re.compile(r"^task_[a-z0-9_]{12,64}$")

SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "secret_key",
    "access_key",
    "dsn",
    "database_url",
    "minio_access_key",
    "minio_secret_key",
    "cos_secret_id",
    "cos_secret_key",
    "env",
    ".env",
    "raw_filename",
    "raw_payload",
    "raw_response",
    "internal_path",
}


@dataclass(frozen=True)
class TaskTraceTimeline:
    trace: TaskTraceRecord | None
    spans: list[TaskSpanRecord]


@dataclass(frozen=True)
class TaskTraceContext:
    task_trace_id: str
    task_type: str
    request_id: str | None = None
    parent_request_id: str | None = None
    actor_user_id: str | None = None
    client_type: str | None = "web_admin"
    resource_type: str | None = None
    resource_id: str | None = None


class TaskTraceService:
    def __init__(self, repo: TaskTraceRepository, *, default_request_id: str | None = None) -> None:
        self._repo = repo
        self.default_request_id = default_request_id

    @staticmethod
    def generate_task_trace_id(task_type: str) -> str:
        slug = re.sub(r"[^a-z0-9_]+", "_", task_type.lower()).strip("_")[:24] or "task"
        return f"task_{slug}_{uuid4().hex[:16]}"

    @staticmethod
    def validate_task_trace_id(value: str | None) -> str | None:
        if not value:
            return None
        candidate = value.strip().lower()
        if not TASK_TRACE_ID_PATTERN.fullmatch(candidate):
            return None
        return candidate

    def build_context(
        self,
        *,
        task_type: str,
        task_trace_id: str | None = None,
        request_id: str | None = None,
        actor_user_id: str | None = None,
        client_type: str | None = "web_admin",
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> TaskTraceContext:
        valid_id = self.validate_task_trace_id(task_trace_id)
        return TaskTraceContext(
            task_trace_id=valid_id or self.generate_task_trace_id(task_type),
            task_type=task_type,
            request_id=request_id or self.default_request_id,
            parent_request_id=request_id or self.default_request_id,
            actor_user_id=actor_user_id,
            client_type=client_type,
            resource_type=resource_type,
            resource_id=resource_id,
        )

    @staticmethod
    def serialize_async_context(context: TaskTraceContext) -> dict[str, str]:
        payload = {
            "task_trace_id": context.task_trace_id,
            "task_type": context.task_type,
        }
        if context.parent_request_id:
            payload["parent_request_id"] = context.parent_request_id
        if context.actor_user_id:
            payload["actor_user_id"] = context.actor_user_id
        if context.client_type:
            payload["client_type"] = context.client_type
        if context.resource_type:
            payload["resource_type"] = context.resource_type
        if context.resource_id:
            payload["resource_id"] = context.resource_id
        return payload

    def record_context_span(
        self,
        context: TaskTraceContext,
        *,
        span_name: str,
        status: str = "success",
        sequence: int = 0,
        started_at: str | None = None,
        ended_at: str | None = None,
        duration_ms: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        error_code: str | None = None,
        summary: str | None = None,
        metadata: dict[str, Any] | None = None,
        commit: bool = True,
    ) -> None:
        self.record_span(
            task_trace_id=context.task_trace_id,
            task_type=context.task_type,
            span_name=span_name,
            status=status,
            sequence=sequence,
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            request_id=context.request_id,
            parent_request_id=context.parent_request_id,
            actor_user_id=context.actor_user_id,
            client_type=context.client_type,
            resource_type=resource_type or context.resource_type,
            resource_id=resource_id or context.resource_id,
            error_code=error_code,
            summary=summary,
            metadata=metadata,
            commit=commit,
        )

    def record_context_span_safe(
        self,
        context: TaskTraceContext,
        *,
        span_name: str,
        status: str = "success",
        sequence: int = 0,
        started_at: str | None = None,
        ended_at: str | None = None,
        duration_ms: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        error_code: str | None = None,
        summary: str | None = None,
        metadata: dict[str, Any] | None = None,
        commit: bool = True,
    ) -> bool:
        try:
            self.record_context_span(
                context,
                span_name=span_name,
                status=status,
                sequence=sequence,
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
                resource_type=resource_type,
                resource_id=resource_id,
                error_code=error_code,
                summary=summary,
                metadata=metadata,
                commit=commit,
            )
            return True
        except Exception:
            return False

    def record_span(
        self,
        *,
        task_trace_id: str,
        task_type: str,
        span_name: str,
        status: str = "success",
        sequence: int = 0,
        started_at: str | None = None,
        ended_at: str | None = None,
        duration_ms: int | None = None,
        request_id: str | None = None,
        parent_request_id: str | None = None,
        actor_user_id: str | None = None,
        client_type: str | None = "web_admin",
        resource_type: str | None = None,
        resource_id: str | None = None,
        error_code: str | None = None,
        summary: str | None = None,
        metadata: dict[str, Any] | None = None,
        commit: bool = True,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        span_started_at = started_at or now
        span_ended_at = ended_at or span_started_at
        safe_metadata = safe_task_metadata(metadata or {})
        effective_request_id = request_id or self.default_request_id
        effective_parent_request_id = parent_request_id or effective_request_id
        self._repo.insert_span(
            task_trace_id=task_trace_id,
            task_type=task_type,
            span_name=span_name,
            status=status,
            started_at=span_started_at,
            ended_at=span_ended_at,
            duration_ms=duration_ms,
            sequence=sequence,
            request_id=effective_request_id,
            actor_user_id=actor_user_id,
            client_type=client_type,
            resource_type=resource_type,
            resource_id=resource_id,
            error_code=error_code,
            summary=truncate_text(summary or span_name, 255) or span_name,
            metadata=safe_json_dumps(safe_metadata),
        )
        self.refresh_trace(
            task_trace_id=task_trace_id,
            task_type=task_type,
            actor_user_id=actor_user_id,
            client_type=client_type,
            resource_type=resource_type,
            resource_id=resource_id,
            parent_request_id=effective_parent_request_id,
            metadata=safe_metadata,
        )
        if commit:
            self._repo._db.commit()

    def refresh_trace(
        self,
        *,
        task_trace_id: str,
        task_type: str,
        actor_user_id: str | None,
        client_type: str | None,
        resource_type: str | None,
        resource_id: str | None,
        parent_request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        spans = self._repo.list_spans(task_trace_id)
        if not spans:
            return
        existing = self._repo.get_trace(task_trace_id)
        effective_parent_request_id = (
            parent_request_id
            or self.default_request_id
            or (existing.parent_request_id if existing else None)
            or next((span.request_id for span in spans if span.request_id), None)
        )
        started_at = min(span.started_at for span in spans)
        ended_at = max((span.ended_at or span.started_at) for span in spans)
        duration_ms = sum(span.duration_ms or 0 for span in spans)
        failed = next((span for span in spans if span.status in {"failed", "timeout", "cancelled"}), None)
        slowest = max(spans, key=lambda span: span.duration_ms or 0)
        terminal = spans[-1]
        status = failed.status if failed else terminal.status
        self._repo.upsert_trace(
            task_trace_id=task_trace_id,
            task_type=task_type,
            status=status,
            actor_user_id=actor_user_id,
            client_type=client_type,
            parent_request_id=effective_parent_request_id,
            resource_type=resource_type,
            resource_id=resource_id,
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            slowest_span_name=slowest.span_name,
            error_code=failed.error_code if failed else terminal.error_code,
            summary=build_task_summary(task_type, status, duration_ms, slowest.span_name),
            metadata=safe_json_dumps(metadata or {}),
        )

    def get_timeline(self, task_trace_id: str | None) -> TaskTraceTimeline | None:
        valid_id = self.validate_task_trace_id(task_trace_id)
        if valid_id is None:
            return None
        trace = self._repo.get_trace(valid_id)
        spans = self._repo.list_spans(valid_id)
        if trace is None and not spans:
            return None
        return TaskTraceTimeline(trace=trace, spans=spans)

    def list_timelines_by_parent_request_id(self, request_id: str | None) -> list[TaskTraceTimeline]:
        traces = self._repo.list_traces_by_parent_request_id(request_id)
        return [
            TaskTraceTimeline(trace=trace, spans=self._repo.list_spans(trace.task_trace_id))
            for trace in traces
        ]


def elapsed_ms(started_at: float) -> int:
    return max(0, int((perf_counter() - started_at) * 1000))


def build_task_summary(task_type: str, status: str, duration_ms: int | None, slowest_span: str | None) -> str:
    duration_text = f"{duration_ms} ms" if duration_ms is not None else "N/A"
    slowest_text = slowest_span or "N/A"
    return f"{task_type} · {status} · {duration_text} · slowest={slowest_text}"


def safe_task_metadata(value: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, item in value.items():
        normalized = str(key).lower()
        if normalized in SENSITIVE_KEYS:
            sanitized[key] = "******"
            continue
        if isinstance(item, dict):
            sanitized[key] = safe_task_metadata(item)
        elif isinstance(item, list):
            sanitized[key] = [
                safe_task_metadata(element) if isinstance(element, dict) else _safe_scalar(element)
                for element in item[:20]
            ]
        else:
            sanitized[key] = _safe_scalar(item)
    return sanitized


def _safe_scalar(value: Any) -> Any:
    if isinstance(value, str):
        if _looks_like_internal_path(value):
            return "******"
        return truncate_text(value, 300)
    return value


def _looks_like_internal_path(value: str) -> bool:
    return value.startswith(("/Users/", "/var/", "/private/", "/tmp/")) or ":/" in value


def safe_json_dumps(value: dict[str, Any], *, pretty: bool = False) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2 if pretty else None, sort_keys=pretty, default=str)
    return truncate_text(text, 4000) or "{}"


def truncate_text(value: str | None, limit: int) -> str | None:
    if value is None:
        return None
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."
