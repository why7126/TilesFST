"""Tile category persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TileCategoryRecord:
    id: int
    parent_id: int | None
    name: str
    code: str
    sort_order: int
    level: int
    description: str | None
    status: str
    sku_count: int
    path: str
    created_at: str
    updated_at: str


@dataclass
class TileCategoryListResult:
    items: list[TileCategoryRecord]
    total: int
    summary: dict[str, int]


class TileCategoryRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _to_record(row: dict[str, Any]) -> TileCategoryRecord:
        parent = row.get("parent_id")
        return TileCategoryRecord(
            id=int(row["id"]),
            parent_id=int(parent) if parent is not None else None,
            name=row["name"],
            code=row["code"],
            sort_order=int(row["sort_order"]),
            level=int(row["level"]),
            description=row.get("description"),
            status=row["status"],
            sku_count=int(row["sku_count"]),
            path=row["path"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_all(self) -> list[TileCategoryRecord]:
        rows = (
            self._db.execute(
                text("SELECT * FROM tile_categories ORDER BY sort_order ASC, id ASC")
            )
            .mappings()
            .all()
        )
        return [self._to_record(dict(row)) for row in rows]

    def _summary(self) -> dict[str, int]:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) AS total,
                      SUM(CASE WHEN status = 'ENABLED' THEN 1 ELSE 0 END) AS enabled_count,
                      SUM(sku_count) AS bound_sku_total
                    FROM tile_categories
                    """
                )
            )
            .mappings()
            .one()
        )
        return {
            "total": int(row["total"] or 0),
            "enabled_count": int(row["enabled_count"] or 0),
            "bound_sku_total": int(row["bound_sku_total"] or 0),
        }

    def _descendant_ids(self, root_id: int) -> list[int]:
        rows = self._db.execute(
            text(
                """
                WITH RECURSIVE descendants AS (
                  SELECT id FROM tile_categories WHERE id = :root_id
                  UNION ALL
                  SELECT c.id FROM tile_categories c
                  INNER JOIN descendants d ON c.parent_id = d.id
                )
                SELECT id FROM descendants
                """
            ),
            {"root_id": root_id},
        ).fetchall()
        return [int(row[0]) for row in rows]

    def list_categories(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
        level: int | None,
        parent_id: int | None,
    ) -> TileCategoryListResult:
        conditions = ["1=1"]
        params: dict[str, Any] = {}

        if keyword:
            conditions.append("(name LIKE :keyword OR code LIKE :keyword)")
            params["keyword"] = f"%{keyword}%"
        if status:
            conditions.append("status = :status")
            params["status"] = status
        if level is not None:
            conditions.append("level = :level")
            params["level"] = level
        if parent_id is not None:
            ids = self._descendant_ids(parent_id)
            if not ids:
                return TileCategoryListResult(items=[], total=0, summary=self._summary())
            placeholders = ", ".join(f":id{i}" for i in range(len(ids)))
            conditions.append(f"id IN ({placeholders})")
            for i, cat_id in enumerate(ids):
                params[f"id{i}"] = cat_id

        where_sql = " AND ".join(conditions)
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM tile_categories WHERE {where_sql}"),
                params,
            ).scalar_one()
        )

        offset = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM tile_categories
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
        return TileCategoryListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=total,
            summary=self._summary(),
        )

    def get_by_id(self, category_id: int) -> TileCategoryRecord | None:
        row = (
            self._db.execute(
                text("SELECT * FROM tile_categories WHERE id = :id"),
                {"id": category_id},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_code(self, code: str, exclude_id: int | None = None) -> TileCategoryRecord | None:
        sql = "SELECT * FROM tile_categories WHERE code = :code"
        params: dict[str, Any] = {"code": code}
        if exclude_id is not None:
            sql += " AND id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def has_children(self, category_id: int) -> bool:
        count = self._db.execute(
            text("SELECT COUNT(*) FROM tile_categories WHERE parent_id = :id"),
            {"id": category_id},
        ).scalar_one()
        return int(count) > 0

    def create(
        self,
        *,
        parent_id: int | None,
        name: str,
        code: str,
        sort_order: int,
        level: int,
        description: str | None,
        status: str,
        path: str,
    ) -> TileCategoryRecord:
        now = datetime.now(UTC).isoformat()
        cursor = self._db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES (
                  :parent_id, :name, :code, :sort_order, :level, :description,
                  :status, 0, :path, :created_at, :updated_at
                )
                """
            ),
            {
                "parent_id": parent_id,
                "name": name,
                "code": code,
                "sort_order": sort_order,
                "level": level,
                "description": description,
                "status": status,
                "path": path,
                "created_at": now,
                "updated_at": now,
            },
        )
        self._db.commit()
        record = self.get_by_id(int(cursor.lastrowid))
        assert record is not None
        return record

    def update(
        self,
        category_id: int,
        *,
        name: str,
        sort_order: int,
        description: str | None,
        path: str,
    ) -> TileCategoryRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE tile_categories SET
                  name = :name,
                  sort_order = :sort_order,
                  description = :description,
                  path = :path,
                  updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": category_id,
                "name": name,
                "sort_order": sort_order,
                "description": description,
                "path": path,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(category_id)

    def update_status(self, category_id: int, status: str) -> TileCategoryRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                "UPDATE tile_categories SET status = :status, updated_at = :updated_at WHERE id = :id"
            ),
            {"id": category_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(category_id)

    def delete(self, category_id: int) -> bool:
        result = self._db.execute(
            text("DELETE FROM tile_categories WHERE id = :id"),
            {"id": category_id},
        )
        self._db.commit()
        return result.rowcount > 0
