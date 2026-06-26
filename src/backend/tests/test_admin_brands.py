"""Admin brands API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.modules.media.storage import get_media_storage_client, resolve_media_path
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


def _create_brand(
    client: TestClient,
    headers: dict[str, str],
    *,
    name: str = "Test Brand",
    sort_order: int = 10,
) -> int:
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": name, "sort_order": sort_order},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def test_admin_list_brands(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/brands", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]


def test_employee_can_access_brands_api(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/brands", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_create_brand_success(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={
            "name": "MARBLE PRO",
            "sort_order": 10,
            "short_name": "MARBLE",
            "english_name": "MARBLE PRO",
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "MARBLE PRO"
    assert data["status"] == "ENABLED"
    assert data["sku_count"] == 0


def test_create_brand_duplicate_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    payload = {"name": "DUPE BRAND", "sort_order": 20}
    assert client.post("/api/v1/admin/brands", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/brands", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 30011


def test_invalid_sort_order(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": "Bad Sort", "sort_order": 0},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40020


def test_enable_disable_brand(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers, name="Toggle Brand")

    disable = client.post(f"/api/v1/admin/brands/{brand_id}/disable", headers=headers)
    assert disable.status_code == 200
    assert disable.json()["data"]["status"] == "DISABLED"

    enable = client.post(f"/api/v1/admin/brands/{brand_id}/enable", headers=headers)
    assert enable.status_code == 200
    assert enable.json()["data"]["status"] == "ENABLED"


def test_delete_brand_forbidden_when_enabled(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers, name="Enabled Brand")
    response = client.delete(f"/api/v1/admin/brands/{brand_id}", headers=headers)
    assert response.status_code == 409
    assert response.json()["code"] == 30012


def test_delete_brand_success_when_disabled_and_no_sku(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers, name="Deletable Brand")
    client.post(f"/api/v1/admin/brands/{brand_id}/disable", headers=headers)
    response = client.delete(f"/api/v1/admin/brands/{brand_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_list_brands_with_keyword_filter(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    _create_brand(client, headers, name="Keyword Alpha")
    _create_brand(client, headers, name="Other Beta")

    response = client.get(
        "/api/v1/admin/brands",
        headers=headers,
        params={"keyword": "Alpha"},
    )
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["name"] == "Keyword Alpha"


def test_store_owner_forbidden_on_brands_api(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "store_brand_test", "role": "store_owner"},
    )
    password = create.json()["data"]["initial_password"]
    store_headers = _auth_headers(client, "store_brand_test", password)
    response = client.get("/api/v1/admin/brands", headers=store_headers)
    assert response.status_code == 403


def test_upload_brand_logo_returns_accessible_media_url(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    upload = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.webp", b"webp-logo", "image/webp")},
    )
    assert upload.status_code == 200
    data = upload.json()["data"]
    assert data["object_key"].startswith("original/default/brands/logos/")
    assert data["url"] == f"/media/{data['object_key']}"
    assert data["object_key"] in get_media_storage_client().objects

    media = client.get(data["url"])
    assert media.status_code == 200
    assert media.content == b"webp-logo"


def test_upload_brand_logo_rejects_invalid_mime(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.gif", b"gif-logo", "image/gif")},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 50002


def test_upload_brand_logo_rejects_oversized_file(client: TestClient, monkeypatch) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    monkeypatch.setattr(settings, "max_upload_size_mb", 0)
    response = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.webp", b"webp-logo", "image/webp")},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 50003


def test_upload_endpoints_store_expected_minio_prefixes(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cases = [
        (
            "/api/v1/admin/uploads",
            ("avatar.png", b"avatar", "image/png"),
            "original/default/avatars/",
        ),
        (
            "/api/v1/admin/uploads/brand-logos",
            ("logo.webp", b"logo", "image/webp"),
            "original/default/brands/logos/",
        ),
        (
            "/api/v1/admin/uploads/tile-images",
            ("tile.jpg", b"tile-image", "image/jpeg"),
            "original/default/tiles/pending/images/",
        ),
        (
            "/api/v1/admin/uploads/tile-videos",
            ("tile.mp4", b"tile-video", "video/mp4"),
            "videos/default/tiles/pending/",
        ),
    ]

    storage = get_media_storage_client()
    for url, file_tuple, prefix in cases:
        response = client.post(url, headers=headers, files={"file": file_tuple})
        assert response.status_code == 200
        object_key = response.json()["data"]["object_key"]
        assert object_key.startswith(prefix)
        assert object_key in storage.objects


def test_upload_returns_storage_unavailable_when_minio_write_fails(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    storage = get_media_storage_client()
    storage.fail_put = True

    response = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.webp", b"webp-logo", "image/webp")},
    )

    assert response.status_code == 502
    assert response.json()["code"] == 50001


def test_media_route_rejects_path_traversal_object_key(client: TestClient) -> None:
    response = client.get("/media/original/default/brands/logos/%2E%2E/secret.webp")
    assert response.status_code == 400
    assert response.json()["code"] == 40040


def test_media_path_rejects_absolute_and_parent_segments() -> None:
    for object_key in ("../secret.webp", "/absolute/secret.webp", "original/../secret.webp"):
        try:
            resolve_media_path(object_key)
        except Exception as exc:
            assert getattr(exc, "status_code", None) == 400
        else:
            raise AssertionError(f"object key should be rejected: {object_key}")


def test_brand_list_returns_accessible_logo_url(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    upload = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.png", b"png-logo", "image/png")},
    )
    upload_data = upload.json()["data"]
    create = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={
            "name": "Logo Brand",
            "sort_order": 10,
            "logo_object_key": upload_data["object_key"],
        },
    )
    assert create.status_code == 200

    response = client.get("/api/v1/admin/brands", headers=headers, params={"keyword": "Logo Brand"})
    assert response.status_code == 200
    item = response.json()["data"]["items"][0]
    assert item["logo_url"] == upload_data["url"]
    assert client.get(item["logo_url"]).status_code == 200


def test_brand_detail_returns_accessible_logo_url(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    upload = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("detail-logo.webp", b"detail-logo", "image/webp")},
    )
    upload_data = upload.json()["data"]
    create = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={
            "name": "Logo Detail Brand",
            "sort_order": 10,
            "logo_object_key": upload_data["object_key"],
        },
    )
    assert create.status_code == 200
    brand_id = create.json()["data"]["id"]

    response = client.get(f"/api/v1/admin/brands/{brand_id}", headers=headers)
    assert response.status_code == 200
    item = response.json()["data"]
    assert item["logo_url"] == upload_data["url"]
    media = client.get(item["logo_url"])
    assert media.status_code == 200
    assert media.content == b"detail-logo"
