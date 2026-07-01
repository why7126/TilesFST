---
requirement_id: REQ-0018-production-mysql-deployment
title: 生产环境部署与 MySQL 数据库支持
terminal: multi
version: v1
status: in_sprint
owner: product
source: issues/requirements/archive/REQ-0018-production-mysql-deployment/capture.md
priority: P0
parent_requirement:
created_at: 2026-06-28 20:23:08
updated_at: 2026-06-29 09:59:17
---

# REQ-0018 生产环境部署与 MySQL 数据库支持

## 1. 需求背景

TILESFST 当前可在本地与 Docker Compose 演示环境运行：后端 FastAPI + **SQLite 文件库** + MinIO 单桶对象存储（见 `docker-compose.yml`、`docs/02-deployment.md`）。业务功能（管理端、店主端 Web）已在该栈上迭代多 Sprint。

产品方需要 **部署到生产环境**；客户侧已提供 **MySQL 8.0+** 实例（`utf8mb4_unicode_ci`），生产库须使用该实例，**不得**依赖 SQLite 文件卷。

`/req-explore` 已确认：

| 维度 | 决策 |
|---|---|
| 生产拓扑 | **VPS 单机 Docker Compose**（backend + web + MinIO） |
| MySQL | **客户已有实例**，不在 Compose 内起 mysql 服务 |
| 本地开发 | **SQLite 默认**；生产通过 `APP_ENV=production` 或 `DATABASE_URL` 切 MySQL |
| 首版数据 | **空库 + 管理员 seed**（不做 SQLite→MySQL 业务数据迁移工具） |
| 对象存储 | 生产 **继续 MinIO**（单桶策略不变） |

**技术现状（实现约束）**：

- `Settings` 仅暴露 `SQLITE_DATABASE_URL`；无 MySQL driver 依赖。
- `session.py`、`schema.sql`、`migrations.py` 深度绑定 SQLite（`sqlite_master`、`PRAGMA`、`AUTOINCREMENT` 等）。
- Repository 层 SQL 相对可移植，但 **启动建表/迁移路径无法在 MySQL 上原样执行**。
- `AGENTS.md` / `openspec/project.md` 仍声明「后端 = SQLite」；本需求落地后须同步规范。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| **运维 / 部署人员** | 在 VPS 上用 Compose 拉起 backend/web/MinIO，连接外部 MySQL，按文档注入密钥 |
| **后端开发** | 本地继续 SQLite；CI 可验证 MySQL 路径；双环境不互相破坏 |
| **管理端用户** | 生产环境可登录、维护商品与媒体（间接受益于后端可用性） |
| **店主端 Web / 小程序** | 生产可读已发布内容（本期无端侧改动） |

## 3. 范围

### 3.1 本期包含

- 后端 **双数据库策略**：development/demo → SQLite；production → MySQL（FR-001～FR-003）
- MySQL **schema 初始化**（baseline，对应当前 SQLite 最终表结构）（FR-004）
- 生产 **空库启动**：建表 + 默认管理员 seed（与现有 `ADMIN_*` env 行为一致）（FR-005）
- **生产 Compose 编排**（如 `docker-compose.prod.yml` 或等价文件 + 启动说明）：backend、web、minio、minio-init；**不含** mysql 服务（FR-006）
- **环境变量与文档**：根目录 `.env.example`、`docs/02-deployment.md`、`rules/environment.md`、`rules/database.md` 生产章节（FR-007）
- **MinIO 生产部署**：持久化卷、单桶初始化、密钥非默认值（FR-008）
- **测试**：保留 SQLite 测试默认；新增 MySQL 集成验证路径（FR-009）
- OpenSpec Change（建议 `add-production-mysql-deployment`）及实现说明（FR-010）

### 3.2 本期不包含

