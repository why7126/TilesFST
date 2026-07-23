"""Admin dashboard summary API integration tests."""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_employee(username: str = "dashboard_operator") -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if repo.get_by_username(username):
            return
        repo.create_user(
            username=username,
            password="Operator123!",
            display_name="运营账号",
            role="employee",
        )
    finally:
        session.close()


def _create_brand(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": f"Dashboard Brand {suffix}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_category(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={
            "name": f"Dash{suffix}",
            "sort_order": 10,
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_spec(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:4]
    response = client.post(
        "/api/v1/admin/tile-specs",
        headers=headers,
        json={
            "width_mm": 600 + int(suffix[:2], 16) % 200,
            "length_mm": 1200 + int(suffix[2:], 16) % 200,
            "sort_order": 10,
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_sku(client: TestClient, headers: dict[str, str]) -> None:
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json={
            "save_mode": "create",
            "name": "Dashboard Test SKU",
            "sku_code": f"SKU-DSH-{uuid4().hex[:6]}",
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "surface_finish": "亮光面",
            "reference_price": 199.0,
            "images": [
                {
                    "object_key": "tiles/dashboard/main.jpg",
                    "url": "/media/tiles/dashboard/main.jpg",
                    "is_main": True,
                    "sort_order": 0,
                }
            ],
        },
    )
    assert response.status_code == 200


def _create_banner(client: TestClient, headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/admin/banners",
        headers=headers,
        json={
            "title": f"Dashboard Banner {uuid4().hex[:6]}",
            "display_client": "MINIAPP_HOME",
            "position": "MINIAPP_HOME_CAROUSEL",
            "image_object_key": "images/default/banners/dashboard.jpg",
            "image_source": "custom_upload",
            "jump_type": "NO_JUMP",
            "sort_order": 10,
            "status": "DRAFT",
        },
    )
    assert response.status_code == 200


def test_admin_dashboard_summary_uses_real_counts(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    _create_sku(client, headers)
    _create_banner(client, headers)

    response = client.get("/api/v1/admin/dashboard/summary", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    data = body["data"]
    assert data["sku_total"]["value"] == 1
    assert data["brand_total"]["value"] == 1
    assert data["banner_total"]["value"] == 1
    assert data["user_total"]["value"] == 1
    assert data["user_total"]["visible"] is True


def test_admin_dashboard_summary_empty_database_returns_zero(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.get("/api/v1/admin/dashboard/summary", headers=headers)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["sku_total"]["value"] == 0
    assert data["brand_total"]["value"] == 0
    assert data["banner_total"]["value"] == 0
    assert data["user_total"]["value"] == 1


def test_admin_dashboard_summary_requires_admin_auth(client: TestClient) -> None:
    response = client.get("/api/v1/admin/dashboard/summary")

    assert response.status_code == 401
    assert response.json()["code"] == 40102


def test_employee_dashboard_summary_hides_user_total(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "dashboard_operator", "Operator123!")

    response = client.get("/api/v1/admin/dashboard/summary", headers=headers)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["user_total"]["value"] == 0
    assert data["user_total"]["visible"] is False
    assert data["user_total"]["description"] == "仅系统管理员可见"
