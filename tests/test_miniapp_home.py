from __future__ import annotations

from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy import text


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _seed_public_catalog(api_client: TestClient) -> None:
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
                   '灰色', 128.0, '内部备注不可公开', 'PUBLISHED', :now, :now),
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
                  (1, 'tiles/1.webp', '/media/tiles/1.webp', 1, 1),
                  (1, 'tiles/1-detail.webp', '/media/tiles/1-detail.webp', 0, 2),
                  (2, 'tiles/2.webp', '/media/tiles/2.webp', 1, 1),
                  (4, 'tiles/4.webp', '/media/tiles/4.webp', 1, 1)
                """
            )
        )
        db.execute(
            text(
                """
                INSERT INTO tile_videos (tile_id, object_key, file_name, file_size_bytes, duration_seconds, sort_order, created_at)
                VALUES
                  (1, 'videos/1.mp4', '/media/videos/1.mp4', 1024, 8.5, 1, :now)
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
                  sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  (1, '小程序首页轮播', 'MINIAPP_HOME', 'MINIAPP_HOME_CAROUSEL', 'banners/home.webp',
                   'custom_upload', NULL, 'SKU_DETAIL', 1, NULL, NULL, 1,
                   NULL, NULL, 'ONLINE', '内部备注', :now, :now)
                """
            ),
            {"now": now},
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
    assert data["banners"][0]["image_url"] == "/media/banners/home.webp"
    assert [item["title"] for item in data["shortcuts"]] == ["选瓷砖", "品牌馆", "新品榜", "热销榜"]
    assert data["new_products"][0]["sku_code"] in {"FST-001", "FST-002", "FST-004"}
    assert data["new_products"][0]["cover_image"].startswith("/media/tiles/")
    assert data["new_products"][0]["price_display"].startswith("¥")
    assert all(item["price_display"] != "到店咨询" for item in data["new_products"])
    assert all(item["price_display"] != "到店咨询" for item in data["hot_products"])
    assert "remark" not in data["new_products"][0]
    assert "object_key" not in data["banners"][0]
    assert all(item["sku_code"] != "FST-DRAFT" for item in data["new_products"])
    assert any(item["action_type"] in {"copy_wechat", "phone"} for item in data["services"])


def test_miniapp_products_return_has_more_for_waterfall(api_client: TestClient) -> None:
    _seed_public_catalog(api_client)

    response = api_client.get("/api/v1/miniapp/products?page=1&page_size=1")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 3
    assert data["has_more"] is True


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
    assert data["items"][0]["cover_image"] == "/media/tiles/1.webp"
    assert "remark" not in data["items"][0]
    assert "object_key" not in response.text
    assert data["facets"]["brands"][0]["value"] == "1"
    assert data["facets"]["categories"][0]["value"] == "1"
    assert data["facets"]["specs"][0]["value"] == "800×800mm"
    assert any(item["value"] == "100-200" for item in data["facets"]["price_ranges"])


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
                  (2, 1, '通体大理石', 'polished-marble', 2, 2, '内部备注不可公开',
                   'ENABLED', 0, '/客厅/通体大理石', :now, :now),
                  (3, 1, '柔光砖', 'soft-matte', 1, 2, '内部备注不可公开',
                   'ENABLED', 0, '/客厅/柔光砖', :now, :now),
                  (4, 1, '下架分类', 'disabled-child', 0, 2, NULL,
                   'DISABLED', 0, '/客厅/下架分类', :now, :now),
                  (5, NULL, '停用一级', 'disabled-root', 0, 1, NULL,
                   'DISABLED', 0, '/停用一级', :now, :now),
                  (6, 2, '三级分类', 'third-level', 1, 3, NULL,
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
    assert data["version"].startswith("3-")
    assert [item["name"] for item in data["items"]] == ["客厅"]
    assert [item["name"] for item in data["items"][0]["children"]] == ["柔光砖", "通体大理石"]
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

    response = api_client.get("/api/v1/miniapp/categories/tree?depth=2")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == [
        {
            "id": 1,
            "name": "客厅",
            "sort": 1,
            "children": [],
        }
    ]


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
                  sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  (2, 'Web 首页轮播', 'WEB_HOME', 'HOME_TOP_CAROUSEL', 'banners/web.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, 1,
                   NULL, NULL, 'ONLINE', NULL, :now, :now),
                  (3, '专题页顶部 Banner', 'TOPIC', 'TOPIC_TOP_BANNER', 'banners/topic.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, 1,
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
    assert banners[0]["image_url"] == "/media/banners/home.webp"


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
                "contact_type": "copy_wechat",
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
    assert data["image_count"] == 2
    assert data["video_count"] == 1
    assert data["media"][0]["media_type"] == "image"
    assert data["media"][0]["url"] == "/media/tiles/1.webp"
    assert data["media"][-1]["media_type"] == "video"
    assert data["media"][-1]["url"] == "/media/videos/1.mp4"
    assert data["parameters"][0]["label"] == "SKU 编码"
    assert data["category_path"] == ["客厅"]
    assert data["favorite"] is False
    assert data["share"]["path"] == "/pages/tile-detail/index?skuId=1&source=share"
    assert data["same_series_recommendations"][0]["product_id"] in {2, 4}
    assert all(item["product_id"] != 1 for item in data["same_series_recommendations"])
    assert "object_key" not in data
    assert "内部备注" not in response.text
    assert "库存" not in response.text


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
                "parent_category_id": 1,
                "category_index": 1,
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
    assert 6 <= len(data["suggestions"]) <= 10
    assert any(item["entity_type"] == "sku" and "FST-001" in item["text"] for item in data["suggestions"])
    assert all(item["entity_type"] != "certificate" for item in data["suggestions"])
    assert "FST-DRAFT" not in response.text
    assert "检测证书" not in response.text


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
                   '/media/certs/1.pdf', 'certs/1.pdf', 'cert.pdf', 'application/pdf',
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
    assert data["total"] == 2
    assert data["has_more"] is False
    assert data["facets"]["brands"][0]["label"] == "菲尚特"
    assert any(section["entity_type"] == "certificate" for section in data["sections"])
    assert "银河灰检测证书" in response.text
    assert "银河灰内部证书" not in response.text
    assert "FST-DRAFT" not in response.text
    assert "内部备注" not in response.text
    assert "raw_object_key" not in response.text


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
                "sort": "default",
                "filterSnapshot": {"categoryId": "1"},
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