- Docker Compose **内嵌** MySQL 服务或 MySQL 镜像维护
- **SQLite → MySQL 业务数据**一键迁移 / ETL 工具
- MySQL **高可用**、只读副本、自动备份 job（可在 runbook 写运维建议，非交付物）
- **K8s / Helm / Terraform** 等编排
- 云 RDS 专有集成（连接串兼容即可，不绑定厂商）
- **Alembic 全量替换**现有 SQLite 增量迁移（可文档化后续路线；本期 MySQL 采用 baseline + forward SQL）
- 前端 / 小程序 UI 或 API 契约变更
- 管理端「系统设置」中在线修改数据库连接（仍属运维级 env，见 REQ-0017 边界）

## 4. 功能要求

### FR-001 统一数据库连接配置

系统 MUST 支持通过环境变量选择数据库后端：

| 环境 | 默认行为 |
|---|---|
| `APP_ENV` ≠ `production`（含 `development`、未设置） | 使用 **SQLite**；未设置 `DATABASE_URL` 时回退 `SQLITE_DATABASE_URL`（保持现有默认路径） |
| `APP_ENV=production` | **MUST** 使用 MySQL；**MUST** 配置有效 `DATABASE_URL`（MySQL DSN） |

规则：

- MUST 引入统一 **`DATABASE_URL`**（SQLAlchemy URL，如 `mysql+pymysql://user:pass@host:3306/dbname?charset=utf8mb4`）。
- `SQLITE_DATABASE_URL` MAY 保留为 dev 便捷项；当 `DATABASE_URL` 未设置且非 production 时，由 `SQLITE_DATABASE_URL` 构造 SQLite 连接。
- production 启动时若 `DATABASE_URL` 缺失或指向 SQLite，MUST **fail fast**（明确错误日志，不静默回退 SQLite）。
- MUST 添加 MySQL Python driver 依赖（如 `pymysql` 或团队选定等价物），并在 `pyproject.toml` / Docker 镜像中安装。

### FR-002 MySQL 连接与会话

- MySQL engine MUST 使用合适连接参数（如 `pool_pre_ping=True`、合理 `pool_size`；具体值在 OpenSpec design 中确定）。
- MUST **NOT** 对 MySQL 连接使用 SQLite 专有 `connect_args={"check_same_thread": False}`。
- 字符集 MUST 为 **`utf8mb4`**；collation SHOULD 为 **`utf8mb4_unicode_ci`**（与客户实例一致）；DSN 或连接 init 中 MUST 显式声明或校验。
- 客户 MySQL 为 **MySQL 8.0+**；实现与文档 MUST 注明最低版本。

### FR-003 双路径初始化（SQLite 与 MySQL 分离）

- **SQLite 路径**：MAY 继续现有 `schema.sql` + `migrations.py` 行为，保证本地/Demo 不回退。
- **MySQL 路径**：MUST **NOT** 执行依赖 `sqlite_master` / `PRAGMA` 的逻辑。
- MySQL MUST 使用独立初始化入口，例如：
  - `schema.mysql.sql`（baseline 全量建表），及/或
  - 版本化 MySQL migration SQL（forward-only）
- 初始化 MUST **幂等或可安全重复**（至少：表已存在时不致命失败，或有明确 migration 版本表）。
- OpenSpec `design.md` MUST 记录 SQLite 与 MySQL 迁移策略差异及后续 Alembic 可选路线。

### FR-004 MySQL Schema 与 SQLite 最终态对齐

MySQL baseline schema MUST 覆盖当前 SQLite **最终**业务表（与现有功能一致），包括但不限于：

`users`、`brands`、`tile_categories`、`tiles`、`tile_images`、`tile_videos`、`tile_specs`、`topics`、`banners`、`system_settings`、`audit_logs`、`profile_activity_logs`、`password_change_attempts` 等（以 `schema.sql` + `migrations.py` 合并后的实际表为准）。

类型映射原则（OpenSpec db.md MUST 明细）：

| SQLite 现状 | MySQL 映射（建议） |
|---|---|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `BIGINT AUTO_INCREMENT PRIMARY KEY` |
| `TEXT`（ISO 时间戳） | `DATETIME(3)` 或 `VARCHAR(64)`（选定一种并全表一致） |
| `TEXT`（UUID 主键） | `CHAR(36)` / `VARCHAR(36)` |
| `REAL` | `DECIMAL` 或 `DOUBLE`（按字段语义） |
| `CHECK` 约束 | MySQL 8.0 支持；MUST 保留关键枚举约束 |

