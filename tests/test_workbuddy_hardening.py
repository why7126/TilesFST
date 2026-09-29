import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from src.mcp.workbuddy.adapters.api_client import BackendApiError, safe_error_result
from src.mcp.workbuddy.adapters.idempotency import WriteJournal
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig
from src.mcp.workbuddy.tools.registry import ToolRegistry


class Client:
    def __init__(self):
        self.calls = []

    def get(self, path, query=None):
        self.calls.append((path, query))
        return {"data": {"id": "user-1", "role": "admin", "status": "active"}}

    def post(self, path, **kwargs):
        self.calls.append((path, kwargs))
        return {"data": {"id": 42}}


@pytest.fixture
def registry(tmp_path):
    config = WorkBuddyConnectorConfig(
        api_base_url="http://localhost:8000", api_token="synthetic-token", enable_write_tools=True,
        write_scopes=frozenset({"tile_sku:write", "brand:write", "category:write"}),
        idempotency_dir=str(tmp_path / "journal"),
    )
    return ToolRegistry(Client(), config)


@pytest.mark.parametrize("args", [
    {}, {"payload": {}, "confirmed": True, "idempotency_key": "x"},
    {"payload": {"name": "demo"}, "confirmed": "true", "idempotency_key": "test-12345"},
    {"payload": {}, "confirmed": True, "idempotency_key": "test-12345"},
    {"payload": {"name": 123}, "confirmed": True, "idempotency_key": "test-12345"},
])
def test_invalid_writes_never_reach_api(registry, args):
    assert registry.call_tool("create_tile_sku", args)["ok"] is False
    assert registry.client.calls == []


@pytest.mark.parametrize("name", ["preview_manage_brand", "preview_manage_category"])
def test_preview_validates_missing_business_fields(registry, name):
    result = registry.call_tool(name, {"operation": "create", "payload": {}})
    assert set(result["missing_fields"]) == {"name", "sort_order"}
    assert result["side_effects"] is False
    assert result["next_step"]
    assert registry.client.calls == []


def test_invalid_enum_does_not_unpublish(registry):
    result = registry.call_tool("set_tile_sku_status", {
        "sku_id": 1, "target_status": "typo", "confirmed": True, "idempotency_key": "test-12345",
    })
    assert result["error"] == "invalid_arguments"
    assert registry.client.calls == []


@pytest.mark.parametrize("status", ["DISABLED", "DRAFT"])
def test_unpublish_matches_backend_and_legacy_alias(registry, status):
    registry.config = replace(registry.config, write_scopes=frozenset({"tile_sku:publish"}))
    preview = registry.call_tool("preview_publish_tile_sku", {"sku_id": 1, "target_status": status})
    assert preview["target"]["target_status"] == "DISABLED"
    result = registry.call_tool("set_tile_sku_status", {
        "sku_id": 1, "target_status": status, "confirmed": True, "idempotency_key": "status-test-key",
    })
    assert result["ok"] is True
    assert registry.client.calls[-1][0] == "/api/v1/admin/tile-skus/1/unpublish"


@pytest.mark.parametrize("patch", [
    {"file_name": "no-extension"}, {"file_name": "image.exe"}, {"file_name": "../image.png"},
    {"file_name": "image\r\n.png"}, {"file_name": "C:\\image.png"},
    {"base64_content": ""}, {"base64_content": "!invalid!"},
])
def test_invalid_media_never_reaches_backend(registry, patch):
    registry.config = replace(registry.config, write_scopes=frozenset({"media:upload"}))
    result = registry.call_tool("upload_tile_media", {
        "target": "tile_image", "content_type": "image/png", "file_name": "image.png",
        "base64_content": "ZGVtbw==", "confirmed": True, "idempotency_key": "media-test-key", **patch,
    })
    assert result["error"] == "invalid_media"
    assert registry.client.calls == []


def test_idempotency_survives_new_registry_and_rejects_conflict(registry):
    args = {"payload": {"name": "demo"}, "confirmed": True, "idempotency_key": "test-12345"}
    assert registry.call_tool("create_tile_sku", args)["ok"] is True
    other = ToolRegistry(registry.client, registry.config)
    assert other.call_tool("create_tile_sku", args)["error"] == "duplicate_operation"
    assert other.call_tool("create_tile_sku", {**args, "payload": {"name": "other"}})["error"] == "idempotency_conflict"
    assert sum(path.endswith("tile-skus") for path, _ in registry.client.calls) == 1


def test_uncertain_result_never_retries(tmp_path):
    journal = WriteJournal(str(tmp_path))
    calls = []

    def timeout():
        calls.append(1)
        raise TimeoutError()

    with pytest.raises(TimeoutError):
        journal.execute("user", "key", "tool", {}, timeout)
    assert journal.execute("user", "key", "tool", {}, timeout)["error"] == "operation_uncertain"
    assert len(calls) == 1


def test_concurrent_duplicate_has_one_side_effect(tmp_path):
    journal = WriteJournal(str(tmp_path))
    calls = []

    def action():
        calls.append(1)
        return {"ok": True}

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: journal.execute("user", "key", "tool", {}, action), range(8)))
    assert len(calls) == 1
    assert sum(result["ok"] for result in results) == 1


def test_journal_is_identity_scoped_and_contains_no_payload(tmp_path):
    journal = WriteJournal(str(tmp_path))
    for user in ("a", "b"):
        assert journal.execute(user, "key", "tool", {"name": "synthetic-private"}, lambda: {"ok": True})["ok"]
    for state in tmp_path.glob("*/state.json"):
        assert "synthetic-private" not in state.read_text()
        assert set(json.loads(state.read_text())) == {"state", "digest"}


