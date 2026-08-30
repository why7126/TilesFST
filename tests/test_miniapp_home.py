from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.exceptions import AppError
from app.modules.media.storage import (
    MEDIA_NOT_FOUND,
    MediaObjectInfo,
    StoredMediaObject,
    set_media_storage_client,
)
from app.services.log_service import EVENT_DEFINITIONS
from app.services.miniapp_home_service import MiniappHomeService
from app.repositories.miniapp_home_repository import MiniappHomeRepository


def _now() -> str:
    return datetime.now(UTC).isoformat()


MINIAPP_DYNAMIC_USAGE_EVENT_SAMPLES = {
    "brand_products_load",
    "brand_products_load_more",
    "certificate_list_load",
    "certificate_list_refresh",
    "certificate_list_load_more",
    "product_list_filter_open",
    "product_list_filter_apply",
    "product_list_sort_change",
    "product_list_refresh",
    "product_list_load_more",
    "miniapp_home_new_product_click",
    "miniapp_home_hot_product_click",
    "miniapp_home_waterfall_product_click",
    "miniapp_home_favorite_visual_click",
}


class _MemoryMediaStorageClient:
    def __init__(self, objects: dict[str, StoredMediaObject] | None = None, *, use_default: bool = True) -> None:
        self.objects = objects or {}
        self.use_default = use_default

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        self.objects[object_key] = StoredMediaObject(content=content, content_type=content_type)

    def get_object(self, object_key: str) -> StoredMediaObject:
        if object_key in self.objects:
            return self.objects[object_key]
        if self.use_default:
            return StoredMediaObject(content=b"image", content_type="image/webp")
        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在")

    def get_object_info(self, object_key: str) -> MediaObjectInfo:
        stored_object = self.get_object(object_key)
        return MediaObjectInfo(
            content_type=stored_object.content_type,
            total_size=stored_object.total_size or len(stored_object.content),
        )

    def get_object_range(self, object_key: str, offset: int, length: int) -> StoredMediaObject:
        stored_object = self.get_object(object_key)
        return StoredMediaObject(
            content=stored_object.content[offset : offset + length],
            content_type=stored_object.content_type,
            total_size=stored_object.total_size or len(stored_object.content),
        )

    def build_direct_read_url(self, object_key: str, expires_seconds: int) -> str:
        return f"https://storage.example.test/{object_key}?expires={expires_seconds}"


@pytest.fixture(autouse=True)
def miniapp_media_storage() -> None:
    set_media_storage_client(_MemoryMediaStorageClient())
    yield
    set_media_storage_client(None)


def test_miniapp_new_product_filter_uses_mysql_date_expression() -> None:
    where, params = MiniappHomeRepository._product_filters(
        keyword=None,
        category_id=None,
        category_level=None,
        brand_id=None,
        spec=None,
        price_min=None,
        price_max=None,
        filter_type=None,
        filter_value=None,
        only_new=True,
        dialect_name="mysql",
    )

    assert "DATE_SUB(UTC_TIMESTAMP(), INTERVAL 90 DAY)" in where
    assert "datetime('now', '-90 days')" not in where
    assert params == {}


def test_miniapp_search_product_filters_brand_fast_path_skips_keyword_like() -> None:
    where, params = MiniappHomeRepository._search_product_filters(
        keyword="菲尚特",
        brand=None,
        category=None,
        spec=None,
        price_min=None,
        price_max=None,
        search_brand_id=1,
    )

    assert "t.brand_id = :search_brand_id" in where
    assert "t.name LIKE :keyword" not in where
    assert "b.name LIKE :keyword" not in where
    assert params["search_brand_id"] == 1
    assert params["exact_keyword"] == "菲尚特"


