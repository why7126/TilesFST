"""Line-delimited JSON-RPC stdio MCP entrypoint for WorkBuddy."""

from __future__ import annotations

import json
import logging
import sys
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from src.mcp.workbuddy.config import load_config
from src.mcp.workbuddy.tools.registry import ToolRegistry, build_registry

PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_PROTOCOL_VERSIONS = ("2024-11-05", "2025-03-26", PROTOCOL_VERSION)


class RpcRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    jsonrpc: Literal["2.0"]
    id: str | int | None = None
    method: str
    params: dict[str, Any] = {}


class InitializeParams(BaseModel):
    model_config = ConfigDict(strict=True, extra="allow")

    protocolVersion: str
    capabilities: dict[str, Any]
    clientInfo: dict[str, Any]


class RpcResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    jsonrpc: Literal["2.0"]
    id: str | int
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None


def is_client_response(message: Any) -> bool:
    try:
        response = RpcResponse.model_validate(message)
        if (response.result is None) == (response.error is None):
            return False
        if response.error is not None:
            return type(response.error.get("code")) is int and isinstance(response.error.get("message"), str)
        return True
    except ValidationError:
        return False


def rpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle_request(message: Any, registry: ToolRegistry) -> dict[str, Any] | None:
    if is_client_response(message):
        return None
    try:
        parsed = RpcRequest.model_validate(message)
        if parsed.jsonrpc != "2.0" or ("id" in message and parsed.id is None):
            raise ValueError
    except (ValidationError, ValueError):
        return rpc_error(None, -32600, "Invalid Request")
    request_id, method, params = parsed.id, parsed.method, parsed.params
    # Notifications never execute tools, including tools/call without an id.
    if "id" not in message:
        return None
    try:
        result = _dispatch(method, params, registry)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except (ValidationError, ValueError):
        return rpc_error(request_id, -32602, "Invalid params")
    except LookupError:
        return rpc_error(request_id, -32601, "Method not found")
    except Exception:
        return rpc_error(request_id, -32603, "Internal error")


def _dispatch(method: str, params: dict[str, Any], registry: ToolRegistry) -> dict[str, Any]:
    if method == "initialize":
        initialization = InitializeParams.model_validate(params)
        if not all(isinstance(initialization.clientInfo.get(key), str)
                   for key in ("name", "version")):
            raise ValueError
        version = initialization.protocolVersion
        return {
            "protocolVersion": version if version in SUPPORTED_PROTOCOL_VERSIONS else PROTOCOL_VERSION,
            "serverInfo": {"name": "projecttilesfst-workbuddy", "version": "0.1.0"},
            "capabilities": {"tools": {}},
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": registry.list_tools()}
    if method == "tools/call":
        name = params.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("tools/call requires a tool name")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ValueError("tools/call arguments must be an object")
        payload = registry.call_tool(name, arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": payload.get("ok") is False,
        }
    raise LookupError


def main() -> int:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    registry = build_registry(load_config())
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_request(message, registry)
        except json.JSONDecodeError as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Invalid JSON: {exc.msg}"},
            }
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
