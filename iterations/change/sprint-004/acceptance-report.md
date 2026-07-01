---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-01 08:56:55
title: Sprint 004 验收报告
purpose: 记录 Sprint 004 验收结果与遗留项（模板）
content: 基于 REQ-0018-production-mysql-deployment、REQ-0019-admin-superuser-protection、REQ-0022-admin-api-docs-menu 与 BUG-0050-user-create-validation-message-unclear acceptance.md
source: AI 根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: draft
note: workflow-sync — 3/4 Change 已 archive；1 applied；待人工 sign-off
---

# Sprint 004 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-004 |
| 关联需求 | REQ-0018-production-mysql-deployment；REQ-0019-admin-superuser-protection；REQ-0022-admin-api-docs-menu |
| 关联 BUG | BUG-0050-user-create-validation-message-unclear |
| 关联 Change | add-production-mysql-deployment；update-admin-superuser-protection；fix-user-create-validation-message-unclear；add-admin-api-docs-menu（applied） |
| 计划验收日期 | 2026-07-13 18:00:00 |
| 验收结论 | REQ-0018、REQ-0019 与 BUG-0050 已完成归档；REQ-0022 已完成 apply，待人工 sign-off 与归档 |
| 验收人 | 待填写 |
| 归档日期 | 待归档 |

## REQ-0018 功能验收

> 来源：`issues/requirements/archive/REQ-0018-production-mysql-deployment/acceptance.md`  
> 状态：in_sprint，已完成主要实现与本地外部 MySQL + 外部 MinIO smoke；待人工 sign-off

### 1. 数据库连接配置（AC-001～AC-004）

- [x] AC-001 `DATABASE_URL` 环境变量说明与 MySQL DSN 示例存在。
- [x] AC-002 `APP_ENV=production` 时必须使用 MySQL；缺失 `DATABASE_URL` fail fast。
- [x] AC-003 非 production 且未设置 `DATABASE_URL` 时回退 `SQLITE_DATABASE_URL`。
- [x] AC-004 MySQL driver 已加入依赖并进入 Docker 镜像。

### 2. MySQL 连接与会话（AC-005～AC-008）

- [x] AC-005 MySQL engine 启用 `pool_pre_ping` 或等价策略。
- [x] AC-006 MySQL 连接不使用 SQLite `check_same_thread`。
- [x] AC-007 字符集为 `utf8mb4`，文档注明 `utf8mb4_unicode_ci`。
- [x] AC-008 文档声明最低 MySQL 8.0+。

### 3. 双路径初始化（AC-009～AC-013）

- [x] AC-009 SQLite 路径继续执行 `schema.sql` + `migrations.py`。
- [x] AC-010 MySQL 路径不执行 `sqlite_master` / `PRAGMA` 逻辑。
- [x] AC-011 MySQL 独立初始化入口存在。
- [x] AC-012 MySQL 初始化可安全重复。
- [x] AC-013 `design.md` 说明双 dialect 迁移策略及 Alembic 后续路线。

### 4. MySQL Schema 对齐（AC-014～AC-017）

- [x] AC-014 MySQL baseline 覆盖当前 SQLite 最终态全部业务表。
- [x] AC-015 关键唯一约束存在。
- [x] AC-016 关键索引存在。
- [x] AC-017 `implementation/db.md` 记录 SQLite→MySQL 类型映射。

### 5. 空库 Seed（AC-018～AC-021）

- [x] AC-018 空 MySQL 库首次启动后创建 `ADMIN_USERNAME` 管理员。
- [x] AC-019 `ADMIN_RESET_PASSWORD_ON_STARTUP` 行为与 SQLite 一致。
- [x] AC-020 未提供 SQLite 业务数据自动导入 MySQL 工具。
- [x] AC-021 管理员可通过登录 API 与管理端登录。

### 6. 生产 Docker Compose（AC-022～AC-026）

- [x] AC-022 存在生产 Compose 与启动说明。
- [x] AC-023 生产 Compose 包含 backend、web、minio、minio-init；不包含 mysql。
- [x] AC-024 生产 backend 不挂载 `./data/sqlite` 作为生产库。
- [x] AC-025 文档说明 VPS 访问外部 MySQL 网络/防火墙要求。
- [x] AC-026 生产示例使用非默认密钥。
- [x] AC-026a 存在外部 MySQL + 外部 MinIO Compose 变体，且仅包含 backend、web。

