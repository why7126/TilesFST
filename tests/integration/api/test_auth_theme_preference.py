from __future__ import annotations

from fastapi.testclient import TestClient


def _login(client: TestClient, username: str = "admin", password: str = "AdminPass123!") -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password, "remember_me": False},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['data']['access_token']}"}


def test_current_user_theme_mode_defaults_to_system(api_client: TestClient) -> None:
    headers = _login(api_client)

    response = api_client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["data"]["theme_mode"] == "system"


def test_update_current_user_theme_preference_persists(api_client: TestClient) -> None:
    headers = _login(api_client)

    update = api_client.patch(
        "/api/v1/auth/me/theme",
        headers=headers,
        json={"theme_mode": "comfort_dark"},
    )
    assert update.status_code == 200
    assert update.json()["data"]["theme_mode"] == "comfort_dark"

    current = api_client.get("/api/v1/auth/me", headers=headers)
    assert current.status_code == 200
    assert current.json()["data"]["theme_mode"] == "comfort_dark"


def test_invalid_theme_preference_returns_400_without_changing_value(api_client: TestClient) -> None:
    headers = _login(api_client)
    ok = api_client.patch(
        "/api/v1/auth/me/theme",
        headers=headers,
        json={"theme_mode": "light"},
    )
    assert ok.status_code == 200

    invalid = api_client.patch(
        "/api/v1/auth/me/theme",
        headers=headers,
        json={"theme_mode": "blue"},
    )
    assert invalid.status_code == 400
    assert invalid.json() == {"code": 40001, "message": "无效的主题模式", "data": None}

    current = api_client.get("/api/v1/auth/me", headers=headers)
    assert current.json()["data"]["theme_mode"] == "light"


def test_unauthenticated_user_cannot_update_theme_preference(api_client: TestClient) -> None:
    response = api_client.patch("/api/v1/auth/me/theme", json={"theme_mode": "light"})

    assert response.status_code == 401
    assert response.json()["code"] == 40102


def test_disabled_user_cannot_update_theme_preference(api_client: TestClient) -> None:
    admin_headers = _login(api_client)
    created = api_client.post(
        "/api/v1/admin/users",
        headers=admin_headers,
        json={"username": "themeuser", "display_name": "Theme User", "role": "employee"},
    )
    assert created.status_code == 200
    user_id = created.json()["data"]["user"]["id"]
    password = created.json()["data"]["initial_password"]
    user_headers = _login(api_client, "themeuser", password)

    disabled = api_client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=admin_headers,
        json={"status": "disabled"},
    )
    assert disabled.status_code == 200

    response = api_client.patch(
        "/api/v1/auth/me/theme",
        headers=user_headers,
        json={"theme_mode": "comfort_dark"},
    )

    assert response.status_code == 403
    assert response.json()["code"] == 40301
