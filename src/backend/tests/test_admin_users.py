"""Admin users API integration tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_db, get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _assert_basic_password_policy(password: str) -> None:
    assert 5 <= len(password) <= 32
    assert any("A" <= char <= "Z" or "a" <= char <= "z" for char in password)
    assert any("0" <= char <= "9" for char in password)


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


def _get_user_snapshot(username: str) -> dict[str, object]:
    session = get_session_factory()()
    try:
        row = session.execute(
            text(
                """
                SELECT id, username, display_name, role, status, password_hash,
                       avatar_object_key, token_version
                FROM users
                WHERE username = :username
                """
            ),
            {"username": username},
        ).mappings().one()
        return dict(row)
    finally:
        session.close()


def test_admin_list_users(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]
    admin_item = next(
        item
        for item in body["data"]["items"]
        if item["username"] == DEFAULT_ADMIN_USERNAME
    )
    assert admin_item["is_protected"] is True
    assert admin_item["protected_reason"] == "系统保底管理员账号不允许执行该操作"


def test_admin_user_detail_marks_default_admin_protected(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    admin_id = str(_get_user_snapshot(DEFAULT_ADMIN_USERNAME)["id"])

    response = client.get(f"/api/v1/admin/users/{admin_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["username"] == DEFAULT_ADMIN_USERNAME
    assert data["is_protected"] is True
    assert data["protected_reason"] == "系统保底管理员账号不允许执行该操作"


def test_role_admin_user_is_not_protected_by_role(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "ordinary_admin", "role": "admin"},
    )
    assert create.status_code == 200

    response = client.get("/api/v1/admin/users", headers=headers)

    assert response.status_code == 200
    ordinary_admin = next(
        item
        for item in response.json()["data"]["items"]
        if item["username"] == "ordinary_admin"
    )
    assert ordinary_admin["role"] == "admin"
    assert ordinary_admin["is_protected"] is False
    assert ordinary_admin["protected_reason"] is None


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
    _assert_basic_password_policy(data["initial_password"])


def test_create_user_duplicate_username(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    payload = {"username": "dup_user_01", "role": "employee"}
    assert client.post("/api/v1/admin/users", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/users", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 40910
    assert response.json()["message"] == "用户名已存在"


def test_create_user_short_username_returns_business_message(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "abc", "role": "store_owner"},
    )
    body = response.json()

    assert response.status_code == 400
    assert body["code"] == 40010
    assert "detail" not in body
    assert body["data"] is None
    assert body["message"] == "用户名长度须为 4–32 位"


def test_create_user_invalid_username_format_returns_business_message(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "1abc", "role": "store_owner"},
    )
    body = response.json()

    assert response.status_code == 400
    assert body["code"] == 40010
    assert body["message"] == "用户名须以小写字母开头，仅含小写字母、数字、_、-、."


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
    _assert_basic_password_policy(response.json()["data"]["password"])


def test_protected_admin_cannot_be_edited(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    before = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)

    response = client.patch(
        f"/api/v1/admin/users/{before['id']}",
        headers=headers,
        json={
            "display_name": "不可修改",
            "role": "employee",
            "avatar_object_key": "avatars/new.png",
        },
    )

    assert response.status_code == 403
    assert response.json()["code"] == 30060
    after = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)
    assert after["display_name"] == before["display_name"]
    assert after["role"] == before["role"]
    assert after["avatar_object_key"] == before["avatar_object_key"]


def test_protected_admin_cannot_reset_password(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    before = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)

    response = client.post(
        f"/api/v1/admin/users/{before['id']}/reset-password",
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["code"] == 30060
    assert "data" in response.json()
    after = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)
    assert after["password_hash"] == before["password_hash"]
    assert after["token_version"] == before["token_version"]


def test_protected_admin_cannot_change_status(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    before = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)

    response = client.patch(
        f"/api/v1/admin/users/{before['id']}/status",
        headers=headers,
        json={"status": "disabled"},
    )

    assert response.status_code == 403
    assert response.json()["code"] == 30060
    after = _get_user_snapshot(DEFAULT_ADMIN_USERNAME)
    assert after["status"] == before["status"]


def test_keyword_matches_username_and_display_name_only(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    username = "kw_search_user"
    display_name = "昵称搜索专用"
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": username, "display_name": display_name, "role": "employee"},
    )
    assert create.status_code == 200
    user_id = create.json()["data"]["user"]["id"]

    session = get_session_factory()()
    try:
        session.execute(
            text("UPDATE users SET email = :email, phone = :phone WHERE id = :id"),
            {
                "email": "kw-only-email@example.com",
                "phone": "13900001111",
                "id": user_id,
            },
        )
        session.commit()
    finally:
        session.close()

    by_username = client.get(
        "/api/v1/admin/users",
        headers=headers,
        params={"keyword": "kw_search"},
    )
    assert by_username.status_code == 200
    usernames = [item["username"] for item in by_username.json()["data"]["items"]]
    assert username in usernames

    by_display_name = client.get(
        "/api/v1/admin/users",
        headers=headers,
        params={"keyword": "昵称搜索"},
    )
    assert by_display_name.status_code == 200
    usernames = [item["username"] for item in by_display_name.json()["data"]["items"]]
    assert username in usernames

    by_email = client.get(
        "/api/v1/admin/users",
        headers=headers,
        params={"keyword": "kw-only-email"},
    )
    assert by_email.status_code == 200
    usernames = [item["username"] for item in by_email.json()["data"]["items"]]
    assert username not in usernames

    by_phone = client.get(
        "/api/v1/admin/users",
        headers=headers,
        params={"keyword": "13900001111"},
    )
    assert by_phone.status_code == 200
    usernames = [item["username"] for item in by_phone.json()["data"]["items"]]
    assert username not in usernames


def test_user_list_returns_accessible_avatar_url(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    upload = client.post(
        "/api/v1/admin/uploads",
        headers=headers,
        files={"file": ("avatar.png", b"png-avatar", "image/png")},
    )
    assert upload.status_code == 200
    upload_data = upload.json()["data"]
    create = client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={
            "username": "avatar_user_01",
            "role": "employee",
            "avatar_object_key": upload_data["object_key"],
        },
    )
    assert create.status_code == 200

    response = client.get(
        "/api/v1/admin/users",
        headers=headers,
        params={"keyword": "avatar_user_01"},
    )
    assert response.status_code == 200
    item = response.json()["data"]["items"][0]
    assert item["avatar_url"] == upload_data["url"]
    assert client.get(item["avatar_url"]).status_code == 200
