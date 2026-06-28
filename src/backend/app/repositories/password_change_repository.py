"""Password change attempt persistence for rate limiting."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class PasswordChangeAttemptRecord:
    id: str
    user_id: str
    success: bool
    created_at: str


class PasswordChangeRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert_attempt(self, *, user_id: str, success: bool) -> PasswordChangeAttemptRecord:
        now = datetime.now(UTC).isoformat()
        attempt_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO password_change_attempts (id, user_id, success, created_at)
                VALUES (:id, :user_id, :success, :created_at)
                """
            ),
            {
                "id": attempt_id,
                "user_id": user_id,
                "success": 1 if success else 0,
                "created_at": now,
            },
        )
        self._db.commit()
        return PasswordChangeAttemptRecord(
            id=attempt_id,
            user_id=user_id,
            success=success,
            created_at=now,
        )

    def count_recent_failures(self, user_id: str, *, minutes: int = 15) -> int:
        cutoff = (datetime.now(UTC) - timedelta(minutes=minutes)).isoformat()
        count = self._db.execute(
            text(
                """
                SELECT COUNT(*) FROM password_change_attempts
                WHERE user_id = :user_id
                  AND success = 0
                  AND created_at >= :cutoff
                """
            ),
            {"user_id": user_id, "cutoff": cutoff},
        ).scalar_one()
        return int(count)

    def count_recent_successes(self, user_id: str, *, hours: int = 24) -> int:
        cutoff = (datetime.now(UTC) - timedelta(hours=hours)).isoformat()
        count = self._db.execute(
            text(
                """
                SELECT COUNT(*) FROM password_change_attempts
                WHERE user_id = :user_id
                  AND success = 1
                  AND created_at >= :cutoff
                """
            ),
            {"user_id": user_id, "cutoff": cutoff},
        ).scalar_one()
        return int(count)
