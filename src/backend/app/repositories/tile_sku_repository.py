"""Tile SKU admin data access layer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class TileSkuRecord:
    id: int
    name: str
    sku_code: str
    brand_id: int
    category_id: int
    spec_id: int | None
    size: str
    surface_finish: str
    color_family: str | None
    reference_price: float | None
    remark: str | None
    status: str
    created_at: str
    updated_at: str
    brand_name: str
    category_name: str
    main_image_url: str | None
    image_count: int
    video_count: int
    has_main_image: bool


@dataclass
class TileSkuImageRecord:
    id: int
    tile_id: int
    object_key: str
    url: str
    is_main: int
    sort_order: int


@dataclass
class TileSkuVideoRecord:
    id: int
    tile_id: int
    object_key: str
    file_name: str
    file_size_bytes: int | None
    duration_seconds: float | None
    sort_order: int


class TileSkuRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    @staticmethod
    def _material_completeness(has_main: bool, image_count: int, video_count: int) -> str:
        if image_count == 0:
            return "missing_images"
        if not has_main:
            return "missing_main_image"
        if video_count == 0:
            return "missing_videos"
        return "complete"

    def _list_base_sql(self) -> str:
        return """
            SELECT
              t.id, t.name, t.sku_code, t.brand_id, t.category_id, t.spec_id,
              t.size, t.surface_finish, t.color_family, t.reference_price,
              t.remark, t.status, t.created_at, t.updated_at,
              b.name AS brand_name,
              c.name AS category_name,
              (
                SELECT ti.url FROM tile_images ti
                WHERE ti.tile_id = t.id AND ti.is_main = 1
                ORDER BY ti.sort_order, ti.id LIMIT 1
              ) AS main_image_url,
              (SELECT COUNT(*) FROM tile_images ti WHERE ti.tile_id = t.id) AS image_count,
              (SELECT COUNT(*) FROM tile_videos tv WHERE tv.tile_id = t.id) AS video_count,
              (
                SELECT COUNT(*) FROM tile_images ti
                WHERE ti.tile_id = t.id AND ti.is_main = 1
              ) AS has_main_image
            FROM tiles t
            JOIN brands b ON b.id = t.brand_id
            JOIN tile_categories c ON c.id = t.category_id
        """

    def _to_record(self, row: dict) -> TileSkuRecord:
        image_count = int(row["image_count"] or 0)
        video_count = int(row["video_count"] or 0)
        has_main = int(row["has_main_image"] or 0) > 0
        return TileSkuRecord(
            id=int(row["id"]),
            name=row["name"],
            sku_code=row["sku_code"],
            brand_id=int(row["brand_id"]),
            category_id=int(row["category_id"]),
            spec_id=int(row["spec_id"]) if row.get("spec_id") is not None else None,
            size=row["size"],
            surface_finish=row["surface_finish"],
            color_family=row.get("color_family"),
            reference_price=row.get("reference_price"),
            remark=row.get("remark"),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            brand_name=row["brand_name"],
            category_name=row["category_name"],
            main_image_url=row.get("main_image_url"),
            image_count=image_count,
            video_count=video_count,
            has_main_image=has_main,
        )

    def get_summary(self) -> dict[str, int]:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) AS total,
                      SUM(CASE WHEN status = 'PUBLISHED' THEN 1 ELSE 0 END) AS published_count,
                      SUM(CASE WHEN status = 'NEEDS_COMPLETION' THEN 1 ELSE 0 END) AS needs_completion_count,
                      SUM(CASE WHEN status = 'DRAFT' THEN 1 ELSE 0 END) AS draft_count
                    FROM tiles
                    """
                )
            )
            .mappings()
            .first()
        )
        if not row:
            return {
                "total": 0,
                "published_count": 0,
                "needs_completion_count": 0,
                "draft_count": 0,
            }
        return {
            "total": int(row["total"] or 0),
            "published_count": int(row["published_count"] or 0),
            "needs_completion_count": int(row["needs_completion_count"] or 0),
            "draft_count": int(row["draft_count"] or 0),
        }

    def list_skus(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: int | None,
        category_id: int | None,
        status: str | None,
        material_completeness: str | None,
    ) -> tuple[list[TileSkuRecord], int]:
        where_parts: list[str] = []
        params: dict = {"limit": page_size, "offset": (page - 1) * page_size}

        if keyword:
            where_parts.append("(t.name LIKE :kw OR t.sku_code LIKE :kw)")
            params["kw"] = f"%{keyword.strip()}%"
        if brand_id is not None:
            where_parts.append("t.brand_id = :brand_id")
            params["brand_id"] = brand_id
        if category_id is not None:
            where_parts.append("t.category_id = :category_id")
            params["category_id"] = category_id
        if status:
            where_parts.append("t.status = :status")
            params["status"] = status

        if material_completeness == "missing_images":
            where_parts.append(
                "(SELECT COUNT(*) FROM tile_images ti WHERE ti.tile_id = t.id) = 0"
            )
        elif material_completeness == "missing_main_image":
            where_parts.append(
                "(SELECT COUNT(*) FROM tile_images ti WHERE ti.tile_id = t.id AND ti.is_main = 1) = 0"
            )
        elif material_completeness == "missing_videos":
            where_parts.append(
                "(SELECT COUNT(*) FROM tile_videos tv WHERE tv.tile_id = t.id) = 0"
            )
        elif material_completeness == "complete":
            where_parts.append(
                """
                (SELECT COUNT(*) FROM tile_images ti WHERE ti.tile_id = t.id AND ti.is_main = 1) > 0
                AND (SELECT COUNT(*) FROM tile_images ti WHERE ti.tile_id = t.id) > 0
                AND (SELECT COUNT(*) FROM tile_videos tv WHERE tv.tile_id = t.id) > 0
                """
            )

        where_sql = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        base = self._list_base_sql()

        rows = (
            self._db.execute(
                text(
                    f"{base} {where_sql} ORDER BY t.updated_at DESC LIMIT :limit OFFSET :offset"
                ),
                params,
            )
            .mappings()
            .all()
        )
        total_row = (
            self._db.execute(
                text(f"SELECT COUNT(*) AS cnt FROM tiles t {where_sql}"),
                params,
            )
            .mappings()
            .first()
        )
        total = int(total_row["cnt"]) if total_row else 0
        return [self._to_record(dict(r)) for r in rows], total

    def get_by_id(self, tile_id: int) -> TileSkuRecord | None:
        row = (
            self._db.execute(
                text(f"{self._list_base_sql()} WHERE t.id = :id"),
                {"id": tile_id},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_sku_code(self, sku_code: str, *, exclude_id: int | None = None) -> TileSkuRecord | None:
        sql = f"{self._list_base_sql()} WHERE t.sku_code = :sku_code"
        params: dict = {"sku_code": sku_code}
        if exclude_id is not None:
            sql += " AND t.id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def get_first_brand_id(self) -> int | None:
        row = self._db.execute(text("SELECT id FROM brands ORDER BY id LIMIT 1")).first()
        return int(row[0]) if row else None

    def get_first_category_id(self) -> int | None:
        row = self._db.execute(text("SELECT id FROM tile_categories ORDER BY id LIMIT 1")).first()
        return int(row[0]) if row else None

    def brand_exists(self, brand_id: int) -> bool:
        row = self._db.execute(text("SELECT 1 FROM brands WHERE id = :id"), {"id": brand_id}).first()
        return row is not None

    def category_exists(self, category_id: int) -> bool:
        row = self._db.execute(
            text("SELECT 1 FROM tile_categories WHERE id = :id"), {"id": category_id}
        ).first()
        return row is not None

    def create_sku(
        self,
        *,
        name: str,
        sku_code: str,
        brand_id: int,
        category_id: int,
        spec_id: int | None,
        size: str,
        surface_finish: str,
        color_family: str | None,
        reference_price: float | None,
        remark: str | None,
        status: str,
    ) -> TileSkuRecord:
        now = self._now()
        result = self._db.execute(
            text(
                """
                INSERT INTO tiles (
                  name, sku_code, brand_id, category_id, spec_id, size, surface_finish,
                  color_family, reference_price, remark, status, created_at, updated_at
                ) VALUES (
                  :name, :sku_code, :brand_id, :category_id, :spec_id, :size, :surface_finish,
                  :color_family, :reference_price, :remark, :status, :created_at, :updated_at
                )
                """
            ),
            {
                "name": name,
                "sku_code": sku_code,
                "brand_id": brand_id,
                "category_id": category_id,
                "spec_id": spec_id,
                "size": size,
                "surface_finish": surface_finish,
                "color_family": color_family,
                "reference_price": reference_price,
                "remark": remark,
                "status": status,
                "created_at": now,
                "updated_at": now,
            },
        )
        tile_id = int(result.lastrowid)
        self._increment_sku_count(brand_id, category_id)
        if spec_id is not None:
            self._increment_spec_sku_count(spec_id)
        self._db.commit()
        record = self.get_by_id(tile_id)
        assert record is not None
        return record

    def update_sku(
        self,
        tile_id: int,
        *,
        name: str,
        sku_code: str,
        brand_id: int,
        category_id: int,
        spec_id: int | None,
        size: str,
        surface_finish: str,
        color_family: str | None,
        reference_price: float | None,
        remark: str | None,
        status: str,
        old_brand_id: int,
        old_category_id: int,
        old_spec_id: int | None,
    ) -> TileSkuRecord:
        now = self._now()
        self._db.execute(
            text(
                """
                UPDATE tiles SET
                  name = :name, sku_code = :sku_code, brand_id = :brand_id,
                  category_id = :category_id, spec_id = :spec_id, size = :size,
                  surface_finish = :surface_finish,
                  color_family = :color_family, reference_price = :reference_price,
                  remark = :remark, status = :status, updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": tile_id,
                "name": name,
                "sku_code": sku_code,
                "brand_id": brand_id,
                "category_id": category_id,
                "spec_id": spec_id,
                "size": size,
                "surface_finish": surface_finish,
                "color_family": color_family,
                "reference_price": reference_price,
                "remark": remark,
                "status": status,
                "updated_at": now,
            },
        )
        if old_brand_id != brand_id:
            self._decrement_sku_count(old_brand_id)
            self._increment_sku_count(brand_id, 0)
        if old_category_id != category_id:
            self._decrement_sku_count_category(old_category_id)
            self._increment_sku_count(0, category_id)
        if old_spec_id != spec_id:
            if old_spec_id is not None:
                self._decrement_spec_sku_count(old_spec_id)
            if spec_id is not None:
                self._increment_spec_sku_count(spec_id)
        self._db.commit()
        record = self.get_by_id(tile_id)
        assert record is not None
        return record

    def update_status(self, tile_id: int, status: str) -> TileSkuRecord:
        now = self._now()
        self._db.execute(
            text("UPDATE tiles SET status = :status, updated_at = :updated_at WHERE id = :id"),
            {"id": tile_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        record = self.get_by_id(tile_id)
        assert record is not None
        return record

    def delete_sku(
        self,
        tile_id: int,
        *,
        brand_id: int,
        category_id: int,
        spec_id: int | None,
    ) -> None:
        self._db.execute(text("DELETE FROM tile_images WHERE tile_id = :id"), {"id": tile_id})
        self._db.execute(text("DELETE FROM tile_videos WHERE tile_id = :id"), {"id": tile_id})
        self._db.execute(text("DELETE FROM tiles WHERE id = :id"), {"id": tile_id})
        self._decrement_sku_count(brand_id)
        self._decrement_sku_count_category(category_id)
        if spec_id is not None:
            self._decrement_spec_sku_count(spec_id)
        self._db.commit()

    def list_images(self, tile_id: int) -> list[TileSkuImageRecord]:
        rows = (
            self._db.execute(
                text(
                    "SELECT * FROM tile_images WHERE tile_id = :id ORDER BY sort_order, id"
                ),
                {"id": tile_id},
            )
            .mappings()
            .all()
        )
        return [
            TileSkuImageRecord(
                id=int(r["id"]),
                tile_id=int(r["tile_id"]),
                object_key=r["object_key"],
                url=r["url"],
                is_main=int(r["is_main"]),
                sort_order=int(r["sort_order"]),
            )
            for r in rows
        ]

    def list_videos(self, tile_id: int) -> list[TileSkuVideoRecord]:
        rows = (
            self._db.execute(
                text("SELECT * FROM tile_videos WHERE tile_id = :id ORDER BY sort_order, id"),
                {"id": tile_id},
            )
            .mappings()
            .all()
        )
        return [
            TileSkuVideoRecord(
                id=int(r["id"]),
                tile_id=int(r["tile_id"]),
                object_key=r["object_key"],
                file_name=r["file_name"],
                file_size_bytes=r.get("file_size_bytes"),
                duration_seconds=r.get("duration_seconds"),
                sort_order=int(r["sort_order"]),
            )
            for r in rows
        ]

    def replace_images(
        self,
        tile_id: int,
        images: list[dict],
    ) -> None:
        self._db.execute(text("DELETE FROM tile_images WHERE tile_id = :id"), {"id": tile_id})
        for idx, img in enumerate(images):
            self._db.execute(
                text(
                    """
                    INSERT INTO tile_images (tile_id, object_key, url, is_main, sort_order)
                    VALUES (:tile_id, :object_key, :url, :is_main, :sort_order)
                    """
                ),
                {
                    "tile_id": tile_id,
                    "object_key": img["object_key"],
                    "url": img["url"],
                    "is_main": 1 if img.get("is_main") else 0,
                    "sort_order": img.get("sort_order", idx),
                },
            )
        self._db.commit()

    def replace_videos(
        self,
        tile_id: int,
        videos: list[dict],
    ) -> None:
        now = self._now()
        self._db.execute(text("DELETE FROM tile_videos WHERE tile_id = :id"), {"id": tile_id})
        for idx, vid in enumerate(videos):
            self._db.execute(
                text(
                    """
                    INSERT INTO tile_videos (
                      tile_id, object_key, file_name, file_size_bytes,
                      duration_seconds, sort_order, created_at
                    ) VALUES (
                      :tile_id, :object_key, :file_name, :file_size_bytes,
                      :duration_seconds, :sort_order, :created_at
                    )
                    """
                ),
                {
                    "tile_id": tile_id,
                    "object_key": vid["object_key"],
                    "file_name": vid["file_name"],
                    "file_size_bytes": vid.get("file_size_bytes"),
                    "duration_seconds": vid.get("duration_seconds"),
                    "sort_order": vid.get("sort_order", idx),
                    "created_at": now,
                },
            )
        self._db.commit()

    @staticmethod
    def generate_draft_sku_code() -> str:
        return f"DRAFT-{uuid4().hex[:8].upper()}"

    def _increment_sku_count(self, brand_id: int, category_id: int) -> None:
        if brand_id:
            self._db.execute(
                text("UPDATE brands SET sku_count = sku_count + 1 WHERE id = :id"),
                {"id": brand_id},
            )
        if category_id:
            self._db.execute(
                text("UPDATE tile_categories SET sku_count = sku_count + 1 WHERE id = :id"),
                {"id": category_id},
            )

    def _decrement_sku_count(self, brand_id: int) -> None:
        self._db.execute(
            text(
                """
                UPDATE brands SET sku_count = CASE WHEN sku_count > 0 THEN sku_count - 1 ELSE 0 END
                WHERE id = :id
                """
            ),
            {"id": brand_id},
        )

    def _decrement_sku_count_category(self, category_id: int) -> None:
        self._db.execute(
            text(
                """
                UPDATE tile_categories SET sku_count = CASE WHEN sku_count > 0 THEN sku_count - 1 ELSE 0 END
                WHERE id = :id
                """
            ),
            {"id": category_id},
        )

    def _increment_spec_sku_count(self, spec_id: int) -> None:
        self._db.execute(
            text(
                "UPDATE tile_specs SET sku_count = sku_count + 1, updated_at = :updated_at "
                "WHERE id = :id"
            ),
            {"id": spec_id, "updated_at": self._now()},
        )

    def _decrement_spec_sku_count(self, spec_id: int) -> None:
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

    @staticmethod
    def compute_material_completeness(record: TileSkuRecord) -> str:
        return TileSkuRepository._material_completeness(
            record.has_main_image, record.image_count, record.video_count
        )