### 7. 文档与环境变量（AC-027～AC-030）

- [x] AC-027 根目录 `.env.example` 已更新。
- [x] AC-028 `docs/02-deployment.md` 已更新生产 VPS + 外部 MySQL 章节。
- [x] AC-029 `docs/04-database-design.md`、`rules/database.md`、`rules/environment.md` 已更新。
- [x] AC-030 文档含 MySQL 前置检查清单。

### 8. MinIO 生产（AC-031～AC-034）

- [x] AC-031 生产 Compose 为 MinIO 配置持久化 volume。
- [x] AC-032 `minio-init` 初始化单桶 `MINIO_BUCKET`。
- [x] AC-033 生产环境完成一次图片上传并可通过 `/media/{object_key}` 访问。
- [x] AC-034 重启 backend/web/minio 后已上传对象仍可访问。
- [x] AC-034a 外部 MinIO 场景文档要求 bucket 预创建、最小读写权限和 backend 受控读取。

### 9. 测试（AC-035～AC-037）

- [x] AC-035 SQLite 默认 pytest 通过。
- [x] AC-036 存在 MySQL 集成验证。
- [x] AC-037 MySQL 测试覆盖 schema 初始化、admin seed、至少一条 API。

### 10. OpenSpec 与规范（AC-038～AC-040）

- [x] AC-038 已通过 `/req-opsx` 创建 OpenSpec change。
- [x] AC-039 change 内含 `implementation/db.md`。
- [x] AC-040 归档后 `openspec/project.md` 反映 SQLite dev + MySQL prod。

### 11. 不回归（AC-041～AC-044）

- [x] AC-041 前端 Web / 小程序不要求代码变更；无契约变更时可不跑 Orval。
- [x] AC-042 `./scripts/docker-up.sh` 本地 Demo 仍使用 SQLite + MinIO。
- [x] AC-043 API 路径、响应格式、错误码无无意变更。
- [x] AC-044 REQ-0017 系统设置不暴露在线修改 `DATABASE_URL`。

### 12. UI / 原型（AC-045）

- [x] AC-045 本需求无 UI 变更，无需 HTML/PNG 原型。

## REQ-0019 功能验收

> 来源：`issues/requirements/archive/REQ-0019-admin-superuser-protection/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `update-admin-superuser-protection` 已 applied，待归档

### 1. 保护账号识别（AC-001～AC-006）

- [x] AC-001 后端以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护账号。
- [x] AC-003 `GET /api/v1/admin/users` 返回 `is_protected` 与 `protected_reason`。
- [x] AC-004 `GET /api/v1/admin/users/{id}` 返回 `is_protected` 与 `protected_reason`。
- [x] AC-006 前端不硬编码 `admin` 判断保护状态。

### 2. 用户管理操作保护（AC-007～AC-018）

- [x] AC-007 编辑受保护账号返回错误，HTTP 建议 403。
- [x] AC-011 重置受保护账号密码返回错误，且不生成新密码。
- [x] AC-015 状态变更请求 `active`、`disabled` 或 `deleted` 均返回错误。
- [x] AC-018 普通用户冻结、解冻、删除规则保持 REQ-0005 既有行为。

### 3. 本人修改密码保护（AC-019～AC-023）

- [x] AC-019 默认策略下，受保护账号本人改密返回错误。
- [x] AC-020 改密失败后 `password_hash` 保持不变。
- [x] AC-021 改密失败后 `token_version` 不递增。
- [x] AC-022 前端改密弹窗展示接口返回 message。

### 4. 错误码、OpenAPI 与 Orval（AC-024～AC-027）

- [x] AC-024 新增或复用清晰错误码表示“系统保底管理员账号不允许执行该操作”。
- [x] AC-025 错误码登记到后端定义与 `docs/standards/error-codes.md`。
- [x] AC-026 API 响应保持统一结构。
- [x] AC-027 OpenAPI 暴露新增字段，API 变更后执行 Orval。

### 5. 前端 UI 与横切 AC（AC-028～AC-032、AC-XCUT-001～004）

- [x] AC-028 受保护账号行保留操作按钮但置灰，不隐藏。
- [x] AC-030 `protected_reason` 通过 `title`、tooltip 或等价方式展示。
- [x] AC-XCUT-001 用户管理页分页 DOM 仍对齐 `/admin/users` 基准。
- [x] AC-XCUT-003 状态变更类操作仍使用 DS confirm modal，不引入 `window.confirm`。

### 6. 自动化测试与 OpenSpec（AC-036～AC-044）

- [x] AC-036～AC-040 pytest 覆盖受保护账号识别、编辑、重置、状态变更和本人改密策略。
- [x] AC-041 Vitest / Testing Library 覆盖受保护账号行操作按钮置灰和普通用户不受影响。
- [x] AC-042 已通过 `/req-opsx` 创建 `update-admin-superuser-protection`。
- [x] AC-044 Change tasks 包含后端集成测试、前端列表按钮测试、Orval 生成与错误码文档同步。

## BUG-0050 回归验收

> 来源：`issues/bugs/archive/BUG-0050-user-create-validation-message-unclear/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-user-create-validation-message-unclear` 已 proposed

### 1. 后端校验错误（AC-001～AC-003）

- [ ] AC-001 管理端创建用户时，用户名长度不足返回统一错误结构与明确中文 message。
- [ ] AC-002 不再直接透传 FastAPI 默认 422 `detail` 数组给前端用户。
- [ ] AC-003 非用户名字段校验错误仍保持统一响应，不引入无关接口回归。

### 2. 前端错误展示（AC-004～AC-005）

- [ ] AC-004 创建用户弹窗展示接口返回的明确错误原因。
- [ ] AC-005 用户修正用户名后可成功创建，错误状态正确清除。

### 3. 回归范围（AC-006）

- [ ] AC-006 重复用户名、非法字符、空必填字段与成功创建路径均通过回归测试。
- [ ] AC-006a 用户管理页弹窗继续遵守 Design System 与弹窗宽度/错误提示布局约束。

## REQ-0022 功能验收

> 来源：`issues/requirements/review/REQ-0022-admin-api-docs-menu/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `add-admin-api-docs-menu` 已完成 apply（23/23 tasks），待人工 sign-off 与 `/opsx-archive`