def _seed_public_catalog(api_client: TestClient) -> None:
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  id, parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES
                  (2, 1, '客厅大板', 'living-slab', 2, 2, NULL, 'ENABLED', 1, '/客厅/客厅大板', :now, :now),
                  (3, 1, '柔光砖', 'soft-tile', 3, 2, NULL, 'ENABLED', 1, '/客厅/柔光砖', :now, :now),
                  (4, 1, '隐藏类目', 'hidden-category', 4, 2, NULL, 'DISABLED', 1, '/客厅/隐藏类目', :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                UPDATE tiles
                SET category_id = CASE id
                  WHEN 2 THEN 3
                  WHEN 4 THEN 2
                  ELSE category_id
                END
                WHERE id IN (2, 4)
                """
            )
        )
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (1, '菲尚特', 1, 'FST', 'Feishangte', 'logos/fst.webp',
                   '品牌说明', 'ENABLED', 2, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  id, parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES
                  (1, NULL, '客厅', 'living-room', 1, 1, NULL, 'ENABLED', 2, '/客厅', :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tile_specs (
                  id, width_mm, length_mm, thickness_mm, unit, display_name,
                  sort_order, status, sku_count, remark, created_at, updated_at
                ) VALUES
                  (1, 800, 800, NULL, 'mm', '800×800mm', 1, 'ENABLED', 2, NULL, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tiles (
                  id, name, sku_code, brand_id, category_id, spec_id, size,
                  surface_finish, color_family, reference_price, remark, status,
                  created_at, updated_at
                ) VALUES
                  (1, '银河灰', 'FST-001', 1, 1, 1, '800×800', '现代简约',
                   '灰色', 128.0, '适合客厅通铺，建议搭配浅色美缝。', 'PUBLISHED', :now, :now),
                  (2, '暖玉白', 'FST-002', 1, 1, 1, '800×800', '轻奢',
                   '白色', 168.0, '内部备注不可公开', 'PUBLISHED', :now, :now),
                  (4, '银河灰柔光', 'FST-004', 1, 1, 1, '800×800', '柔光',
                   '灰色', 138.0, '公开备注', 'PUBLISHED', :now, :now),
                  (3, '草稿砖', 'FST-DRAFT', 1, 1, 1, '800×800', '现代',
                   '灰色', 99.0, '不可见', 'DRAFT', :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tile_images (tile_id, object_key, url, is_main, sort_order)
                VALUES
                  (1, 'tiles/1.webp', '/media/original/default/tiles/1/images/2026/06/1.webp', 1, 1),
                  (1, 'tiles/1-detail.webp', '/media/original/default/tiles/1/images/2026/06/1-detail.webp', 0, 2),
                  (2, 'tiles/2.webp', '/media/original/default/tiles/2/images/2026/06/2.webp', 1, 1),
                  (4, 'tiles/4.webp', '/media/original/default/tiles/4/images/2026/06/4.webp', 1, 1)
                """
            )
        )
        db.execute(
            text(
                """
                INSERT INTO tile_videos (tile_id, object_key, file_name, file_size_bytes, duration_seconds, sort_order, created_at)
                VALUES
                  (1, 'videos/1.mp4', 'original-upload-name.mp4', 1024, 8.5, 1, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO banners (
                  id, title, display_client, position, image_object_key, image_source,
                  sku_gallery_asset_id, jump_type, sku_id, external_url, topic_id,
                  brand_id, sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  (1, '小程序首页轮播', 'MINIAPP_HOME', 'MINIAPP_HOME_CAROUSEL', 'banners/home.webp',
                   'custom_upload', NULL, 'SKU_DETAIL', 1, NULL, NULL, NULL, 1,
                   NULL, NULL, 'ONLINE', '内部备注', :now, :now),
                  (7, '品牌列表页轮播', 'MINIAPP_HOME', 'MINIAPP_BRAND_LIST_CAROUSEL', 'banners/brand-list.webp',
                   'brand_logo', NULL, 'BRAND_DETAIL', NULL, NULL, NULL, 1, 2,
                   NULL, NULL, 'ONLINE', '内部备注', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()


def _set_recall_pin(
    sku_id: int,
    *,
    sort_order: int,
    starts_at: str | None = None,
    ends_at: str | None = None,
) -> None:
    from app.db.session import get_session_factory

    db = get_session_factory()()
    try:
        db.execute(
            text(
                """
                UPDATE tiles
                SET recall_pin_sort_order = :sort_order,
                    recall_pin_starts_at = :starts_at,
                    recall_pin_ends_at = :ends_at
                WHERE id = :id
                """
            ),
            {
                "id": sku_id,
                "sort_order": sort_order,
                "starts_at": starts_at,
                "ends_at": ends_at,
            },
        )
        db.commit()
    finally:
        db.close()


def test_miniapp_home_returns_public_data_and_hides_internal_fields(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get("/api/v1/miniapp/home")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["store"]["name"] == "菲尚特瓷砖馆"
    assert data["banners"][0]["title"] == "小程序首页轮播"
    assert data["banners"][0]["jump_type"] == "product"
    assert data["banners"][0]["image_url"] == "/media/banners/home.display.webp"
    assert data["banners"][0]["thumbnail_url"] == "/media/banners/home.thumb.webp"
    assert data["banners"][0]["display_url"] == "/media/banners/home.display.webp"
    assert [item["title"] for item in data["shortcuts"]] == ["选瓷砖", "品牌馆", "新品榜", "热销榜"]
    assert data["new_products"][0]["sku_code"] in {"FST-001", "FST-002", "FST-004"}
    assert data["new_products"][0]["cover_image"].startswith("/media/tiles/")
    assert data["new_products"][0]["cover_image"].endswith(".thumb.webp")
    assert data["new_products"][0]["price_display"].startswith("¥")
    assert all(item["price_display"] != "到店咨询" for item in data["new_products"])
    assert all(item["price_display"] != "到店咨询" for item in data["hot_products"])
    assert all(item["price_display"] != "暂无参考价" for item in data["new_products"])
    assert all(item["price_display"] != "暂无参考价" for item in data["hot_products"])
    assert "remark" not in data["new_products"][0]
    assert "object_key" not in data["banners"][0]
    assert all(item["sku_code"] != "FST-DRAFT" for item in data["new_products"])
    assert data["services"]
    assert {item["action_type"] for item in data["services"]} == {"none"}
    assert all(item.get("action_value") is None for item in data["services"])


def test_miniapp_public_banners_hide_internal_no_jump_titles(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO banners (
                  id, title, display_client, position, image_object_key, image_source,
                  sku_gallery_asset_id, jump_type, sku_id, external_url, topic_id,
                  brand_id, sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  (901, 'internal-MINIAPP_HOME_NO_JUMP-1786622496149', 'MINIAPP_HOME',
                   'MINIAPP_HOME_CAROUSEL', 'banners/internal-home.webp', 'custom_upload',
                   NULL, 'NO_JUMP', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'ONLINE',
                   '内部标题不得公开', :now, :now),
                  (902, 'internal-MINIAPP_BRAND_LIST_NO_JUMP-1786622496150', 'MINIAPP_HOME',
                   'MINIAPP_BRAND_LIST_CAROUSEL', 'banners/internal-brand.webp', 'custom_upload',
                   NULL, 'NO_JUMP', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'ONLINE',
                   '内部标题不得公开', :now, :now),
                  (903, 'internal-MINIAPP_HOME_SEARCH-1786622496151', 'MINIAPP_HOME',
                   'MINIAPP_HOME_CAROUSEL', 'banners/internal-search.webp', 'custom_upload',
                   NULL, 'TOPIC_PAGE', NULL, NULL, 1, NULL, 0, NULL, NULL, 'ONLINE',
                   '内部标题不得作为搜索词', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    home_response = api_client.get("/api/v1/miniapp/home")
    brand_response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10")

    assert home_response.status_code == 200
    assert brand_response.status_code == 200
    home_banners = home_response.json()["data"]["banners"]
    brand_banners = brand_response.json()["data"]["banners"]
    internal_home_banner = next(item for item in home_banners if item["id"] == 901)
    internal_search_banner = next(item for item in home_banners if item["id"] == 903)
    internal_brand_banner = next(item for item in brand_banners if item["id"] == 902)

    assert internal_home_banner["title"] == ""
    assert internal_home_banner["jump_type"] == "none"
    assert internal_home_banner["search_keyword"] is None
    assert internal_search_banner["title"] == ""
    assert internal_search_banner["jump_type"] == "search"
    assert internal_search_banner["search_keyword"] is None
    assert internal_brand_banner["title"] == ""
    assert internal_brand_banner["jump_type"] == "none"
    assert all("internal" not in item["title"].lower() for item in home_banners + brand_banners)
    assert all("MINIAPP_" not in item["title"] for item in home_banners + brand_banners)
    assert all("NO_JUMP" not in item["title"] for item in home_banners + brand_banners)


def test_miniapp_home_ignores_legacy_contact_settings_for_privacy_contract(
    api_client: TestClient,
) -> None:
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO system_settings (`key`, value, updated_at, updated_by)
                VALUES
                  ('miniapp.contact_phone', '13800000000', :now, NULL),
                  ('miniapp.contact_wechat', 'FeishangteTiles', :now, NULL)
                ON CONFLICT(`key`) DO UPDATE SET
                  value = excluded.value,
                  updated_at = excluded.updated_at
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/home")

    assert response.status_code == 200
    services = response.json()["data"]["services"]
    assert services
    assert {item["action_type"] for item in services} == {"none"}
    assert all(item.get("action_value") is None for item in services)
    assert all(item["key"] not in {"phone", "wechat"} for item in services)


def test_miniapp_products_return_has_more_for_waterfall(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get("/api/v1/miniapp/products?page=1&page_size=1")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 3
    assert data["has_more"] is True


def test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '停用品牌', 2, 'OFF', 'OffBrand', 'logos/off.webp',
                   '内部备注不可公开', 'DISABLED', 1, :now, :now),
                  (3, '无公开 SKU 品牌', 3, 'EMPTY', 'EmptyBrand', 'logos/empty.webp',
                   '启用品牌可展示', 'ENABLED', 0, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tiles (
                  id, name, sku_code, brand_id, category_id, spec_id, size,
                  surface_finish, color_family, reference_price, remark, status,
                  created_at, updated_at
                ) VALUES
                  (5, '停用品牌砖', 'FST-OFF', 2, 1, 1, '800×800', '柔光',
                   '灰色', 118.0, '内部备注不可公开', 'PUBLISHED', :now, :now),
                  (6, '无公开草稿砖', 'FST-EMPTY', 3, 1, 1, '800×800', '柔光',
                   '灰色', 118.0, '内部备注不可公开', 'DRAFT', :now, :now),
                  (7, '隐藏类目砖', 'FST-HIDDEN-CAT', 1, 4, 1, '800×800', '柔光',
                   '灰色', 118.0, '内部备注不可公开', 'PUBLISHED', :now, :now),
                  (8, '客厅大板砖', 'FST-SLAB', 1, 2, 1, '800×800', '柔光',
                   '灰色', 118.0, '公开备注', 'PUBLISHED', :now, :now),
                  (9, '柔光类目砖', 'FST-SOFT-CAT', 1, 3, 1, '800×800', '柔光',
                   '灰色', 118.0, '公开备注', 'PUBLISHED', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 2
    assert data["has_more"] is False
    assert [item["title"] for item in data["banners"]] == ["品牌列表页轮播"]
    assert data["banners"][0]["jump_type"] == "brand"
    assert data["banners"][0]["target_id"] == 1
    assert data["banners"][0]["image_url"] == "/media/banners/brand-list.display.webp"
    assert data["items"][0] == {
        "brand_id": 1,
        "brand_name": "菲尚特",
        "brand_short_name": "FST",
        "english_name": "Feishangte",
        "brand_logo_url": None,
        "brand_logo_thumbnail_url": "/media/logos/fst.thumb.webp",
        "brand_entry_path": "/pages/brand-detail/index?brandId=1",
        "product_count": 5,
        "leaf_category_names": ["客厅", "客厅大板", "柔光砖"],
        "leaf_categories": [
            {"category_id": 1, "category_name": "客厅"},
            {"category_id": 2, "category_name": "客厅大板"},
            {"category_id": 3, "category_name": "柔光砖"},
        ],
        "description": "品牌说明",
        "available": True,
    }
    assert data["items"][1] == {
        "brand_id": 3,
        "brand_name": "无公开 SKU 品牌",
        "brand_short_name": "EMPTY",
        "english_name": "EmptyBrand",
        "brand_logo_url": None,
        "brand_logo_thumbnail_url": "/media/logos/empty.thumb.webp",
        "brand_entry_path": "/pages/brand-detail/index?brandId=3",
        "product_count": 0,
        "leaf_category_names": [],
        "leaf_categories": [],
        "description": "启用品牌可展示",
        "available": True,
    }
    assert "停用品牌" not in response.text
    assert "内部备注" not in response.text
    assert "object_key" not in response.text

    keyword_response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10&keyword=FST")
    assert keyword_response.status_code == 200
    keyword_data = keyword_response.json()["data"]
    assert keyword_data["banners"] == []
    assert keyword_data["total"] == 1
    assert [item["brand_name"] for item in keyword_data["items"]] == ["菲尚特"]

    english_response = api_client.get(
        "/api/v1/miniapp/brands?page=1&pageSize=10&keyword=EmptyBrand"
    )
    assert english_response.status_code == 200
    english_data = english_response.json()["data"]
    assert english_data["banners"] == []
    assert english_data["total"] == 1
    assert [item["brand_name"] for item in english_data["items"]] == ["无公开 SKU 品牌"]

    disabled_response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10&keyword=OffBrand")
    assert disabled_response.status_code == 200
    disabled_data = disabled_response.json()["data"]
    assert disabled_data["banners"] == []
    assert disabled_data["total"] == 0
    assert disabled_data["items"] == []


def test_miniapp_product_list_supports_context_filters_sort_and_facets(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get(
        "/api/v1/miniapp/products",
        params={
            "categoryId": 1,
            "keyword": "银河",
            "brandId": 1,
            "spec": "800×800mm",
            "priceRange": "100-150",
            "sort": "price_asc",
            "page": 1,
            "pageSize": 1,
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["page_size"] == 1
    assert data["total"] == 2
    assert data["has_more"] is True
    assert data["items"][0]["sku_code"] == "FST-001"
    assert data["items"][0]["cover_image"] == "/media/tiles/1.thumb.webp"
    assert "remark" not in data["items"][0]
    assert "object_key" not in response.text
    assert data["facets"]["brands"][0]["value"] == "1"
    assert data["facets"]["categories"][0]["value"] == "1"
    assert data["facets"]["specs"][0]["value"] == "800×800mm"
    assert any(item["value"] == "100-200" for item in data["facets"]["price_ranges"])


def test_miniapp_list_product_cards_skip_media_existence_probe(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed_public_catalog(api_client)

    def fail_media_probe(object_key: str) -> bool:
        raise AssertionError("list product cards must not probe media storage")

    monkeypatch.setattr(MiniappHomeService, "_media_object_exists", fail_media_probe)

    product_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"keyword": "银河", "page": 1, "pageSize": 10},
    )
    search_home_response = api_client.get("/api/v1/miniapp/search/home")

    assert product_response.status_code == 200
    assert search_home_response.status_code == 200
    assert all(
        item["cover_image"].endswith(".thumb.webp")
        for item in product_response.json()["data"]["items"]
    )
    assert all(
        item["cover_image"].endswith(".thumb.webp")
        for item in search_home_response.json()["data"]["recent_browsing"]
    )


def test_miniapp_home_and_detail_recommendation_cards_use_lightweight_media_path(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed_public_catalog(api_client)
    original_variant_urls = MiniappHomeService._image_variant_urls
    calls: list[tuple[str, bool]] = []

    def track_variant_urls(
        cls: type[MiniappHomeService],
        object_key: str,
        *,
        verify_exists: bool = True,
    ) -> dict[str, str | None]:
        calls.append((object_key, verify_exists))
        return original_variant_urls(object_key, verify_exists=verify_exists)

    monkeypatch.setattr(MiniappHomeService, "_image_variant_urls", classmethod(track_variant_urls))

    home_response = api_client.get("/api/v1/miniapp/home")
    detail_response = api_client.get("/api/v1/miniapp/skus/1")

    assert home_response.status_code == 200
    assert detail_response.status_code == 200
    tile_calls = [(key, verify) for key, verify in calls if key.startswith("tiles/")]
    assert any(verify is False for _, verify in tile_calls)
    assert any(verify is True for _, verify in tile_calls)


def test_miniapp_product_list_brand_default_sort_uses_published_at_and_id(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    try:
        db.execute(
            text(
                """
                UPDATE tiles
                SET published_at = CASE id
                    WHEN 1 THEN NULL
                    WHEN 2 THEN '2026-06-01T00:00:00+00:00'
                    WHEN 4 THEN '2026-06-01T00:00:00+00:00'
                    ELSE published_at
                  END,
                  created_at = CASE id
                    WHEN 1 THEN '2026-06-03T00:00:00+00:00'
                    WHEN 2 THEN '2026-05-02T00:00:00+00:00'
                    WHEN 4 THEN '2026-05-03T00:00:00+00:00'
                    ELSE created_at
                  END,
                  updated_at = CASE id
                    WHEN 1 THEN '2026-06-04T00:00:00+00:00'
                    WHEN 2 THEN '2026-06-02T00:00:00+00:00'
                    WHEN 4 THEN '2026-06-03T00:00:00+00:00'
                    ELSE updated_at
                  END,
                  category_id = CASE id
                    WHEN 2 THEN 3
                    WHEN 4 THEN 2
                    ELSE category_id
                  END
                WHERE id IN (1, 2, 4)
                """
            )
        )
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '另一品牌', 2, 'OTHER', 'OtherBrand', 'logos/other.webp',
                   '启用品牌', 'ENABLED', 1, :now, :now)
                """
            ),
            {"now": _now()},
        )
        db.execute(
            text(
                """
                INSERT INTO tiles (
                  id, name, sku_code, brand_id, category_id, spec_id, size,
                  surface_finish, color_family, reference_price, remark, status,
                  published_at, created_at, updated_at
                ) VALUES
                  (5, '其他品牌砖', 'OTH-001', 2, 1, 1, '800×800', '柔光',
                   '灰色', 118.0, NULL, 'PUBLISHED',
                   '2026-05-01T00:00:00+00:00', '2026-05-01T00:00:00+00:00',
                   '2026-07-01T00:00:00+00:00')
                """
            )
        )
        db.commit()
    finally:
        db.close()

    first_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "page": 1, "pageSize": 2},
    )
    second_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "page": 2, "pageSize": 2},
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200
    first_data = first_page.json()["data"]
    second_data = second_page.json()["data"]
    assert first_data["total"] == 3
    assert first_data["has_more"] is True
    assert second_data["has_more"] is False
    merged_codes = [item["sku_code"] for item in first_data["items"] + second_data["items"]]
    assert merged_codes == ["FST-002", "FST-004", "FST-001"]
    assert "OTH-001" not in first_page.text + second_page.text

    new_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "section": "new", "page": 1, "pageSize": 3},
    )
    hot_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "section": "hot", "page": 1, "pageSize": 3},
    )
    price_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "sort": "price_asc", "page": 1, "pageSize": 3},
    )

    assert new_response.status_code == 200
    assert hot_response.status_code == 200
    assert price_response.status_code == 200
    assert [item["sku_code"] for item in new_response.json()["data"]["items"]] == [
        "FST-001",
        "FST-004",
        "FST-002",
    ]
    assert [item["sku_code"] for item in hot_response.json()["data"]["items"]] == [
        "FST-001",
        "FST-004",
        "FST-002",
    ]
    assert [item["sku_code"] for item in price_response.json()["data"]["items"]] == [
        "FST-001",
        "FST-004",
        "FST-002",
    ]


