"""Unified audit log persistence (system settings, profile, etc.)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.log_service import safe_json_dumps, sanitize_metadata
from app.services.task_trace_service import TaskTraceService


@dataclass
class AuditLogRecord:
    id: str
    actor_user_id: str | None
    domain: str
    action_type: str
    summary: str
    metadata: str | None
    created_at: str
    task_trace_id: str | None = None
    task_type: str | None = None
    actor_display_name: str | None = None


class AuditLogRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert(
        self,
        *,
        actor_user_id: str | None,
        domain: str,
        action_type: str,
        summary: str,
        metadata: str | None = None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> AuditLogRecord:
        now = datetime.now(UTC).isoformat()
        log_id = str(uuid4())
        safe_task_trace_id = TaskTraceService.validate_task_trace_id(task_trace_id)
        safe_task_type = _normalize_task_type(task_type) if safe_task_trace_id else None
        safe_metadata = _sanitize_metadata_json(metadata)
        self._db.execute(
            text(
                """
                INSERT INTO audit_logs (
                  id, actor_user_id, domain, action_type, summary,
                  task_trace_id, task_type, metadata, created_at
                ) VALUES (
                  :id, :actor_user_id, :domain, :action_type, :summary,
                  :task_trace_id, :task_type, :metadata, :created_at
                )
                """
            ),
            {
                "id": log_id,
                "actor_user_id": actor_user_id,
                "domain": domain,
                "action_type": action_type,
                "summary": summary,
                "task_trace_id": safe_task_trace_id,
                "task_type": safe_task_type,
                "metadata": safe_metadata,
                "created_at": now,
            },
        )
        self._db.commit()
        return AuditLogRecord(
            id=log_id,
            actor_user_id=actor_user_id,
            domain=domain,
            action_type=action_type,
            summary=summary,
            metadata=safe_metadata,
            created_at=now,
            task_trace_id=safe_task_trace_id,
            task_type=safe_task_type,
        )

    def list_recent_by_domain(
        self,
        domain: str,
        *,
        limit: int = 10,
    ) -> list[AuditLogRecord]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT
                      a.id,
                      a.actor_user_id,
                      a.domain,
                      a.action_type,
                      a.summary,
                      a.task_trace_id,
                      a.task_type,
                      a.metadata,
                      a.created_at,
                      u.display_name AS actor_display_name
                    FROM audit_logs a
                    LEFT JOIN users u ON u.id = a.actor_user_id
                    WHERE a.domain = :domain
                    ORDER BY a.created_at DESC
                    LIMIT :limit
                    """
                ),
                {"domain": domain, "limit": limit},
            )
            .mappings()
            .all()
        )
        return [self._to_record(dict(row)) for row in rows]

    @staticmethod
    def _to_record(row: dict[str, Any]) -> AuditLogRecord:
        return AuditLogRecord(
            id=row["id"],
            actor_user_id=row.get("actor_user_id"),
            domain=row["domain"],
            action_type=row["action_type"],
            summary=row["summary"],
            metadata=row.get("metadata"),
            created_at=row["created_at"],
            task_trace_id=row.get("task_trace_id"),
            task_type=row.get("task_type"),
            actor_display_name=row.get("actor_display_name"),
        )


def _normalize_task_type(value: str | None) -> str | None:
    if not value:
        return None
    stripped = value.strip()
    return stripped[:64] or None


def _sanitize_metadata_json(value: str | None) -> str | None:
    if not value:
        return value
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return value
    if not isinstance(parsed, dict):
        return value
    return safe_json_dumps(sanitize_metadata(parsed))
