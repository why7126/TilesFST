"""Brand persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class BrandRecord:
    id: int
    name: str
    sort_order: int
    short_name: str | None
    english_name: str | None
    logo_object_key: str | None
    description: str | None
    status: str
    sku_count: int
    created_at: str
    updated_at: str


@dataclass
class BrandListResult:
    items: list[BrandRecord]
    total: int
    summary: dict[str, int]


class BrandRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _to_record(row: dict[str, Any]) -> BrandRecord:
        return BrandRecord(
            id=int(row["id"]),
            name=row["name"],
            sort_order=int(row["sort_order"]),
            short_name=row.get("short_name"),
            english_name=row.get("english_name"),
            logo_object_key=row.get("logo_object_key"),
            description=row.get("description"),
            status=row["status"],
            sku_count=int(row["sku_count"]),
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
                    FROM brands
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

    def list_brands(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
    ) -> BrandListResult:
        conditions = ["1=1"]
        params: dict[str, Any] = {}

        if keyword:
            conditions.append(
                "(name LIKE :keyword OR short_name LIKE :keyword OR english_name LIKE :keyword)"
            )
            params["keyword"] = f"%{keyword}%"
        if status:
            conditions.append("status = :status")
            params["status"] = status

        where_sql = " AND ".join(conditions)
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM brands WHERE {where_sql}"),
                params,
            ).scalar_one()
        )

        offset = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM brands
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
        return BrandListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=total,
            summary=self._summary(),
        )

    def get_by_id(self, brand_id: int) -> BrandRecord | None:
        row = (
            self._db.execute(text("SELECT * FROM brands WHERE id = :id"), {"id": brand_id})
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_name(self, name: str, exclude_id: int | None = None) -> BrandRecord | None:
        sql = "SELECT * FROM brands WHERE name = :name"
        params: dict[str, Any] = {"name": name}
        if exclude_id is not None:
            sql += " AND id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def create(
        self,
        *,
        name: str,
        sort_order: int,
        short_name: str | None,
        english_name: str | None,
        logo_object_key: str | None,
        description: str | None,
        status: str = "ENABLED",
    ) -> BrandRecord:
        now = datetime.now(UTC).isoformat()
        cursor = self._db.execute(
            text(
                """
                INSERT INTO brands (
                  name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES (
                  :name, :sort_order, :short_name, :english_name, :logo_object_key,
                  :description, :status, 0, :created_at, :updated_at
                )
                """
            ),
            {
                "name": name,
                "sort_order": sort_order,
                "short_name": short_name,
                "english_name": english_name,
                "logo_object_key": logo_object_key,
                "description": description,
                "status": status,
                "created_at": now,
                "updated_at": now,
            },
        )
        self._db.commit()
        brand_id = int(cursor.lastrowid)
        record = self.get_by_id(brand_id)
        assert record is not None
        return record

    def update(
        self,
        brand_id: int,
        *,
        name: str,
        sort_order: int,
        short_name: str | None,
        english_name: str | None,
        logo_object_key: str | None,
        description: str | None,
    ) -> BrandRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE brands SET
                  name = :name,
                  sort_order = :sort_order,
                  short_name = :short_name,
                  english_name = :english_name,
                  logo_object_key = :logo_object_key,
                  description = :description,
                  updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": brand_id,
                "name": name,
                "sort_order": sort_order,
                "short_name": short_name,
                "english_name": english_name,
                "logo_object_key": logo_object_key,
                "description": description,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(brand_id)

    def update_status(self, brand_id: int, status: str) -> BrandRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text("UPDATE brands SET status = :status, updated_at = :updated_at WHERE id = :id"),
            {"id": brand_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(brand_id)

    def delete(self, brand_id: int) -> bool:
        result = self._db.execute(text("DELETE FROM brands WHERE id = :id"), {"id": brand_id})
        self._db.commit()
        return result.rowcount > 0
