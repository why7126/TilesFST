"""Banner persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

VALID_BANNER_SCOPE_SQL = (
    "display_client = 'MINIAPP_HOME' "
    "AND position IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')"
)


@dataclass
class BannerRecord:
    id: int
    title: str
    display_client: str
    position: str
    image_object_key: str
    image_source: str
    sku_gallery_asset_id: int | None
    jump_type: str
    sku_id: int | None
    external_url: str | None
    topic_id: int | None
    brand_id: int | None
    sort_order: int
    valid_from: str | None
    valid_to: str | None
    status: str
    remark: str | None
    created_at: str
    updated_at: str


@dataclass
class BannerListResult:
    items: list[BannerRecord]
    total: int
    summary: dict[str, int]


def compute_time_status(
    *,
    status: str,
    valid_from: str | None,
    valid_to: str | None,
    now: datetime | None = None,
) -> str | None:
    current = now or datetime.now(UTC)
    if valid_to:
        try:
            to_dt = datetime.fromisoformat(valid_to.replace("Z", "+00:00"))
            if to_dt.tzinfo is None:
                to_dt = to_dt.replace(tzinfo=UTC)
            if to_dt < current:
                return "EXPIRED"
        except ValueError:
            pass
    if status != "ONLINE":
        return None
    if valid_from:
        try:
            from_dt = datetime.fromisoformat(valid_from.replace("Z", "+00:00"))
            if from_dt.tzinfo is None:
                from_dt = from_dt.replace(tzinfo=UTC)
            if from_dt > current:
                return "PENDING"
        except ValueError:
            pass
    return "ACTIVE"


def _time_status_sql(time_status: str, now_iso: str) -> str:
    expired = f"(valid_to IS NOT NULL AND valid_to < '{now_iso}')"
    not_expired = f"(valid_to IS NULL OR valid_to >= '{now_iso}')"
    if time_status == "EXPIRED":
        return expired
    if time_status == "PENDING":
        return (
            f"status = 'ONLINE' AND {not_expired} "
            f"AND valid_from IS NOT NULL AND valid_from > '{now_iso}'"
        )
    if time_status == "ACTIVE":
        return (
            f"status = 'ONLINE' AND {not_expired} "
            f"AND (valid_from IS NULL OR valid_from <= '{now_iso}')"
        )
    return "1=1"


class BannerRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    @staticmethod
    def _to_record(row: dict[str, Any]) -> BannerRecord:
        return BannerRecord(
            id=int(row["id"]),
            title=row["title"],
            display_client=row["display_client"],
            position=row["position"],
            image_object_key=row["image_object_key"],
            image_source=row["image_source"],
            sku_gallery_asset_id=(
                int(row["sku_gallery_asset_id"]) if row.get("sku_gallery_asset_id") is not None else None
            ),
            jump_type=row["jump_type"],
            sku_id=int(row["sku_id"]) if row.get("sku_id") is not None else None,
            external_url=row.get("external_url"),
            topic_id=int(row["topic_id"]) if row.get("topic_id") is not None else None,
            brand_id=int(row["brand_id"]) if row.get("brand_id") is not None else None,
            sort_order=int(row["sort_order"]),
            valid_from=row.get("valid_from"),
            valid_to=row.get("valid_to"),
            status=row["status"],
            remark=row.get("remark"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _summary(self, *, where_sql: str, params: dict[str, Any]) -> dict[str, int]:
        now_iso = datetime.now(UTC).isoformat()
        total_row = (
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM banners WHERE {VALID_BANNER_SCOPE_SQL}")
            )
            .mappings()
            .one()
        )
        filtered_row = (
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM banners WHERE {where_sql}"),
                params,
            )
            .mappings()
            .one()
        )
        online_row = (
            self._db.execute(
                text(
                    f"SELECT COUNT(*) AS c FROM banners "
                    f"WHERE {VALID_BANNER_SCOPE_SQL} AND status = 'ONLINE'"
                ),
            )
            .mappings()
            .one()
        )
        pending_sql = _time_status_sql("PENDING", now_iso)
        pending_row = (
            self._db.execute(
                text(
                    f"SELECT COUNT(*) AS c FROM banners "
                    f"WHERE {VALID_BANNER_SCOPE_SQL} AND {pending_sql}"
                ),
            )
            .mappings()
            .one()
        )
        return {
            "total": int(total_row["c"] or 0),
            "filtered_count": int(filtered_row["c"] or 0),
            "online_count": int(online_row["c"] or 0),
            "pending_count": int(pending_row["c"] or 0),
        }

    def list_banners(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        display_client: str | None,
        status: str | None,
        time_status: str | None,
    ) -> BannerListResult:
        conditions = [VALID_BANNER_SCOPE_SQL]
        params: dict[str, Any] = {}
        now_iso = datetime.now(UTC).isoformat()

        if keyword:
            conditions.append(
                "(title LIKE :keyword OR position LIKE :keyword OR external_url LIKE :keyword)"
            )
            params["keyword"] = f"%{keyword}%"
        if display_client:
            conditions.append("display_client = :display_client")
            params["display_client"] = display_client
        if status:
            conditions.append("status = :status")
            params["status"] = status
        if time_status:
            conditions.append(_time_status_sql(time_status, now_iso))

        where_sql = " AND ".join(conditions)
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) AS c FROM banners WHERE {where_sql}"),
                params,
            ).scalar_one()
        )

        offset = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM banners
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
        return BannerListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=total,
            summary=self._summary(where_sql=where_sql, params=params),
        )

    def get_by_id(self, banner_id: int) -> BannerRecord | None:
        row = (
            self._db.execute(
                text(f"SELECT * FROM banners WHERE id = :id AND {VALID_BANNER_SCOPE_SQL}"),
                {"id": banner_id},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_unique_key(
        self,
        display_client: str,
        position: str,
        title: str,
        *,
        exclude_id: int | None = None,
    ) -> BannerRecord | None:
        sql = """
            SELECT * FROM banners
            WHERE display_client = :display_client
              AND position = :position
              AND title = :title
        """
        params: dict[str, Any] = {
            "display_client": display_client,
            "position": position,
            "title": title,
        }
        if exclude_id is not None:
            sql += " AND id != :exclude_id"
            params["exclude_id"] = exclude_id
        row = self._db.execute(text(sql), params).mappings().first()
        return self._to_record(dict(row)) if row else None

    def create(
        self,
        *,
        title: str,
        display_client: str,
        position: str,
        image_object_key: str,
        image_source: str,
        sku_gallery_asset_id: int | None,
        jump_type: str,
        sku_id: int | None,
        external_url: str | None,
        topic_id: int | None,
        brand_id: int | None,
        sort_order: int,
        valid_from: str | None,
        valid_to: str | None,
        remark: str | None,
    ) -> BannerRecord:
        now = datetime.now(UTC).isoformat()
        cursor = self._db.execute(
            text(
                """
                INSERT INTO banners (
                  title, display_client, position, image_object_key, image_source,
                  sku_gallery_asset_id, jump_type, sku_id, external_url, topic_id,
                  brand_id, sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES (
                  :title, :display_client, :position, :image_object_key, :image_source,
                  :sku_gallery_asset_id, :jump_type, :sku_id, :external_url, :topic_id,
                  :brand_id, :sort_order, :valid_from, :valid_to, 'DRAFT', :remark, :created_at, :updated_at
                )
                """
            ),
            {
                "title": title,
                "display_client": display_client,
                "position": position,
                "image_object_key": image_object_key,
                "image_source": image_source,
                "sku_gallery_asset_id": sku_gallery_asset_id,
                "jump_type": jump_type,
                "sku_id": sku_id,
                "external_url": external_url,
                "topic_id": topic_id,
                "brand_id": brand_id,
                "sort_order": sort_order,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "remark": remark,
                "created_at": now,
                "updated_at": now,
            },
        )
        self._db.commit()
        banner_id = int(cursor.lastrowid)
        record = self.get_by_id(banner_id)
        assert record is not None
        return record

    def update(
        self,
        banner_id: int,
        *,
        title: str,
        display_client: str,
        position: str,
        image_object_key: str,
        image_source: str,
        sku_gallery_asset_id: int | None,
        jump_type: str,
        sku_id: int | None,
        external_url: str | None,
        topic_id: int | None,
        brand_id: int | None,
        sort_order: int,
        valid_from: str | None,
        valid_to: str | None,
        remark: str | None,
    ) -> BannerRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE banners SET
                  title = :title,
                  display_client = :display_client,
                  position = :position,
                  image_object_key = :image_object_key,
                  image_source = :image_source,
                  sku_gallery_asset_id = :sku_gallery_asset_id,
                  jump_type = :jump_type,
                  sku_id = :sku_id,
                  external_url = :external_url,
                  topic_id = :topic_id,
                  brand_id = :brand_id,
                  sort_order = :sort_order,
                  valid_from = :valid_from,
                  valid_to = :valid_to,
                  remark = :remark,
                  updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": banner_id,
                "title": title,
                "display_client": display_client,
                "position": position,
                "image_object_key": image_object_key,
                "image_source": image_source,
                "sku_gallery_asset_id": sku_gallery_asset_id,
                "jump_type": jump_type,
                "sku_id": sku_id,
                "external_url": external_url,
                "topic_id": topic_id,
                "brand_id": brand_id,
                "sort_order": sort_order,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "remark": remark,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(banner_id)

    def update_status(self, banner_id: int, status: str) -> BannerRecord | None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text("UPDATE banners SET status = :status, updated_at = :updated_at WHERE id = :id"),
            {"id": banner_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(banner_id)

    def delete(self, banner_id: int) -> bool:
        result = self._db.execute(text("DELETE FROM banners WHERE id = :id"), {"id": banner_id})
        self._db.commit()
        return result.rowcount > 0

    def get_tile_image(self, image_id: int) -> dict[str, Any] | None:
        row = (
            self._db.execute(
                text("SELECT * FROM tile_images WHERE id = :id"),
                {"id": image_id},
            )
            .mappings()
            .first()
        )
        return dict(row) if row else None

    def get_sku_main_image_key(self, sku_id: int) -> str | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT object_key FROM tile_images
                    WHERE tile_id = :tile_id AND is_main = 1
                    ORDER BY sort_order, id
                    LIMIT 1
                    """
                ),
                {"tile_id": sku_id},
            )
            .mappings()
            .first()
        )
        return row["object_key"] if row else None

    def sku_exists(self, sku_id: int) -> bool:
        row = self._db.execute(text("SELECT 1 FROM tiles WHERE id = :id"), {"id": sku_id}).first()
        return row is not None

    def brand_exists(self, brand_id: int) -> bool:
        row = self._db.execute(
            text("SELECT 1 FROM brands WHERE id = :id AND status = 'ENABLED'"),
            {"id": brand_id},
        ).first()
        return row is not None

    def get_brand_logo_key(self, brand_id: int) -> str | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT logo_object_key FROM brands
                    WHERE id = :id AND status = 'ENABLED'
                    """
                ),
                {"id": brand_id},
            )
            .mappings()
            .first()
        )
        return row["logo_object_key"] if row else None
