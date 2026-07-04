---
title: 验收标准
purpose: REQ-0024 产品使用日志与埋点验收清单
content: 功能、数据模型、API、管理端 UI、安全、事件字典与知识库横切 AC
source: AI 根据 requirement.md、user-stories.md、business-flow.md 与 best-practices 生成
update_method: PRD、事件字典、原型、OpenSpec 或 Sprint 评审变更时同步更新
owner: product
status: draft
created_at: 2026-07-02 13:04:31
updated_at: 2026-07-02 15:31:45
note: REQ-0024-product-usage-logging
---

# 验收标准

## 1. 数据采集

- [ ] AC-001 后端 MUST 在统一中间件或等价入口为 API 请求生成或透传 `request_id`。
- [ ] AC-002 API 请求日志 MUST 记录 method、path、status_code、duration_ms、actor_user_id、actor_role、client_type、request_id、created_at。
- [ ] AC-003 异常请求 MUST 记录 error_code、错误消息摘要和 request_id。
- [ ] AC-004 健康检查、静态资源、Swagger 文档、媒体直出等噪声路由 MUST 默认排除。
- [ ] AC-005 行为事件 MUST 基于 `tracking-events.md` 事件字典采集，不得随意拼接未登记的 `event_name`。
- [ ] AC-006 行为事件上报失败 MUST 不阻断用户主业务流程，并 SHOULD 记录可观测错误摘要。

## 2. 数据模型与存储

- [ ] AC-007 日志数据 MUST 存储于关系型数据库，SQLite demo 与 MySQL production 均可运行。
- [ ] AC-008 OpenSpec design MUST 明确采用扩展 `audit_logs` 或新增 `request_logs` / `usage_events` 的方案与取舍。
- [ ] AC-009 日志写入 MUST 通过 Repository 或统一数据访问层，SQL MUST 参数化。
- [ ] AC-010 常用筛选字段 MUST 建立索引或等价优化，至少覆盖 `created_at`、`log_type`、`actor_user_id`、`request_id`、`status_code`、`path`。
- [ ] AC-011 日志查询 MUST 按时间倒序分页，禁止无条件全表扫描后在内存中过滤。
- [ ] AC-012 metadata MUST 使用 JSON 或等价结构保存脱敏上下文；解析失败时列表页仍能展示基础字段。
- [ ] AC-013 MUST 明确日志保留周期和清理策略，并与系统设置审计配置保持一致或说明新增配置项。

## 3. API

- [ ] AC-014 `GET /api/v1/admin/logs` MUST 仅允许系统管理员分页查询日志列表。
- [ ] AC-015 `GET /api/v1/admin/logs/{id}` MUST 仅允许系统管理员查询单条日志详情。
- [ ] AC-016 `POST /api/v1/usage-events` MUST 校验事件名、必填属性、字段类型、字段长度与禁止字段。
- [ ] AC-017 列表接口 MUST 返回统一 `ApiResponse` 与分页结构：`items`、`total`、`page`、`page_size`。
- [ ] AC-018 参数非法 MUST 返回统一参数校验错误；日志不存在 MUST 返回 404 类错误。
- [ ] AC-019 接口新增或变更 MUST 同步 OpenAPI、`docs/03-api-index.md`、错误码文档、Orval 客户端与后端测试。

## 4. 管理端页面

