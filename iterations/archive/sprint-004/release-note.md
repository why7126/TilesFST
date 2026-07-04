---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-04 08:16:02
title: Sprint 004 发布说明
purpose: 记录 Sprint 004 交付能力与发布注意事项（初稿）
content: 基于 REQ-0018-production-mysql-deployment、REQ-0019-admin-superuser-protection、REQ-0022-admin-api-docs-menu、REQ-0023-api-docs-swagger-detail-link、REQ-0025-brand-logo-fst-favicon、REQ-0026-product-release-management、REQ-0024-product-usage-logging、BUG-0050-user-create-validation-message-unclear、BUG-0051-api-docs-swagger-ui-link-wrong、BUG-0052-api-docs-metric-cards-inconsistent、BUG-0053-api-docs-list-layout-pagination-inconsistent、BUG-0054-admin-content-padding-too-large、BUG-0055-admin-list-layout-unification 与相关 OpenSpec Change
source: AI 根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: published
note: Sprint 004 已关闭；13/13 Change 已归档，发布说明作为迭代级交付记录发布
---

# Sprint 004 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-004 |
| 关联需求 | REQ-0018-production-mysql-deployment；REQ-0019-admin-superuser-protection；REQ-0022-admin-api-docs-menu；REQ-0023-api-docs-swagger-detail-link；REQ-0025-brand-logo-fst-favicon；REQ-0026-product-release-management；REQ-0024-product-usage-logging |
| 关联 BUG | BUG-0050-user-create-validation-message-unclear；BUG-0051-api-docs-swagger-ui-link-wrong；BUG-0052-api-docs-metric-cards-inconsistent；BUG-0053-api-docs-list-layout-pagination-inconsistent；BUG-0054-admin-content-padding-too-large；BUG-0055-admin-list-layout-unification |
| 关联 Change | add-production-mysql-deployment；update-admin-superuser-protection；fix-user-create-validation-message-unclear；add-admin-api-docs-menu（applied）；add-api-docs-swagger-detail-link（applied）；fix-api-docs-swagger-ui-link-wrong（archived）；fix-api-docs-metric-cards-inconsistent（archived）；fix-api-docs-list-layout-pagination-inconsistent（archived）；update-brand-logo-fst-favicon（archived）；add-product-release-management（archived）；add-product-usage-logging（proposed）；fix-admin-content-padding-too-large（proposed）；fix-admin-list-layout-unification（applied） |
| 计划周期 | 2026-06-29 10:03:38 ~ 2026-07-13 18:00:00 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **已发布（Published）** |
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

### 接口文档指标卡一致性修复

- `/admin/api-docs` 标题下方接口摘要指标卡需与 `/admin/tile-skus` 同类指标卡结构和视觉层级一致。
- 指标卡需使用 `.metric-label`、`.metric-value`、`.metric-desc` 管理端基准 class。
- 修复不得新增裸 Hex，不改变接口目录数据、Swagger 策略、Orval 方法名或权限边界。

### Swagger UI 入口修复

- `/admin/api-docs` 右上角【Swagger UI】入口通过 Web 层代理进入 FastAPI Swagger UI，不再回退到 Web 首页。
- Vite dev proxy 补齐 Swagger 相关路径，保证本地开发环境 `http://localhost:3000/docs` 可达后端 Swagger。
- Docker Web Nginx 补齐 `/docs`、`/redoc` 及 Swagger 相关路径代理，保证 Docker Web 端口访问一致。
- 修复不得硬编码后端宿主机端口，不得影响 `/api/`、`/media/` 与 `/openapi.json`。
- 生产环境仍保持 Swagger 只读策略，不能因代理修复放开 Try It Out。

### 接口文档列表分页一致性修复

- `/admin/api-docs` 接口列表区域需直接移除冗余标题「系统接口」，不改名保留，也不按接口数据行过滤处理。
- 接口列表需提供与瓷砖 SKU 页一致的分页交互，包括页码按钮、每页条数选择和筛选后回到第 1 页。
- 修复不得改变接口目录数据、Swagger 策略、Orval 方法名、权限边界、后端 API、数据库或对象存储配置。

### 管理端全局内容区域内边距修复

- 管理端 Admin Shell 右侧主内容区域的 desktop padding 调整为 `24px 24px 48px`，不再沿用 `48px 56px 72px`。
- Tablet 与 mobile padding 分别收窄到 `20px 16px 40px` 与 `16px 12px 32px` 量级。
- `.content-inner` 不再使用 `1080px` 硬上限，最终宽度策略在 OpenSpec design 中记录。
- SKU 页和系统设置页不再保留与全局 Shell 策略冲突的页面级宽度上限。
- `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/system-settings` 作为视觉回归基准。
- 本修复不修改后端 API、数据库、Orval、Docker、店主端或小程序。

