from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.core.request_logging import ALLOWED_CLIENT_TYPES
from app.services.tile_sku_admin_service import VALID_PAGE_SIZES

from src.mcp.workbuddy.adapters.api_client import TilesFSTApiClient
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig
from src.mcp.workbuddy.http_server import app
from src.mcp.workbuddy.server import handle_request
from src.mcp.workbuddy.tools.registry import ToolRegistry


@pytest.fixture(autouse=True)
def isolate_write_journal(tmp_path, monkeypatch):
    from src.mcp.workbuddy.adapters.idempotency import WriteJournal
    original = WriteJournal.__init__
    monkeypatch.setattr(WriteJournal, "__init__", lambda self, directory: original(self, str(tmp_path / "journal")))


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict | None]] = []

    def get(self, path: str, query: dict | None = None) -> dict:
        self.calls.append(("GET", path, query))
        if path.endswith("/tile-skus"):
            assert query is not None and query["page_size"] in VALID_PAGE_SIZES
            return {
                "data": {
                    "items": [
                        {
                            "id": 1,
                            "name": "Moon White",
                            "sku_code": "MW-001",
                            "status": "PUBLISHED",
                            "brand_name": "Demo",
                            "category_name": "Wall",
                            "material_completeness": "complete",
                        }
                    ],
                    "summary": {
                        "total": 1,
                        "published_count": 1,
                        "needs_completion_count": 0,
                        "draft_count": 0,
                    },
                    "pagination": {"total": 1},
                }
            }
        if path.endswith("/brands"):
            return {"data": {"items": [{"id": 1, "name": "Demo"}], "pagination": {"total": 1}}}
        if path.endswith("/tile-categories"):
            return {"data": {"items": [{"id": 1, "name": "Wall"}], "pagination": {"total": 1}}}
        return {"data": {"id": 1}}

    def upload_file(self, path: str, **kwargs) -> dict:
        self.calls.append(("UPLOAD", path, kwargs))
        return {
            "data": {
                "object_key": "images/default/tiles/pending/demo.jpg",
                "url": "/media/images/default/tiles/pending/demo.jpg",
                "task_trace_id": "trace_1",
            }
        }


def test_workbuddy_client_type_is_logged() -> None:
    assert "workbuddy_connector" in ALLOWED_CLIENT_TYPES


def test_registry_lists_read_and_preview_tools_by_default() -> None:
    registry = ToolRegistry(
        FakeClient(),  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )

    names = {tool["name"] for tool in registry.list_tools()}

    assert "search_tile_skus" in names
    assert "preview_media_upload" in names
    assert "create_tile_sku" not in names


def test_preview_media_upload_is_dry_run_without_api_call() -> None:
    client = FakeClient()
    registry = ToolRegistry(
        client,  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )

    result = registry.call_tool(
        "preview_media_upload",
        {
            "target": "tile_image",
            "file_name": "tile.jpg",
            "content_type": "image/jpeg",
            "file_size_bytes": 1024,
        },
    )

    assert result["ok"] is True
    assert result["dry_run"] is True
    assert result["side_effects"] is False
    assert client.calls == []


def test_catalog_summary_is_deterministic() -> None:
    registry = ToolRegistry(
        FakeClient(),  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )

    result = registry.call_tool("summarize_catalog", {"sample_size": 5})

    assert result["ok"] is True
    assert result["data"]["sku_summary"]["total"] == 1
    assert result["data"]["representative_skus"][0]["sku_code"] == "MW-001"
    assert result["data"]["brand_count"] == 1
    assert result["data"]["category_count"] == 1


def test_stdio_json_rpc_tools_list() -> None:
    registry = ToolRegistry(
        FakeClient(),  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )

    response = handle_request(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        registry,
    )

    assert response is not None
    assert response["id"] == 1
    assert any(tool["name"] == "search_tile_skus" for tool in response["result"]["tools"])
    search = next(tool for tool in response["result"]["tools"] if tool["name"] == "search_tile_skus")
    page_size = search["inputSchema"]["properties"]["page_size"]
    assert set(page_size["enum"]) == VALID_PAGE_SIZES
    assert page_size["default"] == 20


@pytest.mark.parametrize("name", ["search_tile_skus", "summarize_catalog", "unknown"])
def test_stdio_tool_result_uses_text_content(name) -> None:
    registry = ToolRegistry(
        FakeClient(),  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )
    response = handle_request(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name}}, registry,
    )
    result = response["result"]
    assert result["content"][0]["type"] == "text"
    payload = json.loads(result["content"][0]["text"])
    assert payload["ok"] is (name != "unknown")
    assert result["isError"] is (name == "unknown")


