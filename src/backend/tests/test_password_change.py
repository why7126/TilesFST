"""Password change API integration tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import text

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_user(
    username: str = "operator01",
    password: str = "Operator123!",
    role: str = "employee",
) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if repo.get_by_username(username):
            return
        repo.create_user(
            username=username,
            password=password,
            display_name="运营一号",
            role=role,
        )
    finally:
        session.close()


def _set_system_setting(key: str, value: str) -> None:
    session = get_session_factory()()
    try:
        repo = SystemSettingsRepository(session)
        repo.set(key, value, updated_by=None)
    finally:
        session.close()


def test_change_password_success(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={
            "old_password": "Operator123!",
            "new_password": "Operator456!",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["success"] is True

    login = client.post(
        "/api/v1/auth/login",
        json={"username": "operator01", "password": "Operator456!", "remember_me": False},
    )
    assert login.status_code == 200


def test_change_password_old_incorrect(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "wrong-old", "new_password": "Operator456!"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40020


def test_change_password_weak(client: TestClient) -> None:
    _set_system_setting("security.password_min_length", "8")
    _set_system_setting("security.require_uppercase", "false")
    _set_system_setting("security.require_special", "false")
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "password123"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40022


def test_change_password_policy(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "short1"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40021


def test_change_password_same_as_old(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "Operator123!"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40023


def test_old_jwt_invalid_after_password_change(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    old_token = headers["Authorization"].removeprefix("Bearer ")

    change = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "Operator789!"},
    )
    assert change.status_code == 200

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {old_token}"},
    )
    assert me.status_code == 401

    login = client.post(
        "/api/v1/auth/login",
        json={"username": "operator01", "password": "Operator789!", "remember_me": False},
    )
    assert login.status_code == 200


def test_login_token_contains_tv(client: TestClient) -> None:
    data = _login(client, "admin", "AdminPass123!")
    payload = jwt.decode(
        data["access_token"],
        settings.app_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert "tv" in payload


def test_employee_can_change_password(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "Operator456!"},
    )
    assert response.status_code == 200


def test_store_owner_forbidden(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if not repo.get_by_username("owner01"):
            repo.create_user(
                username="owner01",
                password="Owner12345!",
                display_name="店主",
                role="store_owner",
            )
    finally:
        session.close()

    headers = _auth_headers(client, "owner01", "Owner12345!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Owner12345!", "new_password": "Owner56789!"},
    )
    assert response.status_code == 403


def test_rate_limit_after_failed_attempts(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    for _ in range(5):
        client.post(
            "/api/v1/admin/profile/password",
            headers=headers,
            json={"old_password": "bad", "new_password": "Operator456!"},
        )
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "Operator456!"},
    )
    assert response.status_code == 429
    assert response.json()["code"] == 42901


def test_protected_admin_cannot_change_own_password(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        before = session.execute(
            text(
                """
                SELECT password_hash, token_version
                FROM users
                WHERE username = :username
                """
            ),
            {"username": DEFAULT_ADMIN_USERNAME},
        ).mappings().one()
    finally:
        session.close()

    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "AdminPass123!", "new_password": "AdminPass456!"},
    )

    assert response.status_code == 403
    assert response.json()["code"] == 30060
    session = get_session_factory()()
    try:
        after = session.execute(
            text(
                """
                SELECT password_hash, token_version
                FROM users
                WHERE username = :username
                """
            ),
            {"username": DEFAULT_ADMIN_USERNAME},
        ).mappings().one()
    finally:
        session.close()
    assert after["password_hash"] == before["password_hash"]
    assert after["token_version"] == before["token_version"]