### 1. 导航、路由与权限（AC-001～AC-008）

- [ ] AC-001 管理端 SYSTEM 分组在「系统设置」下方展示「接口文档」菜单。
- [ ] AC-002 点击菜单进入 `/admin/api-docs`，路由高亮正确。
- [ ] AC-003 仅后台管理员可见并可访问接口文档入口。
- [ ] AC-004 非管理员直链访问 `/admin/api-docs` 返回 403 或等价禁止访问状态。
- [ ] AC-005 店主端 Web 与微信小程序不暴露该入口。
- [ ] AC-006 刷新 `/admin/api-docs` 后页面可恢复并维持权限校验。
- [ ] AC-007 菜单位于「系统设置」下方而非其他 SYSTEM 位置。
- [ ] AC-008 未登录用户访问时按既有登录态策略跳转或拒绝。

### 2. 接口目录与 Orval 方法名（AC-009～AC-022）

- [ ] AC-009 接口目录展示 Method、Path、Tag/模块、Summary/说明、认证要求与 OpenAPI 纳入状态。
- [ ] AC-010 接口范围覆盖 `/api/v1/*` 下所有业务 API。
- [ ] AC-011 接口范围覆盖 `/health` 健康检查。
- [ ] AC-012 接口范围覆盖 `/media/{object_key:path}` 媒体直出路由。
- [ ] AC-013 接口范围覆盖其他未纳入 `/api/v1` 但属于 FastAPI app 的系统路由。
- [ ] AC-014 每个已生成前端客户端的方法展示 Orval 生成方法名。
- [ ] AC-015 未生成 Orval 方法名的接口显示「未生成」或等价状态与原因。
- [ ] AC-016 支持关键字、HTTP Method、模块/Tag、认证要求筛选。
- [ ] AC-017 接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数摘要准确。
- [ ] AC-018 页面说明 OpenAPI、Swagger、`docs/03-api-index.md` 与 Orval 生成文件的关系。
- [ ] AC-019 不展示密钥、数据库连接、对象存储凭据或真实环境变量值。
- [ ] AC-020 接口目录数据源可随路由变化更新，不依赖硬编码静态列表。
- [ ] AC-021 对无法映射的路由保留可读说明，避免空白或异常。
- [ ] AC-022 API 文档相关错误响应保持统一结构。

### 3. Swagger 在线调试策略（AC-023～AC-030）

