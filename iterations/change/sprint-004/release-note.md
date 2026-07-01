---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-01 08:56:55
title: Sprint 004 发布说明
purpose: 记录 Sprint 004 交付能力与发布注意事项（初稿）
content: 基于 REQ-0018-production-mysql-deployment、REQ-0019-admin-superuser-protection、REQ-0022-admin-api-docs-menu、BUG-0050-user-create-validation-message-unclear 与相关 OpenSpec Change
source: AI 根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: draft
note: REQ-0018 与 REQ-0019 已完成主要实现；BUG-0050 已归档；REQ-0022 已完成 apply，待人工验收与归档
---

# Sprint 004 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-004 |
| 关联需求 | REQ-0018-production-mysql-deployment；REQ-0019-admin-superuser-protection；REQ-0022-admin-api-docs-menu |
| 关联 BUG | BUG-0050-user-create-validation-message-unclear |
| 关联 Change | add-production-mysql-deployment；update-admin-superuser-protection；fix-user-create-validation-message-unclear；add-admin-api-docs-menu（applied） |
| 计划周期 | 2026-06-29 10:03:38 ~ 2026-07-13 18:00:00 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **实现进行中（In progress）** |
<!-- workflow-sync:release-status:end -->

## 计划新增能力

### 生产环境部署与 MySQL 数据库支持

- `APP_ENV=production` 时 backend 必须通过 MySQL `DATABASE_URL` 连接客户已有 MySQL 8.0+ 实例。
- 非生产环境继续默认使用 SQLite，`./scripts/docker-up.sh` 行为不回归。
- 新增 MySQL baseline / migration 初始化路径，禁止 MySQL 路径执行 SQLite-only `PRAGMA` / `sqlite_master` 逻辑。
- 空 MySQL 库首次启动后按 `ADMIN_*` env 创建默认管理员，密码 bcrypt 存储。
- 新增生产向 Docker Compose（backend、web、minio、minio-init），不内嵌 mysql 服务。
- 新增外部服务型生产 Compose（backend、web），同时连接外部 MySQL 与外部 MinIO/S3 兼容对象存储。
- 生产 MinIO 保持单桶 `MINIO_BUCKET` + 前缀策略，使用持久化 volume 与非默认密钥。
- 新增 MySQL 集成验证路径，覆盖 schema init、admin seed 和至少一条 API。

### 管理端超级管理员账号保护

- 后端以 `ADMIN_USERNAME` / `settings.admin_username` 识别受保护系统账号，不新增 `super_admin` 角色。
- 用户列表与详情返回 `is_protected`、`protected_reason`，前端不得硬编码 `admin`。
- 管理端编辑、重置密码、冻结、解冻、删除受保护账号时返回统一错误。
- 默认策略下，受保护账号本人修改密码也应被拒绝，避免破坏保底管理员恢复路径。
- 用户管理列表保留操作按钮但置灰，并展示不可操作原因。

### 创建用户校验提示修复

- 管理端创建用户时，用户名长度不足等校验失败场景必须展示明确中文原因。
- 后端 `POST /api/v1/admin/users` 请求体验证错误需进入统一错误结构，避免直接暴露 FastAPI 默认 422 `detail` 数组。
- 前端创建用户弹窗必须优先展示接口返回的业务 message，不再仅显示通用兜底文案。
- 修复需覆盖 `abc` 等小于 4 位用户名、非法字符、重复用户名与创建成功路径。

### 管理端接口文档菜单与在线调试

- 管理端 SYSTEM 分组在「系统设置」下方新增「接口文档」菜单，路由为 `/admin/api-docs`。
- 仅后台管理员可见并可访问；非管理员直链访问应返回 403 或等价禁止访问状态。
- 页面展示系统所有接口，范围包含 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他 FastAPI app routes。
- 页面展示每个接口的 Method、Path、Tag/模块、认证要求、OpenAPI 纳入状态与 Orval 生成方法名。
- 本地/开发/演示环境允许 Swagger 在线调试；生产环境展示入口但隐藏或禁用 Swagger `Try It Out`。

## 数据库变更（计划）

