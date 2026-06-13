"""Tile data access layer."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TileRecord:
    id: int
    name: str
    model: str
    category_id: int | None
    color: str | None
    size: str | None
    description: str | None
    status: str
    created_at: str | None
    updated_at: str | None


class TileRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_record(self, row: dict) -> TileRecord:
        return TileRecord(
            id=row["id"],
            name=row["name"],
            model=row["model"],
            category_id=row["category_id"],
            color=row["color"],
            size=row["size"],
            description=row["description"],
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
        where = "WHERE status = 'published'"
        if keyword:
            where += " AND (name LIKE :kw OR model LIKE :kw)"
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
