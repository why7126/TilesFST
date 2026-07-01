"""Admin API docs inventory tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
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
        repo.create_user(
            username="api_docs_employee",
            password="Operator123!",
            display_name="接口文档运营",
            role="employee",
        )
    finally:
        session.close()


def test_admin_can_fetch_api_docs_inventory(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.get("/api/v1/admin/api-docs", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert body["data"]["summary"]["total_routes"] > 0
    assert body["data"]["environment"]["allow_try_it_out"] is True


def test_employee_forbidden_on_api_docs_inventory(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "api_docs_employee", "Operator123!")

    response = client.get("/api/v1/admin/api-docs", headers=headers)

    assert response.status_code == 403
    assert response.json()["code"] == 40302


def test_api_docs_inventory_includes_non_api_v1_routes(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.get("/api/v1/admin/api-docs", headers=headers)
    routes = response.json()["data"]["routes"]

    health = next(item for item in routes if item["path"] == "/health")
    media = next(item for item in routes if item["path"] == "/media/{object_key:path}")
    api_docs = next(item for item in routes if item["path"] == "/api/v1/admin/api-docs")

    assert health["method"] == "GET"
    assert health["auth_requirement"] == "public"
    assert health["orval_method_name"] == "healthCheckHealthGet"

    assert media["source"] == "media-passthrough"
    assert media["included_in_openapi"] is False
    assert media["orval_method_name"] is None
    assert media["missing_orval_reason"] == "未纳入 OpenAPI schema"

    assert api_docs["auth_requirement"] == "admin"
    assert api_docs["orval_method_name"] == "getApiDocsApiV1AdminApiDocsGet"


def test_swagger_try_it_out_policy_follows_environment(monkeypatch) -> None:
    monkeypatch.setattr(settings, "app_env", "production")
    assert settings.allow_swagger_try_it_out() is False

    monkeypatch.setattr(settings, "app_env", "demo")
    assert settings.allow_swagger_try_it_out() is True
