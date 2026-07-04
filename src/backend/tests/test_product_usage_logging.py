"""Product usage logging API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.log_repository import LogRepository
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_employee() -> tuple[str, str]:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        existing = repo.get_by_username("log_employee")
        if existing is None:
            created = repo.create_user(
                username="log_employee",
                password="Operator123!",
                display_name="日志员工",
                role="employee",
            )
            return created.id, "Operator123!"
        return existing.id, "Operator123!"
    finally:
        session.close()


def test_request_logging_records_admin_api_request(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/brands", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("x-request-id")

    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT method, path, status_code, request_id, actor_role, client_type
                    FROM request_logs
                    WHERE path = '/api/v1/admin/brands'
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
    finally:
        session.close()

    assert row["method"] == "GET"
    assert row["status_code"] == 200
    assert row["request_id"] == response.headers["x-request-id"]
    assert row["actor_role"] == "admin"
    assert row["client_type"] == "web_admin"


def test_request_logging_excludes_health(client: TestClient) -> None:
    assert client.get("/health").status_code == 200
    session = get_session_factory()()
    try:
        count = session.execute(
            text("SELECT COUNT(*) FROM request_logs WHERE path = '/health'")
        ).scalar_one()
    finally:
        session.close()
    assert count == 0


def test_usage_event_success_and_admin_log_detail(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "entity_update",
            "client_type": "web_admin",
            "page_path": "/admin/tile-skus",
            "properties": {
                "module": "SKU 管理",
                "entity_type": "tile_sku",
                "entity_id": "sku_843291",
                "changed_fields": ["main_image"],
                "result": "success",
            },
            "duration_ms": 321,
        },
    )
    assert response.status_code == 200
    event_id = response.json()["data"]["id"]

    list_response = client.get(
        "/api/v1/admin/logs",
        headers=headers,
        params={"log_type": "usage_event", "path_or_request_id": "/admin/tile-skus"},
    )
    assert list_response.status_code == 200
    data = list_response.json()["data"]
    assert data["total"] >= 1
    assert any(item["id"] == event_id for item in data["items"])
    assert next(item for item in data["items"] if item["id"] == event_id)["duration_ms"] == 321
    assert "summary" in data

    detail = client.get(f"/api/v1/admin/logs/{event_id}", headers=headers)
    assert detail.status_code == 200
    detail_data = detail.json()["data"]
    assert detail_data["log"]["id"] == event_id
    assert detail_data["event"]["fields"]["event_name"] == "entity_update"
    assert "tile_sku" in detail_data["metadata_json"]


def test_usage_event_accepts_ui_behavior_events(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    detail_view = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "detail_view",
            "page_path": "/admin/logs",
            "properties": {
                "module": "log_audit",
                "entity_type": "log",
                "entity_id": "log_20260703_009418",
            },
        },
    )
    assert detail_view.status_code == 200

    copy_request_id = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "copy_request_id",
            "page_path": "/admin/logs",
            "properties": {
                "module": "log_audit",
                "entity_type": "request_log",
                "entity_id": "req_79f1c2b4a8d04e31",
                "request_id": "req_79f1c2b4a8d04e31",
            },
        },
    )
    assert copy_request_id.status_code == 200


def test_usage_event_rejects_unknown_and_forbidden_properties(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    unknown = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={"event_name": "free_click", "properties": {}},
    )
    assert unknown.status_code == 400
    assert unknown.json()["code"] == 40001

    forbidden = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "page_view",
            "properties": {
                "page_path": "/admin/logs",
                "module": "log_audit",
                "token": "secret",
            },
        },
    )
    assert forbidden.status_code == 400
    assert forbidden.json()["code"] == 40001


def test_admin_logs_forbidden_for_employee(client: TestClient) -> None:
    _, password = _create_employee()
    headers = _auth_headers(client, "log_employee", password)
    response = client.get("/api/v1/admin/logs", headers=headers)
    assert response.status_code == 403


def test_admin_log_not_found(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/logs/missing-log", headers=headers)
    assert response.status_code == 404
    assert response.json()["code"] == 30070


def test_repository_filters_and_masks_metadata(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "search_submit",
            "properties": {
                "module": "log_audit",
                "keyword": "SKU 843291",
                "result_count": 1,
            },
        },
    )

    session = get_session_factory()()
    try:
        result = LogRepository(session).list_logs(
            page=1,
            page_size=20,
            log_type="usage_event",
            keyword="SKU 843291",
        )
    finally:
        session.close()

    assert result.total >= 1
    assert result.items[0].log_type == "usage_event"