索引与唯一约束 MUST 与现有查询路径一致（如 `users.username`、`tiles.sku_code`、`audit_logs` 复合索引等）。

### FR-005 空库启动与管理员 Seed

- 生产 **空库** 首次启动：执行 MySQL schema 初始化后，若不存在默认管理员，MUST 按现有规则创建 `ADMIN_USERNAME` / `ADMIN_INITIAL_PASSWORD`（bcrypt 哈希）。
- `ADMIN_RESET_PASSWORD_ON_STARTUP` 行为 MUST 与 SQLite 环境一致；文档 MUST 强调生产使用后改回 `false`。
- MUST **NOT** 在本期交付 SQLite 存量数据自动导入 MySQL。
- Demo seed（品牌、类目等）为 **可选**；MVP 验收以「空库 + 管理员可登录」为准。

### FR-006 生产 Docker Compose（VPS）

MUST 提供生产向 Compose 文件（命名如 `docker-compose.prod.yml`）及启动说明，满足：

| 服务 | 要求 |
|---|---|
| `backend` | 连接 **外部** MySQL（经 env）；不挂载 `./data/sqlite` 作为生产库 |
| `web` | 与现网一致，Nginx 反代 API；`client_max_body_size` 与上传限制对齐 |
| `minio` + `minio-init` | 持久化卷；单桶 `MINIO_BUCKET` 初始化 |
| `mysql` | **MUST NOT** 出现在生产 Compose 中 |

Compose 示例 MUST 说明：

- VPS 防火墙：backend 仅需访问 MySQL 主机:3306（或客户指定端口）及内部 MinIO
- 宿主机端口映射策略（沿用 `HOST_PORT_*` 覆盖模式）
- 生产 **不得** 使用 `.env.example` 默认密钥

### FR-007 文档与环境变量

MUST 同步更新：

| 文件 | 内容 |
|---|---|
| 根目录 `.env.example` | `DATABASE_URL`、`APP_ENV=production` 示例、MySQL 说明、与 `SQLITE_DATABASE_URL` 关系 |
| `src/backend/.env.example`、`src/backend/.env.docker` | 开发默认仍为 SQLite |
| `docs/02-deployment.md` | 生产 VPS + 外部 MySQL + MinIO 章节 |
| `docs/04-database-design.md` | 双引擎说明、MySQL 字符集 |
| `rules/database.md` | 从「仅 SQLite」扩展为 SQLite（dev）+ MySQL（prod） |
| `rules/environment.md` | 生产密钥与 `DATABASE_URL` 注入 |
| `README.md` | 生产部署入口链接（若已有部署节则增补） |

文档 MUST 包含客户 MySQL 前置条件检查清单：版本 ≥8.0、`utf8mb4` / `utf8mb4_unicode_ci`、账号权限（DDL + DML）、网络可达。

### FR-008 MinIO 生产（继续自建）

- 生产 MUST 继续使用 **MinIO**（非切换云 S3），并遵守 **单桶 + 前缀** 策略（`rules/object-storage.md`）。
- 生产 Compose MUST 为 MinIO 配置 **持久化 volume**；`MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` MUST 非默认值。
- backend `MINIO_ENDPOINT` 在 Compose 网络内指向 `minio:9000`；对外 Console/API 端口通过 env 映射。
- 上传、媒体 URL、`object_key` 规则 **无变更**；验收须包含一次图片上传与读取。

### FR-009 测试与 CI

- 现有 pytest **默认** MAY 继续使用临时 SQLite 文件（不强制本地装 MySQL）。
- MUST 新增至少一种 **MySQL 验证**方式（二选一或组合）：
  - CI job 使用 MySQL 8 service container 跑集成测试；或
  -  documented manual smoke + 专用 pytest marker（如 `@pytest.mark.mysql`）在 CI optional job 执行
