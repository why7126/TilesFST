"""SQLite persistence for system_settings KV store."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class SystemSettingRecord:
    key: str
    value: str
    updated_at: str
    updated_by: str | None


class SystemSettingsRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, key: str) -> SystemSettingRecord | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT key, value, updated_at, updated_by
                    FROM system_settings
                    WHERE key = :key
                    """
                ),
                {"key": key},
            )
            .mappings()
            .first()
        )
        if row is None:
            return None
        return self._to_record(dict(row))

    def set(self, key: str, value: str, updated_by: str | None) -> SystemSettingRecord:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                INSERT INTO system_settings (key, value, updated_at, updated_by)
                VALUES (:key, :value, :updated_at, :updated_by)
                ON CONFLICT(key) DO UPDATE SET
                  value = excluded.value,
                  updated_at = excluded.updated_at,
                  updated_by = excluded.updated_by
                """
            ),
            {"key": key, "value": value, "updated_at": now, "updated_by": updated_by},
        )
        self._db.commit()
        return SystemSettingRecord(key=key, value=value, updated_at=now, updated_by=updated_by)

    def delete(self, key: str) -> None:
        self._db.execute(text("DELETE FROM system_settings WHERE key = :key"), {"key": key})
        self._db.commit()

    def delete_by_prefix(self, prefix: str) -> int:
        result = self._db.execute(
            text("DELETE FROM system_settings WHERE key LIKE :pattern"),
            {"pattern": f"{prefix}%"},
        )
        self._db.commit()
        return int(result.rowcount or 0)

    def list_by_prefix(self, prefix: str) -> list[SystemSettingRecord]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT key, value, updated_at, updated_by
                    FROM system_settings
                    WHERE key LIKE :pattern
                    ORDER BY key
                    """
                ),
                {"pattern": f"{prefix}%"},
            )
            .mappings()
            .all()
        )
        return [self._to_record(dict(row)) for row in rows]

    @staticmethod
    def _to_record(row: dict[str, Any]) -> SystemSettingRecord:
        return SystemSettingRecord(
            key=row["key"],
            value=row["value"],
            updated_at=row["updated_at"],
            updated_by=row.get("updated_by"),
        )
