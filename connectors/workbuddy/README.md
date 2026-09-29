---
purpose: WorkBuddy connector package
content: Manifest, MCP config, Skill, icon and deployment notes for Tencent WorkBuddy integration
created_at: 2026-09-04 00:00:00
updated_at: 2026-09-11 09:12:44
---

# WorkBuddy Connector

This package is the external connector delivery boundary for Tencent WorkBuddy.

## Local Stdio PoC

Use `mcp.json` with a local WorkBuddy-compatible MCP client. The server command is:

```bash
python -m src.mcp.workbuddy.server
```

The connector uses `TILESFST_API_BASE_URL` and `TILESFST_CONNECTOR_TOKEN` to call the existing ProjectTilesFST backend.

## HTTPS Remote MCP

部署包使用无状态 Streamable HTTP JSON，协议协商上限为 2025-06-18。单实例 Compose、构建、网关请求头、凭据目录权限与复跑命令见 [远程部署手册](../../deploy/prod/workbuddy.md)。官方 SDK 本地互操作通过不等于 WorkBuddy 原生 HTTPS 验收通过。

The remote entrypoint is:

```bash
uvicorn src.mcp.workbuddy.http_server:app --host 0.0.0.0 --port 8010
```

远程入口必须使用企业 HTTPS 网关与 `TILESFST_CONNECTOR_REMOTE_CREDENTIALS_FILE` 按用户映射凭据。旧共享 Bearer 配置已停用。写入还需要持久化共享幂等目录。映射格式、迁移、轮换和部署约束见 [部署说明](../../docs/02-deployment.md#workbuddy-远程身份与幂等)，不得将真实凭据写入交付包。

## Tools

- Read-only: SKU search, SKU detail, brand list, category list, catalog summary.
- Dry-run management: SKU create/update/status, brand/category maintenance, media upload preview.
- Controlled management writes: hidden by default and enabled only when `TILESFST_CONNECTOR_ENABLE_WRITE_TOOLS=true`, with matching write scopes and explicit confirmation.

The connector must not expose raw object keys, database DSNs, object storage credentials, auth headers, session headers, or local filesystem paths.
