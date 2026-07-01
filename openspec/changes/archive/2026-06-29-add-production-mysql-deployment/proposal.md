---
change_id: add-production-mysql-deployment
title: 生产环境部署与 MySQL 数据库支持
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 09:55:35
source_requirement: REQ-0018-production-mysql-deployment
status: proposed
---

## Why

TILESFST 当前部署基线面向本地开发与演示环境，后端默认依赖 SQLite 文件卷。客户生产环境已提供 MySQL 8.0+ 实例，平台需要在不破坏本地 SQLite 默认体验的前提下，支持 VPS Docker Compose 生产部署、外部 MySQL、MinIO 持久化与可验证的上线 runbook。

## What Changes

- 新增生产数据库能力：`APP_ENV=production` 时必须使用 MySQL `DATABASE_URL`，缺失或指向 SQLite 时 fail fast；非生产默认继续 SQLite。
- 新增 MySQL 独立初始化能力：MySQL 不执行 `sqlite_master` / `PRAGMA` 逻辑，使用 baseline DDL 或 forward-only migration，空库启动后 seed 默认管理员。
- 新增生产部署能力：提供 `docker-compose.prod.yml` 或等价生产 Compose，包含 backend、web、minio、minio-init，连接外部 MySQL，且不内嵌 mysql 服务。
- 增补生产 MinIO 要求：生产 Compose 必须持久化 MinIO 卷，继续使用单桶 `MINIO_BUCKET` 与现有对象 Key / URL 规则。
- 增补测试要求：保留 SQLite pytest 默认路径，新增 MySQL 集成验证路径，覆盖 schema 初始化、管理员 seed 和至少一条读写 API。
- 同步部署、数据库、环境变量、README、OpenSpec 项目技术栈等文档；本 change 不引入前端 UI 或小程序行为变更。

## Capabilities

### New Capabilities

- `database`: 开发/演示 SQLite 与生产 MySQL 双数据库选择、MySQL schema 初始化、管理员 seed、双路径迁移策略。
- `deployment`: VPS Docker Compose 生产部署、外部 MySQL 接入、生产环境变量、生产 runbook 与本地 demo 不回归。

### Modified Capabilities

- `object-storage`: 生产部署下 MinIO 仍采用单桶策略，并必须使用持久化 volume 与非默认密钥完成对象上传/读取验证。
- `testing`: 新增 MySQL 集成验证要求，同时保持现有 SQLite 默认测试路径通过。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `Settings`、数据库 session/初始化、MySQL driver、管理员 seed、启动 fail-fast |
| 数据库 | 新增 MySQL baseline DDL / migration 路径；SQLite 路径保持 |
| Docker / 部署 | 新增生产 Compose；dev/demo `docker-compose.yml` 和 `scripts/docker-up.sh` 不回归 |
| 对象存储 | 生产 MinIO 持久化与单桶初始化；上传/读取规则不变 |
| Web / 管理端 | 无 UI 变更；生产 Web Nginx 继续反代 API 与 `/media/` |
| API / Orval | 不新增或修改 API 契约；若实现中无契约变更可不运行 Orval |
| 测试 | SQLite pytest 继续默认；新增 MySQL optional/CI 集成验证 |
| 文档 | `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`、`docs/02-deployment.md`、`docs/04-database-design.md`、`rules/database.md`、`rules/environment.md`、`README.md`、`openspec/project.md` |
