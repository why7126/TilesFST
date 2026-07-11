---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-11 17:18:39
title: Sprint 004 验收报告
purpose: 记录 Sprint 004 验收结果与遗留项（模板）
content: 基于 REQ-0018-production-mysql-deployment、REQ-0019-admin-superuser-protection、REQ-0022-admin-api-docs-menu、REQ-0023-api-docs-swagger-detail-link、REQ-0025-brand-logo-fst-favicon、REQ-0026-product-release-management、REQ-0024-product-usage-logging、BUG-0050-user-create-validation-message-unclear、BUG-0051-api-docs-swagger-ui-link-wrong、BUG-0052-api-docs-metric-cards-inconsistent、BUG-0053-api-docs-list-layout-pagination-inconsistent、BUG-0054-admin-content-padding-too-large 与 BUG-0055-admin-list-layout-unification acceptance.md
source: AI 根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: accepted
note: workflow-sync — 13/13 Change 已 archive；0 applied；待人工 sign-off
---

# Sprint 004 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-004 |
| 关联需求 | REQ-0018-production-mysql-deployment；REQ-0019-admin-superuser-protection；REQ-0022-admin-api-docs-menu；REQ-0023-api-docs-swagger-detail-link；REQ-0025-brand-logo-fst-favicon；REQ-0026-product-release-management；REQ-0024-product-usage-logging |
| 关联 BUG | BUG-0050-user-create-validation-message-unclear；BUG-0051-api-docs-swagger-ui-link-wrong；BUG-0052-api-docs-metric-cards-inconsistent；BUG-0053-api-docs-list-layout-pagination-inconsistent；BUG-0054-admin-content-padding-too-large；BUG-0055-admin-list-layout-unification |
| 关联 Change | add-production-mysql-deployment；update-admin-superuser-protection；fix-user-create-validation-message-unclear；add-admin-api-docs-menu（applied）；add-api-docs-swagger-detail-link（applied）；fix-api-docs-swagger-ui-link-wrong（archived）；fix-api-docs-metric-cards-inconsistent（archived）；fix-api-docs-list-layout-pagination-inconsistent（archived）；update-brand-logo-fst-favicon（archived）；add-product-release-management（archived）；add-product-usage-logging（proposed）；fix-admin-content-padding-too-large（archived）；fix-admin-list-layout-unification（applied） |
| 计划验收日期 | 2026-07-13 18:00:00 |
| 验收结论 | Sprint 004 范围内 13/13 OpenSpec Change 已完成 archive，相关 specs 已合并，Sprint 可关闭 |
| 验收人 | Codex |
| 归档日期 | 2026-07-04 08:13:26 |

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

> 来源：`issues/requirements/archive/REQ-0022-admin-api-docs-menu/acceptance.md`  
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

## REQ-0023 功能验收

> 来源：`issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `add-api-docs-swagger-detail-link` 已完成 apply（17/17 tasks），待人工 sign-off 与 `/opsx-archive`

### 1. 行级 Swagger 详情入口（AC-001～AC-006）

- [ ] AC-001 管理员访问 `/admin/api-docs` 时，接口列表表格展示行级操作列。
- [ ] AC-002 `included_in_openapi=true` 且 `operation_id` 非空的接口行展示可点击「查看」入口。
- [ ] AC-003 点击可用「查看」入口在新窗口或新标签页打开 Swagger UI。
- [ ] AC-004 Swagger UI 链接定位到具体 `operationId` 锚点，而不是仅打开通用 `/docs`。
- [ ] AC-005 Swagger 深链对 tag 与 operationId 做 URL 安全编码。
- [ ] AC-006 当前 `/admin/api-docs` 页面在点击后保持原筛选条件、列表状态和登录状态。

### 2. 非 OpenAPI 路由禁用态（AC-007～AC-011）

- [ ] AC-007 `included_in_openapi=false` 的路由仍展示在接口目录中。
- [ ] AC-008 `included_in_openapi=false` 的路由显示禁用态「查看」或等价不可点击状态。
- [ ] AC-009 禁用态入口给出「未纳入 OpenAPI，暂无 Swagger 详情」或等价原因。
- [ ] AC-010 禁用态入口不带可点击 href，不跳转到通用 `/docs` 或错误 operationId。
- [ ] AC-011 `included_in_openapi=true` 但 `operation_id` 缺失时按不可跳转状态处理。

### 3. 权限、安全与 UI 回归（AC-012～AC-021）

- [ ] AC-012 `employee` 用户仍无法访问 `/admin/api-docs`，并且看不到行级查看入口。
- [ ] AC-013 行级 Swagger 链接不在 URL、hash、query 或 DOM 可见文本中暴露 Bearer Token、Cookie、用户信息、数据库连接串、MinIO 凭据或环境变量真实值。
- [ ] AC-014 新窗口打开使用 `rel="noreferrer"` 或等价安全属性。
- [ ] AC-015 本需求不新增 Swagger 自动注入 token 的机制。
- [ ] AC-016 生产环境仍隐藏或禁用 Swagger `Try It Out`，不因行级入口放宽策略。
- [ ] AC-017～AC-021 新增 ACTION 列后桌面和窄视口不重叠，空结果不渲染误导行操作，TSX/CSS 不新增裸 Hex。

### 4. 测试与治理（AC-022～AC-025、AC-XCUT-001～004）

- [ ] AC-022 前端测试覆盖 OpenAPI 路由生成 `/docs#/{tag}/{operationId}` 链接。
- [ ] AC-023 前端测试覆盖非 OpenAPI 路由的禁用态「查看」。
- [ ] AC-024 前端测试断言链接使用新窗口打开且不包含 token。
- [ ] AC-025 若实现新增后端字段，需同步 OpenAPI、Orval 与 `docs/03-api-index.md`；若仅前端构造链接，则记录为无 API 变更。
- [ ] AC-XCUT-001～004 管理端列表页 gate 通过，分页 DOM、fixed feedback、confirm N/A 与禁止原生弹窗约束不回归。

