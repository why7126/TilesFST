---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-04 15:36:01
title: Sprint 004 迭代说明
purpose: 记录 Sprint 004 目标、范围、Change、工作量与风险
content: 生产环境部署与 MySQL 数据库支持（REQ-0018）+ 管理端超级管理员账号保护（REQ-0019）+ 创建用户校验提示修复（BUG-0050）+ 管理端接口文档菜单与在线调试（REQ-0022）+ 接口文档列表行级 Swagger 详情入口（REQ-0023）+ Swagger UI 入口修复（BUG-0051）+ 接口文档指标卡一致性修复（BUG-0052）+ 接口文档列表分页一致性修复（BUG-0053）+ 管理端全局内容区域内边距修复（BUG-0054）+ 管理端多列表页布局与筛选分页交互统一修复（BUG-0055）+ 品牌区 Logo、菲尚特FST 文案与网页图标统一（REQ-0025）+ 产品版本发布与公告管理（REQ-0026）+ 产品使用行为埋点与接口请求日志详情（REQ-0024）
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: completed
note: workflow-sync — workflow-sync 自动同步 — 13/13 Change archived；0 applied；Sprint `completed`
---

# Sprint 004

## Sprint 目标

本迭代原主线聚焦 **生产环境部署与 MySQL 数据库支持**，将 TILESFST 从当前本地/demo SQLite 部署能力扩展到 VPS Docker Compose + 外部 MySQL 8.0+ + MinIO 持久化的生产部署路径，同时保持本地 `./scripts/docker-up.sh` SQLite 默认体验不回归。

2026-06-30 追加 **管理端超级管理员账号保护**：以 `ADMIN_USERNAME` 对应账号作为受保护系统账号，禁止管理端编辑、重置密码、冻结、删除及默认策略下本人改密，避免失去系统保底管理员。

2026-06-30 追加 **创建用户校验提示修复**：将已评审 BUG-0050 纳入本 Sprint，修复用户管理弹窗创建用户时用户名长度不足返回默认 422 `detail`、前端只能展示兜底错误的问题。

2026-07-01 追加 **管理端接口文档菜单与在线调试**：将已评审 REQ-0022 纳入本 Sprint，在系统设置下方新增 `/admin/api-docs` 管理端入口，支持管理员查看系统所有接口、Swagger 调试策略与 Orval 方法名映射。

2026-07-01 追加 **Swagger UI 入口修复**：将已评审 BUG-0051 纳入本 Sprint，按用户确认的 Web 层代理 Swagger 方案，修复接口文档页右上角【Swagger UI】进入 Web 首页的问题。

2026-07-01 追加 **接口文档指标卡一致性修复**：将已评审 BUG-0052 纳入本 Sprint，修复 `/admin/api-docs` 标题下方摘要指标卡与 `/admin/tile-skus` 同类指标卡 DOM/class 与视觉层级不一致的问题。

2026-07-01 追加 **接口文档列表分页一致性修复**：将已评审 BUG-0053 纳入本 Sprint，修复 `/admin/api-docs` 接口列表冗余「系统接口」标题与分页交互未对齐瓷砖 SKU 页的问题。

2026-07-02 追加 **接口文档列表行级 Swagger 详情入口**：将已评审 REQ-0023 纳入本 Sprint，在 `/admin/api-docs` 接口列表增加行级「查看」入口，新窗口打开 Swagger UI 并定位到具体 operationId 锚点；非 OpenAPI 路由显示禁用态且不生成可点击链接。

2026-07-01 追加 **品牌区 Logo、菲尚特FST 文案与网页图标统一**：将已评审 REQ-0025 纳入本 Sprint，统一管理端 Sidebar 品牌区 Logo、`菲尚特FST`、版本号、`家居建材资料库` 与浏览器标签图标。

2026-07-02 追加 **产品版本发布与公告管理**：将已评审 REQ-0026 纳入本 Sprint，建立产品版本发布对象、公开 Mintlify 发布公告、发布前校验门禁、`releases/` 顶层目录治理和发布命令族设计；OpenSpec Change 已创建为 `add-product-release-management`。

2026-07-02 追加 **产品使用行为埋点与接口请求日志详情**：将已评审 REQ-0024 纳入本 Sprint，建设 API 请求日志、产品行为事件字典、日志详情存储与管理端日志审计页；产品 v2 原型和 PNG Golden Reference 已落盘，OpenSpec Change 已创建为 `add-product-usage-logging`。

2026-07-03 追加 **管理端全局内容区域内边距修复**：将已评审 BUG-0054 纳入本 Sprint，修复 Admin Shell 右侧主内容区域 padding 过大、`content-inner` 旧宽度上限和 SKU / 系统设置页面级宽度分叉，OpenSpec Change 已创建为 `fix-admin-content-padding-too-large`。

2026-07-03 追加 **管理端多列表页布局与筛选分页交互统一修复**：将已评审 BUG-0055 纳入本 Sprint，统一瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计与接口文档页面的模块顺序、筛选/搜索区、固定操作列和最多 5 个可点击页码，OpenSpec Change 已创建为 `fix-admin-list-layout-unification`。

正式纳入范围：

1. **REQ-0018-production-mysql-deployment** — 生产环境部署与 MySQL 数据库支持。
2. **REQ-0019-admin-superuser-protection** — 管理端超级管理员账号保护。
3. **BUG-0050-user-create-validation-message-unclear** — 创建用户校验失败未明确提示具体问题点。
4. **REQ-0022-admin-api-docs-menu** — 管理端接口文档菜单与在线调试。
5. **BUG-0051-api-docs-swagger-ui-link-wrong** — 接口文档页 Swagger UI 入口跳转到 Web 首页。
6. **BUG-0052-api-docs-metric-cards-inconsistent** — 接口文档页指标卡样式与瓷砖 SKU 页不一致。
7. **BUG-0053-api-docs-list-layout-pagination-inconsistent** — 接口文档列表冗余系统接口信息且分页未与 SKU 页一致。
8. **REQ-0023-api-docs-swagger-detail-link** — 接口文档列表行级查看并跳转 Swagger 详情。
9. **REQ-0025-brand-logo-fst-favicon** — 品牌区 Logo、菲尚特FST 文案与网页图标统一。
10. **REQ-0026-product-release-management** — 产品版本发布与公告管理。
11. **REQ-0024-product-usage-logging** — 产品使用行为埋点与接口请求日志详情。
12. **BUG-0054-admin-content-padding-too-large** — 管理端全局右侧内容区域内边距过大。
13. **BUG-0055-admin-list-layout-unification** — 管理端多列表页布局、筛选区、操作列与分页不统一。

### REQ-0018-production-mysql-deployment 要点

- **优先级**：P0
- **类型**：基础设施 / 部署 / 数据库
- **范围**：后端双数据库策略、MySQL baseline 初始化、空库管理员 seed、生产 Compose、MinIO 生产持久化、环境变量与部署文档、MySQL 验证路径。
- **不包含**：Compose 内嵌 MySQL、SQLite 到 MySQL 业务数据迁移、高可用、K8s/Helm/Terraform、云厂商专有集成、前端/小程序 UI 改动。
- **OpenSpec**：`add-production-mysql-deployment`（proposed，OpenSpec strict validate 已通过）。
- **验收重点**：生产 `APP_ENV=production` 必须连接 MySQL 并 fail-fast；本地 SQLite 不回归；生产 MinIO 单桶持久化；MySQL 集成验证覆盖 schema init、admin seed、登录或 CRUD；文档和 `.env.example` 同步。

### REQ-0019-admin-superuser-protection 要点

- **优先级**：P1
- **类型**：管理端 / 用户与权限
- **范围**：后端统一识别 `settings.admin_username` 受保护账号；用户列表/详情返回 `is_protected` 与 `protected_reason`；禁止编辑、重置密码、冻结/解冻、删除和默认策略下本人改密；前端用户管理列表禁用受保护账号操作按钮并展示原因。
- **不包含**：新增 `super_admin` / `root` 角色枚举；改变既有 RBAC；移除 `.env` 级运维恢复机制；店主端、小程序改造。
- **OpenSpec**：`update-admin-superuser-protection`（proposed）。
- **验收重点**：后端 403 保护与数据库不变；OpenAPI/Orval 暴露新增字段；错误码登记；用户管理行操作禁用态对齐现有列表页；普通用户操作不回归。

### BUG-0050-user-create-validation-message-unclear 要点

