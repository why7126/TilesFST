---
change_id: add-production-mysql-deployment
title: 生产环境部署与 MySQL 数据库支持设计
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 09:55:35
source_requirement: REQ-0018-production-mysql-deployment
status: proposed
---

## Context

当前本地与 Docker 演示部署使用 FastAPI + SQLite 文件库 + MinIO。`docker-compose.yml` 将 `./data/sqlite` 挂载给 backend，`docs/02-deployment.md` 也以 SQLite 为默认数据库说明。后端配置尚无统一 `DATABASE_URL`，数据库初始化链路绑定 SQLite 专有能力，包括 `sqlite_master`、`PRAGMA`、`AUTOINCREMENT` 等。

客户生产环境已提供 MySQL 8.0+，字符集 / collation 为 `utf8mb4_unicode_ci`。本 change 需要引入生产 MySQL 路径，但不能让本地开发者和现有 CI 必须安装 MySQL。

## Conflict Resolution

| 检查项 | 需求 / 验收 | 现有 specs / 实现 | 决议 |
|---|---|---|---|
| 数据库定位 | production 必须 MySQL，dev/demo 默认 SQLite | `openspec/project.md` 与 `rules/database.md` 仍描述 SQLite | 新增 `database` capability；归档前同步项目技术栈为 SQLite(dev/demo)+MySQL(prod) |
| 生产 Compose | backend/web/minio/minio-init，外部 MySQL，不含 mysql 服务 | `docker-compose.yml` 是本地 demo，挂载 SQLite | 新增 `deployment` capability；创建 prod Compose 变体，保留 dev Compose |
| MinIO | 生产继续自建 MinIO 单桶 | `object-storage` 已约束单桶与 Key | 对 `object-storage` 增补生产持久化与冒烟要求 |
| UI 原型 | 无 UI 变更 | UI rules 不适用 | UI Explore Gate = N/A；无 prototype 冲突 |
| API 契约 | 登录与上传等既有 API 可用 | `api-governance` 已约束 envelope/OpenAPI | 不新增 API spec；实现若不改契约则无需 Orval |

## Goals / Non-Goals

**Goals:**

- `APP_ENV=production` 时强制 MySQL `DATABASE_URL`，无效配置快速失败。
- 非 production 默认继续使用 `SQLITE_DATABASE_URL`，`./scripts/docker-up.sh` 行为不变。
- MySQL 使用独立 baseline / migration 路径，覆盖当前 SQLite 最终业务表。
- 空 MySQL 首次启动后自动创建默认管理员，行为与现有 `ADMIN_*` env 一致。
- 新增生产 Compose 与 runbook，连接外部 MySQL，继续使用 MinIO 单桶持久化。
- 增加 MySQL 验证路径，并保留 SQLite pytest 默认路径。

**Non-Goals:**

- 不提供 SQLite 到 MySQL 的业务数据 ETL / 一键迁移工具。
- 不在生产 Compose 内启动 mysql 服务。
- 不实现 MySQL 高可用、自动备份 job、主从、读写分离。
- 不引入 K8s、Helm、Terraform 或云厂商专有配置。
- 不把 `DATABASE_URL` 暴露到管理端系统设置页面。
- 不做 Web / 小程序 UI 改动。

## Decisions

### D1：统一 `DATABASE_URL`，按 `APP_ENV` 强制生产 MySQL

- **决策**：新增 `DATABASE_URL`，保留 `SQLITE_DATABASE_URL` 作为非生产默认值。`APP_ENV=production` 时 `DATABASE_URL` 必须存在且 dialect 为 `mysql` / `mysql+pymysql`，否则启动失败。
- **理由**：生产配置必须显式，避免静默回退 SQLite 造成数据写入容器或本地文件卷。
- **替代方案**：使用 `DATABASE_ENGINE=mysql` + 多个分散 env；被拒绝，因为 SQLAlchemy URL 已能表达 driver、host、db、charset。

### D2：按 dialect 拆分 engine 参数