### 5. 验证记录

| 时间 | 类型 | 结果 |
|---|---|---|
| 2026-07-02 10:34:20 | 前端测试 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx` 通过：1 file, 11 tests |
| 2026-07-02 10:34:20 | 前端回归 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` 通过：3 files, 19 tests |
| 2026-07-02 10:34:20 | 工程影响 | 仅前端行级链接与禁用态调整；不需要后端 pytest、数据库迁移、MinIO、Orval 或 Docker Compose 配置变更 |
| 2026-07-02 10:34:20 | 样式约束 | `ApiDocsPage.tsx` 与 `api-docs.css` 未新增裸 Hex / `rgba(...)` |

## BUG-0051 回归验收

> 来源：`issues/bugs/archive/BUG-0051-api-docs-swagger-ui-link-wrong/acceptance.md`
> 状态：done；OpenSpec Change `fix-api-docs-swagger-ui-link-wrong` 已归档

### 1. 本地开发 Swagger UI 入口（AC-001）

- [x] AC-001 启动本地后端与 Web 开发服务后，admin 进入 `/admin/api-docs` 点击【Swagger UI】。
- [x] AC-001 Web 开发服务通过 Vite dev proxy 将 `/docs` 转发到后端 Swagger UI。
- [x] AC-001 打开的页面不是 Web 首页，并展示 FastAPI Swagger UI 标识。

### 2. Docker Web Swagger 代理（AC-002）

- [x] AC-002 Docker Compose 启动 Web 与 Backend 后，通过 Web 宿主机端口进入 `/admin/api-docs`。
- [x] AC-002 点击【Swagger UI】后，Web 容器 Nginx 将 `/docs` 转发到 backend。
- [x] AC-002 打开的页面不是 `http://localhost:3000/` 首页，而是 Web 代理后的后端 Swagger UI。

### 3. OpenAPI 与生产策略不回归（AC-003～AC-004）

- [x] AC-003 【OpenAPI JSON】入口返回后端 `/openapi.json`，包含 `openapi`、`info`、`paths` 字段。
- [x] AC-003 `/openapi.json` 不返回 Web SPA 的 `index.html`。
- [x] AC-004 生产环境仍可展示 Swagger 文档入口或只读入口。
- [x] AC-004 生产环境 Swagger UI 中 Try It Out 被隐藏或禁用。

### 4. 测试、代理与权限（AC-005～AC-007）

- [x] AC-005 `ApiDocsPage` 单元测试覆盖【Swagger UI】与【Swagger 只读】链接行为。
- [x] AC-006 Vite dev proxy 与 Docker Nginx 覆盖 Swagger 相关路径。
- [x] AC-006 `/api/`、`/media/`、`/openapi.json` 既有代理能力不受影响。
- [x] AC-007 `/admin/api-docs` 仍仅 admin 可访问，employee 仍不可见或不可直链访问。

## BUG-0052 回归验收

> 来源：`issues/bugs/archive/BUG-0052-api-docs-metric-cards-inconsistent/acceptance.md`
> 状态：done；OpenSpec Change `fix-api-docs-metric-cards-inconsistent` 已归档

