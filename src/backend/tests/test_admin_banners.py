"""Admin banners API integration tests."""

from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import text

from app.core.config import settings
from app.db.migrations import BANNER_SCOPE_DELETE_CONDITION, _cleanup_legacy_banner_scope
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login

pytest_plugins = ("tests.test_auth",)


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_employee() -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if repo.get_by_username("operator01"):
            return
        repo.create_user(
            username="operator01",
            password="Operator123!",
            display_name="运营一号",
            role="employee",
        )
    finally:
        session.close()


def _create_brand(
    client: TestClient,
    headers: dict[str, str],
    *,
    logo_object_key: str | None = None,
    name: str | None = None,
) -> int:
    suffix = uuid4().hex[:6]
    payload = {"name": name or f"Banner Brand {suffix}", "sort_order": 10}
    if logo_object_key is not None:
        payload["logo_object_key"] = logo_object_key
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json=payload,
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_category(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": f"Bnr{suffix}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_spec(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:4]
    width = 600 + int(suffix[:2], 16) % 200
    length = 1200 + int(suffix[2:], 16) % 200
    response = client.post(
        "/api/v1/admin/tile-specs",
        headers=headers,
        json={"width_mm": width, "length_mm": length, "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_sku(client: TestClient, headers: dict[str, str]) -> tuple[int, str]:
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    main_key = "images/default/tiles/pending/test-main.jpg"
    response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json={
            "save_mode": "create",
            "name": "Banner Test SKU",
            "sku_code": f"SKU-BNR-{uuid4().hex[:6]}",
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "surface_finish": "亮光面",
            "reference_price": 199.0,
            "images": [
                {
                    "object_key": main_key,
                    "url": f"/media/{main_key}",
                    "is_main": True,
                    "sort_order": 0,
                }
            ],
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"], main_key


def _banner_payload(
    *,
    title: str = "Test Banner",
    jump_type: str = "NO_JUMP",
    sku_id: int | None = None,
    image_object_key: str = "images/default/banners/test.jpg",
    image_source: str = "custom_upload",
    external_url: str | None = None,
    topic_id: int | None = None,
    brand_id: int | None = None,
) -> dict:
    return {
        "title": title,
        "display_client": "MINIAPP_HOME",
        "position": "MINIAPP_HOME_CAROUSEL",
        "image_object_key": image_object_key,
        "image_source": image_source,
        "jump_type": jump_type,
        "sku_id": sku_id,
        "external_url": external_url,
        "topic_id": topic_id,
        "brand_id": brand_id,
        "sort_order": 10,
    }


def _create_banner(client: TestClient, headers: dict[str, str], **kwargs) -> int:
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(**kwargs),
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _assert_error_is_sanitized(response_text: str) -> None:
    forbidden_fragments = [
        "SELECT ",
        "INSERT ",
        "UPDATE ",
        "Traceback",
        "DATABASE_URL",
        "mysql://",
        "mysql+pymysql://",
        "MINIO_SECRET",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in response_text


def test_list_banners_and_summary(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/banners", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]
    assert "filtered_count" in body["data"]["summary"]


def test_employee_can_access_banners(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/banners", headers=headers)
    assert response.status_code == 200


def test_create_banner_default_draft(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    title = f"Draft Banner {uuid4().hex[:6]}"
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(title=title),
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "DRAFT"
    assert data["title"] == title
    assert data["display_client"] == "MINIAPP_HOME"
    assert data["position"] == "MINIAPP_HOME_CAROUSEL"


def test_rejects_legacy_display_client_and_position(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    legacy_client = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json={
            **_banner_payload(title=f"Legacy Client {uuid4().hex[:6]}"),
            "display_client": "WEB_HOME",
        },
    )
    assert legacy_client.status_code == 400
    assert "当前仅支持小程序首页轮播和品牌列表页轮播" in legacy_client.text

    legacy_position = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json={
            **_banner_payload(title=f"Legacy Position {uuid4().hex[:6]}"),
            "position": "HOME_TOP_CAROUSEL",
        },
    )
    assert legacy_position.status_code == 400
    assert "当前仅支持小程序首页轮播和品牌列表页轮播" in legacy_position.text

    brand_list = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json={
            **_banner_payload(title=f"Brand List {uuid4().hex[:6]}"),
            "position": "MINIAPP_BRAND_LIST_CAROUSEL",
        },
    )
    assert brand_list.status_code == 200
    assert brand_list.json()["data"]["position"] == "MINIAPP_BRAND_LIST_CAROUSEL"


def test_create_banner_duplicate_title(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    title = f"Dupe Banner {uuid4().hex[:6]}"
    payload = _banner_payload(title=title)
    assert client.post("/api/v1/admin/banners", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/banners", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 30051


def test_jump_validation_sku_detail(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    sku_id, main_key = _create_sku(client, headers)
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"SKU Banner {uuid4().hex[:6]}",
            jump_type="SKU_DETAIL",
            sku_id=sku_id,
            image_object_key=main_key,
            image_source="sku_main_image",
        ),
    )
    assert response.status_code == 200
    assert response.json()["data"]["sku_id"] == sku_id

    bad = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Bad SKU Banner {uuid4().hex[:6]}",
            jump_type="SKU_DETAIL",
            sku_id=999999,
            image_object_key=main_key,
            image_source="sku_main_image",
        ),
    )
    assert bad.status_code == 400
    assert bad.json()["code"] == 30052


def test_jump_validation_brand_detail(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    logo_key = "images/default/brands/logos/banner-brand.webp"
    brand_id = _create_brand(client, headers, logo_object_key=logo_key)
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Brand Banner {uuid4().hex[:6]}",
            jump_type="BRAND_DETAIL",
            brand_id=brand_id,
            image_object_key=logo_key,
            image_source="brand_logo",
        ),
    )
    assert response.status_code == 200
    assert response.json()["data"]["brand_id"] == brand_id
    assert response.json()["data"]["sku_id"] is None
    assert response.json()["data"]["topic_id"] is None

    bad = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Bad Brand Banner {uuid4().hex[:6]}",
            jump_type="BRAND_DETAIL",
            brand_id=999999,
            image_object_key=logo_key,
            image_source="brand_logo",
        ),
    )
    assert bad.status_code == 400
    assert bad.json()["code"] == 30052
    _assert_error_is_sanitized(bad.text)


def test_brand_detail_banner_custom_upload_and_update_round_trip(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    original_logo = "images/default/brands/logos/banner-edit-original.webp"
    next_logo = "images/default/brands/logos/banner-edit-next.webp"
    original_brand_id = _create_brand(client, headers, logo_object_key=original_logo)
    next_brand_id = _create_brand(client, headers, logo_object_key=next_logo)
    custom_key = "images/default/banners/brand-custom.webp"
    updated_key = "images/default/banners/brand-custom-updated.webp"

    create = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json={
            **_banner_payload(
                title=f"Brand Custom {uuid4().hex[:6]}",
                jump_type="BRAND_DETAIL",
                brand_id=original_brand_id,
                image_object_key=custom_key,
                image_source="custom_upload",
            ),
            "position": "MINIAPP_BRAND_LIST_CAROUSEL",
            "valid_from": "2026-08-01T00:00:00+00:00",
            "valid_to": "2026-08-31T23:59:59+00:00",
            "remark": "create custom upload",
        },
    )
    assert create.status_code == 200
    created = create.json()["data"]
    banner_id = created["id"]
    assert created["brand_id"] == original_brand_id
    assert created["image_source"] == "custom_upload"
    assert created["image_object_key"] == custom_key

    update = client.put(
        f"/api/v1/admin/banners/{banner_id}",
        headers=headers,
        json={
            **_banner_payload(
                title=f"Brand Custom Updated {uuid4().hex[:6]}",
                jump_type="BRAND_DETAIL",
                brand_id=next_brand_id,
                image_object_key=updated_key,
                image_source="custom_upload",
            ),
            "position": "MINIAPP_BRAND_LIST_CAROUSEL",
            "sort_order": 3,
            "valid_from": "2026-09-01T00:00:00+00:00",
            "valid_to": "2026-09-30T23:59:59+00:00",
            "remark": "updated custom upload",
        },
    )
    assert update.status_code == 200
    updated = update.json()["data"]
    assert updated["brand_id"] == next_brand_id
    assert updated["image_source"] == "custom_upload"
    assert updated["image_object_key"] == updated_key
    assert updated["sort_order"] == 3
    assert updated["valid_from"] == "2026-09-01T00:00:00+00:00"
    assert updated["valid_to"] == "2026-09-30T23:59:59+00:00"
    assert updated["remark"] == "updated custom upload"

    detail = client.get(f"/api/v1/admin/banners/{banner_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["brand_id"] == next_brand_id
    listing = client.get(
        "/api/v1/admin/banners",
        headers=headers,
        params={"status": "DRAFT"},
    )
    assert listing.status_code == 200
    listed = [item for item in listing.json()["data"]["items"] if item["id"] == banner_id]
    assert listed and listed[0]["image_object_key"] == updated_key


def test_brand_detail_banner_rejects_disabled_missing_logo_and_logo_mismatch(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    disabled_brand_id = _create_brand(
        client,
        headers,
        logo_object_key="images/default/brands/logos/disabled.webp",
    )
    assert client.post(f"/api/v1/admin/brands/{disabled_brand_id}/disable", headers=headers).status_code == 200

    disabled = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Disabled Brand {uuid4().hex[:6]}",
            jump_type="BRAND_DETAIL",
            brand_id=disabled_brand_id,
            image_object_key="images/default/brands/logos/disabled.webp",
            image_source="brand_logo",
        ),
    )
    assert disabled.status_code == 400
    assert disabled.json()["code"] == 30052
    _assert_error_is_sanitized(disabled.text)

    no_logo_brand_id = _create_brand(client, headers)
    no_logo = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"No Logo Brand {uuid4().hex[:6]}",
            jump_type="BRAND_DETAIL",
            brand_id=no_logo_brand_id,
            image_object_key="images/default/brands/logos/missing.webp",
            image_source="brand_logo",
        ),
    )
    assert no_logo.status_code == 400
    assert no_logo.json()["code"] == 30052
    assert "品牌无 Logo" in no_logo.text
    _assert_error_is_sanitized(no_logo.text)

    logo_key = "images/default/brands/logos/mismatch-real.webp"
    brand_id = _create_brand(client, headers, logo_object_key=logo_key)
    mismatch = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Logo Mismatch {uuid4().hex[:6]}",
            jump_type="BRAND_DETAIL",
            brand_id=brand_id,
            image_object_key="images/default/brands/logos/mismatch-submitted.webp",
            image_source="brand_logo",
        ),
    )
    assert mismatch.status_code == 400
    assert mismatch.json()["code"] == 30052
    assert "品牌 Logo 引用不一致" in mismatch.text
    _assert_error_is_sanitized(mismatch.text)