- **决策**：SQLite engine 继续使用 `check_same_thread=False`；MySQL engine 使用 `pool_pre_ping=True`，并设置保守连接池默认值（如 pool_size=5、max_overflow=10，最终以实现和文档为准）。
- **理由**：SQLite 与 MySQL 连接参数不兼容，强行共用会导致启动失败或连接不稳定。

### D3：MySQL 使用 baseline DDL + forward-only 迁移入口

- **决策**：新增 `schema.mysql.sql` 和可选 `mysql_migrations/`，首版允许 baseline only，但必须具备幂等或版本记录能力。SQLite 保留 `schema.sql` + `migrations.py`。
- **理由**：现有 SQLite 迁移逻辑包含 MySQL 不支持的 introspection 和 DDL 语法，不能复用。
- **后续路线**：后续可单独 OpenSpec Change 引入 Alembic 统一迁移。

### D4：MySQL DDL 对齐 SQLite 最终态

- **决策**：实现阶段先从 `schema.sql` + `migrations.py` 汇总最终表结构，再生成 MySQL baseline。`implementation/db.md` 必须记录表清单、类型映射、索引与约束。
- **理由**：客户生产空库上线需要功能完整，而不是只覆盖初始 schema。

### D5：生产 Compose 不内嵌 MySQL

- **决策**：新增 `docker-compose.prod.yml` 或等价生产文件，仅包含 backend、web、minio、minio-init；backend 通过 env 访问客户 MySQL。
- **理由**：客户已有 MySQL 实例，生产 Compose 只负责应用栈与对象存储。

### D6：MinIO 生产继续单桶 + 持久化

- **决策**：生产仍使用一个 `MINIO_BUCKET`，桶内沿用 `original/`、`videos/`、`videos/covers/`、`processed/` 等前缀。MinIO volume 必须持久化，密钥必须非默认。
- **理由**：保持现有媒体 URL 和 object_key 兼容，不扩大存储迁移范围。

### D7：测试分层

- **决策**：SQLite pytest 仍为默认本地/CI路径；MySQL 验证可通过 CI service container 或 `@pytest.mark.mysql` optional job / documented manual smoke 提供。
- **理由**：生产化不应提高日常开发门槛，但必须覆盖 MySQL 启动和读写路径。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| SQLite 与 MySQL SQL 细节不兼容 | DDL 单独维护；Repository SQL 差异通过测试暴露；复杂查询必要时按 dialect 分支 |
| MySQL baseline 漏表或漏索引 | 从最终 SQLite schema 与 migrations 汇总；`implementation/db.md` 列表化；MySQL 测试覆盖关键表 |
| 生产 secret 误用示例值 | `.env.example` 与部署文档明确禁止；Compose 示例使用占位强提醒 |
| 网络不可达导致上线失败 | runbook 添加 MySQL host/port、白名单、账号权限检查；backend fail-fast 日志可定位 |
| 本地开发被 MySQL 依赖拖慢 | MySQL 测试 optional/CI service；默认 SQLite 不变 |

## Migration Plan

1. 新增 env 与后端配置解析，非 production 保持 SQLite。
2. 新增 MySQL driver 与 dialect-aware engine。
3. 新增 MySQL baseline DDL / migration 入口与 `implementation/db.md`。
4. 接入 MySQL 初始化与管理员 seed。
5. 新增生产 Compose 与生产部署文档。
6. 补充 MySQL 测试 / smoke，并跑 SQLite 回归。
7. 更新 docs、rules、README 与 `openspec/project.md`。

## Rollback

- dev/demo 回滚：继续使用 `docker-compose.yml` 与 SQLite 文件卷。
- production 回滚：停止 prod Compose，恢复上一镜像与上一份 env；MySQL schema 变更首版只做新增 baseline，rollback 主要以数据库备份恢复为准。

## Open Questions

- MySQL driver 最终使用 `pymysql` 还是等价驱动，由实现阶段根据 `pyproject.toml` 与部署镜像兼容性确定。
- MySQL 时间字段统一选择 `DATETIME(3)` 还是 `VARCHAR(64)`，实现阶段需在 `implementation/db.md` 固化。
