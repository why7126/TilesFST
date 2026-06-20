"""Tile data access layer."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TileRecord:
    id: int
    name: str
    sku_code: str
    category_id: int | None
    color_family: str | None
    size: str | None
    remark: str | None
    status: str
    created_at: str | None
    updated_at: str | None

    @property
    def model(self) -> str:
        return self.sku_code


class TileRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_record(self, row: dict) -> TileRecord:
        return TileRecord(
            id=row["id"],
            name=row["name"],
            sku_code=row["sku_code"],
            category_id=row["category_id"],
            color_family=row.get("color_family"),
            size=row["size"],
            remark=row.get("remark"),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def get_by_id(self, tile_id: int) -> TileRecord | None:
        row = (
            self._db.execute(text("SELECT * FROM tiles WHERE id = :id"), {"id": tile_id})
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def list_published(
        self, *, page: int = 1, page_size: int = 20, keyword: str | None = None
    ) -> tuple[list[TileRecord], int]:
        offset = (page - 1) * page_size
        params: dict = {"limit": page_size, "offset": offset}
        where = "WHERE status = 'PUBLISHED'"
        if keyword:
            where += " AND (name LIKE :kw OR sku_code LIKE :kw)"
            params["kw"] = f"%{keyword}%"

        rows = (
            self._db.execute(
                text(f"SELECT * FROM tiles {where} ORDER BY id DESC LIMIT :limit OFFSET :offset"),
                params,
            )
            .mappings()
            .all()
        )
        total_row = (
            self._db.execute(text(f"SELECT COUNT(*) AS cnt FROM tiles {where}"), params)
            .mappings()
            .first()
        )
        total = int(total_row["cnt"]) if total_row else 0
        return [self._to_record(dict(r)) for r in rows], total
