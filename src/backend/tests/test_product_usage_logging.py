"""Product usage logging API integration tests."""

from __future__ import annotations

import json
import sqlite3
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy import text

from app.core.config import settings
from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory, init_database, reset_engine
from app.modules.media import storage as media_storage
from app.modules.media.storage import ImageThumbnailResult, get_media_storage_client
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.log_repository import LogRepository
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRepository
from app.services.log_service import LogService
from app.services.task_trace_service import TaskTraceService
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


PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _fake_generated_variant(
    content: bytes,
    content_type: str | None,
    *,
    target_max_size_kb: int = 0,
    **_: object,
) -> ImageThumbnailResult:
    generated = f"variant-{target_max_size_kb}".encode()
    return ImageThumbnailResult(
        content=generated,
        content_type="image/webp",
        width=1,
        height=1,
        original_width=1,
        original_height=1,
        original_size=len(content),
        size=len(generated),
        resized=False,
    )


def _task_spans(task_trace_id: str) -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        rows = (
            session.execute(
                text(
                    """
                    SELECT span_name, status, duration_ms, started_at, ended_at, error_code, metadata
                    FROM task_trace_spans
                    WHERE task_trace_id = :task_trace_id
                    ORDER BY sequence ASC, created_at ASC
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .all()
        )
        return [dict(row) for row in rows]
    finally:
        session.close()


def _latest_upload_image_spans() -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        trace_id = (
            session.execute(
                text(
                    """
                    SELECT task_trace_id
                    FROM task_trace_spans
                    WHERE task_type = 'upload_image'
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                )
            )
            .scalar_one()
        )
        return _task_spans(str(trace_id))
    finally:
        session.close()