- 新增 MySQL baseline DDL 或 MySQL migration 入口。
- MySQL baseline 覆盖当前 SQLite 最终态业务表。
- 保留 SQLite `schema.sql` + `migrations.py` 作为 dev/demo 默认路径。
- 文档化 SQLite 到 MySQL 类型映射、索引、唯一约束和外键语义。
- REQ-0019 不计划新增表结构，但会保护既有 `users` 记录不被管理端破坏性更新。
- BUG-0050 不计划新增表结构。

## API 变更（计划）

- REQ-0018 不计划新增或修改 API 契约。
- 既有 `POST /api/v1/auth/login` 用作生产 admin seed 验证。
- 既有上传与 `/media/{object_key}` 用作 MinIO 生产 smoke。
- REQ-0019 计划在用户列表/详情响应中新增 `is_protected` 与 `protected_reason` 字段。
- REQ-0019 计划为受保护账号操作增加或复用 403 错误码，并同步 `docs/standards/error-codes.md`。
- API 契约变化后必须补跑 Orval 并更新前端类型。
- BUG-0050 计划修正 `POST /api/v1/admin/users` 用户名校验失败响应；若统一错误响应或 OpenAPI 错误示例发生契约变化，需同步 API 文档并评估 Orval。
- REQ-0022 新增 `GET /api/v1/admin/api-docs` 管理端接口目录聚合 API，用于补充 OpenAPI 默认遗漏的 `/health`、`/media/{object_key:path}` 与其他非 `/api/v1` 路由。
- REQ-0022 已同步 OpenAPI、Orval 生成方法名映射与 `docs/03-api-index.md` 的关系说明。

## 部署注意事项

- 生产必须配置 `APP_ENV=production` 与 MySQL `DATABASE_URL`。
- 生产不得使用 `.env.example` 默认 `APP_SECRET_KEY`、MySQL 密码、MinIO 密钥或管理员初始密码。
- 客户 MySQL 前置条件：MySQL 8.0+、`utf8mb4`、`utf8mb4_unicode_ci`、账号具备 DDL + DML 权限、VPS 到 MySQL 网络可达。
- 生产 Compose 不包含 mysql 服务，backend 不挂载 `./data/sqlite` 作为生产数据库。
- 外部 MinIO 场景使用 `docker-compose.prod.external.yml`，不会启动本地 minio/minio-init，需运维提前创建 `MINIO_BUCKET` 并配置最小读写权限。
- MinIO volume 必须持久化；重启后媒体对象仍应可读取。

## 不在本 Sprint

- SQLite 到 MySQL 业务数据迁移工具。
- MySQL 高可用、自动备份、主从、读写分离。
- K8s / Helm / Terraform。
- 新增 `super_admin` / `root` 角色枚举。
- 店主端 Web 或微信小程序页面改造。
- 视频、图片或对象存储能力变更。
- 面向外部用户的公开接口文档站点。
- 生产环境 Swagger `Try It Out`。
- 通过管理端编辑 OpenAPI schema、Orval 配置或后端路由。

## 验收提示

- SQLite 默认 pytest 通过。
- MySQL optional 集成验证入口已提供；真实 MySQL 验证需配置 `MYSQL_TEST_DATABASE_URL`。
- 生产 Compose 配置校验通过。
- 生产类媒体上传、读取和重启后读取 smoke 已在本地外部 MySQL + 外部 MinIO 环境通过；目标 VPS 上线前仍需按实际域名/网络复测。
- `openspec validate add-production-mysql-deployment --strict` 通过。
- REQ-0019 已创建 `update-admin-superuser-protection`，开发时执行 `/opsx-apply update-admin-superuser-protection`。
- REQ-0019 验收需覆盖后端保护、前端置灰、错误码、Orval 和普通用户不回归。
- BUG-0050 已创建 `fix-user-create-validation-message-unclear`，开发时执行 `/opsx-apply fix-user-create-validation-message-unclear`。
- BUG-0050 验收需覆盖后端统一 422/业务错误、前端弹窗错误展示、用户管理页弹窗布局与既有成功创建路径不回归。
- REQ-0022 已完成 apply，验收覆盖管理员权限、`/admin/api-docs` 导航、非 `/api/v1` 路由清单、生产 Try It Out 禁用、Orval 方法名展示与管理端横切 UI gate。
- API governance 校验剩余失败为既有管理端路由缺少 decorator tags，本次新增 `admin_api_docs.py` 已补齐 tags。