- **严重等级**：medium
- **类型**：管理端 / 用户管理 / 表单校验反馈
- **现象**：创建用户时输入 `abc` 这类小于 4 位用户名，后端返回 FastAPI 默认 422 `detail`，前端无法读取统一 `message`，只能展示兜底失败文案。
- **根因**：`UserCreateRequest.username` 的 Pydantic `min_length=4` 在进入 `validate_username()` 前拦截，业务层中文错误文案没有机会返回；全局异常处理未统一转换请求体验证错误。
- **修复范围**：创建用户 API 的用户名校验错误结构、前端弹窗错误提示展示、用户名其他格式错误与重复用户名回归、合法创建不回归。
- **OpenSpec**：`fix-user-create-validation-message-unclear`（proposed）。
- **验收重点**：`username="abc"` 返回统一 `{ code, message, data }` 且 message 明确；弹窗能定位用户名字段；后端 pytest 与前端组件测试覆盖。

### REQ-0022-admin-api-docs-menu 要点

- **优先级**：P1
- **类型**：管理端 / 接口文档
- **范围**：SYSTEM 分组在「系统设置」下方新增「接口文档」菜单；注册 `/admin/api-docs`；管理员可查看系统全部接口目录、Swagger/OpenAPI 入口、生产 Try It Out 策略与 Orval 生成方法名。
- **系统所有接口定义**：包含 `/api/v1/*`、`/health`、`/media/{object_key:path}` 以及其他未纳入 `/api/v1` 但属于 FastAPI app 的路由。
- **不包含**：接口编辑、Mock、公开接口文档、生产环境 Try It Out、通过管理端修改 OpenAPI/Orval/后端路由、展示密钥或真实环境变量。
- **OpenSpec**：`add-admin-api-docs-menu`（applied，23/23 tasks complete，OpenSpec strict validate 已通过）。
- **验收重点**：仅管理员可访问；生产展示入口但隐藏/禁用 Try It Out；接口目录含非 `/api/v1` 路由；Orval 方法名可定位前端联调；符合管理端列表/表单横切一致性 gate。

### BUG-0052-api-docs-metric-cards-inconsistent 要点

- **严重等级**：medium
- **类型**：管理端 / 接口文档 / UI 一致性
- **现象**：`/admin/api-docs` 标题下方接口摘要指标卡与 `/admin/tile-skus` 标题下方 SKU 统计指标卡视觉不一致。
- **根因**：接口文档页摘要卡仅复用 `summary-grid` / `metric-card` 容器，但内部使用 `p.metric-label` + `strong` + `span`，缺少管理端基准结构 `.metric-value` 与 `.metric-desc`，导致通用 metric 样式无法完整命中。
- **修复范围**：调整接口文档页摘要卡 DOM/class 到管理端 metric 基准结构，补充前端测试，确认接口目录、Swagger 策略、Orval 展示和权限不回归。
- **OpenSpec**：`fix-api-docs-metric-cards-inconsistent`（archived，13/13 tasks complete，OpenSpec specs 已合并）。
- **验收重点**：四个摘要卡包含 `.metric-label`、`.metric-value`、`.metric-desc`；视觉层级与 SKU 页一致；不新增裸 Hex；不影响 API/数据库/Orval/Docker。

### BUG-0051-api-docs-swagger-ui-link-wrong 要点

- **严重等级**：high
- **类型**：管理端 / 接口文档 / Swagger 入口
- **现象**：在 `/admin/api-docs` 点击右上角【Swagger UI】后，浏览器进入 `http://localhost:3000/` Web 首页，而不是 FastAPI Swagger UI。
- **根因**：页面链接为相对路径 `/docs`，但 Vite dev proxy 与 Docker Web Nginx 均未代理 Swagger 路由，Docker 下 `/docs` 落入 SPA fallback 并被 React 通配路由重定向到 `/`。
- **修复范围**：使用 Web 层代理 Swagger，补齐 Vite dev proxy 与 Docker Nginx 的 `/docs`、`/redoc` 及 Swagger 相关路径代理；保持 `/api/`、`/media/`、`/openapi.json` 不回归；不得在前端硬编码后端端口。
- **OpenSpec**：`fix-api-docs-swagger-ui-link-wrong`（archived，14/14 tasks complete，OpenSpec strict validate 已通过）。
- **验收重点**：本地开发与 Docker Web 端口点击【Swagger UI】均进入后端 Swagger；`/openapi.json` 仍返回 OpenAPI JSON；生产环境仍禁用或隐藏 Try It Out；管理端权限边界不变。

### BUG-0053-api-docs-list-layout-pagination-inconsistent 要点

- **严重等级**：medium
- **类型**：管理端 / 接口文档 / 列表 UI 一致性
- **现象**：`/admin/api-docs` 接口列表区域固定展示冗余标题「系统接口」，底部仅显示统计文本，没有与瓷砖 SKU 页一致的页码按钮和每页条数选择。
- **产品确认**：用户反馈中的「第一行【系统接口】信息」指接口列表区标题，修复时 MUST 直接移除该标题，不改名保留，也不按接口数据行过滤处理。
- **修复范围**：移除冗余标题；为接口列表增加前端分页状态、页码按钮、每页条数选择；筛选变化后回到第 1 页；补充 Vitest 覆盖分页 DOM 与筛选回页。
- **OpenSpec**：`fix-api-docs-list-layout-pagination-inconsistent`（archived，OpenSpec specs 已合并）。
- **验收重点**：分页 DOM 对齐 `/admin/tile-skus` / 管理端列表页；不修改后端 API、数据库、MinIO 或 Orval，除非后续设计明确改造接口契约。

### REQ-0023-api-docs-swagger-detail-link 要点

- **优先级**：P1
- **类型**：管理端 / 接口文档页
- **范围**：在 `/admin/api-docs` 接口列表新增行级 ACTION「查看」入口；OpenAPI 路由在新窗口打开 Swagger UI 并跳转到具体 `operationId` 锚点；非 OpenAPI 或缺少 `operation_id` 的路由显示禁用态、隐藏可点击链接并说明原因；点击后保留当前管理端筛选、列表和登录上下文。
- **不包含**：不内嵌 Swagger UI；不为 `included_in_openapi=false` 路由生成伪详情页；不向 Swagger URL、query、hash 或 DOM 注入 token；不改变生产环境 Try It Out 禁用策略。
- **OpenSpec**：`add-api-docs-swagger-detail-link`（applied，17/17 tasks complete，OpenSpec strict validate 已通过）。
- **验收重点**：`/docs#/{tag}/{operationId}` 深链编码正确；新窗口 `rel="noreferrer"`；非 OpenAPI 路由无 href；employee 仍不可访问；Vitest 覆盖链接、禁用态和 token 不泄露。

### REQ-0025-brand-logo-fst-favicon 要点

- **优先级**：P1
- **类型**：管理端 / Shell 品牌展示 / favicon
- **范围**：管理端 Sidebar 顶部品牌区展示用户提供的菲尚特 Logo、`菲尚特FST`、现有产品版本号和 `家居建材资料库`；浏览器 favicon / apple-touch-icon 替换为同一品牌 Logo 或派生图标。
- **不包含**：不改 Banner 管理主体页面；不新增后端 API、数据库、对象存储上传流程、店主 Web 或小程序品牌露出；不改变版本号维护机制。
- **OpenSpec**：`update-brand-logo-fst-favicon`（archived，OpenSpec specs 已合并）。
- **验收重点**：Sidebar 展开态与收起态无重叠；文案必须为 `菲尚特FST` 和 `家居建材资料库`；favicon 不再展示默认图标；不影响现有导航、权限、路由、API、数据库或 Orval。

### REQ-0026-product-release-management 要点