def test_external_url_validation(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Bad URL {uuid4().hex[:6]}",
            jump_type="EXTERNAL_LINK",
            external_url="http://insecure.example.com",
        ),
    )
    assert response.status_code == 400
    assert response.json()["code"] == 30054

    ok = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Good URL {uuid4().hex[:6]}",
            jump_type="EXTERNAL_LINK",
            external_url="https://example.com/promo",
        ),
    )
    assert ok.status_code == 200


def test_topic_page_jump(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    topics = client.get("/api/v1/admin/topics", headers=headers)
    assert topics.status_code == 200
    items = topics.json()["data"]["items"]
    assert len(items) >= 2
    topic_id = items[0]["id"]
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json=_banner_payload(
            title=f"Topic Banner {uuid4().hex[:6]}",
            jump_type="TOPIC_PAGE",
            topic_id=topic_id,
        ),
    )
    assert response.status_code == 200
    assert response.json()["data"]["topic_id"] == topic_id


def test_online_offline_and_delete_matrix(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    banner_id = _create_banner(client, headers, title=f"Lifecycle {uuid4().hex[:6]}")

    online = client.post(f"/api/v1/admin/banners/{banner_id}/online", headers=headers)
    assert online.status_code == 200
    assert online.json()["data"]["status"] == "ONLINE"

    delete_blocked = client.delete(f"/api/v1/admin/banners/{banner_id}", headers=headers)
    assert delete_blocked.status_code == 409
    assert delete_blocked.json()["code"] == 30053

    offline = client.post(f"/api/v1/admin/banners/{banner_id}/offline", headers=headers)
    assert offline.status_code == 200
    assert offline.json()["data"]["status"] == "OFFLINE"

    delete_ok = client.delete(f"/api/v1/admin/banners/{banner_id}", headers=headers)
    assert delete_ok.status_code == 200


def test_time_status_filter(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    future_from = "2099-01-01T00:00:00+00:00"
    future_to = "2099-12-31T23:59:59+00:00"
    banner_id = _create_banner(
        client,
        headers,
        title=f"Pending {uuid4().hex[:6]}",
    )
    client.put(
        f"/api/v1/admin/banners/{banner_id}",
        headers=headers,
        json={
            **_banner_payload(title=f"Pending {uuid4().hex[:6]}"),
            "valid_from": future_from,
            "valid_to": future_to,
        },
    )
    client.post(f"/api/v1/admin/banners/{banner_id}/online", headers=headers)

    response = client.get(
        "/api/v1/admin/banners",
        headers=headers,
        params={"time_status": "PENDING"},
    )
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()["data"]["items"]]
    assert banner_id in ids


def test_topics_list(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/topics", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) >= 2
    assert all(item["status"] == "ENABLED" for item in items)


def test_banner_image_upload(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
        b"\x0d\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    response = client.post(
        "/api/v1/admin/uploads/banner-images",
        headers=headers,
        files={"file": ("banner.png", BytesIO(png_bytes), "image/png")},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["object_key"].startswith(f"{settings.object_storage_prefix_images.rstrip('/')}/")
    assert "banners" in data["object_key"]
    assert data["url"].startswith("/media/")


def test_banner_image_upload_rejects_invalid_type(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/uploads/banner-images",
        headers=headers,
        files={"file": ("bad.txt", BytesIO(b"not-an-image"), "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 50002


def test_get_update_banner(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    title = f"Update Me {uuid4().hex[:6]}"
    banner_id = _create_banner(client, headers, title=title)

    get_resp = client.get(f"/api/v1/admin/banners/{banner_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["time_status"] is None

    new_title = f"Updated {uuid4().hex[:6]}"
    update = client.put(
        f"/api/v1/admin/banners/{banner_id}",
        headers=headers,
        json=_banner_payload(title=new_title),
    )
    assert update.status_code == 200
    assert update.json()["data"]["title"] == new_title

    legacy_update = client.put(
        f"/api/v1/admin/banners/{banner_id}",
        headers=headers,
        json={
            **_banner_payload(title=f"Legacy Update {uuid4().hex[:6]}"),
            "position": "TOPIC_TOP_BANNER",
        },
    )
    assert legacy_update.status_code == 400
    assert "当前仅支持小程序首页轮播和品牌列表页轮播" in legacy_update.text


def test_legacy_banner_cleanup_removes_old_scope_and_preserves_media_reference(
) -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE banners (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  display_client TEXT NOT NULL,
                  position TEXT NOT NULL,
                  image_object_key TEXT NOT NULL,
                  image_source TEXT NOT NULL,
                  sku_gallery_asset_id INTEGER,
                  jump_type TEXT NOT NULL,
                  sku_id INTEGER,
                  external_url TEXT,
                  topic_id INTEGER,
                  sort_order INTEGER NOT NULL DEFAULT 100,
                  valid_from TEXT,
                  valid_to TEXT,
                  status TEXT NOT NULL DEFAULT 'DRAFT',
                  remark TEXT,
                  created_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO banners (
                  title, display_client, position, image_object_key, image_source,
                  sku_gallery_asset_id, jump_type, sku_id, external_url, topic_id,
                  sort_order, valid_from, valid_to, status, remark, created_at, updated_at
                ) VALUES
                  ('Valid Miniapp', 'MINIAPP_HOME', 'MINIAPP_HOME_CAROUSEL', 'banners/home.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, 1,
                   NULL, NULL, 'DRAFT', NULL, '2026-01-01T00:00:00+00:00', '2026-01-01T00:00:00+00:00'),
                  ('Legacy Web', 'WEB_HOME', 'HOME_TOP_CAROUSEL', 'banners/web.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, 1,
                   NULL, NULL, 'DRAFT', NULL, '2026-01-01T00:00:00+00:00', '2026-01-01T00:00:00+00:00'),
                  ('Legacy Topic', 'TOPIC', 'TOPIC_TOP_BANNER', 'banners/topic.webp',
                   'custom_upload', NULL, 'NO_JUMP', NULL, NULL, NULL, 1,
                   NULL, NULL, 'DRAFT', NULL, '2026-01-01T00:00:00+00:00', '2026-01-01T00:00:00+00:00')
                """
            )
        )
        deleted = _cleanup_legacy_banner_scope(connection)

        assert deleted == 2
        assert "display_client != 'MINIAPP_HOME'" in BANNER_SCOPE_DELETE_CONDITION
        remaining = connection.execute(
            text("SELECT title, image_object_key FROM banners")
        ).mappings().all()
        assert [(row["title"], row["image_object_key"]) for row in remaining] == [
            ("Valid Miniapp", "banners/home.webp")
        ]


def test_banner_not_found(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/banners/999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["code"] == 30050
