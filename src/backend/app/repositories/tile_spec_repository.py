"""Tile spec persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TileSpecRecord:
    id: int
    width_mm: int
    length_mm: int
    thickness_mm: float | None
    unit: str
    display_name: str
    sort_order: int
    status: str
    sku_count: int
    remark: str | None
    created_at: str
    updated_at: str


@dataclass
class TileSpecListResult:
    items: list[TileSpecRecord]
    total: int
    summary: dict[str, int]


def build_display_name(width_mm: int, length_mm: int, unit: str = "mm") -> str:
    return f"{width_mm}×{length_mm}{unit}"


class TileSpecRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    @staticmethod
    def _to_record(row: dict[str, Any]) -> TileSpecRecord:
        thickness = row.get("thickness_mm")
        return TileSpecRecord(
            id=int(row["id"]),
            width_mm=int(row["width_mm"]),
            length_mm=int(row["length_mm"]),
            thickness_mm=float(thickness) if thickness is not None else None,
            unit=row["unit"],
            display_name=row["display_name"],
            sort_order=int(row["sort_order"]),
            status=row["status"],
            sku_count=int(row["sku_count"]),
            remark=row.get("remark"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _summary(self) -> dict[str, int]:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) AS total,
                      SUM(CASE WHEN status = 'ENABLED' THEN 1 ELSE 0 END) AS enabled_count,
                      SUM(CASE WHEN status = 'DISABLED' THEN 1 ELSE 0 END) AS disabled_count,
                      SUM(CASE WHEN sku_count = 0 THEN 1 ELSE 0 END) AS unlinked_sku_count
                    FROM tile_specs
                    """
                )
            )
            .mappings()
            .one()
        )
        return {
            "total": int(row["total"] or 0),
            "enabled_count": int(row["enabled_count"] or 0),
            "disabled_count": int(row["disabled_count"] or 0),
            "unlinked_sku_count": int(row["unlinked_sku_count"] or 0),
        }

    def list_specs(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
    ) -> TileSpecListResult:
        conditions = ["1=1"]
        params: dict[str, Any] = {}

        if keyword:
            conditions.append(
                "(display_name LIKE :keyword OR CAST(width_mm AS TEXT) LIKE :keyword "
                "OR CAST(length_mm AS TEXT) LIKE :keyword OR remark LIKE :keyword)"
            )
            params["keyword"] = f"%{keyword}%"
        if status:
            conditions.append("status = :status")
            params["status"] = status

        where_sql = " AND ".join(conditions)
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM tile_specs WHERE {where_sql}"),
                params,
            ).scalar_one()
        )

        offset = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM tile_specs
                    WHERE {where_sql}
                    ORDER BY sort_order ASC, updated_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {**params, "limit": page_size, "offset": offset},
            )
            .mappings()
            .all()
        )
        return TileSpecListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=total,
            summary=self._summary(),
        )

    def get_by_id(self, spec_id: int) -> TileSpecRecord | None:
        row = (
            self._db.execute(text("SELECT * FROM tile_specs WHERE id = :id"), {"id": spec_id})
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_dimensions(
        self,
        *,
        width_mm: int,
        length_mm: int,
        unit: str = "mm",
        exclude_id: int | None = None,
    ) -> TileSpecRecord | None:
        sql = (
            "SELECT * FROM tile_specs WHERE width_mm = :width_mm "
            "AND length_mm = :length_mm AND unit = :unit"
        )
        params: dict[str, Any] = {
            "width_mm": width_mm,
            "length_mm": length_mm,
            "unit": unit,
        }
        if exclude_id is not None:
            sql += " AND id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def create(
        self,
        *,
        width_mm: int,
        length_mm: int,
        thickness_mm: float | None,
        sort_order: int,
        remark: str | None,
    ) -> TileSpecRecord:
        now = self._now()
        display_name = build_display_name(width_mm, length_mm)
        result = self._db.execute(
            text(
                """
                INSERT INTO tile_specs (
                  width_mm, length_mm, thickness_mm, unit, display_name,
                  sort_order, status, sku_count, remark, created_at, updated_at
                ) VALUES (
                  :width_mm, :length_mm, :thickness_mm, 'mm', :display_name,
                  :sort_order, 'ENABLED', 0, :remark, :created_at, :updated_at
                )
                """
            ),
            {
                "width_mm": width_mm,
                "length_mm": length_mm,
                "thickness_mm": thickness_mm,
                "display_name": display_name,
                "sort_order": sort_order,
                "remark": remark,
                "created_at": now,
                "updated_at": now,
            },
        )
        spec_id = int(result.lastrowid)
        self._db.commit()
        record = self.get_by_id(spec_id)
        assert record is not None
        return record

    def update(
        self,
        spec_id: int,
        *,
        width_mm: int,
        length_mm: int,
        thickness_mm: float | None,
        sort_order: int,
        remark: str | None,
    ) -> TileSpecRecord | None:
        now = self._now()
        display_name = build_display_name(width_mm, length_mm)
        self._db.execute(
            text(
                """
                UPDATE tile_specs SET
                  width_mm = :width_mm,
                  length_mm = :length_mm,
                  thickness_mm = :thickness_mm,
                  display_name = :display_name,
                  sort_order = :sort_order,
                  remark = :remark,
                  updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": spec_id,
                "width_mm": width_mm,
                "length_mm": length_mm,
                "thickness_mm": thickness_mm,
                "display_name": display_name,
                "sort_order": sort_order,
                "remark": remark,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(spec_id)

    def update_status(self, spec_id: int, status: str) -> TileSpecRecord | None:
        now = self._now()
        self._db.execute(
            text(
                "UPDATE tile_specs SET status = :status, updated_at = :updated_at WHERE id = :id"
            ),
            {"id": spec_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(spec_id)

    def delete(self, spec_id: int) -> None:
        self._db.execute(text("DELETE FROM tile_specs WHERE id = :id"), {"id": spec_id})
        self._db.commit()

    def increment_sku_count(self, spec_id: int) -> None:
        self._db.execute(
            text(
                "UPDATE tile_specs SET sku_count = sku_count + 1, updated_at = :updated_at "
                "WHERE id = :id"
            ),
            {"id": spec_id, "updated_at": self._now()},
        )

    def decrement_sku_count(self, spec_id: int) -> None:
        self._db.execute(
            text(
                """
                UPDATE tile_specs SET
                  sku_count = CASE WHEN sku_count > 0 THEN sku_count - 1 ELSE 0 END,
                  updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {"id": spec_id, "updated_at": self._now()},
        )