- **优先级**：P1
- **类型**：发布治理 / 静态文档 / 命令规范
- **范围**：产品版本发布对象、多个 Sprint 合并为一个产品版本、公开 Mintlify 发布公告、发布前校验门禁、发布公告内容结构、`releases/` 顶层目录治理和发布命令族设计。
- **不包含**：当前阶段不直接创建 `releases/`；不新增管理端、登录页、店主端或小程序入口；不支持草稿/待发布/已发布/撤回状态机；不新增后端公告 API 或数据库表。
- **OpenSpec**：`add-product-release-management`（archived，27/27 tasks complete）。
- **验收重点**：发布前校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example`；公告记录新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围；新增 `releases/` 前必须先通过 OpenSpec Change 修改目录规范。

### REQ-0024-product-usage-logging 要点

- **优先级**：P1
- **类型**：平台治理 / 日志与埋点 / 管理端列表页
- **范围**：API 请求日志采集、产品使用行为事件字典、日志详情 metadata 存储、管理端 SYSTEM / 日志审计列表、筛选、分页、详情抽屉、request_id 复制、敏感字段脱敏、日志保留周期与 SQLite/MySQL 索引策略。
- **不包含**：复杂 BI、第三方埋点平台、完整请求体/响应体默认保存、日志批量导出、外部日志系统、消息队列异步采集、容器 stdout/Nginx access log/数据库慢查询统一接入。
- **OpenSpec**：`add-product-usage-logging`（proposed，OpenSpec strict validate 已通过）。
- **验收重点**：`GET /api/v1/admin/logs`、`GET /api/v1/admin/logs/{id}`、`POST /api/v1/usage-events` 权限和统一响应；事件字典和后端 Schema 校验；日志审计页对齐产品 v2 PNG Golden Reference；列表分页和指标卡符合 admin-list 横切 gate；敏感字段不落库或脱敏展示。

### BUG-0054-admin-content-padding-too-large 要点

- **严重等级**：medium
- **类型**：管理端 / Admin Shell / 全局布局
- **现象**：管理端右侧主内容区域 padding 与内容宽度限制偏保守，导致日志审计、SKU、用户、Dashboard、系统设置等页面在桌面宽屏下有效内容区域偏小。
- **根因**：`.admin-shell .main-content` 仍使用 `48px 56px 72px`，`.content-inner` 保留 `1080px` 硬上限，同时 SKU 页和系统设置页存在页面级宽度覆盖，形成全局与局部分叉。
- **修复范围**：Desktop 主内容 padding 调整为 `24px 24px 48px`；tablet / mobile 联动收窄；放宽 `content-inner`；清理 SKU 与系统设置页面级宽度分叉；保持侧栏折叠、独立滚动、列表分页与表单布局不回归。
- **OpenSpec**：`fix-admin-content-padding-too-large`（proposed，OpenSpec strict validate 已通过）。
- **验收重点**：`/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/system-settings` 基准页面视觉回归；无新增裸 Hex；不影响 API、数据库、Orval、Docker、店主端和小程序。

### BUG-0055-admin-list-layout-unification 要点

- **严重等级**：medium
- **类型**：管理端 / 多列表页 / UI 一致性
- **现象**：瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计与接口文档页面的模块顺序、筛选/搜索交互、最后一列固定浮动和分页页码呈现不统一。
- **根因**：各管理端列表页在不同 Sprint 中独立实现或局部修复，未形成统一 `AdminListPage` DOM / 样式契约；接口文档页已沉淀 sticky action column 与分页形态，但未横向回灌到全部列表页。
- **修复范围**：统一模块顺序为标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块；以 SKU 页为筛选/搜索基线并移除【查询】/【搜索】显式提交按钮；统一重置按钮尺寸；以接口文档页为基线固定最后一列；分页最多展示 5 个可点击页码。
- **OpenSpec**：`fix-admin-list-layout-unification`（proposed，OpenSpec strict validate 已通过）。
- **验收重点**：8 个目标页面桌面视口横向对比；筛选变化和每页条数变化回到第 1 页；最后一列横向滚动保持可见；新增/编辑/启停/删除/查看/重置密码等行操作不回退；不影响 API、数据库、Orval、Docker、店主端或小程序。

## Scope

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0018 | 生产环境部署与 MySQL 数据库支持 | P0 | done | archived `add-production-mysql-deployment`（2026-06-29 16:25:27） |
| REQ-0019 | 管理端超级管理员账号保护 | P1 | done | archived `update-admin-superuser-protection`（2026-06-30 19:07:02） |
| REQ-0022 | 管理端接口文档菜单与在线调试 | P1 | done | archived `add-admin-api-docs-menu`（2026-07-01 00:40:14） |
| REQ-0023 | 接口文档列表行级查看并跳转 Swagger 详情 | P1 | done | archived `add-api-docs-swagger-detail-link`（2026-07-02 22:16:42） |
| REQ-0025 | 品牌区 Logo、菲尚特FST 文案与网页图标统一 | P1 | done | archived `update-brand-logo-fst-favicon`（2026-07-02 03:18:58） |
| REQ-0026 | 产品版本发布与公告管理 | P1 | done | status `done` |
| REQ-0024 | 产品使用行为埋点与接口请求日志详情 | P1 | done | archived `add-product-usage-logging`（2026-07-03 23:24:07） |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0050 | 创建用户校验失败未明确提示具体问题点 | medium | done | archived `fix-user-create-validation-message-unclear`（2026-06-30 18:52:07） |
| BUG-0051 | 接口文档页 Swagger UI 入口跳转到 Web 首页 | high | done | archived `fix-api-docs-swagger-ui-link-wrong`（2026-07-01 20:03:09） |
| BUG-0052 | 接口文档页指标卡样式与瓷砖 SKU 页不一致 | medium | done | archived `fix-api-docs-metric-cards-inconsistent`（2026-07-02 08:58:31） |
| BUG-0053 | 接口文档列表冗余系统接口信息且分页未与 SKU 页一致 | medium | done | archived `fix-api-docs-list-layout-pagination-inconsistent`（2026-07-02 09:13:51） |
| BUG-0054 | 管理端全局右侧内容区域内边距过大 | medium | done | archived `fix-admin-content-padding-too-large`（2026-07-03 23:47:11） |
| BUG-0055 | 管理端多列表页布局与筛选分页交互未统一 | medium | done | archived `fix-admin-list-layout-unification`（2026-07-04 07:48:50） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-production-mysql-deployment` | REQ-0018-production-mysql-deployment | archived | archived `add-production-mysql-deployment`（2026-06-29 16:25:27） |
| `update-admin-superuser-protection` | REQ-0019-admin-superuser-protection | archived | archived `update-admin-superuser-protection`（2026-06-30 19:07:02） |
| `fix-user-create-validation-message-unclear` | REQ-0005-user-management | archived | archived `fix-user-create-validation-message-unclear`（2026-06-30 18:52:07） |
| `add-admin-api-docs-menu` | REQ-0022-admin-api-docs-menu | archived | archived `add-admin-api-docs-menu`（2026-07-01 00:40:14） |
| `add-api-docs-swagger-detail-link` | REQ-0023-api-docs-swagger-detail-link | archived | archived `add-api-docs-swagger-detail-link`（2026-07-02 22:16:42） |
| `fix-api-docs-swagger-ui-link-wrong` | BUG-0051-api-docs-swagger-ui-link-wrong | archived | archived `fix-api-docs-swagger-ui-link-wrong`（2026-07-01 20:03:09） |
| `fix-api-docs-metric-cards-inconsistent` | BUG-0052-api-docs-metric-cards-inconsistent | archived | archived `fix-api-docs-metric-cards-inconsistent`（2026-07-02 08:58:31） |
| `fix-api-docs-list-layout-pagination-inconsistent` | BUG-0053-api-docs-list-layout-pagination-inconsistent | archived | archived `fix-api-docs-list-layout-pagination-inconsistent`（2026-07-02 09:13:51） |
| `update-brand-logo-fst-favicon` | REQ-0025-brand-logo-fst-favicon | archived | archived `update-brand-logo-fst-favicon`（2026-07-02 03:18:58） |
| `add-product-release-management` | — | archived | archived `add-product-release-management`（2026-07-02 15:27:00） |
| `add-product-usage-logging` | REQ-0024-product-usage-logging | archived | archived `add-product-usage-logging`（2026-07-03 23:24:07） |
| `fix-admin-content-padding-too-large` | BUG-0054-admin-content-padding-too-large | archived | archived `fix-admin-content-padding-too-large`（2026-07-03 23:47:11） |
| `fix-admin-list-layout-unification` | BUG-0055-admin-list-layout-unification | archived | archived `fix-admin-list-layout-unification`（2026-07-04 07:48:50） |
<!-- workflow-sync:scope-changes:end -->

### 延后项（待评审 / 未纳入本 Sprint）

| 项目 | 状态 | 延后原因 |
|---|---|---|
| REQ-0013-admin-shell-padding-refine | pending_review | 未评审，不得纳入正式规划 |
| Sprint 003 A-002 / A-003 / A-004 对应 UI 抽象 | backlog | 本 Sprint 为基础设施部署，不纳入 UI 模板建设 |
| 系统设置 P1b 登录失败锁定 | backlog | REQ-0017 复盘延后项，需单独 capture/review |

## 工作量估算

