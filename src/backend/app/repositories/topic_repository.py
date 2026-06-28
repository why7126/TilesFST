"""Topic persistence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TopicRecord:
    id: int
    code: str
    title: str
    status: str
    cover_object_key: str | None
    created_at: str
    updated_at: str


class TopicRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _to_record(row: dict[str, Any]) -> TopicRecord:
        return TopicRecord(
            id=int(row["id"]),
            code=row["code"],
            title=row["title"],
            status=row["status"],
            cover_object_key=row.get("cover_object_key"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_topics(
        self,
        *,
        keyword: str | None,
        status: str | None = "ENABLED",
    ) -> list[TopicRecord]:
        conditions = ["1=1"]
        params: dict[str, Any] = {}
        if status:
            conditions.append("status = :status")
            params["status"] = status
        if keyword:
            conditions.append("(title LIKE :keyword OR code LIKE :keyword)")
            params["keyword"] = f"%{keyword}%"

        where_sql = " AND ".join(conditions)
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM topics
                    WHERE {where_sql}
                    ORDER BY title ASC, id ASC
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        return [self._to_record(dict(row)) for row in rows]

    def get_by_id(self, topic_id: int) -> TopicRecord | None:
        row = (
            self._db.execute(text("SELECT * FROM topics WHERE id = :id"), {"id": topic_id})
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def is_enabled(self, topic_id: int) -> bool:
        row = self._db.execute(
            text("SELECT 1 FROM topics WHERE id = :id AND status = 'ENABLED'"),
            {"id": topic_id},
        ).first()
        return row is not None