### 1. 指标卡 DOM 结构（AC-001）

- [x] AC-001 `/admin/api-docs` 标题下方四个摘要指标卡使用管理端基准结构。
- [x] AC-001 每个卡片包含 `.metric-label`、`.metric-value`、`.metric-desc`。
- [x] AC-001 摘要卡不再使用裸 `strong` / `span` 作为数值和说明的唯一样式承载。

### 2. 视觉层级与 token（AC-002～AC-003）

- [x] AC-002 接口文档页指标卡与 `/admin/tile-skus` 同类指标卡在边框、背景、圆角、内边距、数字强调色、数字字号、说明文字弱化层级上一致。
- [x] AC-003 修复不在 TSX/CSS 中新增裸 Hex。
- [x] AC-003 修复复用已有 `summary-grid`、`metric-card`、`metric-label`、`metric-value`、`metric-desc` 语义类。

### 3. 功能、权限与测试不回归（AC-004～AC-007）

- [x] AC-004 接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数仍展示正确。
- [x] AC-004 搜索、Method/Tag/Auth 筛选、OpenAPI JSON、Swagger UI/只读入口、Orval 方法名展示不回归。
- [x] AC-005 admin 可访问，employee 不可见/不可直链访问，店主 Web 与微信小程序不出现入口。
- [x] AC-006 `ApiDocsPage` 测试覆盖摘要指标卡 `.metric-value` 与 `.metric-desc`。
- [x] AC-007 不修改后端 API、数据库、MinIO、上传、Orval 或 Docker Compose 配置。

## BUG-0053 回归验收

> 来源：`issues/bugs/archive/BUG-0053-api-docs-list-layout-pagination-inconsistent/acceptance.md`
> 状态：done；OpenSpec Change `fix-api-docs-list-layout-pagination-inconsistent` 已归档

### 1. 列表标题与分页功能（AC-001～AC-008）

- [x] AC-001 `/admin/api-docs` 接口列表区域直接移除冗余标题「系统接口」，不改名保留，也不按接口数据行过滤处理。
- [x] AC-002 接口列表提供上一页、当前页、下一页分页控件。
- [x] AC-003 每页条数选择包含 10 / 20 / 50 / 100。
- [x] AC-004 默认每页条数为 20。
- [x] AC-005 Method、Tag、Auth 或关键字筛选后，当前页回到第 1 页。
- [x] AC-006 分页总数基于当前筛选后的接口数量计算。
- [x] AC-007 空筛选结果展示明确空态，分页区不出现无效页码。
- [x] AC-008 总页数为 1 时，上一页与下一页按钮不可操作。

### 2. UI 一致性与回归（AC-009～AC-018）

- [x] AC-009 分页 DOM 与瓷砖 SKU 页/管理端列表页一致：左侧 `page-summary`，右侧 `page-right`。
- [x] AC-010 分页按钮复用 `page-buttons`、`page-btn`、`active` 等管理端列表页模式。
- [x] AC-011 每页条数选择复用 `page-size-wrap` 与 `page-size` 模式。
- [x] AC-012 接口列表表格、筛选栏、状态 Badge、方法 Badge 继续继承管理端暗色旗舰风，不新增裸 Hex。
- [x] AC-013 `/admin/api-docs` 仍仅 `admin` 可访问。
- [x] AC-014 OpenAPI JSON 与 Swagger UI 入口仍可用。
- [x] AC-015 生产环境 Swagger 仍保持只读策略。
- [x] AC-016 Orval 方法名展示与「未生成」原因展示不回退。
- [x] AC-017 接口目录仍展示 `/api/v1/*`、`/health`、`/media/{object_key:path}` 和 schema 外路由。
- [x] AC-018 不修改后端 API、数据库、MinIO 或媒体上传策略。

### 3. 测试建议（AC-019～AC-022）

- [x] AC-019 前端 Vitest 覆盖分页 DOM。
- [x] AC-020 前端 Vitest 覆盖筛选后回到第 1 页。
- [x] AC-021 前端 Vitest 覆盖分页切换后表格只展示当前页数据。
- [x] AC-022 如修复仅为前端分页与标题调整，不需要后端 pytest、Orval 或数据库迁移。

### 4. 验证记录