| 工作项 | SP | 人天 | 角色 | 说明 |
|---|---:|---:|---|---|
| 数据库配置与 MySQL driver | 4 | 3.0 | 后端 | `APP_ENV` / `DATABASE_URL` / fail-fast / 日志脱敏 |
| Dialect-aware session 与初始化 | 5 | 4.0 | 后端 | SQLite/MySQL engine 分支；MySQL migration 入口 |
| MySQL baseline DDL 与 seed | 5 | 4.0 | 后端 | 表清单、类型映射、管理员 seed |
| 生产 Docker Compose 与 MinIO | 3 | 2.0 | 后端/DevOps | prod compose、外部 MySQL、MinIO volume |
| 文档与环境变量同步 | 2 | 1.5 | 后端/文档 | `.env.example`、deployment、database、rules、README |
| MySQL 集成验证与 smoke | 2 | 1.5 | 测试/后端 | MySQL 8 service/marker、登录/API、媒体读取 |
| Release / archive 预检 | 0 | 0.0 | 全员 | 归入各项验收 |
| REQ-0019 后端保护与错误码 | 3 | 2.0 | 后端 | 受保护账号判定、列表/详情字段、编辑/重置/状态/改密拦截 |
| REQ-0019 管理端用户列表 UI | 2 | 1.5 | 前端 | 操作按钮禁用态、原因提示、普通用户流程回归 |
| REQ-0019 API 文档与 Orval | 1 | 1.0 | 后端/前端 | OpenAPI 字段、错误码文档、Orval 客户端同步 |
| REQ-0019 自动化测试 | 1 | 1.0 | 测试/前端/后端 | pytest + Vitest 覆盖保护和不回归 |
| BUG-0050 校验错误统一与前端提示 | 3 | 2.0 | 后端/前端/测试 | 用户名长度不足统一错误结构、弹窗展示后端 message、pytest + Vitest 回归 |
| REQ-0022 管理端导航与页面框架 | 3 | 2.0 | 前端 | SYSTEM 菜单、`/admin/api-docs` 路由、管理员权限与页面骨架 |
| REQ-0022 接口目录聚合 | 3 | 2.0 | 后端/前端 | 覆盖 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他 app routes |
| REQ-0022 Swagger 环境策略 | 3 | 2.0 | 后端/前端 | 非生产允许调试；生产展示入口但隐藏/禁用 Try It Out |
| REQ-0022 Orval 方法名映射 | 3 | 2.0 | 前端/API | 展示 Orval 生成方法名；未生成项显示状态与原因 |
| REQ-0022 测试、文档与验收 | 3 | 3.0 | 测试/文档 | pytest/Vitest/Orval/API 文档/生产策略验收 |
| BUG-0051 Swagger Web 代理修复 | 3 | 2.0 | 前端/DevOps/测试 | Vite dev proxy、Docker Nginx Swagger 路由、生产只读策略与页面入口回归 |
| BUG-0052 指标卡一致性修复 | 2 | 1.5 | 前端/测试 | 从 fix_buffer 扣减；已归档 `fix-api-docs-metric-cards-inconsistent` |
| BUG-0053 接口文档列表分页一致性修复 | 2 | 1.5 | 前端/测试 | 从 fix_buffer 扣减；已归档 `fix-api-docs-list-layout-pagination-inconsistent` |
| REQ-0023 接口文档行级 Swagger 详情入口 | 3 | 2.0 | 前端/测试 | 追加范围；已完成 `add-api-docs-swagger-detail-link` apply；覆盖 operationId 深链、非 OpenAPI 禁用态与 token 不泄露回归 |
| REQ-0025 品牌区与 favicon 统一 | 3 | 2.0 | 前端/测试 | 已归档 `update-brand-logo-fst-favicon` |
| REQ-0026 产品版本发布与公告管理 | 3 | 2.0 | 产品/文档/工具链 | 追加范围；已创建 `add-product-release-management`；覆盖 Mintlify 公告、发布校验、`releases/` 目录治理和命令族设计 |
| REQ-0024 产品使用行为埋点与接口请求日志详情 | 8 | 6.0 | 后端/前端/测试 | 追加范围；已创建 `add-product-usage-logging`；覆盖请求日志中间件、行为事件字典、日志查询 API、管理端日志审计列表/详情抽屉与安全脱敏测试 |
| BUG-0054 管理端全局内容区域内边距修复 | 3 | 2.0 | 前端/测试 | 从 fix_buffer 扣减；已创建 `fix-admin-content-padding-too-large`；覆盖 Admin Shell padding、content-inner 宽度和页面级宽度分叉 |
| BUG-0055 管理端多列表页布局统一修复 | 5 | 3.5 | 前端/测试 | fix_buffer 已为 0，按超容量追加；已创建 `fix-admin-list-layout-unification`；覆盖 8 个管理端列表页模块顺序、筛选区、sticky action column 和最多 5 页码 |
| **fix_buffer** | **0** | **0.0** | 全员 | 已被 BUG-0051/BUG-0052/BUG-0053/BUG-0054 消耗完；后续仅 P0 阻断项可追加 |
| **合计** | **83** | **60.5** | — | 10 个已归档 change + 1 个 applied add-* + 2 个进行中/proposed UI Change；追加范围存在高排期风险 |

## 里程碑

| 里程碑 | 目标日期 | 验收输出 |
|---|---|---|
| M1 配置与 DB 设计定稿 | 2026-07-01 18:00:00 | `DATABASE_URL` 策略、MySQL driver、`implementation/db.md` 类型映射初版 |
| M2 MySQL baseline + seed | 2026-07-04 18:00:00 | 空 MySQL schema 初始化、管理员登录 smoke |
| M3 生产 Compose + MinIO | 2026-07-08 18:00:00 | `docker-compose.prod.yml`、MinIO 单桶持久化、外部 MySQL runbook |
| M4 测试与文档收口 | 2026-07-11 18:00:00 | SQLite 回归、MySQL 集成验证、部署文档与 env 同步 |
| M5 Sprint 验收 | 2026-07-13 18:00:00 | acceptance-report 勾选、OpenSpec validate、准备 archive |

## 风险

