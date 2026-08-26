"""Task trace persistence and timeline queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class TaskTraceRecord:
    task_trace_id: str
    task_type: str
    status: str
    parent_request_id: str | None
    behavior_trace_id: str | None
    actor_user_id: str | None
    client_type: str | None
    resource_type: str | None
    resource_id: str | None
    started_at: str
    ended_at: str | None
    duration_ms: int | None
    slowest_span_name: str | None
    error_code: str | None
    summary: str
    metadata: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class TaskSpanRecord:
    id: str
    task_trace_id: str
    task_type: str
    span_name: str
    status: str
    started_at: str
    ended_at: str | None
    duration_ms: int | None
    sequence: int
    request_id: str | None
    behavior_trace_id: str | None
    actor_user_id: str | None
    client_type: str | None
    resource_type: str | None
    resource_id: str | None
    error_code: str | None
    summary: str
    metadata: str | None
    created_at: str


class TaskTraceRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def upsert_trace(
        self,
        *,
        task_trace_id: str,
        task_type: str,
        status: str,
        actor_user_id: str | None,
        client_type: str | None,
        parent_request_id: str | None,
        behavior_trace_id: str | None,
        resource_type: str | None,
        resource_id: str | None,
        started_at: str,
        ended_at: str | None,
        duration_ms: int | None,
        slowest_span_name: str | None,
        error_code: str | None,
        summary: str,
        metadata: str | None,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        existing = self.get_trace(task_trace_id)
        if existing is None:
            self._db.execute(
                text(
                    """
                    INSERT INTO task_traces (
                      id, task_trace_id, task_type, status, actor_user_id, client_type,
                      parent_request_id, behavior_trace_id, resource_type, resource_id, started_at, ended_at, duration_ms,
                      slowest_span_name, error_code, summary, metadata, created_at, updated_at
                    ) VALUES (
                      :id, :task_trace_id, :task_type, :status, :actor_user_id, :client_type,
                      :parent_request_id, :behavior_trace_id, :resource_type, :resource_id, :started_at, :ended_at, :duration_ms,
                      :slowest_span_name, :error_code, :summary, :metadata, :created_at, :updated_at
                    )
                    """
                ),
                {
                    "id": str(uuid4()),
                    "task_trace_id": task_trace_id,
                    "task_type": task_type,
                    "status": status,
                    "actor_user_id": actor_user_id,
                    "client_type": client_type,
                    "parent_request_id": parent_request_id,
                    "behavior_trace_id": behavior_trace_id,
                    "resource_type": resource_type,
                    "resource_id": resource_id,
                    "started_at": started_at,
                    "ended_at": ended_at,
                    "duration_ms": duration_ms,
                    "slowest_span_name": slowest_span_name,
                    "error_code": error_code,
                    "summary": summary,
                    "metadata": metadata,
                    "created_at": now,
                    "updated_at": now,
                },
            )
            return

        self._db.execute(
            text(
                """
                UPDATE task_traces
                SET task_type = :task_type,
                    status = :status,
                    actor_user_id = COALESCE(:actor_user_id, actor_user_id),
                    client_type = COALESCE(:client_type, client_type),
                    parent_request_id = COALESCE(:parent_request_id, parent_request_id),
                    behavior_trace_id = COALESCE(:behavior_trace_id, behavior_trace_id),
                    resource_type = COALESCE(:resource_type, resource_type),
                    resource_id = COALESCE(:resource_id, resource_id),
                    started_at = :started_at,
                    ended_at = :ended_at,
                    duration_ms = :duration_ms,
                    slowest_span_name = :slowest_span_name,
                    error_code = :error_code,
                    summary = :summary,
                    metadata = :metadata,
                    updated_at = :updated_at
                WHERE task_trace_id = :task_trace_id
                """
            ),
            {
                "task_trace_id": task_trace_id,
                "task_type": task_type,
                "status": status,
                "actor_user_id": actor_user_id,
                "client_type": client_type,
                "parent_request_id": parent_request_id,
                "behavior_trace_id": behavior_trace_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "started_at": started_at,
                "ended_at": ended_at,
                "duration_ms": duration_ms,
                "slowest_span_name": slowest_span_name,
                "error_code": error_code,
                "summary": summary,
                "metadata": metadata,
                "updated_at": now,
            },
        )

    def insert_span(
        self,
        *,
        task_trace_id: str,
        task_type: str,
        span_name: str,
        status: str,
        started_at: str,
        ended_at: str | None,
        duration_ms: int | None,
        sequence: int,
        request_id: str | None,
        behavior_trace_id: str | None,
        actor_user_id: str | None,
        client_type: str | None,
        resource_type: str | None,
        resource_id: str | None,
        error_code: str | None,
        summary: str,
        metadata: str | None,
        parent_request_id: str | None = None,
    ) -> str:
        span_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO task_trace_spans (
                  id, task_trace_id, task_type, span_name, status, started_at, ended_at,
                  duration_ms, sequence, request_id, actor_user_id, client_type,
                  behavior_trace_id, resource_type, resource_id, error_code, summary, metadata, created_at
                ) VALUES (
                  :id, :task_trace_id, :task_type, :span_name, :status, :started_at, :ended_at,
                  :duration_ms, :sequence, :request_id, :actor_user_id, :client_type,
                  :behavior_trace_id, :resource_type, :resource_id, :error_code, :summary, :metadata, :created_at
                )
                """
            ),
            {
                "id": span_id,
                "task_trace_id": task_trace_id,
                "task_type": task_type,
                "span_name": span_name,
                "status": status,
                "started_at": started_at,
                "ended_at": ended_at,
                "duration_ms": duration_ms,
                "sequence": sequence,
                "request_id": request_id,
                "behavior_trace_id": behavior_trace_id,
                "actor_user_id": actor_user_id,
                "client_type": client_type,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "error_code": error_code,
                "summary": summary,
                "metadata": metadata,
                "created_at": datetime.now(UTC).isoformat(),
            },
        )
        return span_id

    def get_trace(self, task_trace_id: str) -> TaskTraceRecord | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT *
                    FROM task_traces
                    WHERE task_trace_id = :task_trace_id
                    LIMIT 1
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .first()
        )
        return self._to_trace(dict(row)) if row else None

    def list_traces_by_parent_request_id(self, request_id: str | None) -> list[TaskTraceRecord]:
        if not request_id:
            return []
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT *
                    FROM task_traces
                    WHERE parent_request_id = :request_id
                    ORDER BY created_at DESC
                    LIMIT 20
                    """
                ),
                {"request_id": request_id},
            )
            .mappings()
            .all()
        )
        return [self._to_trace(dict(row)) for row in rows]

    def list_spans(self, task_trace_id: str) -> list[TaskSpanRecord]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT *
                    FROM task_trace_spans
                    WHERE task_trace_id = :task_trace_id
                    ORDER BY sequence ASC, started_at ASC, created_at ASC
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .all()
        )
        return [self._to_span(dict(row)) for row in rows]

    @staticmethod
    def _to_trace(row: dict[str, Any]) -> TaskTraceRecord:
        return TaskTraceRecord(
            task_trace_id=str(row["task_trace_id"]),
            task_type=str(row["task_type"]),
            status=str(row["status"]),
            parent_request_id=row.get("parent_request_id"),
            behavior_trace_id=row.get("behavior_trace_id"),
            actor_user_id=row.get("actor_user_id"),
            client_type=row.get("client_type"),
            resource_type=row.get("resource_type"),
            resource_id=row.get("resource_id"),
            started_at=str(row["started_at"]),
            ended_at=row.get("ended_at"),
            duration_ms=int(row["duration_ms"]) if row.get("duration_ms") is not None else None,
            slowest_span_name=row.get("slowest_span_name"),
            error_code=row.get("error_code"),
            summary=str(row["summary"]),
            metadata=row.get("metadata"),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )

    @staticmethod
    def _to_span(row: dict[str, Any]) -> TaskSpanRecord:
        return TaskSpanRecord(
            id=str(row["id"]),
            task_trace_id=str(row["task_trace_id"]),
            task_type=str(row["task_type"]),
            span_name=str(row["span_name"]),
            status=str(row["status"]),
            started_at=str(row["started_at"]),
            ended_at=row.get("ended_at"),
            duration_ms=int(row["duration_ms"]) if row.get("duration_ms") is not None else None,
            sequence=int(row["sequence"] or 0),
            request_id=row.get("request_id"),
            behavior_trace_id=row.get("behavior_trace_id"),
            actor_user_id=row.get("actor_user_id"),
            client_type=row.get("client_type"),
            resource_type=row.get("resource_type"),
            resource_id=row.get("resource_id"),
            error_code=row.get("error_code"),
            summary=str(row["summary"]),
            metadata=row.get("metadata"),
            created_at=str(row["created_at"]),
        )