- [ ] AC-020 管理端 MUST 在 SYSTEM 分组提供日志审计入口，推荐路由 `/admin/logs` 或 `/admin/audit-logs`。
- [ ] AC-021 日志列表 MUST 支持日志类型、时间范围、操作者、状态 / 结果、资源 / ID、路径 / request_id 筛选，并提供查询与重置。
- [ ] AC-022 日志列表 MUST 展示时间、类型、事件 / 摘要、操作者、客户端、状态 / 结果、耗时、request_id、复制、详情操作。
- [ ] AC-023 指标摘要 MUST 展示 `TODAY LOGS`、`API ERRORS`、`SLOW REQUESTS`、`SENSITIVE OPS` 四类卡片。
- [ ] AC-024 日志详情 MUST 使用右侧抽屉承载，展示基础信息、请求信息、操作者 / 客户端、操作上下文、埋点属性、metadata JSON 分组。
- [ ] AC-025 基础信息 MUST 包含日志 ID、日志类型、状态 / 结果、request_id、发生时间。
- [ ] AC-026 请求信息 MUST 包含 Method、Path、Status Code、Duration、Error Code，慢请求 SHOULD 在 Duration 旁标注。
- [ ] AC-027 操作者 / 客户端 MUST 包含操作者、User ID、客户端、IP 摘要、User Agent 摘要。
- [ ] AC-028 操作上下文 MUST 包含业务动作、操作摘要、失败原因或结果摘要。
- [ ] AC-029 埋点属性 MUST 包含 event_name、module、entity_type、entity_id、changed_fields。
- [ ] AC-030 metadata JSON MUST 使用等宽代码区展示，字段已脱敏且可滚动查看。
- [ ] AC-031 request_id MUST 可复制，复制成功或失败反馈 MUST 不造成页面布局位移。
- [ ] AC-032 普通员工、店主端和匿名用户直链访问日志页面或接口 MUST 返回 403 或无权限页。
- [ ] AC-033 页面 MUST 复用管理端列表页模式，优先使用 `AdminListPage`、shadcn 基础组件和既有管理端样式。

## 5. 安全与隐私

- [ ] AC-034 日志默认 MUST NOT 保存或展示密码、Token、Authorization Header、Cookie、真实密钥、MinIO AccessKey / SecretKey、数据库 DSN。
- [ ] AC-035 请求体和响应体如确需保存，MUST 使用字段白名单、敏感字段黑名单、长度截断和显式配置开关。
- [ ] AC-036 前端脱敏只能作为体验优化，敏感字段过滤 MUST 以后端为安全边界。
- [ ] AC-037 MUST 禁止提交真实日志文件、真实客户数据、运行时数据库文件。
- [ ] AC-038 店主 Web 展示端和微信小程序若纳入本期，MUST 支持匿名会话边界且不得采集敏感个人信息。

## 6. 事件字典

- [ ] AC-039 需求包 MUST 包含 `tracking-events.md`，定义事件名、事件分类、触发时机、必填属性、可选属性和禁止属性。
- [ ] AC-040 MVP MUST 至少覆盖 `page_view`、`search_submit`、`filter_change`、`entity_create`、`entity_update`、`entity_delete`、`status_change`、`media_upload`、`login_success`、`login_failed`、`api_error`。
- [ ] AC-041 后端 MUST 自动补充 user_id、role、client_type、page_path、request_id、session_id、timestamp、user_agent/ip 摘要等上下文。
- [ ] AC-042 新增事件或调整属性 MUST 先更新事件字典，再同步代码枚举、Schema、测试与 OpenSpec。

## 7. 原型验收

- [ ] AC-043 原型 MUST 包含管理端日志审计列表、筛选区、指标摘要、表格、分页和详情抽屉。
- [ ] AC-044 原型 context MUST 明确路由、导航位置、字段、空态、加载态、错误态和权限态。
- [ ] AC-045 UI 实现 MUST 以产品 v2 的 `prototype/web/log-audit-list.png` 和 `prototype/web/log-audit-detail-drawer.png` 作为 Golden Reference，并完成 1440x1024 并排验收。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 1440x1024 下日志审计列表分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 指标摘要卡 DOM MUST 使用 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`。
- [ ] AC-XCUT-003 日志查询、详情加载或复制 request_id 的成功 / 失败反馈 MUST 使用 fixed toast 或等价固定层，不得造成 hero / 表格纵向位移。
- [ ] AC-XCUT-004 N/A — 日志审计列表本期为查询页，无启停、删除、上下架等状态变更操作；若后续新增清理、删除、导出等危险操作，MUST 使用 DS confirm modal，禁止 `window.confirm`。
- [ ] AC-XCUT-005 Vitest SHOULD 覆盖日志列表分页结构 smoke / snapshot、筛选提交、详情抽屉与权限隐藏 / 403。