| 风险 | 等级 | 缓解 |
|---|---|---|
| SQLite 最终态到 MySQL baseline 漏表/漏索引 | high | 先汇总 `schema.sql` + migrations；`implementation/db.md` 表清单逐项勾选；MySQL test 覆盖关键表 |
| Repository SQL 存在 SQLite-only 语法 | high | MySQL 集成测试覆盖登录和至少一条 CRUD；必要时按 dialect 分支 |
| 生产 `.env` 使用示例密钥 | high | 文档和 `.env.example` 显式禁止；release checklist 检查 |
| 外部 MySQL 网络/权限问题 | medium | 部署 runbook 加入 8.0+、utf8mb4、DDL+DML、白名单、端口可达检查 |
| workflow-sync 将 REQ 状态标为 `in_sprint` 但 iteration 为空的历史残留 | low | 本 Sprint 创建后写入 `iteration: sprint-004` 并由 workflow-sync 收敛 |
| fix 缓冲被实现任务挤占 | medium | 保留 10 SP / 7.0 人天缓冲；非 P0 新需求默认下一 Sprint |
| 已进入 apply 后追加 REQ-0019 | medium | 本次为用户显式纳入；执行前必须先 `/req-opsx`，且不得重新打开已归档 REQ-0018 |
| 受保护账号前端只做禁用但后端未拦截 | high | 后端作为强制边界；pytest 覆盖编辑、重置、状态、本人改密拒绝 |
| 管理端用户列表 UI 回归 Sprint 002/003 重复问题 | medium | 引用 `admin-list-page-consistency.md`；保留分页 DOM、fixed toast、DS confirm modal |
| 已进入 in_progress 后追加 BUG-0050 | medium | 本次为用户显式纳入；执行前必须先 `/bug-opsx`，并将 fix-* 挂在既有 `add-user-management` 能力之下 |
| 追加后 fix 缓冲低于 30% 门槛 | medium | 当前保留 10 SP / 7.0 人天缓冲；因 BUG-0050 追加后缓冲约 23%，后续非 P0/P1 项默认延后 |
| 用户创建弹窗错误提示可能回归弹窗 CSS/布局问题 | low | 引用 `admin-modal-width-css-cascade.md`；仅调整错误提示，不改弹窗宽度类名与主体布局 |
| 已进入 in_progress 后追加 REQ-0022 | medium | 本次为用户显式纳入；已创建 `add-admin-api-docs-menu`，执行前需确认 change 仍为 proposed 且通过 strict validate |
| REQ-0022 需要覆盖非 `/api/v1` 路由，OpenAPI 可能默认遗漏 | medium | 后端聚合路由时必须显式补充 `/health`、`/media/{object_key:path}` 与其他 app routes；验收用路由清单对照 |
| 生产环境误开放 Swagger Try It Out | high | 以环境变量/构建配置/Swagger UI 参数为强制 gate；生产 smoke 必须验证 Try It Out 不可用 |
| Orval 方法名映射与实际生成文件漂移 | medium | 实现后执行 Orval，并以 `src/web/src/shared/api/generated.ts` 为事实源校验方法名 |
| 追加后 fix 缓冲进一步低于 30% 门槛 | high | 当前 sprint 已 in_progress 且多次追加；REQ-0022 后不再接收非 P0/P1 新项，必要时拆分到下一 Sprint |
| 已进入 in_progress 后追加 BUG-0052 | medium | 本次为用户显式纳入；执行前必须先 `/bug-opsx`，并将 fix-* 挂在 `add-admin-api-docs-menu` 之下 |
| BUG-0052 消耗 fix_buffer 后缓冲不足 | high | 已从 fix_buffer 扣减 2 SP / 1.5 人天；后续非 P0/P1 项默认延后，避免继续挤占验收与归档时间 |
| 已进入 in_progress 后追加 BUG-0051 | high | 本次为用户显式纳入且 BUG 已 approved；执行前必须先 `/bug-opsx`，并将 fix-* 挂在 `add-admin-api-docs-menu` 之下 |
| Swagger Web 代理误放开生产 Try It Out | high | 修复只补 Web 层代理，不改变后端生产策略；验收必须验证生产 Try It Out 仍不可用 |
| Swagger 代理规则覆盖 SPA 或既有代理 | medium | Vite/Nginx 仅补 Swagger 相关路径；回归 `/api/`、`/media/`、`/openapi.json` 与 `/admin/api-docs` 刷新 |
| 已进入 in_progress 后追加 BUG-0053 | medium | 本次为用户显式纳入且 BUG 已 approved；执行前必须先 `/bug-opsx`，并将 fix-* 挂在 `add-admin-api-docs-menu` 之下 |
| BUG-0053 继续消耗 fix_buffer | high | 已从 fix_buffer 继续扣减 2 SP / 1.5 人天；BUG-0051 追加后剩余 3 SP / 2.0 人天，后续非 P0 缺陷默认延后 |
| 已进入 in_progress 后追加 REQ-0025 | medium | 本次为用户显式纳入且 REQ 已 approved；已创建 `update-brand-logo-fst-favicon`，后续执行 `/opsx-apply` |
| REQ-0025 继续挤占低缓冲 Sprint | medium | 新增 3 SP / 2.0 人天后总估算升至 64 SP / 47.0 人天；后续非 P0/P1 项默认延后 |
| 品牌区调整影响 Sidebar 既有收起交互 | medium | 实现需对照 REQ-0011 展开/收起能力，验收 1366×768 与 1440×1024 视口无重叠 |
| favicon 静态资源路径在 dev/Docker 间不一致 | low | 验收需覆盖 Vite dev 与 Docker Web 入口 HTML 图标声明，避免回退默认图标 |
| 已进入 in_progress 后追加 REQ-0023 | medium | 本次为用户显式纳入且 REQ 已 approved；已完成 `/opsx-apply add-api-docs-swagger-detail-link`，归档前保留人工 sign-off |
| REQ-0023 继续挤占低缓冲 Sprint | high | 新增 3 SP / 2.0 人天后总估算升至 67 SP / 49.0 人天；后续非 P0/P1 项默认延后 |
| Swagger operationId 深链格式与 FastAPI UI 不一致 | medium | OpenSpec design 阶段验证 Swagger UI deepLinking hash 规则；Vitest 覆盖 `/docs#/{tag}/{operationId}` 编码与非 OpenAPI 禁用态 |
| 行级 Swagger 链接泄露鉴权上下文 | high | 链接只使用 `/docs` hash，不拼接 token/query；测试断言 URL 与 DOM 不包含 Bearer Token、Cookie 或用户信息 |
| 已进入 in_progress 后追加 REQ-0026 | high | 本次为用户显式纳入且 REQ 已 approved；执行前必须先 `/req-opsx`，不得绕过 OpenSpec 直接创建 `releases/` 或发布命令 |
| REQ-0026 继续挤占低缓冲 Sprint | high | 新增 3 SP / 2.0 人天后总估算升至 70 SP / 51.0 人天；fix_buffer 低于 30%，后续非 P0/P1 项默认延后 |
| 发布治理涉及目录规范变更 | high | `releases/` 顶层目录必须通过 OpenSpec Change 更新 `rules/directory-structure.md`、AGENTS 与相关文档后才能创建 |
| Mintlify 静态公告可能混入敏感信息 | medium | 公告模板必须包含公开发布内容边界，发布前校验不得泄露密钥、客户数据、内部数据库连接串或不可公开域名 |
| 已进入 in_progress 后追加 REQ-0024 | high | 本次为用户显式纳入且 REQ 已 approved；已通过 `/req-opsx` 创建 `add-product-usage-logging`；实现阶段不得绕过 `/opsx-apply` 直接开发日志表、接口或管理端页面 |
| REQ-0024 继续挤占低缓冲 Sprint | high | 新增 8 SP / 6.0 人天后总估算升至 78 SP / 57.0 人天；fix_buffer 约 3.8%，后续非 P0 阻断项默认延后 |
| 日志能力涉及敏感信息和数据量增长 | high | OpenSpec design MUST 明确脱敏白名单/黑名单、metadata 截断、索引、保留周期和 SQLite/MySQL schema；禁止默认保存完整请求体/响应体 |
| 日志审计页存在管理端列表 UI 复发风险 | medium | 必须引用 `admin-list-page-consistency.md`，对齐产品 v2 PNG、分页 DOM、指标卡 DOM、fixed toast 和详情抽屉无布局位移 |
| 行为埋点事件字典可能失控膨胀 | medium | 仅允许 `tracking-events.md` 登记事件；新增事件必须同步枚举、Schema、测试与 OpenSpec，禁止业务代码随意拼接 event_name |
| 已进入 in_progress 后追加 BUG-0054 | high | 本次为用户显式纳入且 BUG 已 approved；已通过 `/bug-opsx` 创建 `fix-admin-content-padding-too-large`；实现阶段不得绕过 `/opsx-apply` 直接修改 Admin Shell CSS |
| BUG-0054 消耗最后 fix_buffer | high | BUG-0054 新增 3 SP / 2.0 人天并消耗剩余缓冲；fix_buffer 降至 0%，后续除 P0 阻断缺陷外默认移入下一 Sprint |
| 全局 padding 调整引发管理端页面回归 | medium | 实现必须验证 `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/system-settings`，并保留侧栏折叠、独立滚动、分页和表单布局 |
| 已进入 in_progress 后追加 BUG-0055 | high | 本次为用户显式纳入且 BUG 已 approved/in_sprint；已通过 `/bug-opsx` 创建 `fix-admin-list-layout-unification`；实现阶段不得绕过 `/opsx-apply` 直接修改多页面列表布局 |
| BUG-0055 在 fix_buffer 为 0 后继续追加 | high | BUG-0055 新增 5 SP / 3.5 人天，Sprint 估算升至 83 SP / 60.5 人天；后续除 P0 阻断缺陷外默认移入下一 Sprint |
| 多列表页横切统一可能扩大回归面 | high | 实现必须按 `admin-list-page-consistency.md` 做 8 个页面并排验收，优先沉淀共用分页 / sticky action column 契约，避免各页重复局部 CSS |

## 知识库承接

### Knowledge Intake Report

| ID | 优先级 | 描述 | 本 Sprint 承接方式 |
|---|---|---|---|
| A-001 | P0 | 完成 Sprint 003 `acceptance-report.md` 核心 AC 人工勾选 | 采纳：本 Sprint M5 必须对 REQ-0018 AC-001～AC-045 做 sign-off，不允许只写 Published |
| A-002 | P1 | 落地 `AdminListPage` / 列表 DOM 契约 | 部分采纳：REQ-0019 修改用户管理列表，BUG-0052/BUG-0053 要求接口文档 summary metric 与分页 DOM/class 对齐既有基准；模板抽象仍保留 backlog |
| A-003 | P1 | 落地 `AdminFormPage` 单 CTA + AdminToast + DS confirm | 部分采纳：REQ-0022 作为管理端文档页不得引入保存 CTA、原生 confirm 或文档流 success/error banner |
| A-004 | P1 | Modal 宽度 CSS 层叠 gate | 部分采纳：BUG-0050 涉及用户创建弹窗错误提示，要求修复不引入 modal-card 层叠/宽度回归 |
| A-005 | P2 | Sprint scope 冻结策略 | 偏离并标注：本次按用户显式指令追加 REQ-0019、BUG-0050、REQ-0022、BUG-0051、BUG-0052、BUG-0053、REQ-0025、REQ-0023、REQ-0026、REQ-0024、BUG-0054 与 BUG-0055；后续追加项仍需在风险表显式记录 |
| A-006 | P2 | `openspec archive` ADDED 冲突预检脚本 | 部分采纳：归档前运行 `openspec validate add-production-mysql-deployment --strict`，如需工具化另起 REQ |
| A-007 | P2 | trace.md YAML fence CI 校验 | 部分采纳：本 Sprint 人工检查 trace fence；工具化另起 REQ |
| A-008 | P2 | 导出 REQ-0017 五 Tab PNG Golden | 不适用：非本 Sprint 范围 |
| A-009 | P3 | 系统设置 P1b 登录失败锁定 | 延后：需单独需求评审 |

