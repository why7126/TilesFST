"""Unified audit log persistence (system settings, profile, etc.)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class AuditLogRecord:
    id: str
    actor_user_id: str | None
    domain: str
    action_type: str
    summary: str
    metadata: str | None
    created_at: str
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
    ) -> AuditLogRecord:
        now = datetime.now(UTC).isoformat()
        log_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO audit_logs (
                  id, actor_user_id, domain, action_type, summary, metadata, created_at
                ) VALUES (
                  :id, :actor_user_id, :domain, :action_type, :summary, :metadata, :created_at
                )
                """
            ),
            {
                "id": log_id,
                "actor_user_id": actor_user_id,
                "domain": domain,
                "action_type": action_type,
                "summary": summary,
                "metadata": metadata,
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
            metadata=metadata,
            created_at=now,
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
            actor_display_name=row.get("actor_display_name"),
        )