| 时间 | 类型 | 结果 |
|---|---|---|
| 2026-07-02 09:05:28 | 前端测试 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx` 通过：1 file, 9 tests |
| 2026-07-02 09:05:48 | 前端回归 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` 通过：3 files, 17 tests |
| 2026-07-02 09:05:55 | 工程影响 | 仅前端分页与标题调整；不需要后端 pytest、数据库迁移、Orval 或 Docker Compose 配置变更 |
| 2026-07-02 09:05:55 | 知识沉淀 | 未发现新的可复用生产故障经验；不新增 `docs/knowledge-base/incidents/` |

## BUG-0054 回归验收

> 来源：`issues/bugs/archive/BUG-0054-admin-content-padding-too-large/acceptance.md`  
> 状态：done；OpenSpec Change `fix-admin-content-padding-too-large` 已归档，并同步闭环 REQ-0013 当前实际

### 1. Admin Shell 主内容 padding（AC-001、AC-004）

- [ ] AC-001 Desktop 视口（>1023px）下 `.admin-shell .main-content` 使用 `padding: 24px 24px 48px` 或经评审确认的等价值。
- [ ] AC-001 不再沿用旧 `padding: 48px 56px 72px` 或 bottom `72px`。
- [ ] AC-001 主内容仍保持独立滚动，Shell 层不出现横向滚动条。
- [ ] AC-004 ≤1023px 视口下 `.main-content` padding 调整到 `20px 16px 40px` 量级。
- [ ] AC-004 ≤639px 视口下 `.main-content` padding 调整到 `16px 12px 32px` 量级。
- [ ] AC-004 tablet / mobile 下侧栏、用户菜单、折叠按钮既有响应式行为不被破坏。

### 2. 内容宽度策略与页面级分叉（AC-002～AC-003）

- [ ] AC-002 `.admin-shell .content-inner` 不再使用 `max-width: 1080px`。
- [ ] AC-002 最终策略采用 `max-width: 100%` 或 `max-width: min(1440px, 100%)`，并在 Change 设计中明确。
- [ ] AC-002 1440px 与 1920px 视口下，内容区可明显利用更多横向空间。
- [ ] AC-003 SKU 页不再保留 `:has(.sku-page-hero) .content-inner { max-width: 1120px }` 这类 divergent override。
- [ ] AC-003 系统设置页不再通过 `settings-content-inner { max-width: 1080px }` 将页面重新限制到旧宽度。
- [ ] AC-003 全仓 Web 管理端 CSS 不新增与全局 Shell 策略冲突的 `content-inner` / `settings-content-inner` max-width。

### 3. 基准页面视觉回归（AC-005～AC-006）

- [ ] AC-005 `/admin/logs` 指标卡、筛选区、日志表格显示面积明显增大。
- [ ] AC-005 `/admin/tile-skus` 筛选区和 SKU 表格不再被旧 1120px 上限限制。
- [ ] AC-005 `/admin/users` 用户列表、分页和操作列无错位。
- [ ] AC-005 `/admin/dashboard` 指标卡和快捷入口不显得贴边、不过度拥挤。
- [ ] AC-005 `/admin/system-settings` 表单区域跟随全局内容宽度策略，不再被旧 1080px 容器锁定。
- [ ] AC-006 修改使用既有 admin semantic token 或布局尺寸值，不新增裸 Hex。
- [ ] AC-006 不新增卡片套卡片、浮动页面段落卡等违反 Design System 的结构。

### 4. 自动化与范围不扩散（AC-007～AC-008）

- [ ] AC-007 `AdminLayout.test.tsx` 通过。
- [ ] AC-007 `AdminSidebar.collapse.test.tsx` 通过。
- [ ] AC-007 新增或更新测试/静态断言，覆盖 `.main-content` padding、`.content-inner` max-width 与页面级 divergent override。
- [ ] AC-007 前端构建或等价校验通过。
- [ ] AC-008 不修改后端 API、数据库结构、Orval、店主端、小程序或侧栏折叠持久化行为。

## BUG-0055 回归验收

> 来源：`issues/bugs/archive/BUG-0055-admin-list-layout-unification/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-admin-list-layout-unification` 已完成 apply，任务 30/30，待 `/opsx-archive`

### 1. 模块顺序统一（AC-001）

- [x] AC-001 瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计、接口文档页面均按标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块顺序展示。
- [x] AC-001 列表模块上方不再出现重复列表标题、旧版 table toolbar 或割裂的 section heading。

### 2. 筛选/搜索区统一（AC-002～AC-003）

- [x] AC-002 8 个目标页面均不展示文案为【查询】或【搜索】的显式提交按钮。
- [x] AC-002 筛选控件变化后刷新或重新计算列表结果，并将当前页重置为 1。
- [x] AC-003 8 个目标页面的【重置】按钮高度、padding、圆角、字号、边框、图标策略和对齐方式一致。
- [x] AC-003 点击重置后清空或恢复默认筛选条件，并将当前页重置为 1。