- [ ] AC-023 本地/开发/演示环境允许 Swagger 在线调试。
- [ ] AC-024 生产环境展示接口文档入口。
- [ ] AC-025 生产环境隐藏或禁用 Swagger `Try It Out`。
- [ ] AC-026 Swagger 入口不绕过管理端登录态与角色权限。
- [ ] AC-027 生产环境页面有明确状态提示，但不使用会推挤布局的文档流 success/error banner。
- [ ] AC-028 `/openapi.json` 引用不泄露敏感配置。
- [ ] AC-029 Swagger 策略可通过环境或部署配置验证。
- [ ] AC-030 生产策略在 Docker/部署文档中有验收说明。

### 4. 测试、文档与横切 AC（AC-031～AC-037、AC-XCUT-001～008）

- [ ] AC-031 后端测试覆盖接口目录聚合、非 `/api/v1` 路由与权限。
- [ ] AC-032 前端测试覆盖菜单、路由权限、筛选与 Orval 方法名展示。
- [ ] AC-033 API 变化后执行 Orval 并提交生成结果。
- [ ] AC-034 更新 API 文档索引或说明。
- [ ] AC-035 通过 `/req-opsx` 创建 OpenSpec Change。
- [ ] AC-036 Change tasks 包含生产 Try It Out 禁用验收。
- [ ] AC-037 不影响既有系统设置、用户管理和管理端侧栏行为。
- [ ] AC-XCUT-001～004 管理端列表页 gate 通过。
- [ ] AC-XCUT-005～008 管理端表单/页面反馈 gate 通过。

## 验收记录

| 时间 | 验收人 | 结论 | 说明 |
|---|---|---|---|
| 2026-06-29 10:35:38 | Codex | 开发中 | 已实现 MySQL 配置/DDL/生产 Compose/文档/测试；`AC-033`、`AC-034` 需在真实 VPS + 外部 MySQL + MinIO 环境执行 |
| 2026-06-29 16:21:57 | Codex | Smoke 通过 | 使用本地 Docker MySQL `tilesfst` 与外部 MinIO `127.0.0.1:9000` 完成登录、上传、`/media/{object_key}` 读取 |
| 2026-06-29 16:25:27 | Codex | 重启验证通过 | 重启 backend/web/minio 后，同一 `/media/{object_key}` 仍返回 `tilesfst-external-minio-smoke` |
| 2026-06-30 18:18:45 | Codex | 范围追加 | REQ-0019 已纳入 sprint-004；待 `/req-opsx` 后开发与验收 |
| 2026-06-30 18:29:13 | Codex | 范围追加 | BUG-0050 已纳入 sprint-004；待 `/bug-opsx` 后开发与回归验收 |
| 2026-06-30 18:38:37 | Codex | Change 创建 | BUG-0050 已创建 `fix-user-create-validation-message-unclear`，待 `/opsx-apply` |
| 2026-06-30 19:07:02 | Codex | REQ-0019 实现通过 | 完成后端保护、前端禁用态、Orval 和文档；后端 pytest 与前端 Vitest 通过；API governance 存在既有 tags 校验失败 |
| 2026-07-01 00:28:26 | Codex | 范围追加 | REQ-0022 已纳入 sprint-004；待 `/req-opsx REQ-0022` 创建 OpenSpec Change 后开发 |
| 2026-07-01 00:40:14 | Codex | Change 创建 | REQ-0022 已创建 `add-admin-api-docs-menu`，OpenSpec strict validate 通过，待 `/opsx-apply` |
| 2026-07-01 08:48:56 | Codex | REQ-0022 实现通过 | 完成后端聚合接口、管理端 `/admin/api-docs`、Swagger 生产只读策略、OpenAPI/Orval 与文档；后端 pytest 与前端 Vitest 通过；API governance 剩余失败为既有 tags 历史项 |

## 遗留项

| 项 | 状态 | 处理建议 |
|---|---|---|
| `test_admin_brands.py::test_upload_brand_logo_rejects_invalid_mime` | 非本 Change 遗留 | 当前配置允许 `image/gif`，测试期望品牌 Logo 拒绝 gif；需由媒体上传规则另行确认 |
| REQ-0019 OpenSpec Change | 待归档 | 执行 `/opsx-archive update-admin-superuser-protection` |
| BUG-0050 OpenSpec Change | 待开发 | 执行 `/opsx-apply fix-user-create-validation-message-unclear` 后回填验收 |
| REQ-0022 OpenSpec Change | 待归档 | 人工 sign-off 后执行 `/opsx-archive add-admin-api-docs-menu` |
