---
purpose: WorkBuddy MCP runtime
content: ProjectTilesFST WorkBuddy MCP server entrypoints, environment variables, and safety boundaries
created_at: 2026-09-04 00:00:00
updated_at: 2026-09-06 14:48:00
---

# WorkBuddy MCP Runtime

This directory contains runtime code for the ProjectTilesFST WorkBuddy connector.

## Entrypoints

- Local stdio PoC: `python -m src.mcp.workbuddy.server`
- HTTPS remote service: `uvicorn src.mcp.workbuddy.http_server:app --host 0.0.0.0 --port 8010`

Both entrypoints share the same tool registry and backend API adapter.

## Safety Boundaries

- The connector calls existing authenticated `/api/v1/admin/*` APIs only.
- It does not query the database directly.
- It does not access MinIO or object storage directly.
- Requests set `x-client-type=workbuddy_connector` and a generated `x-client-request-id`.
- Write tools are hidden and disabled unless `TILESFST_CONNECTOR_ENABLE_WRITE_TOOLS=true`.
- Write calls require explicit `confirmed=true`, an `idempotency_key`, and a matching `TILESFST_CONNECTOR_WRITE_SCOPES` value.

## Environment Variables

- `TILESFST_API_BASE_URL`: ProjectTilesFST backend base URL.
- `TILESFST_CONNECTOR_TOKEN`: backend Bearer token for connector calls.
- `TILESFST_CONNECTOR_TIMEOUT_SECONDS`: outbound API timeout.
- `TILESFST_CONNECTOR_ENABLE_WRITE_TOOLS`: set `true` only in a controlled enterprise deployment.
- `TILESFST_CONNECTOR_WRITE_SCOPES`: comma-separated scopes, such as `tile_sku:write,brand:write`.
- `TILESFST_CONNECTOR_REMOTE_CREDENTIALS_FILE`: mandatory remote per-user credential mapping; missing configuration fails closed. The former shared HTTP bearer token is no longer accepted.
- `TILESFST_CONNECTOR_IDEMPOTENCY_DIR`: persistent journal for write reservations; all instances must share this directory. Stores only request digests and states, never business payloads.
- `TILESFST_CONNECTOR_RATE_LIMIT_PER_MINUTE`: in-memory HTTP rate limit per client host.
