"""Profile self-service API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

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


def _create_store_owner() -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if repo.get_by_username("owner01"):
            return
        repo.create_user(
            username="owner01",
            password="Owner12345!",
            display_name="店主一号",
            role="store_owner",
        )
    finally:
        session.close()


def test_get_profile_me_as_admin(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["username"] == "admin"
    assert data["display_name"]
    assert data["role"] == "admin"
    assert "remark" in data


def test_patch_profile_me_validation(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    response = client.patch(
        "/api/v1/profile/me",
        headers=headers,
        json={"email": "not-an-email"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40013


def test_patch_profile_me_success(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    response = client.patch(
        "/api/v1/profile/me",
        headers=headers,
        json={
            "display_name": "Admin Profile",
            "email": "admin@tilesfst.com",
            "phone": "138 0000 2026",
            "remark": "负责资料维护",
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["display_name"] == "Admin Profile"
    assert data["email"] == "admin@tilesfst.com"
    assert data["remark"] == "负责资料维护"


def test_patch_profile_rejects_readonly_fields(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    response = client.patch(
        "/api/v1/profile/me",
        headers=headers,
        json={"username": "hacker", "display_name": "Admin Profile"},
    )
    assert response.status_code == 422


def test_employee_can_access_profile_api(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["role"] == "employee"


def test_store_owner_forbidden_on_profile_api(client: TestClient) -> None:
    _create_store_owner()
    headers = _auth_headers(client, "owner01", "Owner12345!")
    response = client.get("/api/v1/profile/me", headers=headers)
    assert response.status_code == 403


def test_profile_activities_limit_and_order(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    client.patch(
        "/api/v1/profile/me",
        headers=headers,
        json={"display_name": "Audit Admin", "remark": "audit test"},
    )
    response = client.get("/api/v1/profile/me/activities", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]
    assert isinstance(items, list)
    assert len(items) >= 1
    assert len(items) <= 5
    assert items[0]["action_type"] in {"profile_update", "avatar_update", "login"}
    assert "summary" in items[0]
    assert "created_at" in items[0]


def test_profile_activities_caps_at_five(client: TestClient) -> None:
    headers = _auth_headers(client, "admin", "AdminPass123!")
    for index in range(6):
        response = client.patch(
            "/api/v1/profile/me",
            headers=headers,
            json={"remark": f"audit cap test {index}"},
        )
        assert response.status_code == 200
    response = client.get("/api/v1/profile/me/activities", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]
    assert len(items) == 5


def test_login_writes_profile_activity(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/profile/me/activities", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]
    assert any(item["action_type"] == "login" for item in items)


def test_employee_can_upload_avatar(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
        b"\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    upload = client.post(
        "/api/v1/admin/uploads",
        headers=headers,
        files={"file": ("avatar.png", png_bytes, "image/png")},
    )
    assert upload.status_code == 200
    object_key = upload.json()["data"]["object_key"]
    patch = client.patch(
        "/api/v1/profile/me",
        headers=headers,
        json={"avatar_object_key": object_key},
    )
    assert patch.status_code == 200
    assert patch.json()["data"]["avatar_object_key"] == object_key