### 管理端多列表页布局与筛选分页交互统一修复

- 统一瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计、接口文档页面的模块顺序。
- 8 个目标页面均按标题模块、指标卡模块、筛选/搜索模块、列表模块顺序呈现。
- 筛选/搜索模块以瓷砖 SKU 页为基线，但不展示【查询】或【搜索】显式提交按钮。
- 重置按钮尺寸、对齐、圆角、字号、边框和图标策略保持一致。
- 列表最后一列以接口文档页为基线固定浮动，横向滚动时操作列保持可见。
- 分页最多展示 5 个可点击页码；总页数为 1 时仍保持统一分页结构和禁用态。
- 本修复不修改后端 API、数据库、Orval、Docker、店主端或小程序。

### 接口文档列表行级查看并跳转 Swagger 详情

- `/admin/api-docs` 接口列表需新增行级 ACTION「查看」入口。
- `included_in_openapi=true` 且存在 `operation_id` 的接口，点击后在新窗口打开 Swagger UI 并定位到具体 `operationId` 锚点。
- `included_in_openapi=false` 或缺少 `operation_id` 的路由仍展示在接口目录中，但「查看」为禁用态且不带可点击 href。
- 行级 Swagger 链接不得在 URL、hash、query 或 DOM 可见文本中暴露 token、Cookie、用户信息、数据库连接串、MinIO 凭据或真实环境变量。
- 点击行级入口不得刷新当前管理端页面，不得丢失当前筛选、分页和登录上下文。

### 品牌区 Logo、菲尚特FST 文案与网页图标统一

- 管理端 Sidebar 顶部品牌区展示用户提供的菲尚特 Logo、`菲尚特FST`、当前产品版本号与 `家居建材资料库`。
- 浏览器标签图标 favicon / apple-touch-icon 使用菲尚特 Logo 或派生图标，不再显示默认图标。
- 展开态、收起态与 hover 态均需保持品牌区无重叠、无裁切、无布局抖动。
- 本需求不修改 Banner 管理主体页面、不新增后端 API、不修改数据库、不引入对象存储上传流程。

### 产品版本发布与公告管理

