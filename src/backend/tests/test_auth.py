"""Auth API integration tests."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_db, get_session_factory, init_database, reset_engine
from app.main import app
from app.repositories.user_repository import UserRepository


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("SQLITE_DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("ADMIN_INITIAL_PASSWORD", "AdminPass123!")
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret-key")
    reset_engine()
    settings.sqlite_database_url = f"sqlite:///{db_path}"
    settings.admin_initial_password = "AdminPass123!"
    settings.app_secret_key = "test-secret-key"
    init_database()

    session = get_session_factory()()
    from app.db.seed import seed_admin_user

    seed_admin_user(session)

    def override_get_db() -> Generator[Session, None, None]:
        db = get_session_factory()()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    reset_engine()


def _login(client: TestClient, username: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password, "remember_me": False},
    )
    assert response.status_code == 200
    return response.json()["data"]


def test_login_success(client: TestClient) -> None:
    data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    assert data["token_type"] == "Bearer"
    assert data["user"]["role"] == "admin"
    assert data["access_token"]


def test_login_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": DEFAULT_ADMIN_USERNAME, "password": "wrong-password", "remember_me": False},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["code"] == 40101
    assert body["message"] == "账号或密码错误"


def test_login_disabled_user(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.create_user(
            username="disabled-user",
            password="Disabled123!",
            display_name="Disabled User",
            role="employee",
            status="disabled",
        )
    finally:
        session.close()

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "disabled-user", "password": "Disabled123!", "remember_me": False},
    )
    assert response.status_code == 403
    assert response.json()["code"] == 40301


def test_me_with_valid_token(client: TestClient) -> None:
    login_data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == DEFAULT_ADMIN_USERNAME


def test_me_with_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == 40102


def test_logout(client: TestClient) -> None:
    login_data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["success"] is True


def test_store_owner_rejected_from_admin_api(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.create_user(
            username="store-owner",
            password="OwnerPass123!",
            display_name="Store Owner",
            role="store_owner",
        )
    finally:
        session.close()

    login_data = _login(client, "store-owner", "OwnerPass123!")
    response = client.post(
        "/api/v1/admin/tiles",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
        json={"name": "测试砖", "model": "T-001", "category": "地砖"},
    )
    assert response.status_code == 403
    assert response.json()["code"] == 40302