@pytest.mark.parametrize(
    ("requested", "expected"),
    [(None, 20), (0, 10), (-1, 10), (5, 10), (10, 10), (11, 20),
     (20, 20), (21, 50), (50, 50), (51, 100), (100, 100), (101, 100)],
)
def test_search_sku_page_size_normalization(requested, expected) -> None:
    client = FakeClient()
    registry = ToolRegistry(
        client,  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )
    args = {"page": 2, "keyword": "demo", "brand_id": 3}
    if requested is not None:
        args["page_size"] = requested
    result = registry.call_tool("search_tile_skus", args)
    assert result["ok"] is True
    assert client.calls == [("GET", "/api/v1/admin/tile-skus", {
        "page": 2, "keyword": "demo", "brand_id": 3, "page_size": expected,
    })]


@pytest.mark.parametrize(("sample_size", "page_size"), [(1, 10), (5, 10), (11, 20), (21, 50), (50, 50)])
def test_catalog_summary_limits_sample_after_legal_page_fetch(sample_size, page_size) -> None:
    class PagedClient(FakeClient):
        def get(self, path, query=None):
            response = super().get(path, query)
            if path.endswith("/tile-skus"):
                response["data"]["items"] = [{"id": i} for i in range(query["page_size"])]
                response["data"]["summary"] = {"total": 200}
            return response

    client = PagedClient()
    registry = ToolRegistry(
        client,  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None),
    )
    result = registry.call_tool("summarize_catalog", {"sample_size": sample_size})
    assert result["ok"] is True
    assert client.calls[0][2] == {"page": 1, "page_size": page_size}
    assert result["data"]["sample_count"] == sample_size
    assert [item["id"] for item in result["data"]["representative_skus"]] == list(range(sample_size))
    assert result["data"]["sku_summary"] == {"total": 200}


def test_http_mcp_health_and_tools_list() -> None:
    client = TestClient(app)

    health = client.get("/health")
    tools = client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
    )

    assert health.status_code == 200
    assert health.json()["ok"] is True
    assert tools.status_code == 401


def test_api_client_headers_include_connector_identity(monkeypatch) -> None:
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return json.dumps({"data": {"ok": True}}).encode()

    def fake_urlopen(request, timeout):
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr("src.mcp.workbuddy.adapters.api_client.urlopen", fake_urlopen)
    client = TilesFSTApiClient(
        WorkBuddyConnectorConfig(
            api_base_url="http://localhost:8000",
            api_token="secret-token",
            timeout_seconds=3,
        )
    )

    client.get("/api/v1/admin/tile-skus", {"page": 1})

    headers = {key.lower(): value for key, value in captured["headers"].items()}
    assert headers["x-client-type"] == "workbuddy_connector"
    assert headers["x-client-request-id"].startswith("wb_")
    assert headers["authorization"] == "Bearer secret-token"
    assert captured["timeout"] == 3


def test_write_tools_are_scope_and_confirmation_gated() -> None:
    registry = ToolRegistry(
        FakeClient(),  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(
            api_base_url="http://localhost:8000",
            api_token=None,
            enable_write_tools=True,
            write_scopes=frozenset(),
        ),
    )

    result = registry.call_tool(
        "create_tile_sku",
        {
            "payload": {"name": "Moon White"},
            "confirmed": True,
            "idempotency_key": "idem-123456",
        },
    )

    assert result["ok"] is False
    assert result["error"] == "missing_scope"


def test_media_upload_uses_backend_upload_api_and_redacts_object_key() -> None:
    client = FakeClient()
    registry = ToolRegistry(
        client,  # type: ignore[arg-type]
        WorkBuddyConnectorConfig(
            api_base_url="http://localhost:8000",
            api_token=None,
            enable_write_tools=True,
            write_scopes=frozenset({"media:upload"}),
        ),
    )

    result = registry.call_tool(
        "upload_tile_media",
        {
            "target": "tile_image",
            "file_name": "demo.jpg",
            "content_type": "image/jpeg",
            "base64_content": "ZGVtbw==",
            "confirmed": True,
            "idempotency_key": "idem-upload-123",
        },
    )

    assert result["ok"] is True
    assert client.calls[0][1] == "/api/v1/auth/me"
    assert client.calls[1][0] == "UPLOAD"
    assert client.calls[1][1] == "/api/v1/admin/uploads/tile-images"
    assert result["data"]["object_key"] == "[redacted]"


def test_api_client_write_headers_include_trace_and_idempotency(monkeypatch) -> None:
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return json.dumps({"data": {"id": 1}}).encode()

    def fake_urlopen(request, timeout):
        captured["headers"] = dict(request.header_items())
        return Response()

    monkeypatch.setattr("src.mcp.workbuddy.adapters.api_client.urlopen", fake_urlopen)
    client = TilesFSTApiClient(
        WorkBuddyConnectorConfig(api_base_url="http://localhost:8000", api_token=None)
    )

    client.post(
        "/api/v1/admin/tile-skus",
        json_body={"name": "Moon White"},
        idempotency_key="idem-123456",
        task_type="sku_create",
    )

    headers = {key.lower(): value for key, value in captured["headers"].items()}
    assert headers["x-idempotency-key"] == "idem-123456"
    assert headers["x-task-type"] == "sku_create"