### 3. 列表固定操作列（AC-004）

- [x] AC-004 8 个目标页面的最后一列表头和单元格在横向滚动时保持可见。
- [x] AC-004 固定列使用与接口文档页一致的右侧背景、左侧分割线和阴影层次。
- [x] AC-004 行 hover 时固定列背景与当前行 hover 状态协调。
- [x] AC-004 固定列内编辑、启停、删除、查看、重置密码等操作权限、禁用态和确认流程不回退。

### 4. 分页页码窗口（AC-005）

- [x] AC-005 分页统一使用左侧 `page-summary` 与右侧 `page-right` 结构。
- [x] AC-005 页码按钮使用 `page-buttons`、`page-btn`、`active` 或等价统一 class。
- [x] AC-005 可点击页码数量不超过 5 个，不包含上一页/下一页按钮。
- [x] AC-005 总页数为 1 时仍展示统一分页结构，上一页/下一页禁用，页码 `1` 为当前态。
- [x] AC-005 切换每页显示条数后页码重置为 1。

### 5. 范围不扩散与测试（AC-006、AC-TEST）

- [x] AC-006 店主 Web 展示端和微信小程序不受本修复影响。
- [x] AC-006 后端 API、数据库、MinIO、媒体上传和 Docker Compose 不发生契约变化。
- [x] AC-TEST 分页窗口计算单元测试覆盖总页数 1、5、6、当前页靠前、居中、靠后。
- [x] AC-TEST 页面测试覆盖无【查询】/【搜索】按钮、保留统一【重置】按钮、DOM 顺序和 sticky action column 契约。

## REQ-0025 功能验收

> 来源：`issues/requirements/archive/REQ-0025-brand-logo-fst-favicon/acceptance.md`
> 状态：done；OpenSpec Change `update-brand-logo-fst-favicon` 已归档

### 1. Sidebar 品牌区（AC-001～AC-008）

- [x] AC-001 展开态顶部品牌区同时展示 Logo、`菲尚特FST`、版本号、`家居建材资料库` 和展开/收起按钮。
- [x] AC-002 主标题文案必须为 `菲尚特FST`。
- [x] AC-003 副标题文案必须为 `家居建材资料库`，不得沿用旧原型中的 `家居建材管理后台`。
- [x] AC-004 版本号沿用现有产品版本来源，视觉上靠近主标题右上侧。
- [x] AC-005 Logo 保持比例，不拉伸、不裁切关键内容。
- [x] AC-006 Logo 区域不得新增独立卡片背景、边框、渐变底纹或投影。
- [x] AC-007 展开/收起按钮与 Logo 同行，保持正方形热区和安全边距。
- [x] AC-008 Sidebar 收起后 Logo 仍可作为品牌识别元素，品牌文案、导航图标无重叠。

### 2. 网页图标、视觉与工程影响（AC-009～AC-018）

- [x] AC-009 浏览器标签 favicon / apple-touch-icon 展示菲尚特 Logo，不显示 Vite、React 或浏览器默认图标。
- [x] AC-010 Banner、用户、品牌、规格等管理页面主体结构、路由、权限与操作行为不因本需求改变。
- [x] AC-011 以 `prototype/web/banner-management-list-logo.html` 与 PNG 验证 Sidebar 品牌区结构；页面主体仅作为承载背景。
- [x] AC-012 在 1366×768、1440×1024 桌面视口下，品牌区无重叠、无明显裁切、无布局抖动。
- [x] AC-013 Web UI 实现使用 semantic token / 既有组件样式；不得新增裸 Hex 或绕过 `cn()` 合并规则。
- [x] AC-014 Logo 图片具备可理解的替代文本；展开/收起按钮保留可访问标签。
- [x] AC-015 不新增、不修改后端 API；无需生成 OpenAPI 或 Orval 客户端。
- [x] AC-016 不新增、不修改 SQLite 表结构或 Pydantic Schema。
- [x] AC-017 不引入 MinIO 上传、读取或 Bucket 变更。
- [x] AC-018 前端至少覆盖品牌文案、版本号展示、favicon 链接或入口 HTML 图标声明的回归检查。

## REQ-0026 功能验收

> 来源：`issues/requirements/archive/REQ-0026-product-release-management/acceptance.md`  
> 状态：done；OpenSpec Change `add-product-release-management` 已 archive，正式规范已合并

### 1. 产品版本发布对象（AC-001～AC-004）