def test_miniapp_product_list_category_and_keyword_default_sort_uses_public_order(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    try:
        db.execute(
            text(
                """
                UPDATE tiles
                SET published_at = CASE id
                    WHEN 1 THEN NULL
                    WHEN 2 THEN '2026-06-01T00:00:00+00:00'
                    WHEN 4 THEN '2026-06-01T00:00:00+00:00'
                    ELSE published_at
                  END,
                  created_at = CASE id
                    WHEN 1 THEN '2026-06-03T00:00:00+00:00'
                    WHEN 2 THEN '2026-05-02T00:00:00+00:00'
                    WHEN 4 THEN '2026-05-03T00:00:00+00:00'
                    ELSE created_at
                  END,
                  updated_at = CASE id
                    WHEN 1 THEN '2026-06-04T00:00:00+00:00'
                    WHEN 2 THEN '2026-06-02T00:00:00+00:00'
                    WHEN 4 THEN '2026-06-03T00:00:00+00:00'
                    ELSE updated_at
                  END,
                  category_id = CASE id
                    WHEN 2 THEN 3
                    WHEN 4 THEN 2
                    ELSE category_id
                  END
                WHERE id IN (1, 2, 4)
                """
            )
        )
        db.commit()
    finally:
        db.close()

    primary_first_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 1, "categoryLevel": "primary", "page": 1, "pageSize": 2},
    )
    primary_second_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 1, "categoryLevel": "primary", "page": 2, "pageSize": 2},
    )
    secondary_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 2, "categoryLevel": "secondary", "page": 1, "pageSize": 2},
    )
    keyword_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"keyword": "FST", "page": 1, "pageSize": 50},
    )
    home_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"page": 1, "pageSize": 3},
    )

    assert primary_first_page.status_code == 200
    assert primary_second_page.status_code == 200
    assert secondary_response.status_code == 200
    assert keyword_response.status_code == 200
    assert home_response.status_code == 200

    primary_codes = [
        item["sku_code"]
        for item in primary_first_page.json()["data"]["items"]
        + primary_second_page.json()["data"]["items"]
    ]
    assert primary_codes == ["FST-002", "FST-004", "FST-001"]
    primary_images = [
        item["cover_image"]
        for item in primary_first_page.json()["data"]["items"]
        + primary_second_page.json()["data"]["items"]
    ]
    assert all(image.startswith("/media/tiles/") for image in primary_images)
    assert all(image.endswith(".thumb.webp") for image in primary_images)
    assert primary_first_page.json()["data"]["has_more"] is True
    assert primary_second_page.json()["data"]["has_more"] is False
    assert [item["sku_code"] for item in secondary_response.json()["data"]["items"]] == ["FST-004"]
    assert secondary_response.json()["data"]["items"][0]["cover_image"] == "/media/tiles/4.thumb.webp"
    assert [item["sku_code"] for item in keyword_response.json()["data"]["items"]] == [
        "FST-002",
        "FST-004",
        "FST-001",
    ]
    assert [item["sku_code"] for item in home_response.json()["data"]["items"]] == [
        "FST-001",
        "FST-004",
        "FST-002",
    ]


def test_miniapp_product_list_recall_pin_applies_before_pagination_and_respects_branches(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    _set_recall_pin(1, sort_order=20)
    _set_recall_pin(2, sort_order=5)
    _set_recall_pin(4, sort_order=10)

    pinned_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "page": 1, "pageSize": 2},
    )
    second_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "page": 2, "pageSize": 2},
    )
    price_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "sort": "price_asc", "page": 1, "pageSize": 3},
    )
    home_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"page": 1, "pageSize": 3},
    )
    new_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "section": "new", "page": 1, "pageSize": 3},
    )
    hot_page = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "section": "hot", "page": 1, "pageSize": 3},
    )

    assert pinned_page.status_code == 200
    assert second_page.status_code == 200
    assert [item["sku_code"] for item in pinned_page.json()["data"]["items"]] == [
        "FST-002",
        "FST-004",
    ]
    assert [
        item["is_recall_pinned"] for item in pinned_page.json()["data"]["items"]
    ] == [True, True]
    assert [item["sku_code"] for item in second_page.json()["data"]["items"]] == ["FST-001"]
    assert [
        item["is_recall_pinned"] for item in second_page.json()["data"]["items"]
    ] == [True]
    assert [item["sku_code"] for item in price_page.json()["data"]["items"]] == [
        "FST-001",
        "FST-004",
        "FST-002",
    ]
    assert all(
        item["is_recall_pinned"] is False for item in price_page.json()["data"]["items"]
    )
    assert [item["sku_code"] for item in home_page.json()["data"]["items"]] == [
        "FST-004",
        "FST-002",
        "FST-001",
    ]
    assert all(item["is_recall_pinned"] is False for item in home_page.json()["data"]["items"])
    assert new_page.status_code == 200
    assert hot_page.status_code == 200
    assert all(item["is_recall_pinned"] is False for item in new_page.json()["data"]["items"])
    assert all(item["is_recall_pinned"] is False for item in hot_page.json()["data"]["items"])


def test_miniapp_product_list_recall_pin_ignores_expired_and_filtered_items(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    _set_recall_pin(
        1,
        sort_order=1,
        starts_at="2099-01-01T00:00:00+00:00",
        ends_at=None,
    )
    _set_recall_pin(2, sort_order=2)
    _set_recall_pin(4, sort_order=3)

    price_filtered_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"brandId": 1, "priceRange": "0-150", "page": 1, "pageSize": 10},
    )
    keyword_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"keyword": "FST", "page": 1, "pageSize": 10},
    )

    assert price_filtered_response.status_code == 200
    assert [item["sku_code"] for item in price_filtered_response.json()["data"]["items"]] == [
        "FST-004",
        "FST-001",
    ]
    assert [
        item["is_recall_pinned"]
        for item in price_filtered_response.json()["data"]["items"]
    ] == [True, False]
    assert keyword_response.status_code == 200
    assert [item["sku_code"] for item in keyword_response.json()["data"]["items"]] == [
        "FST-002",
        "FST-004",
        "FST-001",
    ]
    assert [
        item["is_recall_pinned"] for item in keyword_response.json()["data"]["items"]
    ] == [True, True, False]


