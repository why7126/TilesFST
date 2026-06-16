"""Admin users API integration tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_db, get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_employee(client: TestClient) -> str:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.create_user(
            username="operator01",
            password="Operator123!",
            display_name="运营一号",
            role="employee",
        )
    finally:
        session.close()
    return "operator01"


def test_admin_list_users(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]


def test_employee_forbidden_on_users_api(client: TestClient) -> None:
    _create_employee(client)
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 403
    assert response.json()["code"] == 40302


def test_create_user_success(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={
            "username": "new_store_01",
            "display_name": "",
            "role": "store_owner",
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["user"]["username"] == "new_store_01"
    assert len(data["initial_password"]) >= 12


def test_create_user_duplicate_username(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    payload = {"username": "dup_user_01", "role": "employee"}
    assert client.post("/api/v1/admin/users", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/users", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 40910


def test_cannot_delete_logged_in_user(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "logged_user", "role": "employee"},
    )
    user_id = create.json()["data"]["user"]["id"]

    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.update_last_login_at(user_id)
    finally:
        session.close()

    response = client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=headers,
        json={"status": "deleted"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40011


def test_delete_never_logged_in_user(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "never_logged", "role": "store_owner"},
    )
    user_id = create.json()["data"]["user"]["id"]
    response = client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=headers,
        json={"status": "deleted"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "deleted"


def test_disabled_user_cannot_login(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "freeze_me", "role": "employee"},
    )
    user_id = create.json()["data"]["user"]["id"]
    password = create.json()["data"]["initial_password"]

    client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=headers,
        json={"status": "disabled"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "freeze_me", "password": password, "remember_me": False},
    )
    assert response.status_code == 403
    assert response.json()["code"] == 40301


def test_reset_password(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "reset_pwd_user", "role": "employee"},
    )
    user_id = create.json()["data"]["user"]["id"]
    response = client.post(
        f"/api/v1/admin/users/{user_id}/reset-password",
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["password"]) >= 12
