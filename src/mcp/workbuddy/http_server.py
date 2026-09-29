"""HTTP MCP entrypoint for WorkBuddy remote deployment."""

from __future__ import annotations

import time
import logging
import json
from collections import defaultdict, deque
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from src.mcp.workbuddy.config import load_config
from src.mcp.workbuddy.adapters.auth import authenticate
from src.mcp.workbuddy.server import SUPPORTED_PROTOCOL_VERSIONS, handle_request, rpc_error

config = load_config()
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="ProjectTilesFST WorkBuddy MCP", version="0.1.0")
_requests_by_key: dict[str, deque[float]] = defaultdict(deque)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "remote_auth_configured": bool(config.remote_credentials_file)}


@app.post("/mcp")
async def mcp_endpoint(
    request: Request,
    authorization: str | None = Header(default=None),
) -> Any:
    if request.headers.get("origin"):
        raise HTTPException(status_code=403, detail="Browser origins are not supported")
    _rate_limit(request)
    registry = await run_in_threadpool(authenticate, config, authorization)
    version = request.headers.get("mcp-protocol-version", "2025-03-26")
    if version not in SUPPORTED_PROTOCOL_VERSIONS:
        raise HTTPException(status_code=400, detail="Unsupported MCP protocol version")
    if request.headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
        raise HTTPException(status_code=415, detail="Content-Type must be application/json")
    accept = {part.split(";")[0].strip().lower() for part in request.headers.get("accept", "").split(",")}
    if not {"application/json", "text/event-stream"}.issubset(accept):
        raise HTTPException(status_code=406, detail="Accept must include JSON and event-stream")
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > config.max_request_bytes:
            raise HTTPException(status_code=413, detail="MCP request too large")
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        return JSONResponse(rpc_error(None, -32700, "Parse error"), status_code=400)
    response = await run_in_threadpool(handle_request, payload, registry)
    if response is None:
        return Response(status_code=202)
    status = 400 if response.get("error", {}).get("code") == -32600 else 200
    return JSONResponse(response, status_code=status)


def _rate_limit(request: Request) -> None:
    limit = max(1, config.rate_limit_per_minute)
    key = request.client.host if request.client else "unknown"
    now = time.monotonic()
    for expired_key in list(_requests_by_key):
        if not _requests_by_key[expired_key] or _requests_by_key[expired_key][-1] <= now - 60:
            del _requests_by_key[expired_key]
    if key not in _requests_by_key and len(_requests_by_key) >= 4096:
        raise HTTPException(status_code=429, detail="Connector rate limit capacity reached")
    window = _requests_by_key[key]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= limit:
        raise HTTPException(status_code=429, detail="Connector rate limit exceeded")
    window.append(now)
