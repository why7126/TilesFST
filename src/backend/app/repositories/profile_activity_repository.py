"""Profile activity audit persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class ProfileActivityRecord:
    id: str
    user_id: str
    action_type: str
    summary: str
    metadata: str | None
    created_at: str


class ProfileActivityRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert(
        self,
        *,
        user_id: str,
        action_type: str,
        summary: str,
        metadata: str | None = None,
    ) -> ProfileActivityRecord:
        now = datetime.now(UTC).isoformat()
        activity_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO profile_activity_logs (
                    id, user_id, action_type, summary, metadata, created_at
                ) VALUES (
                    :id, :user_id, :action_type, :summary, :metadata, :created_at
                )
                """
            ),
            {
                "id": activity_id,
                "user_id": user_id,
                "action_type": action_type,
                "summary": summary,
                "metadata": metadata,
                "created_at": now,
            },
        )
        self._db.commit()
        return ProfileActivityRecord(
            id=activity_id,
            user_id=user_id,
            action_type=action_type,
            summary=summary,
            metadata=metadata,
            created_at=now,
        )

    def list_by_user(self, user_id: str, *, limit: int = 5) -> list[ProfileActivityRecord]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT id, user_id, action_type, summary, metadata, created_at
                    FROM profile_activity_logs
                    WHERE user_id = :user_id
                    ORDER BY created_at DESC
                    LIMIT :limit
                    """
                ),
                {"user_id": user_id, "limit": limit},
            )
            .mappings()
            .all()
        )
        return [self._to_record(dict(row)) for row in rows]

    @staticmethod
    def _to_record(row: dict[str, Any]) -> ProfileActivityRecord:
        return ProfileActivityRecord(
            id=row["id"],
            user_id=row["user_id"],
            action_type=row["action_type"],
            summary=row["summary"],
            metadata=row.get("metadata"),
            created_at=row["created_at"],
        )