def test_miniapp_search_sku_results_apply_recall_pin_but_suggestions_do_not(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    _set_recall_pin(1, sort_order=20)
    _set_recall_pin(4, sort_order=1)

    search_response = api_client.get(
        "/api/v1/miniapp/search?keyword=银河&page=1&page_size=10&request_id=req-pin"
    )
    suggestion_response = api_client.get(
        "/api/v1/miniapp/search/suggestions?keyword=银河&scope=all&limit=8&request_id=req-suggest"
    )

    assert search_response.status_code == 200
    data = search_response.json()["data"]
    assert [item["sku_code"] for item in data["items"]] == ["FST-004", "FST-001"]
    assert [item["is_recall_pinned"] for item in data["items"]] == [True, True]
    sku_section = next(section for section in data["sections"] if section["entity_type"] == "sku")
    assert [item["sku_code"] for item in sku_section["items"]] == ["FST-004", "FST-001"]
    assert [item["is_recall_pinned"] for item in sku_section["items"]] == [True, True]
    assert suggestion_response.status_code == 200
    suggestions = suggestion_response.json()["data"]["suggestions"]
    assert [item["text"] for item in suggestions if item["entity_type"] == "sku"] == [
        "银河灰",
        "银河灰柔光",
    ]


def test_miniapp_brand_home_endpoints_return_public_detail_and_certificates(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '停用品牌', 2, 'OFF', 'OffBrand', 'logos/off.webp',
                   '内部品牌备注', 'DISABLED', 1, :now, :now),
                  (3, '无公开商品品牌', 3, 'EMPTY', 'EmptyBrand', 'logos/empty.webp',
                   '启用品牌可展示详情', 'ENABLED', 0, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES
                  (1, 1, '绿色建材认证', 1, 'GREEN_BUILDING', 'GB-001', '认证机构',
                   '/media/certificates/green.webp', 'certificates/raw-key.webp',
                   'green.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '内部证书备注', NULL, :now, :now),
                  (2, 1, '隐藏证书', 2, 'HONOR', 'HIDE-001', '内部机构',
                   '/media/certificates/hidden.webp', 'certificates/hidden-key.webp',
                   'hidden.webp', 'image/webp', 2048, 1, NULL, NULL, 0,
                   '隐藏备注', NULL, :now, :now),
                  (3, 2, '停用品牌证书', 3, 'QUALITY', 'OFF-001', '内部机构',
                   '/media/certificates/off.webp', 'certificates/off-key.webp',
                   'off.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '停用品牌备注', NULL, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES
                  (101, 1, '/media/certificates/green-main.webp',
                   'certificates/green-main-key.webp', 'green-main.webp',
                   'image/webp', 3072, 1, 0, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    list_response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10")
    detail_response = api_client.get("/api/v1/miniapp/brands/1")
    empty_detail_response = api_client.get("/api/v1/miniapp/brands/3")
    certificate_response = api_client.get("/api/v1/miniapp/brands/1/certificates")
    disabled_response = api_client.get("/api/v1/miniapp/brands/2")

    assert list_response.status_code == 200
    brand_list = list_response.json()["data"]
    assert brand_list["items"][0]["brand_id"] == 1
    assert brand_list["items"][0]["brand_logo_url"] is None
    assert brand_list["items"][0]["brand_logo_thumbnail_url"] == "/media/logos/fst.thumb.webp"
    assert "brand_hero_display_url" not in brand_list["items"][0]
    assert "brand_hero_thumbnail_url" not in brand_list["items"][0]
    assert brand_list["items"][0]["brand_entry_path"] == "/pages/brand-detail/index?brandId=1"
    assert brand_list["items"][0]["product_count"] == 3
    assert brand_list["items"][0]["leaf_category_names"] == ["客厅"]
    assert brand_list["items"][0]["leaf_categories"] == [
        {"category_id": 1, "category_name": "客厅"}
    ]
    assert "停用品牌" not in list_response.text
    assert "内部品牌备注" not in list_response.text

    assert detail_response.status_code == 200
    detail = detail_response.json()["data"]
    assert detail["brand_name"] == "菲尚特"
    assert detail["brand_logo_url"] is None
    assert detail["brand_logo_thumbnail_url"] == "/media/logos/fst.thumb.webp"
    assert detail["brand_hero_display_url"] == "/media/logos/fst.display.webp"
    assert detail["brand_hero_thumbnail_url"] == "/media/logos/fst.thumb.webp"
    assert detail["leaf_category_names"] == ["客厅"]
    assert detail["leaf_categories"] == [{"category_id": 1, "category_name": "客厅"}]
    assert detail["product_path"] == "/pages/product-list/index?brandId=1&sourcePage=brand-detail"
    assert detail["certificate_count"] == 1
    assert "logo_object_key" not in detail_response.text
    assert "object_key" not in detail_response.text

    assert empty_detail_response.status_code == 200
    empty_detail = empty_detail_response.json()["data"]
    assert empty_detail["brand_name"] == "无公开商品品牌"
    assert empty_detail["product_count"] == 0
    assert empty_detail["leaf_category_names"] == []
    assert empty_detail["leaf_categories"] == []
    assert empty_detail["brand_hero_display_url"] == "/media/logos/empty.display.webp"
    assert empty_detail["brand_hero_thumbnail_url"] == "/media/logos/empty.thumb.webp"
    assert empty_detail["product_path"] == "/pages/product-list/index?brandId=3&sourcePage=brand-detail"
    assert empty_detail["certificate_count"] == 0

    assert certificate_response.status_code == 200
    certificates = certificate_response.json()["data"]
    assert certificates["total"] == 1
    assert certificates["items"][0]["certificate_name"] == "绿色建材认证"
    assert certificates["items"][0]["file_url"] == "/media/certificates/green-main.webp"
    assert certificates["items"][0]["thumbnail_url"] == "/media/certificates/green-main.thumb.webp"
    assert "file_key" not in certificate_response.text
    assert "green-main-key" not in certificate_response.text
    assert "内部证书备注" not in certificate_response.text
    assert "隐藏证书" not in certificate_response.text
    assert "停用品牌证书" not in certificate_response.text

    assert disabled_response.status_code == 404
    assert disabled_response.json()["code"] == 30030


def test_miniapp_certificate_list_filters_public_data_and_supports_facets(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    future = (datetime.now(UTC).date() + timedelta(days=80)).isoformat()
    soon = (datetime.now(UTC).date() + timedelta(days=8)).isoformat()
    past = (datetime.now(UTC).date() - timedelta(days=8)).isoformat()
    try:
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '停用品牌', 2, 'OFF', 'OffBrand', 'logos/off.webp',
                   '内部品牌备注', 'DISABLED', 1, :now, :now),
                  (3, '无 Logo 品牌', 3, 'NOLOGO', 'NoLogoBrand', NULL,
                   '公开品牌备注', 'ENABLED', 1, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES
                  (10, 1, '绿色建材认证', 1, 'GREEN_BUILDING', 'GB-001', '认证机构',
                   '/media/certificates/green.webp', 'certificates/raw-green.webp',
                   'green.webp', 'image/webp', 2048, 0, :now, :future, 1,
                   '内部证书备注', NULL, :now, :now),
                  (11, 1, '质检 PDF 报告', 2, 'INSPECTION', 'PDF-001', '检测中心',
                   '/media/certificates/report.pdf', 'certificates/raw-report.pdf',
                   'report.pdf', 'application/pdf', 4096, 0, :now, :soon, 1,
                   'PDF 内部备注', NULL, :now, :now),
                  (12, 1, '过期荣誉证书', 3, 'HONOR', 'EXP-001', '荣誉机构',
                   '/media/certificates/expired.webp', 'certificates/raw-expired.webp',
                   'expired.webp', 'image/webp', 2048, 0, :now, :past, 1,
                   '过期备注', NULL, :now, :now),
                  (13, 1, '隐藏证书', 4, 'QUALITY', 'HIDE-001', '内部机构',
                   '/media/certificates/hidden.webp', 'certificates/raw-hidden.webp',
                   'hidden.webp', 'image/webp', 2048, 1, NULL, NULL, 0,
                   '隐藏备注', NULL, :now, :now),
                  (14, 2, '停用品牌证书', 5, 'QUALITY', 'OFF-001', '内部机构',
                   '/media/certificates/off.webp', 'certificates/raw-off.webp',
                   'off.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '停用品牌备注', NULL, :now, :now),
                  (15, 1, '软删除证书', 6, 'QUALITY', 'DEL-001', '内部机构',
                   '/media/certificates/deleted.webp', 'certificates/raw-deleted.webp',
                   'deleted.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '删除备注', :now, :now, :now)
                """
            ),
            {"now": now, "future": future, "soon": soon, "past": past},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES
                  (110, 10, '/media/certificates/green-main.webp',
                   'certificates/raw-green-main.webp', 'green-main.webp',
                   'image/webp', 3072, 1, 0, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/certificates?page=1&pageSize=2")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert data["has_more"] is True
    assert [item["certificate_id"] for item in data["items"]] == [10, 11]
    assert data["items"][0]["brand_id"] == 1
    assert data["items"][0]["certificate_type_label"] == "绿色建材"
    assert data["items"][0]["validity_status"] == "VALID"
    assert data["items"][0]["file_kind"] == "image"
    assert data["items"][0]["file_url"] is None
    assert data["items"][0]["thumbnail_url"] == "/media/certificates/green-main.thumb.webp"
    assert data["items"][0]["file_name"] == "green-main.webp"
    assert data["items"][1]["file_kind"] == "pdf"
    assert data["items"][1]["file_url"] is None
    assert data["items"][1]["thumbnail_url"] is None
    assert "file_key" not in response.text
    assert "raw-green" not in response.text
    assert "内部证书备注" not in response.text
    assert "隐藏证书" not in response.text
    assert "停用品牌证书" not in response.text
    assert "软删除证书" not in response.text
    assert "facets" not in data

    second_page = api_client.get("/api/v1/miniapp/certificates?page=2&pageSize=2")
    assert second_page.status_code == 200
    assert second_page.json()["data"]["total"] == 3
    assert second_page.json()["data"]["items"][0]["certificate_id"] == 12

    name_filtered = api_client.get("/api/v1/miniapp/certificates?keyword=绿色&page=1&pageSize=10")
    assert name_filtered.status_code == 200
    assert name_filtered.json()["data"]["total"] == 1
    assert [item["certificate_id"] for item in name_filtered.json()["data"]["items"]] == [10]

    brand_filtered = api_client.get("/api/v1/miniapp/certificates?keyword=菲尚特&page=1&pageSize=10")
    assert brand_filtered.status_code == 200
    assert brand_filtered.json()["data"]["total"] == 3

    type_filtered = api_client.get("/api/v1/miniapp/certificates?keyword=检测报告&page=1&pageSize=10")
    assert type_filtered.status_code == 200
    assert type_filtered.json()["data"]["total"] == 1
    assert type_filtered.json()["data"]["items"][0]["certificate_id"] == 11

    hidden_filtered = api_client.get("/api/v1/miniapp/certificates?keyword=隐藏&page=1&pageSize=10")
    assert hidden_filtered.status_code == 200
    assert hidden_filtered.json()["data"]["total"] == 0


def test_miniapp_certificate_list_derives_thumbnail_from_image_key_when_urls_are_empty(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES
                  (16, 1, '生产空 URL 图片证书', 1, 'QUALITY', 'IMG-EMPTY-URL', '质检机构',
                   '', '', '', '', 1, 1, NULL, NULL, 1,
                   '内部证书备注', NULL, :now, :now),
                  (17, 1, '生产空 URL PDF 证书', 2, 'INSPECTION', 'PDF-EMPTY-URL', '检测中心',
                   '', 'files/default/brand-certificates/prod-report.pdf',
                   'prod-report.pdf', 'application/pdf', 4096, 1, NULL, NULL, 1,
                   'PDF 内部备注', NULL, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES
                  (116, 16, '',
                   'images/default/brand-certificates/prod-certificate.webp',
                   'prod-certificate.webp', 'image/webp', 3072, 0, 0, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/certificates?keyword=生产空 URL&page=1&pageSize=10")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 2
    assert [item["certificate_id"] for item in data["items"]] == [16, 17]
    assert data["items"][0]["file_kind"] == "image"
    assert data["items"][0]["file_url"] is None
    assert (
        data["items"][0]["thumbnail_url"]
        == "/media/images/default/brand-certificates/prod-certificate.thumb.webp"
    )
    assert data["items"][0]["file_name"] == "prod-certificate.webp"
    assert data["items"][1]["file_kind"] == "pdf"
    assert data["items"][1]["file_url"] is None
    assert data["items"][1]["thumbnail_url"] is None
    assert "file_key" not in response.text
    assert "内部证书备注" not in response.text
    assert "PDF 内部备注" not in response.text


def test_miniapp_certificate_detail_returns_public_data_and_filters_private_records(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    future = (datetime.now(UTC).date() + timedelta(days=120)).isoformat()
    try:
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '停用品牌', 2, 'OFF', 'OffBrand', 'logos/off.webp',
                   '内部品牌备注', 'DISABLED', 1, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES
                  (20, 1, '绿色建材详情证书', 1, 'GREEN_BUILDING', 'GB-DTL-001', '认证机构',
                   '/media/certificates/legacy.webp', 'certificates/raw-legacy.webp',
                   'legacy.webp', 'image/webp', 2048, 0, :now, :future, 1,
                   '适用于门店公开展示的绿色建材认证说明。', NULL, :now, :now),
                  (21, 1, '旧 PDF 证书', 2, 'INSPECTION', 'PDF-DTL-001', '检测中心',
                   '/media/certificates/legacy.pdf', 'certificates/raw-legacy.pdf',
                   'legacy.pdf', 'application/pdf', 4096, 1, NULL, NULL, 1,
                   'PDF 内部备注', NULL, :now, :now),
                  (22, 1, '隐藏证书详情', 3, 'QUALITY', 'HIDE-DTL', '内部机构',
                   '/media/certificates/hidden.webp', 'certificates/raw-hidden.webp',
                   'hidden.webp', 'image/webp', 2048, 1, NULL, NULL, 0,
                   '隐藏备注', NULL, :now, :now),
                  (23, 2, '停用品牌证书详情', 4, 'QUALITY', 'OFF-DTL', '内部机构',
                   '/media/certificates/off.webp', 'certificates/raw-off.webp',
                   'off.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '停用品牌备注', NULL, :now, :now),
                  (24, 1, '软删除证书详情', 5, 'QUALITY', 'DEL-DTL', '内部机构',
                   '/media/certificates/deleted.webp', 'certificates/raw-deleted.webp',
                   'deleted.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '删除备注', :now, :now, :now),
                  (25, 1, '无 Logo 品牌证书详情', 6, 'QUALITY', 'NOLOGO-DTL', '公开机构',
                   '/media/certificates/no-logo.webp', 'certificates/raw-no-logo.webp',
                   'no-logo.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                   '公开备注', NULL, :now, :now)
                """
            ),
            {"now": now, "future": future},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES
                  (210, 20, '/media/certificates/detail-side.webp',
                   'certificates/raw-detail-side.webp', 'detail-side.webp',
                   'image/webp', 3072, 0, 1, :now, :now),
                  (211, 20, '/media/certificates/detail-main.webp',
                   'certificates/raw-detail-main.webp', 'detail-main.webp',
                   'image/webp', 3072, 1, 9, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/certificates/20")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["certificate_id"] == 20
    assert data["certificate_name"] == "绿色建材详情证书"
    assert data["certificate_type_label"] == "绿色建材"
    assert data["brand"]["brand_entry_path"] == "/pages/brand-detail/index?brandId=1"
    assert data["brand"]["brand_logo_thumbnail_url"] == "/media/logos/fst.thumb.webp"
    assert data["share"]["path"] == "/pages/certificate-detail/index?certificateId=20&source=share"
    assert data["media"][0]["url"] == "/media/certificates/detail-main.display.webp"
    assert data["media"][0]["display_url"] == "/media/certificates/detail-main.display.webp"
    assert data["media"][0]["thumbnail_url"] == "/media/certificates/detail-main.thumb.webp"
    assert data["media"][0]["preview_url"] == "/media/certificates/detail-main.webp"
    assert data["media"][0]["original_url"] == "/media/certificates/detail-main.webp"
    assert data["media"][0]["is_main"] is True
    assert data["media"][1]["url"] == "/media/certificates/detail-side.display.webp"
    assert data["media"][1]["display_url"] == "/media/certificates/detail-side.display.webp"
    assert data["media"][1]["original_url"] == "/media/certificates/detail-side.webp"
    assert data["file_url"] == "/media/certificates/detail-main.webp"
    assert data["main_media"]["url"] == "/media/certificates/detail-main.display.webp"
    assert data["validity_status"] == "VALID"
    assert data["remark"] == "适用于门店公开展示的绿色建材认证说明。"
    assert "file_key" not in response.text
    assert "raw-detail" not in response.text
    assert "logo_object_key" not in response.text

    legacy_response = api_client.get("/api/v1/miniapp/certificates/21")
    assert legacy_response.status_code == 200
    legacy = legacy_response.json()["data"]
    assert legacy["media"][0]["media_type"] == "pdf"
    assert legacy["media"][0]["url"] == "/media/certificates/legacy.pdf"
    assert legacy["media"][0]["display_url"] is None
    assert legacy["media"][0]["thumbnail_url"] is None
    assert legacy["media"][0]["preview_url"] is None
    assert legacy["media"][0]["original_url"] is None
    assert legacy["main_media"]["file_name"] == "legacy.pdf"

    db = get_session_factory()()
    try:
        db.execute(text("UPDATE brands SET logo_object_key = NULL WHERE id = 1"))
        db.commit()
    finally:
        db.close()

    no_logo_response = api_client.get("/api/v1/miniapp/certificates/25")
    assert no_logo_response.status_code == 200
    no_logo = no_logo_response.json()["data"]
    assert no_logo["brand"]["brand_logo_thumbnail_url"] is None
    assert no_logo["brand"]["available"] is True

    for certificate_id in [22, 23, 24, 9999]:
        hidden = api_client.get(f"/api/v1/miniapp/certificates/{certificate_id}")
        assert hidden.status_code == 404
        assert hidden.json()["code"] == 30030
        assert "内部" not in hidden.text
        assert "raw-" not in hidden.text


def test_miniapp_certificate_detail_hides_missing_display_variants_and_avoids_original_cold_load(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    set_media_storage_client(
        _MemoryMediaStorageClient(
            {
                "certificates/detail-main.webp": StoredMediaObject(
                    content=b"original",
                    content_type="image/webp",
                ),
                "certificates/detail-side.webp": StoredMediaObject(
                    content=b"original",
                    content_type="image/webp",
                ),
            },
            use_default=False,
        )
    )
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES (
                  29, 1, '无展示图证书', 1, 'GREEN_BUILDING', 'GB-NO-DISPLAY', '认证机构',
                  '/media/certificates/detail-main.webp', 'certificates/detail-main.webp',
                  'detail-main.webp', 'image/webp', 2048, 1, NULL, NULL, 1,
                  '公开备注', NULL, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES (
                  219, 29, '/media/certificates/detail-main.webp',
                  'certificates/detail-main.webp', 'detail-main.webp',
                  'image/webp', 3072, 1, 0, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/certificates/29")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["media"][0]["media_type"] == "image"
    assert data["media"][0]["display_url"] is None
    assert data["media"][0]["thumbnail_url"] is None
    assert data["media"][0]["url"] == ""
    assert data["media"][0]["preview_url"] == "/media/certificates/detail-main.webp"
    assert data["media"][0]["original_url"] == "/media/certificates/detail-main.webp"
    assert data["main_media"]["url"] == ""
    assert "/media/certificates/detail-main.display.webp" not in response.text
    assert data["main_media"]["thumbnail_url"] is None
    assert data["main_media"]["display_url"] is None


def test_miniapp_certificate_detail_uses_migrated_certificate_image_key_for_variants(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    set_media_storage_client(
        _MemoryMediaStorageClient(
            {
                "images/default/brand-certificates/legacy-cert.jpg": StoredMediaObject(
                    content=b"original",
                    content_type="image/jpeg",
                ),
                "images/default/brand-certificates/legacy-cert.thumb.webp": StoredMediaObject(
                    content=b"thumb",
                    content_type="image/webp",
                ),
                "images/default/brand-certificates/legacy-cert.display.webp": StoredMediaObject(
                    content=b"display",
                    content_type="image/webp",
                ),
            },
            use_default=False,
        )
    )
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES (
                  30, 1, '历史图片证书', 1, 'INSPECTION', 'INS-LEGACY', '检测中心',
                  '/media/files/default/brand-certificates/legacy-cert.jpg',
                  'images/default/brand-certificates/legacy-cert.jpg',
                  'legacy-cert.jpg', 'image/jpeg', 4096, 1, NULL, NULL, 1,
                  '公开备注', NULL, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO brand_certificate_images (
                  id, certificate_id, file_url, file_key, file_name, file_mime_type,
                  file_size_bytes, is_main, sort_order, created_at, updated_at
                ) VALUES (
                  230, 30,
                  '/media/files/default/brand-certificates/legacy-cert.jpg',
                  'images/default/brand-certificates/legacy-cert.jpg',
                  'legacy-cert.jpg', 'image/jpeg', 4096, 1, 0, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/certificates/30")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["media"][0]["url"] == "/media/images/default/brand-certificates/legacy-cert.display.webp"
    assert data["media"][0]["display_url"] == "/media/images/default/brand-certificates/legacy-cert.display.webp"
    assert data["media"][0]["thumbnail_url"] == "/media/images/default/brand-certificates/legacy-cert.thumb.webp"
    assert data["media"][0]["original_url"] == "/media/images/default/brand-certificates/legacy-cert.jpg"
    assert "files/default/brand-certificates/legacy-cert" not in response.text
    assert "file_key" not in response.text


def test_miniapp_product_list_primary_category_aggregates_self_and_enabled_children(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  id, parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES
                  (10, NULL, '空间砖', 'space-tile', 10, 1, NULL,
                   'ENABLED', 4, '/空间砖', :now, :now),
                  (11, 10, '客厅空间砖', 'space-living', 1, 2, NULL,
                   'ENABLED', 1, '/空间砖/客厅空间砖', :now, :now),
                  (12, 10, '卧室空间砖', 'space-bedroom', 2, 2, NULL,
                   'ENABLED', 1, '/空间砖/卧室空间砖', :now, :now),
                  (13, 10, '停用空间砖', 'space-disabled', 3, 2, NULL,
                   'DISABLED', 1, '/空间砖/停用空间砖', :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tiles (
                  id, name, sku_code, brand_id, category_id, spec_id, size,
                  surface_finish, color_family, reference_price, remark, status,
                  created_at, updated_at
                ) VALUES
                  (20, '客厅空间灰', 'FST-P-020', 1, 11, 1, '800×800', '柔光',
                   '灰色', 188.0, NULL, 'PUBLISHED', :now, :now),
                  (21, '卧室空间白', 'FST-P-021', 1, 12, 1, '800×800', '柔光',
                   '白色', 198.0, NULL, 'PUBLISHED', :now, :now),
                  (22, '一级直挂砖', 'FST-P-022', 1, 10, 1, '800×800', '柔光',
                   '灰色', 208.0, NULL, 'PUBLISHED', :now, :now),
                  (23, '停用分类砖', 'FST-P-023', 1, 13, 1, '800×800', '柔光',
                   '灰色', 218.0, NULL, 'PUBLISHED', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    primary_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 10, "categoryLevel": "primary", "page": 1, "pageSize": 50},
    )

    assert primary_response.status_code == 200
    primary_data = primary_response.json()["data"]
    assert primary_data["total"] == 3
    assert [item["sku_code"] for item in primary_data["items"]] == ["FST-P-020", "FST-P-021", "FST-P-022"]
    assert "FST-P-023" not in primary_response.text
    assert {item["value"] for item in primary_data["facets"]["categories"]} == {"10", "11", "12"}

    secondary_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 11, "categoryLevel": "secondary", "page": 1, "pageSize": 50},
    )

    assert secondary_response.status_code == 200
    secondary_data = secondary_response.json()["data"]
    assert secondary_data["total"] == 1
    assert secondary_data["items"][0]["sku_code"] == "FST-P-020"

    invalid_response = api_client.get(
        "/api/v1/miniapp/products",
        params={"categoryId": 10, "categoryLevel": "branch"},
    )

    assert invalid_response.status_code == 422
    assert invalid_response.json()["code"] == 40001


def test_miniapp_product_list_filters_unpublished_and_disabled_relations(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brands (
                  id, name, sort_order, short_name, english_name, logo_object_key,
                  description, status, sku_count, created_at, updated_at
                ) VALUES
                  (2, '停用品牌', 2, 'OFF', 'OffBrand', 'logos/off.webp',
                   '内部备注', 'DISABLED', 1, :now, :now)
                """
            ),
            {"now": now},
        )
        db.execute(
            text(
                """
                INSERT INTO tiles (
                  id, name, sku_code, brand_id, category_id, spec_id, size,
                  surface_finish, color_family, reference_price, remark, status,
                  created_at, updated_at
                ) VALUES
                  (5, '停用品牌砖', 'FST-OFF', 2, 1, 1, '800×800', '柔光',
                   '灰色', 118.0, '内部备注不可公开', 'PUBLISHED', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/products?page=1&pageSize=50")

    assert response.status_code == 200
    assert "FST-OFF" not in response.text
    assert "FST-DRAFT" not in response.text
    assert "内部备注" not in response.text


def test_miniapp_product_list_rejects_invalid_parameters(api_client: TestClient) -> None:
    response = api_client.get("/api/v1/miniapp/products?page=0&pageSize=100&sort=manual")

    assert response.status_code == 422
    assert response.json()["code"] == 40001


def test_miniapp_category_tree_returns_public_two_level_data(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  id, parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES
                  (20, 1, '通体大理石', 'polished-marble', 2, 2, '内部备注不可公开',
                   'ENABLED', 0, '/客厅/通体大理石', :now, :now),
                  (21, 1, '防滑砖', 'anti-slip', 1, 2, '内部备注不可公开',
                   'ENABLED', 0, '/客厅/防滑砖', :now, :now),
                  (22, 1, '下架分类', 'disabled-child', 0, 2, NULL,
                   'DISABLED', 0, '/客厅/下架分类', :now, :now),
                  (23, NULL, '停用一级', 'disabled-root', 0, 1, NULL,
                   'DISABLED', 0, '/停用一级', :now, :now),
                  (24, 20, '三级分类', 'third-level', 1, 3, NULL,
                   'ENABLED', 0, '/客厅/通体大理石/三级分类', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/categories/tree?depth=2")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["version"].startswith("5-")
    assert [item["name"] for item in data["items"]] == ["客厅"]
    assert [item["name"] for item in data["items"][0]["children"]] == [
        "防滑砖",
        "客厅大板",
        "通体大理石",
        "柔光砖",
    ]
    assert data["items"][0]["children"][0]["coverUrl"] == "/media/miniapp/category-placeholder.webp"
    assert "description" not in data["items"][0]
    assert "sku_count" not in data["items"][0]
    assert "object_key" not in response.text
    assert "内部备注不可公开" not in response.text
    assert "下架分类" not in response.text
    assert "停用一级" not in response.text
    assert "三级分类" not in response.text


def test_miniapp_category_tree_allows_empty_children(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO tile_categories (
                  id, parent_id, name, code, sort_order, level, description,
                  status, sku_count, path, created_at, updated_at
                ) VALUES
                  (30, NULL, '独立空间', 'empty-root', 5, 1, NULL,
                   'ENABLED', 0, '/独立空间', :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/categories/tree?depth=2")

    assert response.status_code == 200
    data = response.json()["data"]
    empty_root = next(item for item in data["items"] if item["name"] == "独立空间")
    assert empty_root == {"id": 30, "name": "独立空间", "sort": 5, "children": []}


def test_miniapp_home_only_uses_admin_miniapp_home_carousel_banners(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO banners (
                  id, title, display_client, position, image_object_key, image_source,
                  sku_gallery_asset_id, jump_type, sku_id, external_url, topic_id,
                  brand_id, sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  (2, '品牌列表页备用轮播', 'MINIAPP_HOME', 'MINIAPP_BRAND_LIST_CAROUSEL', 'banners/brand-list-extra.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, NULL, 1,
                   NULL, NULL, 'ONLINE', NULL, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/home")

    assert response.status_code == 200
    banners = response.json()["data"]["banners"]
    assert [item["title"] for item in banners] == ["小程序首页轮播"]
    assert banners[0]["image_url"] == "/media/banners/home.display.webp"


def test_miniapp_brand_list_does_not_fallback_to_home_carousel(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    try:
        db.execute(text("DELETE FROM banners WHERE position = 'MINIAPP_BRAND_LIST_CAROUSEL'"))
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/brands?page=1&pageSize=10")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["banners"] == []
    assert data["items"]


def test_miniapp_hot_products_use_usage_events_as_secondary_ranking(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    event_response = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "product_detail_view",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/tile-detail/index?id=1",
            "properties": {
                "product_id": 1,
                "page_path": "/pages/tile-detail/index?id=1",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert event_response.status_code == 200

    response = api_client.get("/api/v1/miniapp/home")

    assert response.status_code == 200
    hot_products = response.json()["data"]["hot_products"]
    assert hot_products[0]["product_id"] == 1
    assert hot_products[0]["is_hot"] is True


def test_miniapp_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "home_contact_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/index/index",
            "properties": {
                "page_path": "/pages/index/index",
                "contact_type": "none",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert accepted.status_code == 200
    assert accepted.json()["data"]["accepted"] is True

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "product_contact_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/tile-detail/index?id=1",
            "properties": {
                "product_id": 1,
                "page_path": "/pages/tile-detail/index?id=1",
                "contact_type": "phone",
                "client_type": "wechat_miniapp",
                "phone": "13800000000",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_certificate_detail_load_failed_usage_event_is_accepted(
    api_client: TestClient,
) -> None:
    for event_name in ["list_search_submit", "list_search_reset"]:
        list_search_event = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": "/pages/certificates/index",
                "properties": {
                    "page_path": "/pages/certificates/index",
                    "sourcePage": "certificate-list",
                    "scope": "certificate",
                    "keyword": "检测报告",
                    "resultCount": 1,
                    "requestId": f"{event_name}-certificate-test",
                    "client_type": "wechat_miniapp",
                },
            },
        )
        assert list_search_event.status_code == 200

    response = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "certificate_detail_load_failed",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/certificate-detail/index",
            "properties": {
                "page_path": "/pages/certificate-detail/index",
                "client_type": "wechat_miniapp",
                "terminal": "wechat_miniapp",
                "certificateId": 1,
                "sourcePage": "certificate-list",
                "sourceModule": "certificate-card",
                "requestId": "debug",
                "errorCode": "detail_request_failed",
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["accepted"] is True


def test_miniapp_sku_detail_returns_public_media_recommendations_and_share(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get("/api/v1/miniapp/skus/1?client_id=client-a")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["product_id"] == 1
    assert data["brand"]["brand_id"] == 1
    assert data["brand"]["brand_logo_url"] == "/media/logos/fst.webp"
    assert data["brand"]["brand_logo_thumbnail_url"] == "/media/logos/fst.thumb.webp"
    assert data["brand"]["brand_entry_path"] == "/pages/brand-detail/index?brandId=1"
    assert data["image_count"] == 2
    assert data["video_count"] == 1
    assert data["media"][0]["media_type"] == "image"
    assert data["media"][0]["url"] == "/media/tiles/1.display.webp"
    assert data["media"][0]["display_url"] == "/media/tiles/1.display.webp"
    assert data["media"][0]["thumbnail_url"] == "/media/tiles/1.thumb.webp"
    assert data["media"][0]["preview_url"] == "/media/tiles/1.webp"
    assert data["media"][0]["original_url"] == "/media/tiles/1.webp"
    assert data["cover_image"] == "/media/tiles/1.thumb.webp"
    assert data["thumbnail_url"] == "/media/tiles/1.thumb.webp"
    assert data["display_url"] == "/media/tiles/1.display.webp"
    assert data["original_url"] == "/media/tiles/1.webp"
    assert data["share"]["image_url"] == "/media/tiles/1.display.webp"
    assert data["media"][-1]["media_type"] == "video"
    assert data["media"][-1]["url"] == "/media/videos/1.mp4"
    assert data["media"][-1]["cover_url"] == "/media/tiles/1.thumb.webp"
    assert "original/default" not in response.text
    assert "original-upload-name.mp4" not in response.text
    assert [item["label"] for item in data["parameters"]] == [
        "类目",
        "规格",
        "主色系",
        "表面工艺",
    ]
    assert all(item["label"] != "SKU 编码" for item in data["parameters"])
    assert "FST-001" not in data["share"]["title"]
    assert data["category_path"] == ["客厅"]
    assert data["favorite"] is False
    assert data["share"]["path"] == "/pages/tile-detail/index?skuId=1&source=share"
    assert data["remark"] == "适合客厅通铺，建议搭配浅色美缝。"
    assert data["same_series_recommendations"][0]["product_id"] in {2, 4}
    assert data["same_series_recommendations"][0]["cover_image"].startswith("/media/tiles/")
    assert data["same_series_recommendations"][0]["cover_image"].endswith(".thumb.webp")
    assert all(item["product_id"] != 1 for item in data["same_series_recommendations"])
    assert "object_key" not in data
    assert "内部备注" not in response.text
    assert "库存" not in response.text


def test_miniapp_sku_detail_hides_missing_display_variants_and_avoids_original_cold_load(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    set_media_storage_client(
        _MemoryMediaStorageClient(
            {
                "tiles/1.webp": StoredMediaObject(content=b"original", content_type="image/webp"),
                "tiles/1-detail.webp": StoredMediaObject(content=b"original", content_type="image/webp"),
            },
            use_default=False,
        )
    )

    response = api_client.get("/api/v1/miniapp/skus/1?client_id=client-a")

    assert response.status_code == 200
    data = response.json()["data"]
    image_media = [item for item in data["media"] if item["media_type"] == "image"]
    assert image_media
    assert all(item["display_url"] is None for item in image_media)
    assert all(item["thumbnail_url"] is None for item in image_media)
    assert all(item["url"] == "" for item in image_media)
    assert all(item["original_url"].endswith(".webp") for item in image_media)
    assert "/media/tiles/1.display.webp" not in response.text
    assert "/media/tiles/1.thumb.webp" not in response.text
    assert data["display_url"] is None
    assert data["thumbnail_url"] is None
    assert data["cover_image"] is None
    assert data["share"]["image_url"] is None


def test_miniapp_sku_detail_omits_empty_or_placeholder_remark(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    try:
        db.execute(text("UPDATE tiles SET status = 'PUBLISHED', remark = ' undefined ' WHERE id = 3"))
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/skus/3")

    assert response.status_code == 200
    assert response.json()["data"]["remark"] is None


def test_miniapp_sku_detail_rejects_unpublished_sku(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get("/api/v1/miniapp/skus/3")

    assert response.status_code == 404
    assert response.json()["code"] == 30030


def test_miniapp_sku_favorite_is_idempotent_and_reflected_in_detail(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    payload = {"client_id": "client-a", "favorite": True}

    first = api_client.put("/api/v1/miniapp/skus/1/favorite", json=payload)
    second = api_client.put("/api/v1/miniapp/skus/1/favorite", json=payload)
    detail = api_client.get("/api/v1/miniapp/skus/1?client_id=client-a")
    cancel = api_client.put(
        "/api/v1/miniapp/skus/1/favorite",
        json={"client_id": "client-a", "favorite": False},
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["data"] == {"sku_id": 1, "favorite": True}
    assert second.json()["data"] == {"sku_id": 1, "favorite": True}
    assert detail.json()["data"]["favorite"] is True
    assert cancel.json()["data"] == {"sku_id": 1, "favorite": False}


def test_miniapp_sku_detail_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "sku_recommend_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/tile-detail/index?skuId=1",
            "properties": {
                "sku_id": 1,
                "target_sku_id": 2,
                "recommend_type": "same_brand",
                "page_path": "/pages/tile-detail/index?skuId=1",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert accepted.status_code == 200

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "sku_load_error",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/tile-detail/index?skuId=1",
            "properties": {
                "sku_id": 1,
                "page_path": "/pages/tile-detail/index?skuId=1",
                "client_type": "wechat_miniapp",
                "error_code": "request_failed",
                "stage": "detail",
                "raw_response": "secret backend body",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001

    for event_name in [
        "sku_video_fullscreen_click",
        "sku_video_fullscreen_enter",
        "sku_video_fullscreen_exit",
        "sku_video_fullscreen_failed",
        "sku_video_action_menu_open",
        "sku_video_action_cancel",
        "sku_video_action_share",
        "sku_video_action_save",
        "sku_video_save_success",
        "sku_video_save_failed",
    ]:
        response = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": "/pages/tile-detail/index?skuId=1",
                "properties": {
                    "sku_id": 1,
                    "media_id": 1000,
                    "page_path": "/pages/tile-detail/index?skuId=1",
                    "client_type": "wechat_miniapp",
                },
            },
        )
        assert response.status_code == 200, response.text


def test_miniapp_home_style_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted_names = [
        (
            "miniapp_home_search_click",
            {"page_path": "/pages/index/index", "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_quick_entry_click",
            {"page_path": "/pages/index/index", "entry_key": "new", "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_waterfall_product_click",
            {"page_path": "/pages/index/index", "product_id": 1, "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_favorite_visual_click",
            {"page_path": "/pages/index/index", "product_id": 1, "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_certificate_tab_click",
            {"page_path": "/pages/certificates/index", "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_waterfall_load",
            {"page_path": "/pages/index/index", "page": 1, "page_size": 12, "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_waterfall_load_failed",
            {"page_path": "/pages/index/index", "page": 2, "reason": "request_failed", "client_type": "wechat_miniapp"},
        ),
        (
            "miniapp_home_waterfall_end_reached",
            {"page_path": "/pages/index/index", "page": 2, "total": 12, "client_type": "wechat_miniapp"},
        ),
    ]
    for event_name, properties in accepted_names:
        response = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": properties["page_path"],
                "properties": properties,
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["data"]["accepted"] is True

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "miniapp_home_quick_entry_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/index/index",
            "properties": {
                "page_path": "/pages/index/index",
                "entry_key": "brand",
                "client_type": "wechat_miniapp",
                "authorization": "Bearer secret",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_brand_list_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "brand_list_card_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/brands/index",
            "properties": {
                "page_path": "/pages/brands/index",
                "brandId": 1,
                "positionIndex": 0,
                "sourcePage": "brand-list",
                "sourceEntry": "tabbar",
                "requestId": "brand-test",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert accepted.status_code == 200

    category_click = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "brand_list_category_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/brands/index",
            "properties": {
                "page_path": "/pages/brands/index",
                "brandId": 1,
                "categoryId": 2,
                "positionIndex": 0,
                "categoryIndex": 1,
                "sourcePage": "brand-list",
                "sourceEntry": "category-chip",
                "requestId": "brand-category-test",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert category_click.status_code == 200

    for event_name in ["list_search_submit", "list_search_reset"]:
        list_search_event = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": "/pages/brand-list/index",
                "properties": {
                    "page_path": "/pages/brand-list/index",
                    "sourcePage": "brand-list",
                    "scope": "brand",
                    "keyword": "携诚",
                    "resultCount": 1,
                    "requestId": f"{event_name}-brand-test",
                    "client_type": "wechat_miniapp",
                },
            },
        )
        assert list_search_event.status_code == 200

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "brand_list_page_view",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/brands/index",
            "properties": {
                "page_path": "/pages/brands/index",
                "sourcePage": "tabbar",
                "resultCount": 1,
                "requestId": "brand-test",
                "client_type": "wechat_miniapp",
                "authorization": "Bearer secret",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_category_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted_names = [
        (
            "category_page_view",
            {"page_path": "/pages/category/index", "has_cache": False, "client_type": "wechat_miniapp"},
        ),
        (
            "primary_category_click",
            {
                "page_path": "/pages/category/index",
                "category_id": 1,
                "category_index": 0,
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "secondary_category_click",
            {
                "page_path": "/pages/category/index",
                "category_id": 2,
                "category_name": "柔光砖",
                "category_level": "secondary",
                "parent_category_id": 1,
                "sourcePage": "category",
                "category_index": 1,
                "action": "product_list_entry",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "primary_category_product_list_click",
            {
                "page_path": "/pages/category/index",
                "category_id": 1,
                "category_name": "客厅",
                "category_level": "primary",
                "sourcePage": "category",
                "category_index": 0,
                "action": "product_list_entry",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "category_load_failed",
            {
                "page_path": "/pages/category/index",
                "error_code": "request_failed",
                "has_cache": True,
                "client_type": "wechat_miniapp",
            },
        ),
    ]
    for event_name, properties in accepted_names:
        response = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": properties["page_path"],
                "properties": properties,
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["data"]["accepted"] is True

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "category_load_failed",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/category/index",
            "properties": {
                "page_path": "/pages/category/index",
                "error_code": "request_failed",
                "has_cache": False,
                "client_type": "wechat_miniapp",
                "raw_response": "secret backend body",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_search_suggestions_exclude_certificates_and_unpublished_items(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES (
                  1, 1, '银河灰检测证书', 1, 'QUALITY', 'CERT-001', '质检机构',
                  '/media/certs/1.pdf', 'certs/1.pdf', 'cert.pdf', 'application/pdf',
                  1024, 1, NULL, NULL, 1, '内部备注', NULL, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get(
        "/api/v1/miniapp/search/suggestions?keyword=银河&scope=all&limit=8&request_id=req-1"
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["request_id"] == "req-1"
    assert 1 <= len(data["suggestions"]) <= 8
    assert any(item["entity_type"] == "sku" and item["text"] == "银河灰" for item in data["suggestions"])
    assert all("FST-" not in item["text"] for item in data["suggestions"])
    assert all(item["entity_type"] in {"sku", "brand"} for item in data["suggestions"])
    assert "FST-DRAFT" not in response.text
    assert "检测证书" not in response.text
    assert "entity_type\":\"keyword" not in response.text
    assert "entity_type\":\"category" not in response.text
    assert "entity_type\":\"spec" not in response.text


def test_miniapp_full_search_returns_tabs_facets_certificates_and_public_filter(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES
                  (1, 1, '银河灰检测证书', 1, 'QUALITY', 'CERT-001', '质检机构',
                   '/media/images/default/brand-certificates/1.webp', 'images/default/brand-certificates/1.webp', 'cert.webp', 'image/webp',
                   1024, 1, NULL, NULL, 1, '内部备注', NULL, :now, :now),
                  (2, 1, '银河灰内部证书', 2, 'QUALITY', 'CERT-002', '质检机构',
                   '/media/certs/2.pdf', 'certs/2.pdf', 'cert2.pdf', 'application/pdf',
                   1024, 1, NULL, NULL, 0, '内部备注', NULL, :now, :now)
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/search?keyword=银河&page=1&page_size=2&request_id=req-2")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["request_id"] == "req-2"
    assert [tab["value"] for tab in data["tabs"]] == ["all", "sku", "brand", "category", "certificate"]
    assert data["tabs"][0]["selected"] is True
    assert data["best_match"]["sku_code"] in {"FST-001", "FST-004"}
    assert data["total"] == 3
    assert data["has_more"] is False
    assert data["facets"] == {
        "brands": [],
        "categories": [],
        "specs": [],
        "price_ranges": [],
    }
    certificate_section = next(section for section in data["sections"] if section["entity_type"] == "certificate")
    certificate_item = certificate_section["items"][0]
    assert certificate_item["certificate_type"] == "QUALITY"
    assert certificate_item["certificate_type_label"] == "质量认证"
    assert certificate_item["brand_name"] == "菲尚特"
    assert certificate_item["file_url"] == "/media/images/default/brand-certificates/1.webp"
    assert certificate_item["thumbnail_url"] == "/media/images/default/brand-certificates/1.thumb.webp"
    assert "银河灰检测证书" in response.text
    assert "银河灰内部证书" not in response.text
    assert "FST-DRAFT" not in response.text
    assert "内部备注" not in response.text
    assert "raw_object_key" not in response.text


def test_miniapp_search_best_match_supports_exact_brand_match(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&page=1&page_size=10&request_id=req-brand"
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["best_match"]["entity_type"] == "brand"
    assert data["best_match"]["name"] == "菲尚特"
    assert data["best_match"]["logo_url"] == "/media/logos/fst.webp"
    assert data["best_match"]["target_path"] == "/pages/search/index?keyword=菲尚特&tab=brand"
    assert data["total"] == 4
    brand_section = next(section for section in data["sections"] if section["entity_type"] == "brand")
    assert brand_section["count"] == 1
    assert brand_section["items"][0]["logo_url"] == "/media/logos/fst.webp"
    assert "logo_object_key" not in response.text
    assert any(section["entity_type"] == "sku" and section["count"] == 3 for section in data["sections"])


def test_miniapp_search_load_more_returns_sku_only_payload(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)

    first_response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=all&page=1&page_size=2&request_id=req-brand"
    )
    second_response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=all&page=2&page_size=2&request_id=req-brand"
    )

    assert first_response.status_code == 200
    first_data = first_response.json()["data"]
    assert first_data["has_more"] is True
    assert first_data["best_match"]["entity_type"] == "brand"
    assert any(section["entity_type"] == "brand" for section in first_data["sections"])

    assert second_response.status_code == 200
    second_data = second_response.json()["data"]
    assert second_data["page"] == 2
    assert second_data["has_more"] is False
    assert second_data["best_match"] is None
    assert second_data["recommended_keywords"] == []
    assert second_data["facets"] == {
        "brands": [],
        "categories": [],
        "specs": [],
        "price_ranges": [],
    }
    assert [section["entity_type"] for section in second_data["sections"]] == ["sku"]
    assert len(second_data["sections"][0]["items"]) == 1
    assert second_data["items"][0]["product_name"] == second_data["sections"][0]["items"][0]["product_name"]


def test_miniapp_search_first_page_skips_search_home_hot_score_branch(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed_public_catalog(api_client)
    original_list_search_named_results = MiniappHomeRepository.list_search_named_results

    def fail_hot_score_sql(self: MiniappHomeRepository) -> str:
        raise AssertionError("search first page must not trigger hot_score metadata LIKE")

    def fail_search_facets(self: MiniappHomeRepository, *, keyword: str) -> dict[str, list[object]]:
        raise AssertionError("search first page must not trigger facets aggregation")

    def assert_brand_only_named_results(
        self: MiniappHomeRepository,
        *,
        keyword: str,
        include_category_spec: bool = True,
    ) -> dict[str, list[object]]:
        assert include_category_spec is False
        return original_list_search_named_results(
            self,
            keyword=keyword,
            include_category_spec=include_category_spec,
        )

    monkeypatch.setattr(MiniappHomeRepository, "_hot_score_sql", fail_hot_score_sql)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_facets", fail_search_facets)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_named_results", assert_brand_only_named_results)

    response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=all&page=1&page_size=10&request_id=req-fast"
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["recommended_keywords"] == ["岩板", "柔光砖", "800×800", "客厅", "菲尚特"]
    assert data["best_match"]["entity_type"] == "brand"
    assert any(section["entity_type"] == "sku" for section in data["sections"])
    assert data["facets"] == {
        "brands": [],
        "categories": [],
        "specs": [],
        "price_ranges": [],
    }
    assert all(section["entity_type"] != "category" for section in data["sections"])


def test_miniapp_search_exact_brand_uses_brand_id_fast_path(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed_public_catalog(api_client)
    original_products = MiniappHomeRepository.list_search_products
    product_calls: list[dict[str, object]] = []

    def track_products(self: MiniappHomeRepository, **kwargs: object) -> object:
        product_calls.append(dict(kwargs))
        return original_products(self, **kwargs)

    def fail_named_results(self: MiniappHomeRepository, **kwargs: object) -> dict[str, list[object]]:
        raise AssertionError("exact brand search should reuse brand fast match")

    def fail_media_probe(object_key: str) -> bool:
        raise AssertionError("search card build must not probe media storage")

    monkeypatch.setattr(MiniappHomeRepository, "list_search_products", track_products)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_named_results", fail_named_results)
    monkeypatch.setattr(MiniappHomeService, "_media_object_exists", fail_media_probe)

    response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=all&page=1&page_size=10&request_id=req-brand-fast"
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert product_calls[0]["search_brand_id"] == 1
    assert "search_brand_match;dur=" in response.headers["server-timing"]
    assert "search_sku_list;dur=" in response.headers["server-timing"]
    assert "search_sku_count;dur=" in response.headers["server-timing"]
    assert "search_product_cards;dur=" in response.headers["server-timing"]
    assert "search_certificates;dur=" in response.headers["server-timing"]
    assert data["best_match"]["entity_type"] == "brand"
    assert [section["entity_type"] for section in data["sections"]] == ["brand", "certificate", "sku"]
    assert data["tabs"][0]["count"] == 4


def test_miniapp_search_single_tabs_only_run_required_queries(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed_public_catalog(api_client)

    calls: list[str] = []
    original_products = MiniappHomeRepository.list_search_products
    original_named = MiniappHomeRepository.list_search_named_results
    original_certificates = MiniappHomeRepository.list_search_certificates

    def track_products(self: MiniappHomeRepository, **kwargs: object) -> object:
        calls.append("sku")
        return original_products(self, **kwargs)

    def track_named(self: MiniappHomeRepository, **kwargs: object) -> object:
        calls.append("brand")
        assert kwargs.get("include_category_spec") is False
        return original_named(self, **kwargs)

    def track_certificates(self: MiniappHomeRepository, **kwargs: object) -> object:
        calls.append("certificate")
        return original_certificates(self, **kwargs)

    def fail_search_facets(self: MiniappHomeRepository, *, keyword: str) -> dict[str, list[object]]:
        raise AssertionError("single tabs must not trigger facets aggregation")

    monkeypatch.setattr(MiniappHomeRepository, "list_search_products", track_products)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_named_results", track_named)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_certificates", track_certificates)
    monkeypatch.setattr(MiniappHomeRepository, "list_search_facets", fail_search_facets)

    brand_response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=brand&page=1&page_size=10&request_id=req-brand-only"
    )
    assert brand_response.status_code == 200
    assert calls == []
    brand_data = brand_response.json()["data"]
    assert [section["entity_type"] for section in brand_data["sections"]] == ["brand"]
    assert brand_data["items"] == []
    assert brand_data["has_more"] is False

    calls.clear()
    certificate_response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=certificate&page=1&page_size=10&request_id=req-cert-only"
    )
    assert certificate_response.status_code == 200
    assert calls == ["certificate"]
    assert [section["entity_type"] for section in certificate_response.json()["data"]["sections"]] == ["certificate"]

    calls.clear()
    sku_response = api_client.get(
        "/api/v1/miniapp/search?keyword=菲尚特&tab=sku&page=1&page_size=10&request_id=req-sku-only"
    )
    assert sku_response.status_code == 200
    assert calls == ["sku"]
    assert [section["entity_type"] for section in sku_response.json()["data"]["sections"]] == ["sku"]


def test_miniapp_search_best_match_prefers_sku_then_certificate_match(
    api_client: TestClient,
) -> None:
    _seed_public_catalog(api_client)
    from app.db.session import get_session_factory

    db = get_session_factory()()
    now = _now()
    try:
        db.execute(
            text(
                """
                INSERT INTO brand_certificates (
                  id, brand_id, name, sort_order, type, certificate_no, issuer,
                  file_url, file_key, file_name, file_mime_type, file_size_bytes,
                  is_permanent, effective_date, expiry_date, is_visible, remark,
                  deleted_at, created_at, updated_at
                ) VALUES (
                  1, 1, 'ddd', 1, 'QUALITY', 'CERT-ONLY', '质检机构',
                  '/media/images/default/brand-certificates/ddd.webp', 'images/default/brand-certificates/ddd.webp', 'ddd.webp', 'image/webp',
                  1024, 1, NULL, NULL, 1, '内部备注', NULL, :now, :now
                )
                """
            ),
            {"now": now},
        )
        db.commit()
    finally:
        db.close()

    response = api_client.get("/api/v1/miniapp/search?keyword=FST-001&page=1&page_size=10&request_id=req-sku")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["best_match"]["entity_type"] == "sku"
    assert data["best_match"]["sku_code"] == "FST-001"

    cert_response = api_client.get(
        "/api/v1/miniapp/search?keyword=CERT-ONLY&page=1&page_size=10&request_id=req-cert-only"
    )

    assert cert_response.status_code == 200
    data = cert_response.json()["data"]
    assert data["best_match"]["entity_type"] == "certificate"
    assert data["best_match"]["name"] == "ddd"
    assert data["best_match"]["certificate_type"] == "QUALITY"
    assert data["best_match"]["certificate_type_label"] == "质量认证"
    assert data["best_match"]["file_url"] == "/media/images/default/brand-certificates/ddd.webp"
    assert data["best_match"]["thumbnail_url"] == "/media/images/default/brand-certificates/ddd.thumb.webp"
    assert data["best_match"]["target_path"] == "/pages/search/index?keyword=CERT-ONLY&tab=certificate"


def test_miniapp_search_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "search_filter_apply",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/search/index",
            "properties": {
                "keyword": "银河",
                "normalizedKeyword": "银河",
                "scope": "all",
                "filterSnapshot": {"brand": "菲尚特"},
                "resultCount": 2,
                "sourcePage": "category",
                "requestId": "req-3",
                "client_type": "wechat_miniapp",
            },
        },
    )
    assert accepted.status_code == 200
    assert accepted.json()["data"]["accepted"] is True

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "search_result_click",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/search/index",
            "properties": {
                "keyword": "银河",
                "normalizedKeyword": "银河",
                "scope": "all",
                "entityType": "sku",
                "sourcePage": "category",
                "requestId": "req-4",
                "client_type": "wechat_miniapp",
                "raw_object_key": "tiles/private.webp",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_product_list_usage_events_validate_dictionary_and_forbidden_properties(
    api_client: TestClient,
) -> None:
    accepted_events = [
        (
            "product_list_page_view",
            {
                "page_path": "/pages/product-list/index",
                "sourcePage": "category",
                "categoryId": "1",
                "categoryName": "客厅",
                "categoryLevel": "primary",
                "sort": "default",
                "filterSnapshot": {"categoryId": "1", "categoryLevel": "primary"},
                "resultCount": 2,
                "pageSize": 12,
                "requestId": "plist-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_list_item_click",
            {
                "page_path": "/pages/product-list/index",
                "skuId": 1,
                "sourcePage": "category",
                "positionIndex": 0,
                "requestId": "plist-2",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_list_filter_apply",
            {
                "page_path": "/pages/product-list/index",
                "sourcePage": "search",
                "filterSnapshot": {"brandId": "1", "spec": "800×800mm"},
                "sort": "price_asc",
                "resultCount": 2,
                "requestId": "plist-3",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_list_load_failed",
            {
                "page_path": "/pages/product-list/index",
                "sourcePage": "brand",
                "page": 2,
                "pageSize": 12,
                "errorCode": "load_more_failed",
                "requestId": "plist-4",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_list_share_click",
            {
                "page_path": "/pages/product-list/index",
                "sourcePage": "share",
                "categoryId": "1",
                "categoryName": "客厅",
                "categoryLevel": "primary",
                "keyword": "客厅砖",
                "share_channel": "wechat_friend",
                "share_path": "/pages/product-list/index?categoryId=1&categoryLevel=primary&categoryName=%E5%AE%A2%E5%8E%85&keyword=%E5%AE%A2%E5%8E%85%E7%A0%96&sourcePage=share",
                "requestId": "plist-share",
                "client_type": "wechat_miniapp",
            },
        ),
    ]

    for event_name, properties in accepted_events:
        response = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": "/pages/product-list/index",
                "properties": properties,
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["accepted"] is True

    rejected = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "product_list_item_exposure",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/product-list/index",
            "properties": {
                "skuId": 1,
                "sourcePage": "category",
                "positionIndex": 0,
                "requestId": "plist-5",
                "client_type": "wechat_miniapp",
                "raw_object_key": "tiles/private.webp",
            },
        },
    )
    assert rejected.status_code == 400
    assert rejected.json()["code"] == 40001


def test_miniapp_contract_drift_usage_events_are_registered_and_persisted(
    api_client: TestClient,
) -> None:
    accepted_events = [
        (
            "favorite_list_page_view",
            {
                "page_path": "/pages/favorites/index",
                "terminal": "miniapp",
                "sourcePage": "tabbar",
                "hasLogin": False,
                "resultCount": 2,
                "requestId": "fav-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "favorite_list_load_failed",
            {
                "page_path": "/pages/favorites/index",
                "terminal": "miniapp",
                "sourcePage": "retry",
                "errorCode": "storage_read_failed",
                "requestId": "fav-2",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "favorite_list_empty_action_click",
            {
                "page_path": "/pages/favorites/index",
                "terminal": "miniapp",
                "target": "product_list",
                "requestId": "fav-3",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "favorite_list_item_click",
            {
                "page_path": "/pages/favorites/index",
                "terminal": "miniapp",
                "objectType": "sku",
                "objectId": 1,
                "index": 0,
                "sourcePage": "favorites",
                "hasLogin": False,
                "resultCount": 2,
                "requestId": "fav-4",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "favorite_list_remove",
            {
                "page_path": "/pages/favorites/index",
                "terminal": "miniapp",
                "objectType": "sku",
                "objectId": 1,
                "sourcePage": "favorites",
                "hasLogin": False,
                "resultCount": 1,
                "requestId": "fav-5",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_detail_view",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "brandName": "菲尚特",
                "tab": "products",
                "page": 1,
                "pageSize": 12,
                "resultCount": 3,
                "requestId": "brand-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_detail_load_failed",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "products",
                "page": 1,
                "pageSize": 12,
                "resultCount": 0,
                "requestId": "brand-2",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_detail_tab_click",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "certificates",
                "page": 1,
                "pageSize": 12,
                "resultCount": 2,
                "requestId": "brand-3",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_products_load",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "products",
                "page": 1,
                "pageSize": 12,
                "resultCount": 3,
                "requestId": "brand-4",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_products_load_more",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "products",
                "page": 2,
                "pageSize": 12,
                "resultCount": 6,
                "requestId": "brand-5",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_products_load_failed",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "products",
                "page": 2,
                "pageSize": 12,
                "resultCount": 3,
                "requestId": "brand-6",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_certificates_load",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "certificates",
                "page": 1,
                "pageSize": 12,
                "resultCount": 2,
                "requestId": "brand-7",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_certificates_load_failed",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "certificates",
                "page": 1,
                "pageSize": 12,
                "resultCount": 0,
                "requestId": "brand-8",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_certificate_click",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "certificates",
                "certificateId": 2,
                "index": 0,
                "requestId": "brand-9",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_certificate_image_failed",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "certificates",
                "certificateId": 2,
                "index": 0,
                "requestId": "brand-10",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_detail_share_click",
            {
                "page_path": "/pages/brand-detail/index",
                "sourcePage": "share",
                "sourceModule": "brand_detail",
                "brandId": 1,
                "tab": "products",
                "page": 1,
                "pageSize": 12,
                "resultCount": 3,
                "share_channel": "wechat_timeline",
                "share_path": "/pages/brand-detail/index?brandId=1&source=share",
                "requestId": "brand-share",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_card_exposure",
            {
                "page_path": "/components/product-card/index",
                "skuId": 1,
                "skuCode": "FST-001",
                "sourcePage": "home",
                "sourceModule": "waterfall",
                "listContext": "首页瀑布流",
                "index": 0,
                "requestId": "card-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_card_exposure",
            {
                "page_path": "/components/product-card/index",
                "skuId": 1,
                "skuCode": "FST-001",
                "sourcePage": "home",
                "sourceModule": "waterfall",
                "listContext": "首页瀑布流",
                "index": 0,
                "requestId": "card-batch-1",
                "exposureCount": 2,
                "exposureItems": [
                    {"skuId": 1, "skuCode": "FST-001", "index": 0, "requestId": "card-batch-1"},
                    {"skuId": 2, "skuCode": "FST-002", "index": 1, "requestId": "card-batch-2"},
                ],
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_card_click",
            {
                "page_path": "/components/product-card/index",
                "skuId": 1,
                "skuCode": "FST-001",
                "sourcePage": "home",
                "sourceModule": "waterfall",
                "listContext": "首页瀑布流",
                "index": 0,
                "requestId": "card-2",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_card_unavailable_click",
            {
                "page_path": "/components/product-card/index",
                "sourcePage": "home",
                "sourceModule": "waterfall",
                "listContext": "首页瀑布流",
                "index": 0,
                "requestId": "card-3",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "product_card_image_failed",
            {
                "page_path": "/components/product-card/index",
                "skuId": 1,
                "sourcePage": "home",
                "sourceModule": "waterfall",
                "listContext": "首页瀑布流",
                "index": 0,
                "requestId": "card-4",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_card_click",
            {
                "page_path": "/components/brand-card/index",
                "brandId": 1,
                "brandName": "菲尚特",
                "sourcePage": "sku-detail",
                "sourceModule": "brand-card",
                "skuId": 1,
                "listContext": "SKU 品牌入口",
                "index": 0,
                "requestId": "brand-card-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_card_click",
            {
                "page_path": "/components/brand-card/index",
                "brandId": 1,
                "brandName": "菲尚特",
                "sourcePage": "certificate_detail",
                "sourceModule": "brand_entry",
                "certificateId": 20,
                "listContext": "证书详情品牌入口",
                "index": 0,
                "requestId": "certificate-detail-brand-card-1",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_card_unavailable_click",
            {
                "page_path": "/components/brand-card/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand-card",
                "listContext": "SKU 品牌入口",
                "index": 0,
                "requestId": "brand-card-2",
                "unavailableReason": "missing_brand_name",
                "client_type": "wechat_miniapp",
            },
        ),
        (
            "brand_card_image_failed",
            {
                "page_path": "/components/brand-card/index",
                "brandId": 1,
                "brandName": "菲尚特",
                "sourcePage": "sku-detail",
                "sourceModule": "brand-card",
                "listContext": "SKU 品牌入口",
                "index": 0,
                "requestId": "brand-card-3",
                "client_type": "wechat_miniapp",
            },
        ),
    ]

    for event_name, properties in accepted_events:
        response = api_client.post(
            "/api/v1/usage-events",
            json={
                "event_name": event_name,
                "client_type": "wechat_miniapp",
                "page_path": properties["page_path"],
                "properties": properties,
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["data"]["accepted"] is True

    from app.db.session import get_session_factory

    session = get_session_factory()()
    try:
        persisted = (
            session.execute(
                text(
                    """
                    SELECT event_name, client_type
                    FROM usage_events
                    """
                )
            )
            .mappings()
            .all()
        )
    finally:
        session.close()

    assert {row["event_name"] for row in persisted} == {
        event_name for event_name, _properties in accepted_events
    }
    assert {row["client_type"] for row in persisted} == {"wechat_miniapp"}

    unknown = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "miniapp_contract_drift_unknown",
            "client_type": "wechat_miniapp",
            "page_path": "/pages/favorites/index",
            "properties": {"page_path": "/pages/favorites/index", "client_type": "wechat_miniapp"},
        },
    )
    assert unknown.status_code == 400
    assert unknown.json()["code"] == 40001

    forbidden = api_client.post(
        "/api/v1/usage-events",
        json={
            "event_name": "brand_card_click",
            "client_type": "wechat_miniapp",
            "page_path": "/components/brand-card/index",
            "properties": {
                "page_path": "/components/brand-card/index",
                "sourcePage": "sku-detail",
                "sourceModule": "brand-card",
                "listContext": "SKU 品牌入口",
                "index": 0,
                "requestId": "brand-card-4",
                "client_type": "wechat_miniapp",
                "raw_object_key": "logos/private.webp",
            },
        },
    )
    assert forbidden.status_code == 400
    assert forbidden.json()["code"] == 40001


def test_miniapp_track_literal_events_are_registered_in_backend_dictionary() -> None:
    source_root = Path(__file__).resolve().parents[1] / "src" / "miniapp"
    literal_events: set[str] = set()
    pattern = re.compile(
        r"\b(?:track|trackListEvent|trackDetailEvent|trackCard|trackBrandCard|trackBrandListEvent)"
        r"\(\s*['\"]([a-zA-Z0-9_]+)['\"]"
    )
    for path in source_root.rglob("*.ts"):
        literal_events.update(pattern.findall(path.read_text()))

    missing = sorted((literal_events | MINIAPP_DYNAMIC_USAGE_EVENT_SAMPLES) - set(EVENT_DEFINITIONS))

    assert missing == []