def test_journal_blocks_duplicate_in_another_process(tmp_path):
    journal = WriteJournal(str(tmp_path))
    assert journal.execute("user", "key", "tool", {}, lambda: {"ok": True})["ok"]
    code = (
        "import sys; from src.mcp.workbuddy.adapters.idempotency import WriteJournal; "
        "result=WriteJournal(sys.argv[1]).execute('user','key','tool',{},lambda: {'ok': True}); "
        "assert result['error']=='duplicate_operation'"
    )
    subprocess.run([sys.executable, "-c", code, str(tmp_path)], check=True, timeout=10)


def test_error_text_is_not_echoed():
    result = safe_error_result(BackendApiError(status_code=400, message="token=synthetic-private"))
    assert "synthetic-private" not in json.dumps(result)


def test_audit_never_contains_payload(registry, caplog):
    import logging
    with caplog.at_level(logging.INFO, logger="src.mcp.workbuddy.tools.registry"):
        registry.call_tool("preview_create_tile_sku", {"payload": {"name": "synthetic-private"}})
    assert "workbuddy_tool_call" in caplog.text
    assert "synthetic-private" not in caplog.text


def test_missing_confirmation_blocks_write(registry):
    result = registry.call_tool("create_tile_sku", {
        "payload": {"name": "demo"}, "confirmed": False, "idempotency_key": "test-12345",
    })
    assert result["error"] == "confirmation_required"
    assert not registry.client.calls


@pytest.fixture
def remote(tmp_path, monkeypatch):
    from src.mcp.workbuddy import http_server
    from src.mcp.workbuddy.adapters import auth
    credentials = tmp_path / "credentials.json"
    credentials.write_text(json.dumps({
        hashlib.sha256(token.encode()).hexdigest(): {"backend_token": token + "-backend", "scopes": scopes}
        for token, scopes in [("alice", ["catalog:read", "tile_sku:write"]), ("bob", ["catalog:read"])]
    }))
    config = WorkBuddyConnectorConfig(
        api_base_url="http://localhost:8000", api_token="must-not-be-used", enable_write_tools=True,
        write_scopes=frozenset({"tile_sku:write"}), remote_credentials_file=str(credentials),
        idempotency_dir=str(tmp_path / "journal"),
    )
    monkeypatch.setattr(http_server, "config", config)
    http_server._requests_by_key.clear()
    seen = []

    def get(self, path, query=None):
        seen.append(self.config.api_token)
        return {"data": {"id": self.config.api_token, "role": "admin", "status": "active"}}

    monkeypatch.setattr(auth.TilesFSTApiClient, "get", get)
    return TestClient(http_server.app, headers={"Accept": "application/json, text/event-stream"}), config, seen, credentials


def test_remote_credentials_are_isolated_and_revocable(remote):
    client, config, seen, credentials = remote
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    for token in ("alice", "bob"):
        assert client.post("/mcp", json=request, headers={"Authorization": f"Bearer {token}"}).status_code == 200
    assert seen == ["alice-backend", "bob-backend"]
    credentials.write_text("{}")
    assert client.post("/mcp", json=request, headers={"Authorization": "Bearer alice"}).status_code == 401


def test_remote_scope_cannot_be_escalated(remote):
    client, _, _, _ = remote
    request = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
        "name": "create_tile_sku", "arguments": {
            "payload": {"name": "demo"}, "confirmed": True, "idempotency_key": "test-12345",
        },
    }}
    response = client.post("/mcp", json=request, headers={"Authorization": "Bearer bob"})
    payload = json.loads(response.json()["result"]["content"][0]["text"])
    assert payload["error"] == "missing_scope"


def test_remote_fail_closed_and_notifications(remote, monkeypatch):
    from src.mcp.workbuddy import http_server
    client, config, _, _ = remote
    headers = {"Authorization": "Bearer alice"}
    notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    response = client.post("/mcp", json=notification, headers=headers)
    assert response.status_code == 202 and not response.content
    assert client.post("/mcp", json=notification).status_code == 401
    assert client.post("/mcp", json=notification, headers={**headers, "Origin": "https://untrusted.invalid"}).status_code == 403
    monkeypatch.setattr(http_server, "config", replace(config, remote_credentials_file=None))
    assert client.post("/mcp", json=notification, headers=headers).status_code == 503


def test_remote_rejects_expired_backend_identity(remote, monkeypatch):
    from src.mcp.workbuddy.adapters.auth import TilesFSTApiClient
    client, _, _, _ = remote

    def expired(*args, **kwargs):
        raise BackendApiError(status_code=401, message="synthetic-private")

    monkeypatch.setattr(TilesFSTApiClient, "get", expired)
    response = client.post("/mcp", json={"method": "tools/list", "id": 1}, headers={"Authorization": "Bearer alice"})
    assert response.status_code == 401
    assert "synthetic-private" not in response.text


def test_remote_forbidden_role_and_rate_limit(remote, monkeypatch):
    from src.mcp.workbuddy import http_server
    from src.mcp.workbuddy.adapters.auth import TilesFSTApiClient
    client, config, _, _ = remote
    monkeypatch.setattr(TilesFSTApiClient, "get", lambda *a, **k: {"data": {
        "id": "user", "status": "active", "role": "customer",
    }})
    monkeypatch.setattr(http_server, "config", replace(config, rate_limit_per_minute=1))
    request = {"id": 1, "method": "tools/list"}
    headers = {"Authorization": "Bearer alice"}
    assert client.post("/mcp", json=request, headers=headers).status_code == 403
    assert client.post("/mcp", json=request, headers=headers).status_code == 429


def test_remote_schema_available_in_openapi(remote):
    client, _, _, _ = remote
    paths = client.get("/openapi.json").json()["paths"]
    assert "/mcp" in paths and "/health" in paths