def test_sqlite_init_migrates_legacy_task_trace_log_tables(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    db_path = tmp_path / "legacy-task-trace.db"
    with sqlite3.connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE audit_logs (
              id TEXT PRIMARY KEY,
              actor_user_id TEXT,
              domain TEXT NOT NULL,
              action_type TEXT NOT NULL,
              summary TEXT NOT NULL,
              metadata TEXT,
              created_at TEXT NOT NULL
            );
            CREATE TABLE request_logs (
              id TEXT PRIMARY KEY,
              request_id TEXT NOT NULL,
              actor_user_id TEXT,
              actor_role TEXT,
              client_type TEXT NOT NULL DEFAULT 'backend',
              method TEXT NOT NULL,
              path TEXT NOT NULL,
              status_code INTEGER NOT NULL,
              duration_ms INTEGER NOT NULL,
              ip_address_masked TEXT,
              user_agent_summary TEXT,
              summary TEXT NOT NULL,
              error_code TEXT,
              result TEXT NOT NULL DEFAULT 'success',
              metadata TEXT,
              created_at TEXT NOT NULL
            );
            CREATE TABLE usage_events (
              id TEXT PRIMARY KEY,
              request_id TEXT,
              actor_user_id TEXT,
              actor_role TEXT,
              client_type TEXT NOT NULL DEFAULT 'web_admin',
              event_name TEXT NOT NULL,
              event_category TEXT NOT NULL,
              page_path TEXT,
              session_id TEXT,
              ip_address_masked TEXT,
              user_agent_summary TEXT,
              summary TEXT NOT NULL,
              duration_ms INTEGER,
              result TEXT NOT NULL DEFAULT 'success',
              metadata TEXT,
              created_at TEXT NOT NULL
            );
            """
        )

    monkeypatch.setattr(settings, "database_url", f"sqlite:///{db_path}")
    monkeypatch.setattr(settings, "app_env", "development")
    reset_engine()
    try:
        init_database()
    finally:
        reset_engine()

    with sqlite3.connect(db_path) as connection:
        for table in ("audit_logs", "request_logs", "usage_events"):
            columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
            indexes = {row[1] for row in connection.execute(f"PRAGMA index_list({table})")}
            assert "task_trace_id" in columns
            assert "task_type" in columns
            if table == "request_logs":
                assert "behavior_trace_id" in columns
                assert "parent_behavior_event_id" in columns
                assert "client_request_id" in columns
                assert "idx_request_logs_client_request_id" in indexes
                assert "idx_request_logs_client_created" in indexes
                assert "idx_request_logs_result_created" in indexes
                assert "idx_request_logs_behavior_trace" in indexes
                assert "idx_request_logs_parent_behavior_event" in indexes
            if table == "usage_events":
                assert "behavior_trace_id" in columns
                assert "behavior_event_id" in columns
                assert "idx_usage_events_client_created" in indexes
                assert "idx_usage_events_result_created" in indexes
                assert "idx_usage_events_behavior_trace" in indexes
                assert "idx_usage_events_behavior_event" in indexes
            if table == "audit_logs":
                assert "idx_audit_logs_created" in indexes
            assert f"idx_{table}_task_trace" in indexes


def test_request_logging_records_admin_api_request(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get(
        "/api/v1/admin/brands",
        headers={
            **headers,
            "x-request-id": "client_must_not_be_trusted",
            "x-client-request-id": "web_admin:client.req-001",
            "x-behavior-trace-id": "bt:pytest-behavior-trace-001",
            "x-behavior-event-id": "be:pytest-behavior-event-001",
        },
        params={"page": 1, "token": "secret-token", "unexpected": "ignored"},
    )
    assert response.status_code == 200
    assert response.headers.get("x-request-id")
    assert response.headers["x-request-id"] != "client_must_not_be_trusted"

    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT method, path, status_code, request_id, client_request_id,
                           behavior_trace_id, parent_behavior_event_id, actor_role, client_type, metadata
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
    assert row["client_request_id"] == "web_admin:client.req-001"
    assert row["behavior_trace_id"] == "bt:pytest-behavior-trace-001"
    assert row["parent_behavior_event_id"] == "be:pytest-behavior-event-001"
    assert row["actor_role"] == "admin"
    assert row["client_type"] == "web_admin"
    metadata = json.loads(row["metadata"])
    snapshot = metadata["request_snapshot"]
    assert snapshot["request"]["route_template"] == "/api/v1/admin/brands"
    assert snapshot["request"]["route_match_status"] == "matched"
    assert snapshot["request"]["request_id"] == response.headers["x-request-id"]
    assert snapshot["request"]["client_request_id"] == "web_admin:client.req-001"
    assert snapshot["request"]["behavior_trace_id"] == "bt:pytest-behavior-trace-001"
    assert snapshot["request"]["parent_behavior_event_id"] == "be:pytest-behavior-event-001"
    assert snapshot["request"]["trusted_request_id_header"] == "x-request-id"
    assert snapshot["request"]["client_request_id_header"] == "x-client-request-id"
    assert snapshot["request"]["behavior_trace_id_header"] == "x-behavior-trace-id"
    assert snapshot["request"]["behavior_event_id_header"] == "x-behavior-event-id"
    assert snapshot["input"]["query"]["allowed"] == {"page": "1"}
    assert snapshot["input"]["query"]["redacted_keys"] == ["token"]
    assert snapshot["input"]["query"]["ignored_keys"] == ["unexpected"]
    assert snapshot["input"]["body_schema_summary"]["body_type"] == "none"
    serialized = json.dumps(snapshot, ensure_ascii=False)
    assert "secret-token" not in serialized
    assert "client_must_not_be_trusted" not in serialized


def test_request_logging_client_request_id_degrades_safely(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get(
        "/api/v1/admin/brands",
        headers={**headers, "x-client-request-id": "bad\nid"},
    )
    assert response.status_code == 200
    assert response.headers.get("x-request-id")

    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT request_id, client_request_id, metadata
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

    assert row["request_id"] == response.headers["x-request-id"]
    assert row["client_request_id"] is None
    metadata = json.loads(row["metadata"])
    assert metadata["request_snapshot"]["request"]["client_request_id"] is None
    assert "bad\nid" not in json.dumps(metadata, ensure_ascii=False)


def test_direct_api_request_keeps_behavior_trace_empty(client: TestClient) -> None:
    response = client.get("/api/v1/tiles")
    assert response.status_code == 200

    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT request_id, behavior_trace_id, parent_behavior_event_id, metadata
                    FROM request_logs
                    WHERE path = '/api/v1/tiles'
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

    assert row["request_id"]
    assert row["behavior_trace_id"] is None
    assert row["parent_behavior_event_id"] is None
    snapshot = json.loads(row["metadata"])["request_snapshot"]
    assert snapshot["request"]["behavior_trace_id"] is None
    assert snapshot["request"]["parent_behavior_event_id"] is None


def test_request_logging_defaults_client_type_by_channel(client: TestClient) -> None:
    miniapp_response = client.get("/api/v1/miniapp/home")
    assert miniapp_response.status_code == 200
    catalog_response = client.get("/api/v1/tiles")
    assert catalog_response.status_code == 200

    session = get_session_factory()()
    try:
        rows = (
            session.execute(
                text(
                    """
                    SELECT path, client_type
                    FROM request_logs
                    WHERE path IN ('/api/v1/miniapp/home', '/api/v1/tiles')
                    ORDER BY created_at DESC
                    """
                )
            )
            .mappings()
            .all()
        )
    finally:
        session.close()

    by_path = {row["path"]: row["client_type"] for row in rows}
    assert by_path["/api/v1/miniapp/home"] == "wechat_miniapp"
    assert by_path["/api/v1/tiles"] == "web_catalog"


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


def test_request_snapshot_logging_failure_does_not_block_business_response(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    def fail_record_request(self: LogService, context) -> None:  # noqa: ANN001
        raise RuntimeError("snapshot storage failed")

    monkeypatch.setattr(LogService, "record_request", fail_record_request)
    response = client.get("/api/v1/admin/brands", headers=headers)

    assert response.status_code == 200
    assert response.headers.get("x-request-id")


def test_avatar_upload_records_stage_trace_spans(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(media_storage, "generate_image_thumbnail", _fake_generated_variant)
    _, password = _create_employee()
    headers = _auth_headers(client, "log_employee", password)

    response = client.post(
        "/api/v1/admin/uploads",
        headers=headers,
        files={"file": ("avatar.png", BytesIO(PNG_BYTES), "image/png")},
    )

    assert response.status_code == 200
    task_trace_id = response.json()["data"]["task_trace_id"]
    spans = _task_spans(task_trace_id)
    by_name = {str(span["span_name"]): span for span in spans}
    for span_name in ("file_read", "original_put_object"):
        assert by_name[span_name]["status"] == "success"
        assert isinstance(by_name[span_name]["duration_ms"], int)
        assert by_name[span_name]["duration_ms"] >= 0
        assert by_name[span_name]["started_at"]
        assert by_name[span_name]["ended_at"]


def test_general_image_upload_records_six_required_stage_trace_spans(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(media_storage, "generate_image_thumbnail", _fake_generated_variant)
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.post(
        "/api/v1/admin/uploads/banner-images",
        headers=headers,
        files={"file": ("banner.png", BytesIO(PNG_BYTES), "image/png")},
    )

    assert response.status_code == 200
    task_trace_id = response.json()["data"]["task_trace_id"]
    spans = _task_spans(task_trace_id)
    required = [
        "file_read",
        "original_put_object",
        "thumbnail_generate",
        "thumbnail_put_object",
        "display_generate",
        "display_put_object",
    ]
    by_name = {str(span["span_name"]): span for span in spans}
    assert list(name for name in required if name in by_name) == required
    assert all(by_name[name]["status"] == "success" for name in required)
    assert all(isinstance(by_name[name]["duration_ms"], int) for name in required)


def test_upload_trace_preserves_original_put_failure_stage(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    storage = get_media_storage_client()
    storage.fail_put = True

    response = client.post(
        "/api/v1/admin/uploads/banner-images",
        headers=headers,
        files={"file": ("banner.png", BytesIO(PNG_BYTES), "image/png")},
    )

    assert response.status_code == 502
    spans = _latest_upload_image_spans()
    by_name = {str(span["span_name"]): span for span in spans}
    assert by_name["file_read"]["status"] == "success"
    assert by_name["original_put_object"]["status"] == "failed"
    assert by_name["original_put_object"]["error_code"]
    assert "thumbnail_generate" not in by_name


def test_upload_trace_records_variant_generation_skip(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    def fail_generate(*_: object, **__: object) -> ImageThumbnailResult:
        raise ValueError("unsupported test image")

    monkeypatch.setattr(media_storage, "generate_image_thumbnail", fail_generate)
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.post(
        "/api/v1/admin/uploads/banner-images",
        headers=headers,
        files={"file": ("banner.png", BytesIO(PNG_BYTES), "image/png")},
    )

    assert response.status_code == 200
    task_trace_id = response.json()["data"]["task_trace_id"]
    spans = _task_spans(task_trace_id)
    by_name = {str(span["span_name"]): span for span in spans}
    assert by_name["thumbnail_generate"]["status"] == "skipped"
    assert by_name["thumbnail_put_object"]["status"] == "skipped"
    assert by_name["display_generate"]["status"] == "skipped"
    assert by_name["display_put_object"]["status"] == "skipped"
    serialized = json.dumps(spans, ensure_ascii=False)
    assert "/Users/" not in serialized
    assert "Authorization" not in serialized
    assert "secret" not in serialized.lower()


def test_file_upload_trace_records_non_image_variant_skip(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")

    response = client.post(
        "/api/v1/admin/uploads/brand-certificates",
        headers=headers,
        files={"file": ("certificate.pdf", BytesIO(b"%PDF-1.4\n%%EOF"), "application/pdf")},
    )

    assert response.status_code == 200
    task_trace_id = response.json()["data"]["task_trace_id"]
    spans = _task_spans(task_trace_id)
    by_name = {str(span["span_name"]): span for span in spans}
    assert by_name["file_read"]["status"] == "success"
    assert by_name["original_put_object"]["status"] == "success"
    assert by_name["thumbnail_generate"]["status"] == "skipped"
    assert by_name["thumbnail_put_object"]["status"] == "skipped"
    assert by_name["display_generate"]["status"] == "skipped"
    assert by_name["display_put_object"]["status"] == "skipped"


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
            "behavior_trace_id": "bt:usage-detail-001",
            "behavior_event_id": "be:usage-detail-view-001",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["behavior_trace_id"] == "bt:usage-detail-001"
    assert response.json()["data"]["behavior_event_id"] == "be:usage-detail-view-001"
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
    event_row = next(item for item in data["items"] if item["id"] == event_id)
    assert event_row["duration_ms"] == 321
    assert event_row["behavior_trace_id"] == "bt:usage-detail-001"
    assert event_row["parent_behavior_event_id"] == "be:usage-detail-view-001"
    assert "summary" in data

    behavior_response = client.get(
        "/api/v1/admin/logs",
        headers=headers,
        params={"behavior_trace_id": "bt:usage-detail-001"},
    )
    assert behavior_response.status_code == 200
    assert any(item["id"] == event_id for item in behavior_response.json()["data"]["items"])

    detail = client.get(f"/api/v1/admin/logs/{event_id}", headers=headers)
    assert detail.status_code == 200
    detail_data = detail.json()["data"]
    assert detail_data["log"]["id"] == event_id
    assert detail_data["event"]["fields"]["event_name"] == "entity_update"
    assert "tile_sku" in detail_data["metadata_json"]


def test_request_snapshot_records_json_body_summary_without_sensitive_values(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/usage-events",
        headers=headers,
        json={
            "event_name": "detail_view",
            "page_path": "/admin/logs",
            "request_id": "req_from_body",
            "properties": {
                "module": "log_audit",
                "entity_type": "log",
                "entity_id": "log_1",
                "token": "secret",
            },
        },
    )
    assert response.status_code == 400

    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT id, metadata
                    FROM request_logs
                    WHERE path = '/api/v1/usage-events'
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

    metadata = json.loads(row["metadata"])
    snapshot = metadata["request_snapshot"]
    body_summary = snapshot["input"]["body_schema_summary"]
    assert body_summary["body_type"] == "json_object"
    assert body_summary["stored_raw_body"] is False
    event_name = next(field for field in body_summary["fields"] if field["name"] == "event_name")
    assert event_name["value"] == "detail_view"
    properties = next(field for field in body_summary["fields"] if field["name"] == "properties")
    assert properties["type"] == "object"
    assert properties["redaction"] == "value_not_stored"
    assert snapshot["response"]["status_code"] == 400
    serialized = json.dumps(snapshot, ensure_ascii=False)
    assert "secret" not in serialized
    assert "raw_payload" not in serialized


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


def test_log_repository_uses_typed_source_when_log_type_is_selected() -> None:
    source, params = LogRepository._list_source_sql(
        log_type="request",
        client_type="web_admin",
        result="failed",
        start_time="2026-08-11T00:00:00+00:00",
    )

    assert "FROM request_logs r" in source
    assert "FROM usage_events" not in source
    assert "FROM audit_logs" not in source
    assert "UNION ALL" not in source
    assert "r.client_type = :client_type" in source
    assert "r.result = :result" in source
    assert "r.created_at >= :start_time" in source
    assert params == {
        "client_type": "web_admin",
        "result": "failed",
        "start_time": "2026-08-11T00:00:00+00:00",
    }


def test_log_repository_pushes_filters_into_mixed_log_sources() -> None:
    source, params = LogRepository._list_source_sql(
        client_type="web_admin",
        result="failed",
        path_or_request_id="req_admin_slow",
        task_trace_id="task_trace_admin_slow",
        start_time="2026-08-11T00:00:00+00:00",
        end_time="2026-08-11T23:59:59+00:00",
    )

    assert source.count("UNION ALL") == 2
    assert "FROM request_logs r" in source
    assert "FROM usage_events e" in source
    assert "FROM audit_logs a" in source
    assert "r.client_type = :client_type" in source
    assert "e.client_type = :client_type" in source
    assert "r.result = :result" in source
    assert "e.result = :result" in source
    assert "a.task_trace_id = :task_trace_id" in source
    assert "a.created_at >= :start_time" in source
    assert "a.created_at <= :end_time" in source
    assert "1 = 0" in source
    assert params["client_type"] == "web_admin"
    assert params["result"] == "failed"
    assert params["path_or_request_id"] == "%req_admin_slow%"
    assert params["task_trace_id"] == "task_trace_admin_slow"


def test_admin_logs_filter_and_detail_task_trace_timeline(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    session = get_session_factory()()
    try:
        admin = UserRepository(session).get_by_username(DEFAULT_ADMIN_USERNAME)
        assert admin is not None
        trace_service = TaskTraceService(TaskTraceRepository(session))
        task_trace_id = trace_service.generate_task_trace_id("upload_video")
        behavior_trace_id = "bt:task-upload-video-001"
        trace_service.record_span(
            task_trace_id=task_trace_id,
            task_type="upload_video",
            span_name="api_receive",
            sequence=10,
            actor_user_id=admin.id,
            request_id="req_task_trace_demo",
            behavior_trace_id=behavior_trace_id,
            resource_type="media",
            resource_id="media_1",
            summary="后端接收上传请求",
            metadata={
                "authorization": "Bearer secret",
                "internal_path": "/Users/demo/private/file.mp4",
                "object_key_prefix": "videos/default/tiles/pending",
            },
        )
        trace_service.record_span(
            task_trace_id=task_trace_id,
            task_type="upload_video",
            span_name="storage_put_object",
            sequence=20,
            actor_user_id=admin.id,
            request_id="req_task_trace_demo",
            behavior_trace_id=behavior_trace_id,
            resource_type="media",
            resource_id="media_1",
            duration_ms=1800,
            summary="对象存储写入完成",
        )
        second_task_trace_id = trace_service.generate_task_trace_id("upload_file")
        trace_service.record_span(
            task_trace_id=second_task_trace_id,
            task_type="upload_file",
            span_name="api_receive",
            sequence=10,
            actor_user_id=admin.id,
            request_id="req_task_trace_demo",
            behavior_trace_id=behavior_trace_id,
            resource_type="media",
            resource_id="media_2",
            summary="后端接收文件上传请求",
        )
        log_id = LogRepository(session).insert_request_log(
            request_id="req_task_trace_demo",
            actor_user_id=admin.id,
            actor_role="admin",
            client_type="web_admin",
            client_request_id=None,
            behavior_trace_id=behavior_trace_id,
            parent_behavior_event_id="be:upload-click-001",
            method="POST",
            path="/api/v1/admin/uploads/tile-videos",
            status_code=200,
            duration_ms=1900,
            ip_address_masked="127.0.*.*",
            user_agent_summary="pytest",
            summary="POST /api/v1/admin/uploads/tile-videos · 200",
            result="success",
            task_trace_id=task_trace_id,
            task_type="upload_video",
            metadata='{"module":"upload"}',
        )
    finally:
        session.close()

    response = client.get(
        "/api/v1/admin/logs",
        headers=headers,
        params={"task_trace_id": task_trace_id},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] >= 1
    item = next(row for row in data["items"] if row["id"] == log_id)
    assert item["actor_username"] == DEFAULT_ADMIN_USERNAME
    assert item["behavior_trace_id"] == "bt:task-upload-video-001"
    assert item["parent_behavior_event_id"] == "be:upload-click-001"
    assert item["task_trace_id"] == task_trace_id
    assert item["task_type"] == "upload_video"
    assert item["task_status"] == "success"
    assert item["task_duration_ms"] >= 1800
    assert item["task_slowest_span_name"] == "storage_put_object"

    detail = client.get(f"/api/v1/admin/logs/{log_id}", headers=headers)
    assert detail.status_code == 200
    detail_data = detail.json()["data"]
    assert detail_data["actor"]["fields"]["操作者"] == DEFAULT_ADMIN_USERNAME
    assert detail_data["basic"]["fields"]["behavior_trace_id"] == "bt:task-upload-video-001"
    assert detail_data["basic"]["fields"]["parent_behavior_event_id"] == "be:upload-click-001"
    assert detail_data["task_trace"]["task_trace_id"] == task_trace_id
    assert detail_data["task_trace"]["parent_request_id"] == "req_task_trace_demo"
    assert detail_data["task_trace"]["behavior_trace_id"] == "bt:task-upload-video-001"
    related_ids = {trace["task_trace_id"] for trace in detail_data["related_task_traces"]}
    assert task_trace_id in related_ids
    assert second_task_trace_id in related_ids
    assert [span["span_name"] for span in detail_data["task_trace"]["spans"]] == [
        "api_receive",
        "storage_put_object",
    ]
    assert detail_data["task_trace"]["spans"][0]["request_id"] == "req_task_trace_demo"
    assert detail_data["task_trace"]["spans"][0]["behavior_trace_id"] == "bt:task-upload-video-001"
    assert detail_data["task_trace"]["spans"][1]["is_slowest"] is True
    serialized = str(detail_data["task_trace"])
    assert "Bearer secret" not in serialized
    assert "/Users/demo/private" not in serialized


def test_audit_logs_persist_task_trace_context_and_redact_metadata(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    session = get_session_factory()()
    try:
        admin = UserRepository(session).get_by_username(DEFAULT_ADMIN_USERNAME)
        assert admin is not None
        trace_service = TaskTraceService(TaskTraceRepository(session))
        task_trace_id = trace_service.generate_task_trace_id("settings_update")
        trace_service.record_span(
            task_trace_id=task_trace_id,
            task_type="settings_update",
            span_name="audit_write",
            sequence=10,
            actor_user_id=admin.id,
            request_id="req_audit_task_trace",
            client_type="web_admin",
            resource_type="system_settings",
            resource_id="security",
            summary="写入系统设置审计日志",
        )
        audit_repo = AuditLogRepository(session)
        log_with_task = audit_repo.insert(
            actor_user_id=admin.id,
            domain="system_settings",
            action_type="settings_update",
            summary="更新 security 分组配置：mask_sensitive_fields",
            task_trace_id=task_trace_id,
            task_type="settings_update",
            metadata=json.dumps(
                {
                    "authorization": "Bearer secret",
                    "cookie": "session=secret",
                    "token": "token-secret",
                    "password": "pass-secret",
                    "access_key": "ak-secret",
                    "secret_key": "sk-secret",
                    "dsn": "mysql://root:secret@localhost/app",
                    ".env": "DATABASE_URL=mysql://root:secret@localhost/app",
                    "internal_path": "/Users/demo/private/.env",
                    "customer_data": "真实客户手机号 13800000000",
                    "group": "security",
                },
                ensure_ascii=False,
            ),
        )
        log_without_task = audit_repo.insert(
            actor_user_id=admin.id,
            domain="system_settings",
            action_type="settings_reset",
            summary="恢复 security 分组默认配置",
            metadata=json.dumps({"group": "security"}, ensure_ascii=False),
        )
    finally:
        session.close()

    response = client.get(
        "/api/v1/admin/logs",
        headers=headers,
        params={"log_type": "audit", "task_trace_id": task_trace_id},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    item = next(row for row in data["items"] if row["id"] == log_with_task.id)
    assert item["task_trace_id"] == task_trace_id
    assert item["task_type"] == "settings_update"
    assert item["task_status"] == "success"

    detail = client.get(f"/api/v1/admin/logs/{log_with_task.id}", headers=headers)
    assert detail.status_code == 200
    detail_data = detail.json()["data"]
    assert detail_data["task_trace"]["task_trace_id"] == task_trace_id
    assert detail_data["task_trace"]["task_type"] == "settings_update"
    serialized = json.dumps(detail_data, ensure_ascii=False)
    assert "Bearer secret" not in serialized
    assert "session=secret" not in serialized
    assert "token-secret" not in serialized
    assert "pass-secret" not in serialized
    assert "ak-secret" not in serialized
    assert "sk-secret" not in serialized
    assert "mysql://root:secret" not in serialized
    assert "/Users/demo/private" not in serialized
    assert "13800000000" not in serialized

    no_task_detail = client.get(f"/api/v1/admin/logs/{log_without_task.id}", headers=headers)
    assert no_task_detail.status_code == 200
    no_task_data = no_task_detail.json()["data"]
    assert no_task_data["task_trace"] is None


def test_admin_logs_observability_endpoint_aggregates_and_traces(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    session = get_session_factory()()
    try:
        admin = UserRepository(session).get_by_username(DEFAULT_ADMIN_USERNAME)
        assert admin is not None
        trace_service = TaskTraceService(TaskTraceRepository(session))
        task_trace_id = trace_service.generate_task_trace_id("save_sku")
        trace_service.record_span(
            task_trace_id=task_trace_id,
            task_type="save_sku",
            span_name="api_validate",
            sequence=10,
            actor_user_id=admin.id,
            request_id="req_observability_demo",
            client_type="web_admin",
            resource_type="tile_sku",
            resource_id="sku_obs_1",
            duration_ms=300,
            summary="校验 SKU",
        )
        trace_service.record_span(
            task_trace_id=task_trace_id,
            task_type="save_sku",
            span_name="db_save",
            status="failed",
            sequence=20,
            actor_user_id=admin.id,
            request_id="req_observability_demo",
            client_type="web_admin",
            resource_type="tile_sku",
            resource_id="sku_obs_1",
            duration_ms=2400,
            error_code="50005",
            summary="数据库保存失败",
            metadata={
                "authorization": "Bearer secret",
                "internal_path": "/Users/demo/.env",
            },
        )
        LogRepository(session).insert_request_log(
            request_id="req_observability_demo",
            actor_user_id=admin.id,
            actor_role="admin",
            client_type="web_admin",
            client_request_id="client_obs_1",
            method="POST",
            path="/api/v1/admin/tile-skus",
            status_code=500,
            duration_ms=2700,
            ip_address_masked="127.0.*.*",
            user_agent_summary="pytest",
            summary="POST /api/v1/admin/tile-skus · 500",
            error_code="50005",
            result="failed",
            task_trace_id=task_trace_id,
            task_type="save_sku",
            metadata='{"module":"sku","authorization":"redacted"}',
        )
        LogRepository(session).insert_usage_event(
            request_id="req_observability_demo",
            actor_user_id=admin.id,
            actor_role="admin",
            client_type="miniapp",
            event_name="sku_load_error",
            event_category="miniapp_sku_detail",
            page_path="/pages/tile-detail/index",
            session_id=None,
            ip_address_masked="127.0.*.*",
            user_agent_summary="pytest",
            summary="sku_load_error",
            duration_ms=1200,
            result="failed",
            task_trace_id=task_trace_id,
            task_type="save_sku",
            metadata='{"module":"sku_detail","error_code":"50005"}',
        )
    finally:
        session.close()

    response = client.get(
        "/api/v1/admin/logs/observability",
        headers=headers,
        params={"task_trace_id": task_trace_id, "request_id": "req_observability_demo"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["summary"]["total_logs"] >= 2
    assert data["summary"]["api_errors"] >= 1
    assert data["summary"]["slow_requests"] >= 1
    assert data["summary"]["failed_tasks"] >= 1
    assert data["summary"]["slow_tasks"] >= 1
    assert data["summary"]["task_success_rate"] == 0.0
    assert data["thresholds"] == {"slow_request_ms": 1000, "slow_task_ms": 1000}
    assert any(item["label"] == "web_admin" for item in data["distributions"]["clients"])
    assert any(item["label"] == "failed" for item in data["distributions"]["task_statuses"])
    assert any(item["path"] == "/api/v1/admin/tile-skus" for item in data["endpoint_errors"])
    assert data["rankings"]["slow_requests"][0]["request_id"] == "req_observability_demo"
    assert data["rankings"]["slow_tasks"][0]["task_trace_id"] == task_trace_id
    assert data["rankings"]["slowest_spans"][0]["span_name"] == "db_save"
    assert data["trace_results"]["request_id"] == "req_observability_demo"
    assert task_trace_id in data["trace_results"]["task_trace_ids"]
    serialized = json.dumps(data, ensure_ascii=False)
    assert "Bearer secret" not in serialized
    assert "/Users/demo/.env" not in serialized

    missing = client.get(
        "/api/v1/admin/logs/observability",
        headers=headers,
        params={"request_id": "req_missing_observability"},
    )
    assert missing.status_code == 200
    assert missing.json()["data"]["trace_results"]["reason"] == "not_found"


def test_admin_logs_observability_forbidden_for_employee(client: TestClient) -> None:
    _, password = _create_employee()
    headers = _auth_headers(client, "log_employee", password)
    response = client.get("/api/v1/admin/logs/observability", headers=headers)
    assert response.status_code == 403