### 早期复盘模式承接

| 来源 | 模式 | 本 Sprint 处理 |
|---|---|---|
| sprint-002 A-005 / A-008 | 对象存储 / 大文件上传部署 checklist | 采纳：引用媒体上传最佳实践，生产 smoke 覆盖 Nginx、后端校验、MinIO、`/media/` |
| sprint-002 A-006 | 单迭代 add change ≤6，预留 fix 缓冲 | 偏离：add-* 数量仍低于上限，但多次追加后 fix_buffer 已低于 30%；已在风险表标注 |
| sprint-002 A-007 | 父 add 优先 archive，delta 冲突预检 | 采纳：本 Sprint 仅 1 个 add-*，归档前 strict validate |

## 横切预防清单

本 Sprint 当前正式范围包含生产部署、管理端用户列表增量、接口文档页与接口文档页 UI fix、管理端全局内容区域布局修复、管理端多列表页布局统一修复，以及管理端 Sidebar 品牌区与 favicon 统一。生产部署包含媒体上传 smoke；REQ-0019 涉及用户管理列表行操作状态，REQ-0022 / BUG-0052 / BUG-0053 / REQ-0023 涉及管理端接口文档页与同类 UI 结构对齐，BUG-0054 涉及 Admin Shell 全局内容宽度并影响日志审计、SKU、用户、Dashboard、系统设置等页面，BUG-0055 直接覆盖 SKU、品牌、类目、规格、Banner、用户、日志审计和接口文档 8 个列表页，必须引用管理端列表页与表单页一致性最佳实践。REQ-0025 不触发列表/表单/弹窗/上传横切最佳实践，但必须对照 `rules/ui-design.md` 与 REQ-0011 侧栏收起交互验收。

- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`

媒体上传验收 gate：

- [ ] 经 Web 入口或等价生产反代完成图片上传，不绕过后端 API。
- [ ] 后端返回 object_key / URL，MinIO 单桶内对象存在。
- [ ] `/media/{object_key}` 可读取对象，非法 object_key 仍被拒绝。
- [ ] Nginx `client_max_body_size` 与 `MAX_IMAGE_SIZE_MB` / `MAX_VIDEO_SIZE_MB` 文档一致。
- [ ] 重启 backend/web/minio 后对象仍可访问。

日志审计页验收 gate：

- [ ] `/admin/logs` 或 `/admin/audit-logs` 位于 SYSTEM 分组，且仅系统管理员可见。
- [ ] 指标卡使用 `.metric-label`、`.metric-value`、`.metric-desc`，展示 Today Logs、API Errors、Slow Requests、Sensitive Ops。
- [ ] 筛选区支持日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id，并提供查询与重置。
- [ ] 表格展示时间、类型、事件 / 摘要、操作者、客户端、状态、耗时、request_id、复制、详情。
- [ ] 分页 DOM 对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码 + 每页条数。
- [ ] 详情抽屉按基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性、metadata JSON 分组。
- [ ] request_id 复制、查询失败、详情加载失败均使用 fixed toast 或等价固定层，不造成页面纵向位移。
- [ ] 产品 v2 `log-audit-list.png` 与 `log-audit-detail-drawer.png` 完成 1440x1024 并排验收。

管理端列表页验收 gate：

- [ ] `/admin/users` 分页 DOM 仍为左侧 `page-summary`、右侧 `page-right` 页码与每页条数。
- [ ] 受保护账号提示使用 fixed toast / title / tooltip 等不会推挤页面布局的方式。
- [ ] 普通用户冻结、解冻、删除、重置密码仍使用 DS confirm modal，不引入 `window.confirm`。
- [ ] 受保护账号仅禁用受限操作，不隐藏操作列，不硬编码 `admin`。

管理端弹窗验收 gate：

- [ ] 用户创建弹窗不新增 `modal-card` 与专属类双挂载问题。
- [ ] 错误提示展示不改变弹窗宽度、遮罩、按钮区与滚动行为。
- [ ] Vitest 覆盖创建失败错误展示，必要时 import 相关 admin CSS 栈防止层叠回归。

管理端接口文档页验收 gate：

- [ ] `/admin/api-docs` 位于 SYSTEM 分组「系统设置」下方，且仅管理员可见。
- [ ] 直链 `/admin/api-docs` 对非管理员返回 403 或等价禁止访问状态。
- [ ] 接口目录包含 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他 FastAPI app routes。
- [ ] 生产环境展示接口文档入口，但 Swagger `Try It Out` 不可用。
- [ ] 页面展示 Orval 生成方法名；未生成项明确显示「未生成」或等价状态。
- [ ] 页面反馈使用 fixed toast / 静态状态，不使用会推挤布局的文档流提示。
- [ ] 摘要指标卡使用 `.metric-label`、`.metric-value`、`.metric-desc`，与 `/admin/tile-skus` 同类指标卡视觉层级一致。
- [ ] 接口列表直接移除冗余标题「系统接口」，不得改名保留。
- [ ] 接口列表分页 DOM 对齐 SKU/用户管理基准：左侧 `page-summary`，右侧 `page-right`、`page-buttons` 与 `page-size-wrap`。
- [ ] Method / Tag / Auth / 关键字筛选后分页回到第 1 页。
- [ ] 点击【Swagger UI】后，Web dev 与 Docker Web 均通过 Web 层代理进入 FastAPI Swagger UI，不进入 SPA fallback 或 Web 首页。
- [ ] `/docs`、`/redoc` 与 Swagger 相关依赖路径代理不影响 `/admin/api-docs` 刷新、`/api/`、`/media/`、`/openapi.json`。
- [ ] 生产环境 Swagger 入口仍保持只读策略，Try It Out 不因 Web 代理而放开。
- [ ] 接口列表 ACTION 列为 OpenAPI 路由提供行级「查看」，新窗口跳转到具体 `operationId` 锚点。
- [ ] `included_in_openapi=false` 或缺少 `operation_id` 的路由显示禁用「查看」，无可点击 href，且说明不可用原因。
- [ ] 行级 Swagger 链接不得携带 token/query 敏感信息，点击后当前 `/admin/api-docs` 筛选、列表与登录上下文不被刷新或覆盖。

管理端品牌区与 favicon 验收 gate：

- [ ] Sidebar 展开态展示 Logo、`菲尚特FST`、版本号、`家居建材资料库` 与收起按钮。
- [ ] Sidebar 收起态 Logo 和收起/展开按钮仍可识别、可点击，无导航图标重叠。
- [ ] 品牌 Logo 不加独立卡片背景、边框、底纹或阴影，不拉伸、不裁切关键图形。
- [ ] favicon / apple-touch-icon 使用菲尚特 Logo 或派生图标，浏览器标签不再显示默认图标。
- [ ] 1366×768 与 1440×1024 视口品牌区无重叠、无布局抖动。

管理端全局内容区域布局验收 gate：

- [ ] Desktop 视口下 `.admin-shell .main-content` 使用 `24px 24px 48px`，不再使用 `48px 56px 72px`。
- [ ] ≤1023px 视口 padding 调整为 `20px 16px 40px`；≤639px 视口 padding 调整为 `16px 12px 32px`。
- [ ] `.admin-shell .content-inner` 不再使用 `max-width: 1080px`，最终宽度策略在 OpenSpec design 中记录。
- [ ] SKU 页不再通过 `:has(.sku-page-hero) .content-inner` 保留 1120px 分叉；系统设置页不再通过 `settings-content-inner` 回退 1080px 旧宽度。
- [ ] `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/system-settings` 在 1440、1920、collapsed、tablet、mobile 基准视口下无横向滚动、无表格/分页/表单错位。
- [ ] 不新增裸 Hex，不改变侧栏展开/收起 localStorage 行为，不影响 API、数据库、Orval、Docker、店主端和小程序。

管理端多列表页布局统一验收 gate：

- [ ] `/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs`、`/admin/api-docs` 均按标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块顺序展示。
- [ ] 8 个目标页面的筛选/搜索区均不展示【查询】或【搜索】显式提交按钮，筛选控件变化后刷新或重新计算列表并回到第 1 页。
- [ ] 8 个目标页面的【重置】按钮高度、padding、圆角、字号、边框、图标策略和对齐方式一致。
- [ ] 8 个目标页面的列表最后一列在横向滚动时固定可见，表头和单元格右侧背景、分割线、阴影与接口文档页 sticky action column 基线一致。
- [ ] 分页统一使用左侧 `page-summary` 与右侧 `page-right`，可点击页码最多 5 个；总页数为 1 时仍展示禁用上一页/下一页与当前页 1。
- [ ] 切换每页显示条数后页码回到第 1 页；新增、编辑、启停、删除、查看、重置密码等行操作权限、禁用态和确认流程不回退。
- [ ] 1366、1440、1920 desktop 视口完成 8 个页面并排验收，tablet / mobile smoke 无控件重叠、文本裁切或明显横向溢出。

## 依赖

```text
sprint-004
└─ REQ-0018-production-mysql-deployment
   └─ add-production-mysql-deployment
      ├─ database capability（新增）
      │  ├─ APP_ENV / DATABASE_URL / MySQL driver
      │  ├─ dialect-aware session
      │  ├─ schema.mysql.sql / migration entry
      │  └─ admin seed
      ├─ deployment capability（新增）
      │  ├─ docker-compose.prod.yml
      │  ├─ external MySQL runbook
      │  └─ env / README / docs sync
      ├─ object-storage capability（MODIFIED）
      │  └─ production MinIO volume + single bucket smoke
      └─ testing capability（MODIFIED）
         └─ MySQL integration path + SQLite regression
