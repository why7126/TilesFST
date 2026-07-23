"""Password change API integration tests."""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import text

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
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


def _get_user_security(username: str) -> dict[str, object]:
    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                SELECT password_hash, token_version
                FROM users
                WHERE username = :username
                """
                ),
                {"username": username},
            )
            .mappings()
            .one()
        )
        return dict(row)
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


@pytest.mark.parametrize(
    ("username", "new_password"),
    [
        ("policyminok", "Abc12"),
        ("policymaxok", "A1" + "a" * 30),
        ("policysymbolok", "Abc12!"),
    ],
)
def test_change_password_policy_accepts_simplified_valid_passwords(
    client: TestClient,
    username: str,
    new_password: str,
) -> None:
    _create_user(username=username)
    headers = _auth_headers(client, username, "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={
            "old_password": "Operator123!",
            "new_password": new_password,
        },
    )
    assert response.status_code == 200


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
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "password123"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40022


@pytest.mark.parametrize(
    ("username", "new_password", "expected_violation"),
    [
        ("policyshort", "A1b2", "min_length"),
        ("policymax", "A1" + "a" * 31, "max_length"),
        ("policyletter", "12345", "missing_letter"),
        ("policydigit", "NoDigitsHere", "missing_digit"),
    ],
)
def test_change_password_policy_details(
    client: TestClient,
    username: str,
    new_password: str,
    expected_violation: str,
) -> None:
    _create_user(username=username)
    before = _get_user_security(username)
    headers = _auth_headers(client, username, "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": new_password},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == 40021
    assert expected_violation in body["data"]["violations"]
    assert body["data"]["policy"]["min_length"] == 5
    assert body["data"]["policy"]["max_length"] == 32
    assert body["data"]["policy"]["require_letter"] is True
    assert body["data"]["policy"]["require_digit"] is True
    assert new_password not in json.dumps(body, ensure_ascii=False)
    after = _get_user_security(username)
    assert after["password_hash"] == before["password_hash"]
    assert after["token_version"] == before["token_version"]


def test_change_password_policy_reports_multiple_details(client: TestClient) -> None:
    _create_user()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.post(
        "/api/v1/admin/profile/password",
        headers=headers,
        json={"old_password": "Operator123!", "new_password": "!!!!"},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == 40021
    assert set(body["data"]["violations"]) >= {"min_length", "missing_letter", "missing_digit"}
    assert "至少需要 5 位字符" in body["message"]


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
        before = (
            session.execute(
                text(
                    """
                SELECT password_hash, token_version
                FROM users
                WHERE username = :username
                """
                ),
                {"username": DEFAULT_ADMIN_USERNAME},
            )
            .mappings()
            .one()
        )
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
        after = (
            session.execute(
                text(
                    """
                SELECT password_hash, token_version
                FROM users
                WHERE username = :username
                """
                ),
                {"username": DEFAULT_ADMIN_USERNAME},
            )
            .mappings()
            .one()
        )
    finally:
        session.close()
    assert after["password_hash"] == before["password_hash"]
    assert after["token_version"] == before["token_version"]
