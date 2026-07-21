"""Public miniapp data aggregation queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class MiniappProductRecord:
    id: int
    name: str
    sku_code: str
    size: str
    surface_finish: str
    color_family: str | None
    reference_price: float | None
    created_at: str
    updated_at: str
    brand_name: str
    category_name: str
    spec_name: str | None
    main_image_url: str | None
    hot_score: int
    brand_id: int
    brand_short_name: str | None
    brand_logo_object_key: str | None
    category_path: str | None
    remark: str | None


@dataclass
class MiniappBannerRecord:
    id: int
    title: str
    image_object_key: str
    jump_type: str
    sku_id: int | None
    external_url: str | None
    topic_id: int | None
    brand_id: int | None
    sort_order: int


@dataclass
class MiniappBrandRecord:
    id: int
    name: str
    sort_order: int
    short_name: str | None
    english_name: str | None
    logo_object_key: str | None
    description: str | None
    product_count: int


@dataclass
class MiniappMediaRecord:
    id: int
    media_type: str
    url: str
    sort_order: int
    is_main: bool = False
    duration_seconds: float | None = None


@dataclass
class MiniappCategoryRecord:
    id: int
    parent_id: int | None
    name: str
    sort_order: int
    level: int
    created_at: str
    updated_at: str


@dataclass
class MiniappNamedResult:
    id: int
    name: str
    count: int


@dataclass
class MiniappCertificateResult:
    id: int
    brand_id: int | None
    name: str
    certificate_no: str | None
    issuer: str | None
    type: str | None
    brand_name: str
    file_url: str
    file_name: str | None = None
    file_mime_type: str | None = None
    is_permanent: bool = False
    effective_date: str | None = None
    expiry_date: str | None = None


class MiniappHomeRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_public_banners(
        self,
        *,
        position: str = "MINIAPP_HOME_CAROUSEL",
        limit: int = 5,
    ) -> list[MiniappBannerRecord]:
        if position not in {"MINIAPP_HOME_CAROUSEL", "MINIAPP_BRAND_LIST_CAROUSEL"}:
            position = "MINIAPP_HOME_CAROUSEL"
        now_iso = datetime.now(UTC).isoformat()
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT id, title, image_object_key, jump_type, sku_id,
                           external_url, topic_id, brand_id, sort_order
                    FROM banners
                    WHERE status = 'ONLINE'
                      AND display_client = 'MINIAPP_HOME'
                      AND position = :position
                      AND (valid_from IS NULL OR valid_from <= :now_iso)
                      AND (valid_to IS NULL OR valid_to >= :now_iso)
                    ORDER BY sort_order ASC, updated_at DESC
                    LIMIT :limit
                    """
                ),
                {"now_iso": now_iso, "position": position, "limit": limit},
            )
            .mappings()
            .all()
        )
        return [
            MiniappBannerRecord(
                id=int(row["id"]),
                title=str(row["title"]),
                image_object_key=str(row["image_object_key"]),
                jump_type=str(row["jump_type"]),
                sku_id=int(row["sku_id"]) if row.get("sku_id") is not None else None,
                external_url=row.get("external_url"),
                topic_id=int(row["topic_id"]) if row.get("topic_id") is not None else None,
                brand_id=int(row["brand_id"]) if row.get("brand_id") is not None else None,
                sort_order=int(row["sort_order"]),
            )
            for row in rows
        ]

    def list_public_brands(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[MiniappBrandRecord], int]:
        params = {"limit": page_size, "offset": (page - 1) * page_size}
        base_sql = """
            SELECT b.id, b.name, b.sort_order, b.short_name, b.english_name,
                   b.logo_object_key, b.description,
                   SUM(
                     CASE
                       WHEN t.id IS NOT NULL
                        AND c.id IS NOT NULL
                        AND (t.spec_id IS NULL OR s.status = 'ENABLED')
                       THEN 1 ELSE 0
                     END
                   ) AS product_count
            FROM brands b
            LEFT JOIN tiles t ON t.brand_id = b.id AND t.status = 'PUBLISHED'
            LEFT JOIN tile_categories c ON c.id = t.category_id AND c.status = 'ENABLED'
            LEFT JOIN tile_specs s ON s.id = t.spec_id
            WHERE b.status = 'ENABLED'
            GROUP BY b.id, b.name, b.sort_order, b.short_name, b.english_name,
                     b.logo_object_key, b.description
        """
        rows = (
            self._db.execute(
                text(
                    f"""
                    {base_sql}
                    ORDER BY b.sort_order ASC, product_count DESC, b.id ASC
                    LIMIT :limit
                    OFFSET :offset
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        total = int(
            self._db.execute(text("SELECT COUNT(*) FROM brands WHERE status = 'ENABLED'")).scalar_one()
            or 0
        )
        return [self._to_brand(dict(row)) for row in rows], total

    def get_public_brand(self, brand_id: int) -> MiniappBrandRecord | None:
        row = (
            self._db.execute(
                text(
                    """
                    SELECT b.id, b.name, b.sort_order, b.short_name, b.english_name,
                           b.logo_object_key, b.description,
                           SUM(
                             CASE
                               WHEN t.id IS NOT NULL
                                AND c.id IS NOT NULL
                                AND (t.spec_id IS NULL OR s.status = 'ENABLED')
                               THEN 1 ELSE 0
                             END
                           ) AS product_count
                    FROM brands b
                    LEFT JOIN tiles t ON t.brand_id = b.id AND t.status = 'PUBLISHED'
                    LEFT JOIN tile_categories c ON c.id = t.category_id AND c.status = 'ENABLED'
                    LEFT JOIN tile_specs s ON s.id = t.spec_id
                    WHERE b.status = 'ENABLED'
                      AND b.id = :brand_id
                    GROUP BY b.id, b.name, b.sort_order, b.short_name, b.english_name,
                             b.logo_object_key, b.description
                    """
                ),
                {"brand_id": brand_id},
            )
            .mappings()
            .first()
        )
        return self._to_brand(dict(row)) if row else None

    def list_public_brand_certificates(
        self,
        *,
        brand_id: int,
        limit: int = 50,
    ) -> list[MiniappCertificateResult]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT bc.id, bc.name, bc.certificate_no, bc.issuer, bc.type,
                           bc.file_url, b.name AS brand_name
                    FROM brand_certificates bc
                    JOIN brands b ON b.id = bc.brand_id
                    WHERE bc.deleted_at IS NULL
                      AND bc.is_visible = 1
                      AND bc.brand_id = :brand_id
                      AND b.status = 'ENABLED'
                    ORDER BY bc.sort_order ASC, bc.updated_at DESC, bc.id DESC
                    LIMIT :limit
                    """
                ),
                {"brand_id": brand_id, "limit": limit},
            )
            .mappings()
            .all()
        )
        return [
            MiniappCertificateResult(
                id=int(row["id"]),
                brand_id=brand_id,
                name=str(row["name"]),
                certificate_no=row.get("certificate_no"),
                issuer=row.get("issuer"),
                type=row.get("type"),
                brand_name=str(row["brand_name"]),
                file_url=str(row["file_url"]),
                file_name=row.get("file_name"),
                file_mime_type=row.get("file_mime_type"),
                is_permanent=bool(row.get("is_permanent")),
                effective_date=row.get("effective_date"),
                expiry_date=row.get("expiry_date"),
            )
            for row in rows
        ]

    def list_public_certificates(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[MiniappCertificateResult], int]:
        where, params = self._certificate_filters()
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        rows = (
            self._db.execute(
                text(
                    f"""
                    {self._certificate_select_sql()}
                    {where}
                    ORDER BY bc.sort_order ASC, bc.updated_at DESC, bc.id DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        total = int(
            self._db.execute(
                text(
                    f"""
                    SELECT COUNT(*)
                    FROM brand_certificates bc
                    JOIN brands b ON b.id = bc.brand_id
                    {where}
                    """
                ),
                params,
            ).scalar_one()
            or 0
        )
        return [self._to_certificate(dict(row)) for row in rows], total

    def list_enabled_categories_for_tree(self, *, depth: int = 2) -> list[MiniappCategoryRecord]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT id, parent_id, name, sort_order, level, created_at, updated_at
                    FROM tile_categories
                    WHERE status = 'ENABLED'
                      AND level BETWEEN 1 AND :depth
                    ORDER BY level ASC, sort_order ASC, created_at ASC, id ASC
                    """
                ),
                {"depth": depth},
            )
            .mappings()
            .all()
        )
        return [
            MiniappCategoryRecord(
                id=int(row["id"]),
                parent_id=int(row["parent_id"]) if row.get("parent_id") is not None else None,
                name=str(row["name"]),
                sort_order=int(row["sort_order"]),
                level=int(row["level"]),
                created_at=str(row["created_at"]),
                updated_at=str(row["updated_at"]),
            )
            for row in rows
        ]

    def list_products(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        keyword: str | None = None,
        category_id: int | None = None,
        category_level: str | None = None,
        brand_id: int | None = None,
        spec: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        sort: str = "default",
        filter_type: str | None = None,
        filter_value: str | None = None,
        only_new: bool = False,
        hot_first: bool = False,
    ) -> tuple[list[MiniappProductRecord], int]:
        where, params = self._product_filters(
            keyword=keyword,
            category_id=category_id,
            category_level=category_level,
            brand_id=brand_id,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
            filter_type=filter_type,
            filter_value=filter_value,
            only_new=only_new,
        )
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        hot_sql = self._hot_score_sql()
        order_sql = self._product_order_sql(sort=sort, hot_first=hot_first)
        rows = (
            self._db.execute(
                text(
                    f"""
                    {self._product_select_sql(hot_sql)}
                    {where}
                    ORDER BY {order_sql}
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) FROM tiles t JOIN brands b ON b.id = t.brand_id JOIN tile_categories c ON c.id = t.category_id LEFT JOIN tile_specs s ON s.id = t.spec_id {where}"),
                params,
            ).scalar_one()
            or 0
        )
        return [self._to_product(dict(row)) for row in rows], total

    def list_product_facets(
        self,
        *,
        keyword: str | None,
        category_id: int | None,
        category_level: str | None,
        brand_id: int | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
    ) -> dict[str, list[MiniappNamedResult]]:
        where, params = self._product_filters(
            keyword=keyword,
            category_id=category_id,
            category_level=category_level,
            brand_id=brand_id,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
            filter_type=None,
            filter_value=None,
            only_new=False,
        )
        facets: dict[str, list[MiniappNamedResult]] = {}
        for key, select_sql, group_sql, order_sql in [
            ("brands", "b.id, b.name", "b.id, b.name", "count DESC, b.sort_order ASC, b.id ASC"),
            ("categories", "c.id, c.name", "c.id, c.name", "count DESC, c.sort_order ASC, c.id ASC"),
            ("specs", "COALESCE(s.id, 0) AS id, COALESCE(s.display_name, t.size) AS name", "COALESCE(s.id, 0), COALESCE(s.display_name, t.size)", "count DESC, name ASC"),
        ]:
            rows = self._db.execute(
                text(
                    f"""
                    SELECT {select_sql}, COUNT(t.id) AS count
                    FROM tiles t
                    JOIN brands b ON b.id = t.brand_id
                    JOIN tile_categories c ON c.id = t.category_id
                    LEFT JOIN tile_specs s ON s.id = t.spec_id
                    {where}
                    GROUP BY {group_sql}
                    ORDER BY {order_sql}
                    LIMIT 12
                    """
                ),
                params,
            ).mappings().all()
            facets[key] = [self._to_named_result(dict(row)) for row in rows if row.get("name")]
        return facets

    def list_search_products(
        self,
        *,
        keyword: str,
        page: int,
        page_size: int,
        brand: str | None,
        category: str | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
    ) -> tuple[list[MiniappProductRecord], int]:
        where, params = self._search_product_filters(
            keyword=keyword,
            brand=brand,
            category=category,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
        )
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        hot_sql = self._hot_score_sql()
        rows = (
            self._db.execute(
                text(
                    f"""
                    {self._product_select_sql(hot_sql)}
                    {where}
                    ORDER BY
                      CASE
                        WHEN lower(t.sku_code) = :exact_keyword THEN 0
                        WHEN lower(t.sku_code) LIKE :prefix_keyword THEN 1
                        WHEN lower(t.name) = :exact_keyword THEN 2
                        WHEN lower(b.name) = :exact_keyword THEN 3
                        WHEN t.sku_code LIKE :keyword OR t.name LIKE :keyword THEN 4
                        ELSE 5
                      END,
                      CASE WHEN main_image_url IS NULL THEN 1 ELSE 0 END,
                      hot_score DESC,
                      t.updated_at DESC,
                      t.id DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        total = int(
            self._db.execute(
                text(
                    f"""
                    SELECT COUNT(*)
                    FROM tiles t
                    JOIN brands b ON b.id = t.brand_id
                    JOIN tile_categories c ON c.id = t.category_id
                    LEFT JOIN tile_specs s ON s.id = t.spec_id
                    {where}
                    """
                ),
                params,
            ).scalar_one()
            or 0
        )
        return [self._to_product(dict(row)) for row in rows], total

    def list_search_named_results(self, *, keyword: str) -> dict[str, list[MiniappNamedResult]]:
        params = {"keyword": f"%{keyword.strip()}%"}
        brands = self._db.execute(
            text(
                """
                SELECT b.id, b.name, COUNT(t.id) AS count
                FROM brands b
                JOIN tiles t ON t.brand_id = b.id AND t.status = 'PUBLISHED'
                JOIN tile_categories c ON c.id = t.category_id AND c.status = 'ENABLED'
                LEFT JOIN tile_specs s ON s.id = t.spec_id
                WHERE b.status = 'ENABLED'
                  AND (s.id IS NULL OR s.status = 'ENABLED')
                  AND b.name LIKE :keyword
                GROUP BY b.id, b.name
                ORDER BY count DESC, b.sort_order ASC, b.id ASC
                LIMIT 8
                """
            ),
            params,
        ).mappings().all()
        categories = self._db.execute(
            text(
                """
                SELECT c.id, c.name, COUNT(t.id) AS count
                FROM tile_categories c
                JOIN tiles t ON t.category_id = c.id AND t.status = 'PUBLISHED'
                JOIN brands b ON b.id = t.brand_id AND b.status = 'ENABLED'
                LEFT JOIN tile_specs s ON s.id = t.spec_id
                WHERE c.status = 'ENABLED'
                  AND (s.id IS NULL OR s.status = 'ENABLED')
                  AND (c.name LIKE :keyword OR c.path LIKE :keyword)
                GROUP BY c.id, c.name
                ORDER BY count DESC, c.sort_order ASC, c.id ASC
                LIMIT 8
                """
            ),
            params,
        ).mappings().all()
        specs = self._db.execute(
            text(
                """
                SELECT s.id, s.display_name AS name, COUNT(t.id) AS count
                FROM tile_specs s
                JOIN tiles t ON t.spec_id = s.id AND t.status = 'PUBLISHED'
                JOIN brands b ON b.id = t.brand_id AND b.status = 'ENABLED'
                JOIN tile_categories c ON c.id = t.category_id AND c.status = 'ENABLED'
                WHERE s.status = 'ENABLED'
                  AND (s.display_name LIKE :keyword OR t.size LIKE :keyword)
                GROUP BY s.id, s.display_name
                ORDER BY count DESC, s.sort_order ASC, s.id ASC
                LIMIT 8
                """
            ),
            params,
        ).mappings().all()
        return {
            "brand": [self._to_named_result(dict(row)) for row in brands],
            "category": [self._to_named_result(dict(row)) for row in categories],
            "spec": [self._to_named_result(dict(row)) for row in specs],
        }

    def list_search_certificates(self, *, keyword: str, limit: int = 8) -> list[MiniappCertificateResult]:
        rows = self._db.execute(
            text(
                """
                SELECT bc.id, bc.name, bc.certificate_no, bc.issuer, bc.file_url, b.name AS brand_name
                FROM brand_certificates bc
                JOIN brands b ON b.id = bc.brand_id
                WHERE bc.deleted_at IS NULL
                  AND bc.is_visible = 1
                  AND b.status = 'ENABLED'
                  AND (
                    bc.name LIKE :keyword OR bc.certificate_no LIKE :keyword
                    OR bc.issuer LIKE :keyword OR b.name LIKE :keyword
                  )
                ORDER BY bc.sort_order ASC, bc.updated_at DESC, bc.id DESC
                LIMIT :limit
                """
            ),
            {"keyword": f"%{keyword.strip()}%", "limit": limit},
        ).mappings().all()
        return [
            MiniappCertificateResult(
                id=int(row["id"]),
                brand_id=None,
                name=str(row["name"]),
                certificate_no=row.get("certificate_no"),
                issuer=row.get("issuer"),
                type=None,
                brand_name=str(row["brand_name"]),
                file_url=str(row["file_url"]),
            )
            for row in rows
        ]

    def list_search_facets(self, *, keyword: str) -> dict[str, list[MiniappNamedResult]]:
        where, params = self._search_product_filters(
            keyword=keyword,
            brand=None,
            category=None,
            spec=None,
            price_min=None,
            price_max=None,
        )
        facets: dict[str, list[MiniappNamedResult]] = {}
        for key, select_sql, group_sql, order_sql in [
            ("brands", "b.id, b.name", "b.id, b.name", "count DESC, b.sort_order ASC, b.id ASC"),
            ("categories", "c.id, c.name", "c.id, c.name", "count DESC, c.sort_order ASC, c.id ASC"),
            ("specs", "COALESCE(s.id, 0) AS id, COALESCE(s.display_name, t.size) AS name", "COALESCE(s.id, 0), COALESCE(s.display_name, t.size)", "count DESC, name ASC"),
        ]:
            rows = self._db.execute(
                text(
                    f"""
                    SELECT {select_sql}, COUNT(t.id) AS count
                    FROM tiles t
                    JOIN brands b ON b.id = t.brand_id
                    JOIN tile_categories c ON c.id = t.category_id
                    LEFT JOIN tile_specs s ON s.id = t.spec_id
                    {where}
                    GROUP BY {group_sql}
                    ORDER BY {order_sql}
                    LIMIT 12
                    """
                ),
                params,
            ).mappings().all()
            facets[key] = [self._to_named_result(dict(row)) for row in rows if row.get("name")]
        return facets

    def get_product(self, product_id: int) -> MiniappProductRecord | None:
        row = (
            self._db.execute(
                text(
                    f"""
                    {self._product_select_sql(self._hot_score_sql())}
                    WHERE t.status = 'PUBLISHED'
                      AND b.status = 'ENABLED'
                      AND c.status = 'ENABLED'
                      AND (s.id IS NULL OR s.status = 'ENABLED')
                      AND t.id = :product_id
                    """
                ),
                {"product_id": product_id},
            )
            .mappings()
            .first()
        )
        return self._to_product(dict(row)) if row else None

    def list_product_images(self, product_id: int) -> list[str]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT object_key FROM tile_images
                    WHERE tile_id = :product_id
                    ORDER BY is_main DESC, sort_order ASC, id ASC
                    """
                ),
                {"product_id": product_id},
            )
            .mappings()
            .all()
        )
        return [str(row["object_key"]) for row in rows if row.get("object_key")]

    def list_product_videos(self, product_id: int) -> list[str]:
        rows = (
            self._db.execute(
                text(
                    """
                    SELECT object_key FROM tile_videos
                    WHERE tile_id = :product_id
                    ORDER BY sort_order ASC, id ASC
                    """
                ),
                {"product_id": product_id},
            )
            .mappings()
            .all()
        )
        return [str(row["object_key"]) for row in rows if row.get("object_key")]

    def list_product_media(self, product_id: int) -> list[MiniappMediaRecord]:
        image_rows = (
            self._db.execute(
                text(
                    """
                    SELECT id, object_key, is_main, sort_order
                    FROM tile_images
                    WHERE tile_id = :product_id
                    ORDER BY is_main DESC, sort_order ASC, id ASC
                    """
                ),
                {"product_id": product_id},
            )
            .mappings()
            .all()
        )
        video_rows = (
            self._db.execute(
                text(
                    """
                    SELECT id, object_key, duration_seconds, sort_order
                    FROM tile_videos
                    WHERE tile_id = :product_id
                    ORDER BY sort_order ASC, id ASC
                    """
                ),
                {"product_id": product_id},
            )
            .mappings()
            .all()
        )
        media = [
            MiniappMediaRecord(
                id=int(row["id"]),
                media_type="image",
                url=str(row["object_key"]),
                sort_order=int(row["sort_order"] or 0),
                is_main=bool(row["is_main"]),
            )
            for row in image_rows
            if row.get("object_key")
        ]
        media.extend(
            MiniappMediaRecord(
                id=int(row["id"]),
                media_type="video",
                url=str(row["object_key"]),
                sort_order=int(row["sort_order"] or 0),
                duration_seconds=(
                    float(row["duration_seconds"]) if row.get("duration_seconds") is not None else None
                ),
            )
            for row in video_rows
            if row.get("object_key")
        )
        return media

    def list_same_series_products(
        self, product: MiniappProductRecord, *, limit: int = 6
    ) -> list[MiniappProductRecord]:
        rows = (
            self._db.execute(
                text(
                    f"""
                    {self._product_select_sql(self._hot_score_sql())}
                    WHERE t.status = 'PUBLISHED'
                      AND t.id != :product_id
                      AND t.category_id = (
                        SELECT category_id FROM tiles WHERE id = :product_id
                      )
                    ORDER BY t.updated_at DESC, t.id DESC
                    LIMIT :limit
                    """
                ),
                {"product_id": product.id, "limit": limit},
            )
            .mappings()
            .all()
        )
        return [self._to_product(dict(row)) for row in rows]

    def list_same_brand_products(
        self,
        product: MiniappProductRecord,
        *,
        exclude_ids: set[int],
        limit: int = 6,
    ) -> list[MiniappProductRecord]:
        params: dict[str, Any] = {
            "product_id": product.id,
            "brand_id": product.brand_id,
            "limit": limit,
        }
        exclude_clause = ""
        for index, product_id in enumerate(sorted(exclude_ids)):
            key = f"exclude_{index}"
            params[key] = product_id
        if exclude_ids:
            exclude_clause = "AND t.id NOT IN ({})".format(
                ", ".join(f":exclude_{index}" for index in range(len(exclude_ids)))
            )
        rows = (
            self._db.execute(
                text(
                    f"""
                    {self._product_select_sql(self._hot_score_sql())}
                    WHERE t.status = 'PUBLISHED'
                      AND t.id != :product_id
                      AND t.brand_id = :brand_id
                      {exclude_clause}
                    ORDER BY hot_score DESC, t.updated_at DESC, t.id DESC
                    LIMIT :limit
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        return [self._to_product(dict(row)) for row in rows]

    def is_favorite(self, *, client_id: str, product_id: int) -> bool:
        row = self._db.execute(
            text(
                """
                SELECT favorite FROM miniapp_sku_favorites
                WHERE client_id = :client_id AND sku_id = :product_id
                """
            ),
            {"client_id": client_id, "product_id": product_id},
        ).scalar_one_or_none()
        return bool(row)

    def set_favorite(self, *, client_id: str, product_id: int, favorite: bool) -> bool:
        now = datetime.now(UTC).isoformat()
        existing = self._db.execute(
            text(
                """
                SELECT id FROM miniapp_sku_favorites
                WHERE client_id = :client_id AND sku_id = :product_id
                """
            ),
            {"client_id": client_id, "product_id": product_id},
        ).scalar_one_or_none()
        if existing is None:
            self._db.execute(
                text(
                    """
                    INSERT INTO miniapp_sku_favorites (
                      client_id, sku_id, favorite, created_at, updated_at
                    ) VALUES (
                      :client_id, :product_id, :favorite, :now, :now
                    )
                    """
                ),
                {
                    "client_id": client_id,
                    "product_id": product_id,
                    "favorite": 1 if favorite else 0,
                    "now": now,
                },
            )
        else:
            self._db.execute(
                text(
                    """
                    UPDATE miniapp_sku_favorites
                    SET favorite = :favorite, updated_at = :now
                    WHERE client_id = :client_id AND sku_id = :product_id
                    """
                ),
                {
                    "client_id": client_id,
                    "product_id": product_id,
                    "favorite": 1 if favorite else 0,
                    "now": now,
                },
            )
        self._db.commit()
        return self.is_favorite(client_id=client_id, product_id=product_id)

    @staticmethod
    def _product_select_sql(hot_score_sql: str) -> str:
        return f"""
            SELECT
              t.id, t.name, t.sku_code, t.size, t.surface_finish,
              t.color_family, t.reference_price, t.remark, t.created_at, t.updated_at,
              b.name AS brand_name,
              b.id AS brand_id,
              b.short_name AS brand_short_name,
              b.logo_object_key AS brand_logo_object_key,
              c.name AS category_name,
              c.path AS category_path,
              s.display_name AS spec_name,
              (
                SELECT ti.object_key FROM tile_images ti
                WHERE ti.tile_id = t.id AND ti.is_main = 1
                ORDER BY ti.sort_order, ti.id LIMIT 1
              ) AS main_image_url,
              ({hot_score_sql}) AS hot_score
            FROM tiles t
            JOIN brands b ON b.id = t.brand_id
            JOIN tile_categories c ON c.id = t.category_id
            LEFT JOIN tile_specs s ON s.id = t.spec_id
        """

    def _hot_score_sql(self) -> str:
        if self._db.bind is not None and self._db.bind.dialect.name == "mysql":
            product_like = """CONCAT('%"product_id": ', t.id, '%')"""
        else:
            product_like = """'%"product_id": ' || t.id || '%'"""
        return """
            SELECT COUNT(*) FROM usage_events ue
            WHERE ue.event_name IN (
              'product_detail_view', 'product_share', 'product_contact_click'
            )
            AND ue.metadata LIKE {product_like}
        """.format(product_like=product_like)

    @staticmethod
    def _product_filters(
        *,
        keyword: str | None,
        category_id: int | None,
        category_level: str | None,
        brand_id: int | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
        filter_type: str | None,
        filter_value: str | None,
        only_new: bool,
    ) -> tuple[str, dict[str, Any]]:
        clauses = ["t.status = 'PUBLISHED'", "b.status = 'ENABLED'", "c.status = 'ENABLED'", "(s.id IS NULL OR s.status = 'ENABLED')"]
        params: dict[str, Any] = {}
        cleaned_keyword = (keyword or "").strip()
        if cleaned_keyword:
            clauses.append(
                """
                (
                  t.name LIKE :keyword OR t.sku_code LIKE :keyword OR b.name LIKE :keyword
                  OR t.size LIKE :keyword OR s.display_name LIKE :keyword
                  OR t.surface_finish LIKE :keyword OR c.name LIKE :keyword
                )
                """
            )
            params["keyword"] = f"%{cleaned_keyword}%"
        if category_id is not None and category_level == "primary":
            clauses.append(
                """
                (
                  t.category_id = :category_id
                  OR t.category_id IN (
                    SELECT child.id
                    FROM tile_categories child
                    WHERE child.parent_id = :category_id
                      AND child.level = 2
                      AND child.status = 'ENABLED'
                  )
                )
                """
            )
            params["category_id"] = category_id
        elif category_id is not None:
            clauses.append("t.category_id = :category_id")
            params["category_id"] = category_id
        if brand_id is not None:
            clauses.append("t.brand_id = :brand_id")
            params["brand_id"] = brand_id
        cleaned_spec = (spec or "").strip()
        if cleaned_spec:
            clauses.append("(s.display_name = :spec OR t.size = :spec)")
            params["spec"] = cleaned_spec
        if price_min is not None:
            clauses.append("t.reference_price >= :price_min")
            params["price_min"] = price_min
        if price_max is not None:
            clauses.append("t.reference_price <= :price_max")
            params["price_max"] = price_max
        cleaned_filter = (filter_value or "").strip()
        if cleaned_filter and filter_type in {"space", "category"}:
            clauses.append("(c.name LIKE :filter_value OR c.path LIKE :filter_value)")
            params["filter_value"] = f"%{cleaned_filter}%"
        elif cleaned_filter and filter_type == "spec":
            clauses.append("(t.size LIKE :filter_value OR s.display_name LIKE :filter_value)")
            params["filter_value"] = f"%{cleaned_filter}%"
        elif cleaned_filter and filter_type == "style":
            clauses.append("t.surface_finish LIKE :filter_value")
            params["filter_value"] = f"%{cleaned_filter}%"
        elif cleaned_filter and filter_type == "color":
            clauses.append("t.color_family LIKE :filter_value")
            params["filter_value"] = f"%{cleaned_filter}%"
        if only_new:
            clauses.append("t.created_at >= datetime('now', '-90 days')")
        return "WHERE " + " AND ".join(clauses), params

    @staticmethod
    def _product_order_sql(*, sort: str, hot_first: bool) -> str:
        if hot_first:
            return "hot_score DESC, t.updated_at DESC, t.id DESC"
        if sort == "price_asc":
            return "CASE WHEN t.reference_price IS NULL THEN 1 ELSE 0 END, t.reference_price ASC, t.updated_at DESC, t.id DESC"
        if sort == "price_desc":
            return "CASE WHEN t.reference_price IS NULL THEN 1 ELSE 0 END, t.reference_price DESC, t.updated_at DESC, t.id DESC"
        return "t.updated_at DESC, t.id DESC"

    @staticmethod
    def _search_product_filters(
        *,
        keyword: str,
        brand: str | None,
        category: str | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
    ) -> tuple[str, dict[str, Any]]:
        cleaned_keyword = keyword.strip()
        clauses = [
            "t.status = 'PUBLISHED'",
            "b.status = 'ENABLED'",
            "c.status = 'ENABLED'",
            "(s.id IS NULL OR s.status = 'ENABLED')",
            """
            (
              t.name LIKE :keyword OR t.sku_code LIKE :keyword OR b.name LIKE :keyword
              OR b.short_name LIKE :keyword OR b.english_name LIKE :keyword
              OR t.size LIKE :keyword OR s.display_name LIKE :keyword
              OR t.surface_finish LIKE :keyword OR t.color_family LIKE :keyword
              OR c.name LIKE :keyword OR c.path LIKE :keyword
            )
            """,
        ]
        params: dict[str, Any] = {
            "keyword": f"%{cleaned_keyword}%",
            "exact_keyword": cleaned_keyword.lower(),
            "prefix_keyword": f"{cleaned_keyword.lower()}%",
        }
        if brand:
            clauses.append("b.name = :brand")
            params["brand"] = brand
        if category:
            clauses.append("(c.name = :category OR c.path LIKE :category_path)")
            params["category"] = category
            params["category_path"] = f"%{category}%"
        if spec:
            clauses.append("(s.display_name = :spec OR t.size = :spec)")
            params["spec"] = spec
        if price_min is not None:
            clauses.append("t.reference_price >= :price_min")
            params["price_min"] = price_min
        if price_max is not None:
            clauses.append("t.reference_price <= :price_max")
            params["price_max"] = price_max
        return "WHERE " + " AND ".join(clauses), params

    @staticmethod
    def _certificate_filters() -> tuple[str, dict[str, Any]]:
        clauses = ["bc.deleted_at IS NULL", "bc.is_visible = 1", "b.status = 'ENABLED'"]
        params: dict[str, Any] = {}
        return "WHERE " + " AND ".join(clauses), params

    @staticmethod
    def _certificate_select_sql() -> str:
        return """
            SELECT
              bc.id, bc.brand_id, bc.name, bc.certificate_no, bc.issuer, bc.type,
              bc.file_url, bc.file_name, bc.file_mime_type, bc.is_permanent,
              bc.effective_date, bc.expiry_date, b.name AS brand_name
            FROM brand_certificates bc
            JOIN brands b ON b.id = bc.brand_id
        """

    @staticmethod
    def _to_named_result(row: dict[str, Any]) -> MiniappNamedResult:
        return MiniappNamedResult(
            id=int(row["id"] or 0),
            name=str(row["name"]),
            count=int(row["count"] or 0),
        )

    @staticmethod
    def _to_certificate(row: dict[str, Any]) -> MiniappCertificateResult:
        return MiniappCertificateResult(
            id=int(row["id"]),
            brand_id=int(row["brand_id"]),
            name=str(row["name"]),
            certificate_no=row.get("certificate_no"),
            issuer=row.get("issuer"),
            type=row.get("type"),
            brand_name=str(row["brand_name"]),
            file_url=str(row["file_url"]),
            file_name=row.get("file_name"),
            file_mime_type=row.get("file_mime_type"),
            is_permanent=bool(row.get("is_permanent")),
            effective_date=row.get("effective_date"),
            expiry_date=row.get("expiry_date"),
        )

    @staticmethod
    def _to_brand(row: dict[str, Any]) -> MiniappBrandRecord:
        return MiniappBrandRecord(
            id=int(row["id"]),
            name=str(row["name"]),
            sort_order=int(row["sort_order"] or 0),
            short_name=row.get("short_name"),
            english_name=row.get("english_name"),
            logo_object_key=row.get("logo_object_key"),
            description=row.get("description"),
            product_count=int(row["product_count"] or 0),
        )

    @staticmethod
    def _to_product(row: dict[str, Any]) -> MiniappProductRecord:
        return MiniappProductRecord(
            id=int(row["id"]),
            name=str(row["name"]),
            sku_code=str(row["sku_code"]),
            size=str(row["size"]),
            surface_finish=str(row["surface_finish"]),
            color_family=row.get("color_family"),
            reference_price=(
                float(row["reference_price"]) if row.get("reference_price") is not None else None
            ),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            brand_name=str(row["brand_name"]),
            category_name=str(row["category_name"]),
            spec_name=row.get("spec_name"),
            main_image_url=row.get("main_image_url"),
            hot_score=int(row["hot_score"] or 0),
            brand_id=int(row["brand_id"]),
            brand_short_name=row.get("brand_short_name"),
            brand_logo_object_key=row.get("brand_logo_object_key"),
            category_path=row.get("category_path"),
            remark=row.get("remark"),
        )