└─ REQ-0019-admin-superuser-protection
   └─ update-admin-superuser-protection（待 /req-opsx）
      ├─ user-management capability（MODIFIED）
      │  ├─ protected account fields
      │  ├─ edit/reset/status operation guard
      │  └─ disabled row actions
      ├─ auth/profile capability（MODIFIED）
      │  └─ protected account password change guard
      ├─ api-governance capability（MODIFIED）
      │  └─ error code + OpenAPI + Orval
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest regression
└─ BUG-0050-user-create-validation-message-unclear
   └─ fix-user-create-validation-message-unclear（proposed）
      ├─ user-management capability（MODIFIED）
      │  ├─ username validation error structure
      │  └─ create user modal error display
      ├─ api-governance capability（MODIFIED）
      │  └─ request validation / business validation message consistency
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest regression
└─ REQ-0022-admin-api-docs-menu
   └─ add-admin-api-docs-menu（applied，23/23 tasks complete）
      ├─ admin-shell capability（MODIFIED）
      │  ├─ SYSTEM menu item below settings
      │  └─ /admin/api-docs route guard
      ├─ api-governance capability（MODIFIED）
      │  ├─ all route inventory
      │  ├─ Swagger Try It Out environment policy
      │  └─ Orval method name mapping
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest + Orval regression
   └─ BUG-0052-api-docs-metric-cards-inconsistent
      └─ fix-api-docs-metric-cards-inconsistent（archived，13/13 tasks complete）
         ├─ admin-api-docs page（MODIFIED）
         │  ├─ metric card DOM/class alignment
         │  └─ no bare Hex / semantic token reuse
         └─ testing capability（MODIFIED）
            └─ ApiDocsPage summary metric class regression
   └─ BUG-0051-api-docs-swagger-ui-link-wrong
      └─ fix-api-docs-swagger-ui-link-wrong（archived，14/14 tasks complete）
         ├─ web-client capability（MODIFIED）
         │  ├─ Swagger UI link regression
         │  └─ Vite dev proxy for Swagger routes
         ├─ deployment capability（MODIFIED）
         │  └─ Docker Nginx Swagger route proxy
         └─ testing capability（MODIFIED）
            └─ ApiDocsPage link + proxy regression
   └─ BUG-0053-api-docs-list-layout-pagination-inconsistent
      └─ fix-api-docs-list-layout-pagination-inconsistent（archived）
         ├─ admin-api-docs page（MODIFIED）
         │  ├─ remove redundant `系统接口` title
         │  ├─ frontend pagination state
         │  └─ page-size selector + filter reset to page 1
         └─ testing capability（MODIFIED）
         └─ Vitest pagination DOM + filter regression
   └─ REQ-0023-api-docs-swagger-detail-link
      └─ add-api-docs-swagger-detail-link（applied，17/17 tasks complete）
         ├─ admin-api-docs page（MODIFIED）
         │  ├─ ACTION column + row View link
         │  ├─ Swagger operationId deep link
         │  └─ non-OpenAPI disabled state
         └─ testing capability（MODIFIED）
            └─ ApiDocsPage link / disabled / token regression
└─ REQ-0025-brand-logo-fst-favicon
   └─ update-brand-logo-fst-favicon（archived）
      ├─ admin-shell capability（MODIFIED）
      │  ├─ Sidebar brand Logo + 菲尚特FST + version badge + 家居建材资料库
      │  ├─ collapsed sidebar brand state
      │  └─ favicon / apple-touch-icon static asset
      └─ testing capability（MODIFIED）
         └─ brand copy, favicon declaration, sidebar layout regression
└─ REQ-0026-product-release-management
   └─ add-product-release-management（archived，27/27 tasks complete）
      ├─ release-governance capability（新增）
      │  ├─ product release object
      │  ├─ multi-Sprint release mapping
      │  ├─ release checklist gate
      │  └─ PRODUCT_VERSION consistency check
      ├─ directory-governance capability（MODIFIED）
      │  └─ releases/ top-level directory rule via OpenSpec
      ├─ static-docs capability（新增）
      │  └─ Mintlify public release announcement source
      └─ command-governance capability（MODIFIED）
         └─ release command family via .cursor/commands source
└─ REQ-0024-product-usage-logging
   └─ add-product-usage-logging（proposed）
      ├─ log-audit capability（新增）
      │  ├─ API request log collection
      │  ├─ usage event dictionary + schema validation
      │  ├─ metadata JSON storage + masking
      │  └─ retention / indexes / SQLite + MySQL compatibility
      ├─ admin-log-audit page（新增）
      │  ├─ SYSTEM / LOG AUDIT menu and route
      │  ├─ metrics + filters + table + pagination
      │  └─ right detail drawer + request_id copy
      ├─ api-governance capability（MODIFIED）
      │  └─ logs list/detail API + usage events API + OpenAPI/Orval sync
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest + permission/security regression
└─ BUG-0054-admin-content-padding-too-large
   └─ fix-admin-content-padding-too-large（proposed）
      ├─ admin-shell capability（MODIFIED）
      │  ├─ global main-content padding
      │  ├─ content-inner width policy
      │  └─ sidebar collapse / independent scroll regression
      ├─ admin-list / admin-form pages（MODIFIED）
      │  ├─ SKU divergent content width override removal
      │  ├─ system settings content width alignment
      │  └─ logs, users, dashboard visual smoke
      └─ testing capability（MODIFIED）
         └─ AdminLayout / AdminSidebar / CSS static regression
└─ BUG-0055-admin-list-layout-unification
   └─ fix-admin-list-layout-unification（applied）
      ├─ admin-list pages（MODIFIED）
      │  ├─ TileSku / Brand / Category / Spec / Banner / User / LogAudit / ApiDocs module order
      │  ├─ unified filter/search region without query/search submit buttons
      │  ├─ sticky action column aligned to ApiDocs baseline
      │  └─ max 5 clickable pagination window
      └─ testing capability（MODIFIED）
         └─ pagination window + DOM order + sticky action column regression
