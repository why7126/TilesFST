"""Admin banners API integration tests."""

from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


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


def _create_brand(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": f"Banner Brand {suffix}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_category(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": f"Banner Cat {suffix}", "code": f"BNR-CAT-{suffix}", "sort_order": 10},
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
) -> dict:
    return {
        "title": title,
        "display_client": "WEB_HOME",
        "position": "HOME_TOP_CAROUSEL",
        "image_object_key": image_object_key,
        "image_source": image_source,
        "jump_type": jump_type,
        "sku_id": sku_id,
        "external_url": external_url,
        "topic_id": topic_id,
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
    assert data["object_key"].startswith(f"{settings.minio_prefix_images.rstrip('/')}/")
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


def test_banner_not_found(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/banners/999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["code"] == 30050
