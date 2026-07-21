from __future__ import annotations

from datetime import UTC, datetime, timedelta

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
    assert all(item["price_display"] != "暂无参考价" for item in data["new_products"])
    assert all(item["price_display"] != "暂无参考价" for item in data["hot_products"])
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
                   '灰色', 118.0, '内部备注不可公开', 'DRAFT', :now, :now)
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
    assert data["banners"][0]["image_url"] == "/media/banners/brand-list.webp"
    assert data["items"][0] == {
        "brand_id": 1,
        "brand_name": "菲尚特",
        "brand_short_name": "FST",
        "english_name": "Feishangte",
        "brand_logo_url": "/media/logos/fst.webp",
        "brand_entry_path": "/pages/brand-detail/index?brandId=1",
        "product_count": 3,
        "description": "品牌说明",
        "available": True,
    }
    assert data["items"][1] == {
        "brand_id": 3,
        "brand_name": "无公开 SKU 品牌",
        "brand_short_name": "EMPTY",
        "english_name": "EmptyBrand",
        "brand_logo_url": "/media/logos/empty.webp",
        "brand_entry_path": "/pages/brand-detail/index?brandId=3",
        "product_count": 0,
        "description": "启用品牌可展示",
        "available": True,
    }
    assert "停用品牌" not in response.text
    assert "内部备注" not in response.text
    assert "object_key" not in response.text


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
    assert brand_list["items"][0]["brand_logo_url"] == "/media/logos/fst.webp"
    assert brand_list["items"][0]["brand_entry_path"] == "/pages/brand-detail/index?brandId=1"
    assert brand_list["items"][0]["product_count"] == 3
    assert "停用品牌" not in list_response.text
    assert "内部品牌备注" not in list_response.text

    assert detail_response.status_code == 200
    detail = detail_response.json()["data"]
    assert detail["brand_name"] == "菲尚特"
    assert detail["product_path"] == "/pages/product-list/index?brandId=1&sourcePage=brand-detail"
    assert detail["certificate_count"] == 1
    assert "logo_object_key" not in detail_response.text
    assert "object_key" not in detail_response.text

    assert empty_detail_response.status_code == 200
    empty_detail = empty_detail_response.json()["data"]
    assert empty_detail["brand_name"] == "无公开商品品牌"
    assert empty_detail["product_count"] == 0
    assert empty_detail["product_path"] == "/pages/product-list/index?brandId=3&sourcePage=brand-detail"
    assert empty_detail["certificate_count"] == 0

    assert certificate_response.status_code == 200
    certificates = certificate_response.json()["data"]
    assert certificates["total"] == 1
    assert certificates["items"][0]["certificate_name"] == "绿色建材认证"
    assert certificates["items"][0]["file_url"] == "/media/certificates/green.webp"
    assert "file_key" not in certificate_response.text
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
    assert data["items"][1]["file_kind"] == "pdf"
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
    assert [item["sku_code"] for item in primary_data["items"]] == ["FST-P-022", "FST-P-021", "FST-P-020"]
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
    assert banners[0]["image_url"] == "/media/banners/home.webp"


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
    assert data["share"]["image_url"] == "/media/tiles/1.webp"
    assert data["media"][-1]["media_type"] == "video"
    assert data["media"][-1]["url"] == "/media/videos/1.mp4"
    assert "original/default" not in response.text
    assert "original-upload-name.mp4" not in response.text
    assert data["parameters"][0]["label"] == "SKU 编码"
    assert [item["label"] for item in data["parameters"]] == [
        "SKU 编码",
        "类目",
        "规格",
        "主色系",
        "表面工艺",
    ]
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
    assert any(item["entity_type"] == "sku" and "FST-001" in item["text"] for item in data["suggestions"])
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
    assert data["best_match"]["target_path"] == "/pages/search/index?keyword=菲尚特&tab=brand"
    assert data["total"] == 3
    assert any(section["entity_type"] == "brand" and section["count"] == 1 for section in data["sections"])
    assert any(section["entity_type"] == "sku" and section["count"] == 3 for section in data["sections"])


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
                  '/media/certs/ddd.pdf', 'certs/ddd.pdf', 'ddd.pdf', 'application/pdf',
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