```

## 发布计划

1. 完成 `/sprint-apply sprint-004` 后，先在本地 SQLite 路径跑后端回归。
2. 使用 MySQL 8 测试实例或 CI service container 跑 MySQL 集成验证。
3. 使用生产 Compose 示例做配置校验，确认不包含 mysql 服务。
4. 完成生产媒体上传与 `/media/{object_key}` 读取 smoke。
5. 对 REQ-0019 执行 `/opsx-apply update-admin-superuser-protection`，再回填验收结果。
6. 对 BUG-0050 执行 `/opsx-apply fix-user-create-validation-message-unclear`，再回填验收结果。
7. REQ-0022 已完成 `/opsx-apply add-admin-api-docs-menu`；后续归档时执行 `/opsx-archive add-admin-api-docs-menu`。
8. BUG-0051 已完成 `/bug-opsx`、`/opsx-apply` 与 `/opsx-archive fix-api-docs-swagger-ui-link-wrong`。
9. BUG-0052 已完成 `/bug-opsx`、`/opsx-apply` 与 `/opsx-archive fix-api-docs-metric-cards-inconsistent`。
10. BUG-0053 已完成 `/bug-opsx`、`/opsx-apply` 与 `/opsx-archive fix-api-docs-list-layout-pagination-inconsistent`。
11. REQ-0023 已纳入本 Sprint，并已完成 `/opsx-apply add-api-docs-swagger-detail-link`；后续人工验收后执行 `/opsx-archive add-api-docs-swagger-detail-link`。
12. REQ-0025 已完成 `/req-opsx`、`/opsx-apply` 与 `/opsx-archive update-brand-logo-fst-favicon`。
13. REQ-0026 已完成 `/opsx-archive add-product-release-management`；Change 已归档并合并正式规范。
14. REQ-0024 已完成 `/req-opsx REQ-0024-product-usage-logging` 创建 `add-product-usage-logging`；后续执行 `/opsx-apply add-product-usage-logging`。
15. BUG-0054 已完成 `/bug-opsx BUG-0054` 创建 `fix-admin-content-padding-too-large`；后续执行 `/opsx-apply fix-admin-content-padding-too-large`。
16. BUG-0055 已完成 `/bug-opsx BUG-0055`、`/opsx-apply fix-admin-list-layout-unification` 与视觉验收确认；后续执行 `/opsx-archive fix-admin-list-layout-unification`。
17. REQ-0019、BUG-0050 与 REQ-0022 已补跑 pytest、Vitest、Orval、OpenAPI 与接口文档校验；API governance 剩余失败为既有管理端路由缺少 decorator tags。
18. 更新 acceptance-report，核心 AC sign-off 后再 `/sprint-archive sprint-004`。

## 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0018-production-mysql-deployment/` |
| REQ | `issues/requirements/archive/REQ-0019-admin-superuser-protection/` |
| REQ | `issues/requirements/archive/REQ-0022-admin-api-docs-menu/` |
| REQ | `issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/` |
| REQ | `issues/requirements/archive/REQ-0025-brand-logo-fst-favicon/` |
| REQ | `issues/requirements/archive/REQ-0026-product-release-management/` |
| REQ | `issues/requirements/review/REQ-0024-product-usage-logging/` |
| BUG | `issues/bugs/archive/BUG-0050-user-create-validation-message-unclear/` |
| BUG | `issues/bugs/archive/BUG-0051-api-docs-swagger-ui-link-wrong/` |
| BUG | `issues/bugs/archive/BUG-0052-api-docs-metric-cards-inconsistent/` |
| BUG | `issues/bugs/archive/BUG-0053-api-docs-list-layout-pagination-inconsistent/` |
| BUG | `issues/bugs/archive/BUG-0054-admin-content-padding-too-large/` |
| BUG | `issues/bugs/archive/BUG-0055-admin-list-layout-unification/` |
| Change | `openspec/changes/add-production-mysql-deployment/` |
| Change | `update-admin-superuser-protection`（proposed） |
| Change | `fix-user-create-validation-message-unclear`（proposed） |
| Change | `openspec/changes/add-admin-api-docs-menu/` |
| Change | `openspec/changes/add-api-docs-swagger-detail-link/` |
| Change | `openspec/changes/archive/2026-07-02-add-product-release-management/` |
| Change | `openspec/changes/add-product-usage-logging/` |
| Change | `openspec/changes/fix-admin-content-padding-too-large/` |
| Change | `openspec/changes/fix-admin-list-layout-unification/` |
| Change | `openspec/changes/archive/2026-07-01-fix-api-docs-swagger-ui-link-wrong/` |
| Change | `openspec/changes/fix-api-docs-list-layout-pagination-inconsistent/` |
| Change | `openspec/changes/update-brand-logo-fst-favicon/` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-002-retrospective.md` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |
| 原型 | `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-list.png` |
| 原型 | `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-detail-drawer.png` |

## 经验复盘

- 文档：[`docs/knowledge-base/retrospectives/sprint-004-retrospective.md`](../../../docs/knowledge-base/retrospectives/sprint-004-retrospective.md)
- 生成：2026-07-04 12:34:17（`/sprint-exps sprint-004`）

## 变更记录

| 时间 | 说明 |
|---|---|
| 2026-06-29 10:03:38 | `/sprint-propose sprint-004` 创建四件套，纳入 REQ-0018 与 `add-production-mysql-deployment` |
| 2026-06-30 18:18:45 | `/sprint-propose REQ-0019 纳入 sprint-004` 追加 REQ-0019；OpenSpec Change 待 `/req-opsx` |
| 2026-06-30 18:26:33 | `/sprint-propose BUG-0050 纳入 sprint-004` 追加 BUG-0050；OpenSpec Change 待 `/bug-opsx` |
| 2026-07-01 14:04:19 | `/sprint-propose BUG-0052 纳入 sprint-004` 追加 BUG-0052；OpenSpec Change 待 `/bug-opsx` |
| 2026-07-01 14:06:33 | `/sprint-propose BUG-0053 纳入 sprint-004` 追加 BUG-0053；OpenSpec Change 待 `/bug-opsx` |
| 2026-07-01 14:06:44 | `/sprint-propose BUG-0051 纳入 sprint-004` 正式追加 BUG-0051；修复方向为 Web 层代理 Swagger，OpenSpec Change 待 `/bug-opsx` |
| 2026-06-30 18:38:37 | `/bug-opsx BUG-0050` 创建 `fix-user-create-validation-message-unclear` 并加入 sprint-004 Change 队列 |
| 2026-07-01 13:53:32 | `/sprint-propose BUG-0051 纳入 sprint-004` 评审门禁未通过，仅记入延后项（待评审），未写入 sprint.yaml / Scope / trace.iteration |
| 2026-07-01 14:03:10 | `/bug-review BUG-0051 --approve` BUG-0051 已评审通过；延后项状态更新为 approved，仍未写入 sprint.yaml / Scope / trace.iteration |
| 2026-07-01 00:28:26 | `/sprint-propose REQ-0022 纳入 sprint-004` 追加 REQ-0022；OpenSpec Change 待 `/req-opsx REQ-0022` |
| 2026-07-01 22:21:51 | `/sprint-propose REQ-0025 纳入 sprint-004` 追加 REQ-0025；OpenSpec Change 后续创建为 `update-brand-logo-fst-favicon` |
| 2026-07-02 09:17:47 | `/sprint-propose REQ-0023 纳入 sprint-004` 追加 REQ-0023；OpenSpec Change 后续创建为 `add-api-docs-swagger-detail-link` |
| 2026-07-02 09:26:53 | `/req-opsx REQ-0023` 创建 `add-api-docs-swagger-detail-link`，OpenSpec strict validate 通过 |
| 2026-07-02 10:34:20 | `/opsx-apply add-api-docs-swagger-detail-link` 完成 REQ-0023 实现与前端回归，17/17 tasks complete |
| 2026-07-02 14:44:48 | `/sprint-propose REQ-0026 纳入 sprint-004` 追加 REQ-0026；OpenSpec Change 待 `/req-opsx REQ-0026-product-release-management` |
| 2026-07-02 14:55:51 | `/req-opsx REQ-0026` 创建 `add-product-release-management`，OpenSpec strict validate 通过 |
| 2026-07-02 15:27:36 | `/opsx-apply add-product-release-management` 完成发布目录治理、模板、校验脚本、release 命令族、测试与同步 |
| 2026-07-02 15:25:19 | `/sprint-propose REQ-0024 纳入 sprint-004` 追加 REQ-0024；OpenSpec Change 后续已创建为 `add-product-usage-logging` |
| 2026-07-03 18:51:53 | `/sprint-propose BUG-0054 纳入 sprint-004` 追加 BUG-0054；OpenSpec Change 已创建为 `fix-admin-content-padding-too-large`；消耗剩余 fix_buffer |
| 2026-07-03 23:30:35 | `/sprint-propose BUG-0055 纳入 sprint-004` 追加 BUG-0055；OpenSpec Change 已创建为 `fix-admin-list-layout-unification`；fix_buffer 为 0 后超容量追加 |
| 2026-07-04 08:13:26 | `/sprint-archive sprint-004` 确认 13/13 Change 已归档，关闭 Sprint 并迁移 `iterations/change/sprint-004` → `iterations/archive/sprint-004` |
| 2026-07-04 12:34:17 | `/sprint-exps sprint-004` 生成 Sprint 经验复盘并回链知识库 |