- [x] AC-001 支持一个产品版本关联多个 Sprint。
- [x] AC-002 支持发布对象追踪关联 REQ、BUG 和 OpenSpec Change。
- [x] AC-003 明确产品版本发布公告与 Sprint 级 `release-note.md` 的职责差异。
- [x] AC-004 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。

### 2. 产品版本号（AC-005～AC-007）

- [x] AC-005 发布时校验 `src/shared/product-version.ts` 中 `PRODUCT_VERSION` 与发布公告版本一致。
- [x] AC-006 不使用 `package.json`、FastAPI `version`、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。
- [x] AC-007 若发布不改变 `PRODUCT_VERSION`，在发布材料中记录原因。

### 3. Mintlify 公开发布公告（AC-008～AC-012）

- [x] AC-008 发布公告面向公开页面展示。
- [x] AC-009 发布公告采用 Mintlify 静态文档生成。
- [x] AC-010 发布公告可在本地或等价环境完成构建/预览校验。
- [x] AC-011 发布公告不依赖后端运行时 API 或数据库才能展示。
- [x] AC-012 发布公告源文件可纳入 Git 管理并适合 Review。

### 4. 公告内容（AC-013～AC-021）

- [x] AC-013 公告包含版本号、发布时间和关联 Sprint。
- [x] AC-014 公告汇总新增功能，并可追踪到 REQ。
- [x] AC-015 公告汇总修复 BUG，并可追踪到 BUG。
- [x] AC-016 公告包含发布注意事项。
- [x] AC-017 公告包含已知问题。
- [x] AC-018 公告包含升级步骤。
- [x] AC-019 公告包含回滚说明。
- [x] AC-020 公告包含影响范围，至少区分 Web 管理端、店主 Web、小程序、后端、数据库、对象存储和 Docker。
- [x] AC-021 公告不泄露密钥、真实客户数据、内部数据库连接串、不可公开域名或敏感运维信息。

### 5. 发布前校验与目录治理（AC-022～AC-032）

- [x] AC-022 发布前校验 OpenSpec Change 已 archive，相关能力已合并到 `openspec/specs/`。
- [x] AC-023 发布前校验测试已按变更范围执行并记录结果。
- [x] AC-024 涉及 API 变更时校验 OpenAPI 与 Orval 已同步。
- [x] AC-025 涉及 Docker Compose 或部署变更时校验部署文档与 Compose 配置已同步。
- [x] AC-026 涉及数据库迁移时校验迁移脚本、数据库文档和回滚说明已同步。
- [x] AC-027 涉及环境变量时校验 `.env.example` 与相关注释已同步。
- [x] AC-028 任一必填校验失败时，发布流程阻断并输出失败原因。
- [x] AC-029～AC-032 新增顶层 `releases/` 前必须先通过 OpenSpec Change，更新目录规范并说明与 iterations、issues、openspec、Mintlify 的关系。

### 6. 发布命令族与明确不做（AC-033～AC-038、AC-KB-001～003）

- [x] AC-033 后续发布命令族至少覆盖创建发布计划、发布前校验、发布公告生成/确认。
- [x] AC-034 新增或修改 slash 命令时以 `.cursor/commands/` 为事实源。
- [x] AC-035 命令同步后运行 `python scripts/sync-agent-commands.py` 或等价同步流程。
- [x] AC-036 不在管理端菜单、登录页、店主端入口或小程序入口新增发布公告入口。
- [x] AC-037 不支持草稿、待发布、已发布、撤回等复杂发布状态机。
- [x] AC-038 不新增后端发布公告 API 或数据库表，除非后续 OpenSpec Change 明确要求。
- [x] AC-KB-001～003 Knowledge-base gate 为 N/A；trace 保留空横切引用，并引用发布/验收门禁风险复盘。

## REQ-0024 功能验收

