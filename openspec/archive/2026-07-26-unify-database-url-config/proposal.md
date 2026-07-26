## Why

当前数据库配置同时暴露 `DATABASE_URL` 与 `SQLITE_DATABASE_URL`，与对象存储配置收敛后的风格不一致，也容易让部署者误解哪个变量才是实际生效入口。

本变更将数据库连接统一为单一 `DATABASE_URL`：本地/demo 默认 SQLite，生产环境覆盖为 MySQL，并保留生产 fail fast 规则。

## What Changes

- 移除后端应用对 `SQLITE_DATABASE_URL` 的配置依赖。
- 将 `.env.example` 中 `DATABASE_URL` 默认值改为本地 SQLite DSN。
- 更新数据库解析逻辑：所有环境均读取 `DATABASE_URL`，生产环境要求其为 MySQL。
- 更新部署、数据库文档和测试。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `database`: 数据库选择策略从 `DATABASE_URL` + `SQLITE_DATABASE_URL` 双变量收敛为单一 `DATABASE_URL`。
- `deployment`: 环境变量文档不再说明 `SQLITE_DATABASE_URL` fallback，统一说明本地 SQLite 与生产 MySQL 都通过 `DATABASE_URL` 配置。

## Impact

- 后端：`src/backend/app/core/config.py`、`src/backend/app/db/session.py`。
- 环境变量：`.env.example` 移除 `SQLITE_DATABASE_URL`。
- 文档：`docs/02-deployment.md`、`docs/04-database-design.md`。
- 测试：更新数据库配置与测试 fixture。
- API / Orval / Web / 小程序：不涉及。
