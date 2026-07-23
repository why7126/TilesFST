"""System settings API and effective upload limits."""

from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient

from app.core.config import settings
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


def test_get_basic_settings_as_admin(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    response = client.get("/api/v1/admin/system-settings/basic", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    data = body["data"]["data"]
    assert data["platform_name"] == "TILESFST"
    assert data["default_language"] == "zh-CN"


def test_employee_forbidden_on_system_settings(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/system-settings/basic", headers=headers)
    assert response.status_code == 403


def test_patch_and_reset_media_group(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    patch = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"max_image_size_mb": 5},
    )
    assert patch.status_code == 200
    assert patch.json()["data"]["data"]["max_image_size_mb"] == 5

    get_after = client.get("/api/v1/admin/system-settings/media", headers=headers)
    assert get_after.json()["data"]["data"]["max_image_size_mb"] == 5

    reset = client.post("/api/v1/admin/system-settings/media/reset", headers=headers)
    assert reset.status_code == 200
    assert reset.json()["data"]["data"]["max_image_size_mb"] == settings.max_image_size_mb
    assert reset.json()["data"]["data"]["max_file_size_mb"] == settings.max_file_size_mb


def test_patch_media_group_updates_document_file_limit(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    patch = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"max_file_size_mb": 25},
    )
    assert patch.status_code == 200
    assert patch.json()["data"]["data"]["max_file_size_mb"] == 25


def test_patch_media_validation_rejects_invalid_size(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    response = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"max_image_size_mb": 999},
    )
    assert response.status_code == 400

    file_response = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"max_file_size_mb": 999},
    )
    assert file_response.status_code == 400


def test_upload_uses_effective_media_limit(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"max_image_size_mb": 1},
    )

    # 2MB file should exceed 1MB limit
    big_content = b"x" * (2 * 1024 * 1024)
    response = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.jpg", BytesIO(big_content), "image/jpeg")},
    )
    assert response.status_code == 400
    assert response.json()["code"] != 0


def test_security_patch_and_jwt_expire(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    patch = client.patch(
        "/api/v1/admin/system-settings/security",
        headers=headers,
        json={"jwt_access_token_expire_minutes": 30},
    )
    assert patch.status_code == 200
    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": settings.admin_username,
            "password": settings.admin_initial_password,
            "remember_me": False,
        },
    )
    assert login.status_code == 200
    assert login.json()["data"]["expires_in"] == 30 * 60


def test_audit_recent_after_patch(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    client.patch(
        "/api/v1/admin/system-settings/basic",
        headers=headers,
        json={"platform_name": "TILESFST Test"},
    )
    recent = client.get("/api/v1/admin/system-settings/audit/recent", headers=headers)
    assert recent.status_code == 200
    items = recent.json()["data"]["items"]
    assert len(items) >= 1
    assert items[0]["action_type"] in {"settings_update", "settings_reset"}


def test_notification_group_get_patch(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    get_resp = client.get("/api/v1/admin/system-settings/notification", headers=headers)
    assert get_resp.status_code == 200
    assert "templates" in get_resp.json()["data"]["data"]

    patch = client.patch(
        "/api/v1/admin/system-settings/notification",
        headers=headers,
        json={"account_freeze_notify": False},
    )
    assert patch.status_code == 200
    assert patch.json()["data"]["data"]["account_freeze_notify"] is False


def test_patch_media_mime_types_accepts_extended_subset(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    patch = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"allowed_image_types": "image/gif,image/jpeg"},
    )
    assert patch.status_code == 200
    assert "image/gif" in patch.json()["data"]["data"]["allowed_image_types"]


def test_patch_media_mime_types_rejects_unknown(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    response = client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"allowed_image_types": "image/foo"},
    )
    assert response.status_code == 400


def test_upload_accepts_gif_when_enabled_in_settings(client: TestClient) -> None:
    headers = _auth_headers(client, settings.admin_username, settings.admin_initial_password)
    client.patch(
        "/api/v1/admin/system-settings/media",
        headers=headers,
        json={"allowed_image_types": "image/gif,image/jpeg"},
    )

    gif_bytes = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00"
        b",\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )
    response = client.post(
        "/api/v1/admin/uploads/brand-logos",
        headers=headers,
        files={"file": ("logo.gif", BytesIO(gif_bytes), "image/gif")},
    )
    assert response.status_code == 200
    assert response.json()["code"] == 0
