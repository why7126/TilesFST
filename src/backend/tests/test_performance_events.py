"""Real-user performance monitoring API tests."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory, init_database, reset_engine
from tests.test_auth import _login, client  # noqa: F401
from pytest import MonkeyPatch


def _auth_headers(client: TestClient) -> dict[str, str]:
    data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    return {"Authorization": f"Bearer {data['access_token']}"}


def test_performance_events_ingest_and_admin_summary(client: TestClient) -> None:
    response = client.post(
        "/api/v1/performance-events",
        json={
            "events": [
                {
                    "client_type": "wechat_miniapp",
                    "page_key": "miniapp/product-detail",
                    "app_version": "v1.2.3",
                    "network_type": "wifi",
                    "device_class": "mid",
                    "metric_name": "first_content_ready",
                    "duration_ms": 1800,
                    "sample_rate": 1,
                    "occurred_at": "2026-08-10T15:00:00Z",
                },
                {
                    "client_type": "wechat_miniapp",
                    "page_key": "miniapp/product-detail",
                    "app_version": "v1.2.3",
                    "network_type": "wifi",
                    "device_class": "mid",
                    "metric_name": "first_content_ready",
                    "duration_ms": 2600,
                    "sample_rate": 1,
                    "occurred_at": "2026-08-10T15:00:01Z",
                },
            ]
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["accepted"] == 2

    summary = client.get(
        "/api/v1/admin/performance-events/summary",
        headers=_auth_headers(client),
        params={"client_type": "wechat_miniapp", "min_samples": 3},
    )
    assert summary.status_code == 200
    data = summary.json()["data"]
    assert data["total_events"] >= 2
    assert data["total"] >= 1
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] >= 1
    item = data["items"][0]
    assert item["page_key"] == "miniapp/product-detail"
    assert item["sample_count"] == 2
    assert item["p95_ms"] == 2600
    assert item["sample_status"] == "insufficient"

    paged_summary = client.get(
        "/api/v1/admin/performance-events/summary",
        headers=_auth_headers(client),
        params={"client_type": "wechat_miniapp", "page": 1, "page_size": 1},
    )
    assert paged_summary.status_code == 200
    paged_data = paged_summary.json()["data"]
    assert paged_data["page"] == 1
    assert paged_data["page_size"] == 1
    assert len(paged_data["items"]) <= 1

    samples = client.get(
        "/api/v1/admin/performance-events/samples",
        headers=_auth_headers(client),
        params={
            "client_type": "wechat_miniapp",
            "page_key": "miniapp/product-detail",
            "metric_name": "first_content_ready",
        },
    )
    assert samples.status_code == 200
    sample_data = samples.json()["data"]
    assert sample_data["total"] >= 2
    assert sample_data["page"] == 1
    assert sample_data["page_size"] == 20
    assert sample_data["total_pages"] >= 1
    sample = sample_data["items"][0]
    assert sample["page_key"] == "miniapp/product-detail"
    assert sample["metric_name"] == "first_content_ready"
    assert sample["duration_ms"] in {1800, 2600}
    assert "metadata" not in sample
    assert "user_agent_summary" not in sample

    paged_samples = client.get(
        "/api/v1/admin/performance-events/samples",
        headers=_auth_headers(client),
        params={
            "client_type": "wechat_miniapp",
            "page_key": "miniapp/product-detail",
            "metric_name": "first_content_ready",
            "page": 1,
            "page_size": 1,
        },
    )
    assert paged_samples.status_code == 200
    paged_sample_data = paged_samples.json()["data"]
    assert paged_sample_data["page"] == 1
    assert paged_sample_data["page_size"] == 1
    assert paged_sample_data["total"] >= 2
    assert paged_sample_data["total_pages"] >= 2
    assert len(paged_sample_data["items"]) == 1


def test_performance_events_reject_sensitive_payload(client: TestClient) -> None:
    response = client.post(
        "/api/v1/performance-events",
        json={
            "events": [
                {
                    "client_type": "web_catalog",
                    "page_key": "catalog/token-leak",
                    "metric_name": "first_content_ready",
                    "duration_ms": 100,
                    "occurred_at": "2026-08-10T15:00:00Z",
                }
            ]
        },
    )
    assert response.status_code == 400
    assert "敏感" in response.json()["message"] or "禁止" in response.json()["message"]


def test_performance_admin_summary_requires_admin(client: TestClient) -> None:
    response = client.get("/api/v1/admin/performance-events/summary")
    assert response.status_code == 401

    samples = client.get("/api/v1/admin/performance-events/samples")
    assert samples.status_code == 401


def test_sqlite_init_creates_performance_events_table(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    db_path = tmp_path / "performance-events.db"
    monkeypatch.setattr(settings, "database_url", f"sqlite:///{db_path}")
    monkeypatch.setattr(settings, "app_env", "development")
    reset_engine()
    try:
        init_database()
    finally:
        reset_engine()

    with sqlite3.connect(db_path) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(performance_events)")}
        indexes = {row[1] for row in connection.execute("PRAGMA index_list(performance_events)")}
    assert {"client_type", "page_key", "metric_name", "duration_ms", "server_received_at"} <= columns
    assert "idx_performance_events_client_page_metric" in indexes
