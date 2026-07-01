---
title: 需求验收标准
purpose: REQ-0018 生产环境部署与 MySQL 数据库支持验收标准
content: 基于 requirement.md 与 business-flow.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或实现变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 20:24:46
updated_at: 2026-06-28 20:24:46
note: REQ-0018-production-mysql-deployment
---

# 验收标准

## 1. 数据库连接配置（FR-001）

- [ ] **AC-001** 存在 `DATABASE_URL` 环境变量说明与示例（MySQL DSN，`charset=utf8mb4`）。
- [ ] **AC-002** `APP_ENV=production` 时 backend MUST 使用 MySQL；缺失 `DATABASE_URL` MUST fail fast，不静默回退 SQLite。
- [ ] **AC-003** `APP_ENV` 非 production 且未设置 `DATABASE_URL` 时，MUST 回退 `SQLITE_DATABASE_URL`（行为与变更前一致）。
- [ ] **AC-004** `pyproject.toml` / Docker 镜像 MUST 包含 MySQL driver 依赖并已安装。

## 2. MySQL 连接与会话（FR-002）

- [ ] **AC-005** MySQL engine MUST 启用 `pool_pre_ping`（或 OpenSpec design 中等价策略）。
- [ ] **AC-006** MySQL 连接 MUST NOT 使用 `check_same_thread` 等 SQLite 专有参数。
- [ ] **AC-007** 连接字符集 MUST 为 `utf8mb4`；文档注明 collation `utf8mb4_unicode_ci` 与客户实例一致。
- [ ] **AC-008** 文档 MUST 声明最低 MySQL 版本 8.0+。

## 3. 双路径初始化（FR-003）

- [ ] **AC-009** SQLite 路径 MUST 继续执行 `schema.sql` + `migrations.py`；本地 demo 无回归。
- [ ] **AC-010** MySQL 路径 MUST NOT 执行 `sqlite_master` / `PRAGMA` 相关逻辑。
- [ ] **AC-011** 存在 MySQL 独立初始化入口（如 `schema.mysql.sql` 或 versioned SQL）。
- [ ] **AC-012** MySQL 初始化 MUST 幂等或可安全重复（空库二次启动不致命失败）。
- [ ] **AC-013** OpenSpec change MUST 含 `design.md` 说明双 dialect 迁移策略及 Alembic 可选后续。

## 4. MySQL Schema 对齐（FR-004）

- [ ] **AC-014** MySQL baseline MUST 包含当前 SQLite 最终态全部业务表（users、brands、tile_categories、tiles、tile_images、tile_videos、tile_specs、topics、banners、system_settings、audit_logs、profile_activity_logs、password_change_attempts 等）。
- [ ] **AC-015** 关键唯一约束 MUST 存在（如 `users.username`、`tiles.sku_code`）。
- [ ] **AC-016** 关键索引 MUST 存在（如 `audit_logs(domain, created_at)` 复合索引）。
- [ ] **AC-017** OpenSpec `implementation/db.md` MUST 记录 SQLite→MySQL 类型映射表。

## 5. 空库 Seed（FR-005）

- [ ] **AC-018** 空 MySQL 库首次启动后 MUST 创建 `ADMIN_USERNAME` 管理员（bcrypt 哈希）。
- [ ] **AC-019** `ADMIN_RESET_PASSWORD_ON_STARTUP` 行为与 SQLite 环境一致；文档强调生产用后改回 `false`。
- [ ] **AC-020** 本期 MUST NOT 提供 SQLite 业务数据自动导入 MySQL 的工具。
- [ ] **AC-021** 管理员 MUST 可通过 `POST /api/v1/auth/login` 与管理端 Web 登录。

## 6. 生产 Docker Compose（FR-006）

- [ ] **AC-022** 存在 `docker-compose.prod.yml`（或文档等价名）及启动说明。
- [ ] **AC-023** 生产 Compose MUST 包含 backend、web、minio、minio-init；MUST NOT 包含 mysql 服务。
- [ ] **AC-024** 生产 backend MUST NOT 将 `./data/sqlite` 作为生产数据库卷。
- [ ] **AC-025** 文档 MUST 说明 VPS 访问外部 MySQL 的网络/防火墙要求。
- [ ] **AC-026** 生产示例 MUST 使用非默认 `APP_SECRET_KEY`、MinIO 密钥。

## 7. 文档与环境变量（FR-007）

- [ ] **AC-027** 已更新根目录 `.env.example`（`DATABASE_URL`、`APP_ENV=production` 说明）。
- [ ] **AC-028** 已更新 `docs/02-deployment.md` 生产 VPS + 外部 MySQL 章节。
- [ ] **AC-029** 已更新 `docs/04-database-design.md`、`rules/database.md`、`rules/environment.md`。
- [ ] **AC-030** 文档含 MySQL 前置检查清单：8.0+、utf8mb4、权限、网络可达。

## 8. MinIO 生产（FR-008）

- [ ] **AC-031** 生产 Compose 为 MinIO 配置持久化 volume。
- [ ] **AC-032** `minio-init` MUST 初始化单桶 `MINIO_BUCKET`（与 dev 策略一致）。
- [ ] **AC-033** 生产环境 MUST 完成一次图片上传并通过 `/media/{object_key}` 访问成功。
- [ ] **AC-034** 重启 backend/web/minio 后已上传对象 MUST 仍可访问。

## 9. 测试（FR-009）

- [ ] **AC-035** `cd src/backend && pytest`（SQLite 默认）MUST 通过。
- [ ] **AC-036** 存在 MySQL 集成验证（CI service container 或 `@pytest.mark.mysql` optional job）。
- [ ] **AC-037** MySQL 测试 MUST 覆盖：schema 初始化、admin seed、至少一条 API（登录或 health + CRUD）。

## 10. OpenSpec 与规范（FR-010）

- [ ] **AC-038** 已通过 `/req-opsx` 创建 OpenSpec change（建议 `add-production-mysql-deployment`）。
- [ ] **AC-039** change 内含 `implementation/db.md`。
- [ ] **AC-040** 归档后 `openspec/project.md` 技术栈 MUST 反映 SQLite dev + MySQL prod。

## 11. 不回归

- [ ] **AC-041** 前端 Web / 小程序 MUST NOT 要求代码变更（无 Orval 契约变更时可不跑 Orval）。
- [ ] **AC-042** `./scripts/docker-up.sh` 本地 Demo MUST 仍使用 SQLite + MinIO。
- [ ] **AC-043** API 路径、响应格式、错误码 MUST 无无意变更。
- [ ] **AC-044** REQ-0017 系统设置 MUST NOT 暴露在线修改 `DATABASE_URL`。

## 12. UI / 原型

- [ ] **AC-045** 本需求无 UI 变更；**无需** HTML/PNG 原型（N/A）。

## 横切 AC（knowledge-base）

> **N/A — 本 REQ 为纯基础设施/部署/数据库，无 admin-list / admin-form / admin-modal / media-upload UI 场景标签。**
