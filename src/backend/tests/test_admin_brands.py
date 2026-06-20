"""Admin brands API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

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
