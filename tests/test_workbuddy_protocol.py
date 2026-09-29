"""Transport contract tests; these do not establish native WorkBuddy compatibility."""

import json
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from src.mcp.workbuddy import http_server
from src.mcp.workbuddy.server import handle_request, PROTOCOL_VERSION


class Registry:
    def __init__(self):
        self.calls = []

    def list_tools(self):
        return [{"name": "test_read", "inputSchema": {"type": "object"}}]

    def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return {"ok": True, "data": {"count": 5}}


@pytest.fixture
def remote(monkeypatch):
    registry = Registry()
    monkeypatch.setattr(http_server, "authenticate", lambda *args: registry)
    http_server._requests_by_key.clear()
    return TestClient(http_server.app, headers={
        "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": PROTOCOL_VERSION,
    }), registry


@pytest.mark.parametrize("version", ["2024-11-05", "2025-03-26", "2025-06-18", "future-version"])
def test_initialization_negotiates(remote, version):
    client, _ = remote
    response = client.post("/mcp", json={"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
        "protocolVersion": version, "capabilities": {}, "clientInfo": {"name": "test", "version": "1"},
    }})
    assert response.status_code == 200
    assert response.json()["result"]["protocolVersion"] == (PROTOCOL_VERSION if version == "future-version" else version)
    assert "mcp-session-id" not in response.headers


@pytest.mark.parametrize("message", [None, [], [1], "private", {},
    {"jsonrpc": "1.0", "id": 1, "method": "ping"},
    {"jsonrpc": "2.0", "id": True, "method": "ping"},
    {"jsonrpc": "2.0", "id": None, "method": "ping"},
    {"jsonrpc": "2.0", "id": {}, "method": "ping"}])
def test_invalid_envelope(remote, message):
    client, registry = remote
    response = client.post("/mcp", content=json.dumps(message), headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == -32600
    assert registry.calls == []


@pytest.mark.parametrize("message", [
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "write"}},
    {"jsonrpc": "2.0", "id": 1, "result": {}},
    {"jsonrpc": "2.0", "id": 1, "error": {"code": -1, "message": "test"}},
])
def test_notifications_and_responses_never_write(remote, message):
    client, registry = remote
    response = client.post("/mcp", json=message)
    assert response.status_code == 202 and response.content == b""
    assert registry.calls == []


@pytest.mark.parametrize(("method", "params", "code"), [
    ("unknown", {}, -32601), ("initialize", {}, -32602),
    ("tools/call", {}, -32602), ("tools/call", {"name": "test", "arguments": []}, -32602),
])
def test_rpc_errors(remote, method, params, code):
    client, _ = remote
    response = client.post("/mcp", json={"jsonrpc": "2.0", "id": "test", "method": method, "params": params})
    assert response.status_code == 200
    assert response.json()["id"] == "test" and response.json()["error"]["code"] == code


def test_transport_rejections(remote, monkeypatch):
    client, _ = remote
    request = {"jsonrpc": "2.0", "id": 1, "method": "ping"}
    assert client.post("/mcp", json=request, headers={"MCP-Protocol-Version": "unsupported"}).status_code == 400
    assert client.post("/mcp", json=request, headers={"Accept": "application/json"}).status_code == 406
    assert client.post("/mcp", content="{}", headers={"Content-Type": "text/plain"}).status_code == 415
    assert client.post("/mcp", json=request, headers={"Origin": "https://untrusted.invalid"}).status_code == 403
    response = client.post("/mcp", content=b'{"secret":', headers={"Content-Type": "application/json"})
    assert response.status_code == 400 and response.json()["error"]["code"] == -32700
    assert "secret" not in response.text
    monkeypatch.setattr(http_server, "config", replace(http_server.config, max_request_bytes=10))
    assert client.post("/mcp", json=request).status_code == 413
    assert client.get("/mcp").status_code == 405
    assert client.delete("/mcp").status_code == 405


def test_missing_version_legacy_default_and_tool_result(remote):
    client, registry = remote
    del client.headers["MCP-Protocol-Version"]
    assert client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "ping"}).json()["result"] == {}
    result = client.post("/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "test_read", "arguments": {}}}).json()["result"]
    assert json.loads(result["content"][0]["text"])["data"]["count"] == 5
    assert len(registry.calls) == 1


def test_stdio_malformed_input_does_not_crash():
    registry = Registry()
    assert handle_request([], registry)["error"]["code"] == -32600
    assert handle_request({"jsonrpc": "2.0", "id": 1, "method": "ping"}, registry)["result"] == {}


def test_official_sdk_over_live_http(remote):
    """Opt-in: uv run --project src/backend --with mcp==1.13.1 python -m pytest ..."""
    import asyncio
    import socket
    import threading
    import time

    import uvicorn

    pytest.importorskip("mcp")
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    _, registry = remote
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(http_server.app, log_config=None, log_level=None, ws="none"))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()

    async def verify():
        async with streamablehttp_client(f"http://127.0.0.1:{port}/mcp") as (reader, writer, session_id):
            async with ClientSession(reader, writer) as session:
                initialized = await session.initialize()
                assert initialized.protocolVersion == PROTOCOL_VERSION
                assert session_id() is None
                assert (await session.list_tools()).tools[0].name == "test_read"
                result = await session.call_tool("test_read", {})
                assert not result.isError
                assert json.loads(result.content[0].text)["data"]["count"] == 5
                await session.send_ping()

    try:
        deadline = time.monotonic() + 5
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started
        asyncio.run(asyncio.wait_for(verify(), timeout=15))
        assert registry.calls == [("test_read", {})]
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        sock.close()
        assert not thread.is_alive()