- 支持一个产品版本合并多个 Sprint，并追踪关联 REQ、BUG 与 OpenSpec Change。
- 发版时必须校验 `src/shared/product-version.ts` 中 `PRODUCT_VERSION` 与产品发布公告版本一致。
- 发布公告面向公开页面，使用 Mintlify 静态文档生成，不依赖后端运行时 API 或数据库才能展示。
- 公告内容必须包含新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
- 发布前必须校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example` 同步。
- 顶层 `releases/` 目录必须先通过 OpenSpec Change 修改目录规范后再创建。
- 本需求不新增管理端菜单、登录页、店主端或小程序入口，不新增后端公告 API 或数据库表。

### 产品使用行为埋点与接口请求日志详情

- 新增 API 请求日志采集能力，记录 method、path、status_code、duration_ms、request_id、操作者、客户端来源与创建时间。
- 新增产品使用行为事件字典和上报契约，覆盖页面访问、搜索筛选、实体操作、状态变更、媒体上传、登录与 API 错误。
- 新增日志详情 metadata 存储与脱敏策略，禁止默认保存完整请求体、完整响应体、密码、Token、Authorization、Cookie、密钥或数据库 DSN。
- 新增管理端 SYSTEM / 日志审计页面，支持 Today Logs、API Errors、Slow Requests、Sensitive Ops 指标摘要。
- 日志审计列表支持日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id 筛选。
- 日志表格展示时间、类型、事件 / 摘要、操作者、客户端、状态、耗时、request_id、复制和详情。
- 详情以右侧抽屉展示基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性和 metadata JSON。
- UI 实现需对齐产品 v2 `log-audit-list.png` 与 `log-audit-detail-drawer.png` Golden Reference。

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
- BUG-0051 不计划新增或修改业务 API 契约，不需要重新生成 Orval；仅涉及 Web 代理配置与页面入口回归。
- BUG-0052 不计划新增或修改 API 契约，不需要重新生成 Orval。
- BUG-0053 不计划新增或修改 API 契约，不需要重新生成 Orval。
- BUG-0054 不计划新增或修改 API 契约，不需要重新生成 Orval。
- BUG-0055 不计划新增或修改 API 契约，不需要重新生成 Orval。
- REQ-0023 已按前端基于 `tag` 与 `operation_id` 构造 Swagger 深链处理，未新增后端字段，无需同步 OpenAPI、Orval 与 `docs/03-api-index.md`。
- REQ-0025 不计划新增或修改 API 契约，不需要重新生成 Orval。
- REQ-0026 不计划新增后端公告 API 或数据库表；若后续 Change 仅生成静态 Mintlify 文档与命令规范，则不需要 Orval。
- REQ-0024 计划新增 `GET /api/v1/admin/logs`、`GET /api/v1/admin/logs/{id}` 与 `POST /api/v1/usage-events`；实现后必须同步 OpenAPI、Orval、`docs/03-api-index.md` 与错误码文档。

## 部署注意事项

- 生产必须配置 `APP_ENV=production` 与 MySQL `DATABASE_URL`。
- 生产不得使用 `.env.example` 默认 `APP_SECRET_KEY`、MySQL 密码、MinIO 密钥或管理员初始密码。
- 客户 MySQL 前置条件：MySQL 8.0+、`utf8mb4`、`utf8mb4_unicode_ci`、账号具备 DDL + DML 权限、VPS 到 MySQL 网络可达。
- 生产 Compose 不包含 mysql 服务，backend 不挂载 `./data/sqlite` 作为生产数据库。
- 外部 MinIO 场景使用 `docker-compose.prod.external.yml`，不会启动本地 minio/minio-init，需运维提前创建 `MINIO_BUCKET` 并配置最小读写权限。
- MinIO volume 必须持久化；重启后媒体对象仍应可读取。
- BUG-0051 将修改 Web 层代理配置；上线前需验证 Docker Web 端口访问 `/docs`、`/redoc`、`/openapi.json` 不进入 SPA fallback。
- REQ-0025 将修改 Web 静态资源与入口 HTML 图标声明；上线前需验证开发环境与 Docker Web 标签图标均显示菲尚特 Logo。
- REQ-0026 将引入产品发布前校验流程；发布前必须记录 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移、`.env.example` 同步、升级步骤、回滚说明、已知问题和影响范围。
- REQ-0024 将新增日志存储表或扩展 `audit_logs`，上线前需确认 SQLite demo 与 MySQL production schema、索引、保留周期和清理策略。
- 日志详情属于敏感信息，生产发布前必须完成脱敏验收，确保不展示密码、Token、Authorization、Cookie、MinIO 密钥、数据库 DSN 或真实客户数据。

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
- 未经 OpenSpec Change 直接创建顶层 `releases/` 目录。
- 管理端、登录页、店主端或小程序内的发布公告入口。
- 复杂 BI、漏斗分析、第三方埋点平台、日志批量导出、外部日志系统和消息队列异步采集。

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
- BUG-0051 已归档 `fix-api-docs-swagger-ui-link-wrong`，验收覆盖 Web dev proxy、Docker Nginx Swagger 代理、OpenAPI JSON、生产只读策略与管理端权限边界。
- BUG-0052 已归档 `fix-api-docs-metric-cards-inconsistent`，验收覆盖接口文档页摘要指标卡 DOM/class、视觉层级、semantic token 与既有接口文档功能不回归。
- BUG-0053 已归档 `fix-api-docs-list-layout-pagination-inconsistent`，验收覆盖接口列表标题移除、分页 DOM、筛选回页、每页条数与既有接口文档功能不回归。
- BUG-0054 已创建 `fix-admin-content-padding-too-large`，后续执行 `/opsx-apply fix-admin-content-padding-too-large`；验收覆盖 Admin Shell padding、content-inner 宽度、SKU / 系统设置页面级宽度分叉和基准页面视觉回归。
- BUG-0055 已完成 `fix-admin-list-layout-unification` apply，任务 30/30；验收覆盖 8 个管理端列表页模块顺序、筛选区、sticky action column、分页最多 5 个可点击页码与关键行操作不回归，后续待 `/opsx-archive fix-admin-list-layout-unification`。
- REQ-0023 已完成 apply；验收覆盖 operationId 深链、新窗口安全属性、非 OpenAPI 禁用态、权限与 token 不泄露。
- REQ-0025 已归档 `update-brand-logo-fst-favicon`，验收覆盖 Sidebar 品牌区文案、Logo、版本号、收起态、favicon 与现有导航/权限不回归。
- REQ-0026 已完成 `add-product-release-management` archive；验收覆盖产品版本对象、Mintlify 静态公告、发布前校验、`releases/` 目录治理与发布命令族。
- REQ-0024 已纳入 Sprint，并已完成 `/req-opsx REQ-0024-product-usage-logging` 创建 `add-product-usage-logging`；后续执行 `/opsx-apply add-product-usage-logging`，验收覆盖日志 API、事件字典、数据库、脱敏、管理端日志审计页和产品 v2 PNG 对齐。