- MySQL 测试 MUST 覆盖：schema 初始化、管理员 seed、至少一条读写 API（如登录或 health + 简单 CRUD）。
- SQLite 回归 MUST 保持通过（`cd src/backend && pytest`）。

### FR-010 OpenSpec 与规范同步

- MUST 通过 `/req-opsx` 创建 OpenSpec Change（建议 `add-production-mysql-deployment`）。
- Delta spec SHOULD 新增或 MODIFIED「部署 / 数据库」相关 capability（如 `database` 或 `deployment` spec，以 opsx 时目录为准）。
- 实现 MUST 在 change 内提供 `implementation/db.md`（MySQL DDL 与类型映射）。
- 归档前 MUST 更新 `openspec/project.md` 技术栈描述（SQLite dev + MySQL prod）。

## 5. UI / UE 约束

- **无** Web 管理端、店主端、小程序 UI 变更。
- 用户可见行为：生产环境 URL 可访问、登录与既有管理功能正常；无新页面。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 安全 | 生产 `APP_SECRET_KEY`、MySQL 密码、MinIO 密钥 MUST 由部署平台注入；日志 MUST NOT 输出明文密码 |
| 可用性 | backend 启动失败（DB 不可达、schema 失败）MUST 快速失败并给出可运维排查的日志 |
| 兼容性 | 本地 `./scripts/docker-up.sh` 行为 MUST 与变更前一致（SQLite + MinIO） |
| 性能 | 连接池参数在 OpenSpec design 中给出默认值；本期不要求读写分离 |
| 备份 | MySQL 备份由客户/运维负责；文档 MAY 给出 mysqldump 建议，非交付代码 |

## 7. 目标架构

```text
┌─────────────────────────────────────────────────────────────┐
│ 客户 MySQL 8.0+（已有实例，utf8mb4_unicode_ci）              │
│ 空库 → schema init → admin seed                              │
└───────────────────────────▲─────────────────────────────────┘
                            │ DATABASE_URL (APP_ENV=production)
┌───────────────────────────┴─────────────────────────────────┐
│ VPS — docker compose prod                                      │
│  ┌────────┐      ┌──────────┐      ┌─────────┐               │
│  │  web   │ ───▶ │ backend  │ ───▶ │  MinIO  │               │
│  └────────┘      └──────────┘      └─────────┘               │
└─────────────────────────────────────────────────────────────┘

本地 / demo：backend ──▶ SQLite 文件（./data/sqlite/）
```

## 8. 关联需求与规范

| 关联 | 关系 |
|---|---|
| `docker-compose.yml` | dev/demo 基准；生产新增 prod 变体 |
| REQ-0017 系统设置 | 运维级 DB 连接不在管理端在线修改 |
| REQ-0012 对象存储 Key | MinIO 单桶与 Key 规则继续适用 |
| `rules/database.md` | MUST 更新双引擎规范 |
| `rules/compatibility.md` | Docker / 本地兼容性说明须增补 |
| `AGENTS.md` §5 技术栈 | 归档后更新「SQLite only」表述 |

## 9. 验收要点（供 `/req-complete` 展开）

1. VPS 上按生产文档启动 Compose，backend 成功连接外部 MySQL 并完成建表。
2. 空库首次启动后，使用 `ADMIN_*` 配置的管理员账号可登录管理端。
3. 本地 `docker-up.sh` 仍使用 SQLite，现有 pytest 通过。
4. 生产环境完成一次媒体上传并经 `/media/{object_key}` 访问成功。
5. 重启 backend 容器后，MySQL 与 MinIO 中数据仍在。
6. `.env.example` 与 `docs/02-deployment.md` 含完整生产检查清单。

## 10. 状态

| 项 | 值 |
|---|---|
| status | in_sprint |
| priority | P0 |
| 建议 Change | `add-production-mysql-deployment` |
| 下一步 | `/req-opsx REQ-0018-production-mysql-deployment` |
