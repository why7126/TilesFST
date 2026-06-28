"""Admin tile specs API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401


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


def _create_spec(
    client: TestClient,
    headers: dict[str, str],
    *,
    width_mm: int = 600,
    length_mm: int = 1200,
    sort_order: int = 10,
) -> int:
    response = client.post(
        "/api/v1/admin/tile-specs",
        headers=headers,
        json={
            "width_mm": width_mm,
            "length_mm": length_mm,
            "sort_order": sort_order,
            "remark": "测试规格",
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def test_list_tile_specs(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/tile-specs", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]


def test_create_and_get_tile_spec(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    spec_id = _create_spec(client, headers, width_mm=800, length_mm=800)
    response = client.get(f"/api/v1/admin/tile-specs/{spec_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["display_name"] == "800×800mm"
    assert data["status"] == "ENABLED"


def test_duplicate_tile_spec(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    _create_spec(client, headers, width_mm=300, length_mm=600, sort_order=20)
    response = client.post(
        "/api/v1/admin/tile-specs",
        headers=headers,
        json={"width_mm": 300, "length_mm": 600, "sort_order": 30},
    )
    assert response.status_code == 409
    assert response.json()["code"] == 30041


def test_disable_enable_and_delete(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    spec_id = _create_spec(client, headers, width_mm=100, length_mm=100, sort_order=90)

    blocked_enabled = client.delete(f"/api/v1/admin/tile-specs/{spec_id}", headers=headers)
    assert blocked_enabled.status_code == 409

    disable = client.post(
        f"/api/v1/admin/tile-specs/{spec_id}/disable",
        headers=headers,
    )
    assert disable.status_code == 200
    assert disable.json()["data"]["status"] == "DISABLED"

    deleted = client.delete(f"/api/v1/admin/tile-specs/{spec_id}", headers=headers)
    assert deleted.status_code == 200


def test_employee_can_manage_tile_specs(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/tile-specs", headers=headers)
    assert response.status_code == 200