> 来源：`issues/requirements/review/REQ-0024-product-usage-logging/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `add-product-usage-logging` 已创建，待 `/opsx-apply`

### 1. 数据采集与存储（AC-001～AC-013）

- [ ] AC-001 后端在统一中间件或等价入口为 API 请求生成或透传 `request_id`。
- [ ] AC-002 API 请求日志记录 method、path、status_code、duration_ms、actor_user_id、actor_role、client_type、request_id、created_at。
- [ ] AC-003 异常请求记录 error_code、错误消息摘要和 request_id。
- [ ] AC-004 健康检查、静态资源、Swagger 文档、媒体直出等噪声路由默认排除。
- [ ] AC-005 行为事件基于 `tracking-events.md` 事件字典采集，不随意拼接未登记 `event_name`。
- [ ] AC-006 行为事件上报失败不阻断用户主业务流程。
- [ ] AC-007～AC-013 日志数据存储于关系型数据库，OpenSpec design 明确扩展 `audit_logs` 或新增 `request_logs` / `usage_events`，并覆盖参数化查询、索引、分页、metadata JSON、保留周期和 SQLite/MySQL 兼容。

### 2. API 与安全（AC-014～AC-019、AC-034～AC-038）

- [ ] AC-014 `GET /api/v1/admin/logs` 仅允许系统管理员分页查询日志列表。
- [ ] AC-015 `GET /api/v1/admin/logs/{id}` 仅允许系统管理员查询单条日志详情。
- [ ] AC-016 `POST /api/v1/usage-events` 校验事件名、必填属性、字段类型、字段长度与禁止字段。
- [ ] AC-017 列表接口返回统一 `ApiResponse` 与分页结构。
- [ ] AC-018 参数非法与日志不存在使用统一错误结构。
- [ ] AC-019 API 变更同步 OpenAPI、`docs/03-api-index.md`、错误码文档、Orval 客户端与后端测试。
- [ ] AC-034～AC-038 日志不保存或展示密码、Token、Authorization Header、Cookie、真实密钥、MinIO AccessKey / SecretKey、数据库 DSN；请求体/响应体需白名单、黑名单、截断和显式开关。

### 3. 管理端日志审计页（AC-020～AC-033）

- [ ] AC-020 管理端在 SYSTEM 分组提供日志审计入口，推荐路由 `/admin/logs` 或 `/admin/audit-logs`。
- [ ] AC-021 筛选区支持日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id，并提供查询与重置。
- [ ] AC-022 列表展示时间、类型、事件 / 摘要、操作者、客户端、状态 / 结果、耗时、request_id、复制、详情操作。
- [ ] AC-023 指标摘要展示 `TODAY LOGS`、`API ERRORS`、`SLOW REQUESTS`、`SENSITIVE OPS`。
- [ ] AC-024～AC-030 详情使用右侧抽屉承载，展示基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性和 metadata JSON。
- [ ] AC-031 request_id 可复制，反馈不造成页面布局位移。
- [ ] AC-032 普通员工、店主端和匿名用户直链访问日志页面或接口返回 403 或无权限页。
- [ ] AC-033 页面复用管理端列表页模式，优先使用 `AdminListPage`、shadcn 基础组件和既有管理端样式。

### 4. 事件字典与原型（AC-039～AC-045、AC-XCUT-001～005）

- [ ] AC-039～AC-042 需求包包含 `tracking-events.md`，MVP 事件覆盖 page_view、search_submit、filter_change、entity_create、entity_update、entity_delete、status_change、media_upload、login_success、login_failed、api_error，并同步代码枚举、Schema、测试与 OpenSpec。
- [ ] AC-043 原型包含管理端日志审计列表、筛选区、指标摘要、表格、分页和详情抽屉。
- [ ] AC-044 原型 context 明确路由、导航位置、字段、空态、加载态、错误态和权限态。
- [ ] AC-045 UI 实现以 `prototype/web/log-audit-list.png` 与 `prototype/web/log-audit-detail-drawer.png` 作为 Golden Reference，并完成 1440x1024 并排验收。
- [ ] AC-XCUT-001～005 管理端列表页 gate 通过：分页 DOM、指标卡 DOM、fixed toast、confirm N/A 与 Vitest smoke / snapshot。

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
| 2026-07-01 14:04:19 | Codex | 范围追加 | BUG-0052 已纳入 sprint-004；待 `/bug-opsx` 后开发与回归验收 |
| 2026-07-01 14:06:33 | Codex | 范围追加 | BUG-0053 已纳入 sprint-004；待 `/bug-opsx` 后开发与回归验收 |
| 2026-07-01 14:06:44 | Codex | 范围追加 | BUG-0051 已纳入 sprint-004；修复方向为 Web 层代理 Swagger，待 `/bug-opsx` 后开发与回归验收 |
| 2026-07-01 20:03:09 | Codex | BUG-0051 实现通过 | 完成 Vite/Nginx Swagger 代理、链接测试与 Docker Web smoke；生产 Try It Out 策略保持禁用 |
| 2026-07-01 22:21:51 | Codex | 范围追加 | REQ-0025 已纳入 sprint-004；后续创建 `update-brand-logo-fst-favicon` 并进入开发验收 |
| 2026-07-02 03:18:58 | Codex | REQ-0025 实现通过 | 完成 Web Logo 资产、Sidebar 品牌区、favicon/apple-touch-icon、相关 Vitest 与 build；使用临时静态验收页检查 1366×768、1440×1024 展开态和 1366×768 收起态 |
| 2026-07-02 09:05:32 | Codex | BUG-0052 实现通过 | 完成接口文档页摘要指标卡 DOM/class 对齐、前端回归测试、OpenSpec specs 合并与归档 |
| 2026-07-02 09:17:47 | Codex | 范围追加 | REQ-0023 已纳入 sprint-004；OpenSpec Change 后续创建为 `add-api-docs-swagger-detail-link` |
| 2026-07-02 09:26:53 | Codex | Change 创建 | REQ-0023 已创建 `add-api-docs-swagger-detail-link`，OpenSpec strict validate 通过 |
| 2026-07-02 10:34:20 | Codex | REQ-0023 实现通过 | 完成接口列表行级 ACTION、Swagger operationId 深链、非 OpenAPI/缺失 operationId 禁用态与前端回归测试 |
| 2026-07-02 14:44:48 | Codex | 范围追加 | REQ-0026 已纳入 sprint-004；待 `/req-opsx REQ-0026-product-release-management` 创建 OpenSpec Change |
| 2026-07-02 14:55:51 | Codex | Change 创建 | REQ-0026 已创建 `add-product-release-management`，OpenSpec strict validate 通过 |
| 2026-07-02 15:25:19 | Codex | 范围追加 | REQ-0024 已纳入 sprint-004；OpenSpec Change 后续已创建为 `add-product-usage-logging` |
| 2026-07-02 15:27:36 | Codex | REQ-0026 实现通过 | 完成发布目录治理、模板、校验脚本、release 命令族、测试与同步 |
| 2026-07-03 18:51:53 | Codex | 范围追加 | BUG-0054 已纳入 sprint-004；OpenSpec Change 已创建为 `fix-admin-content-padding-too-large` |
| 2026-07-03 23:30:35 | Codex | 范围追加 | BUG-0055 已纳入 sprint-004；OpenSpec Change 已创建为 `fix-admin-list-layout-unification`，后续已完成 apply 与视觉验收确认 |
| 2026-07-04 08:13:26 | Codex | 归档通过 | `openspec list --json` 返回无活动 Change；sprint.yaml 中 13 个 Change 均已在 `openspec/changes/archive/`，执行 Sprint 关闭 |

## 遗留项

| 项 | 状态 | 处理建议 |
|---|---|---|
| `test_admin_brands.py::test_upload_brand_logo_rejects_invalid_mime` | 非本 Change 遗留 | 当前配置允许 `image/gif`，测试期望品牌 Logo 拒绝 gif；需由媒体上传规则另行确认 |
| REQ-0019 OpenSpec Change | 待归档 | 执行 `/opsx-archive update-admin-superuser-protection` |
| BUG-0050 OpenSpec Change | 待开发 | 执行 `/opsx-apply fix-user-create-validation-message-unclear` 后回填验收 |
| REQ-0022 OpenSpec Change | 待归档 | 人工 sign-off 后执行 `/opsx-archive add-admin-api-docs-menu` |
| BUG-0051 OpenSpec Change | 已归档 | `openspec/changes/archive/2026-07-01-fix-api-docs-swagger-ui-link-wrong/` |
| BUG-0052 OpenSpec Change | 已归档 | `openspec/changes/archive/2026-07-02-fix-api-docs-metric-cards-inconsistent/` |
| BUG-0053 OpenSpec Change | 已归档 | `openspec/changes/archive/2026-07-02-fix-api-docs-list-layout-pagination-inconsistent/` |
| REQ-0023 OpenSpec Change | 待归档 | 人工 sign-off 后执行 `/opsx-archive add-api-docs-swagger-detail-link` |
| REQ-0025 OpenSpec Change | 已归档 | `openspec/changes/archive/2026-07-02-update-brand-logo-fst-favicon/` |
| REQ-0026 OpenSpec Change | 已归档 | 已执行 `/opsx-archive add-product-release-management` 并同步正式规范 |
| REQ-0024 OpenSpec Change | 已创建 | 后续执行 `/opsx-apply add-product-usage-logging` |
| BUG-0054 OpenSpec Change | 已归档 | `fix-admin-content-padding-too-large` 已 archived，并作为 REQ-0013 当前实际归档依据 |
| BUG-0055 OpenSpec Change | 已应用 | 任务 30/30；后续执行 `/opsx-archive fix-admin-list-layout-unification` |
