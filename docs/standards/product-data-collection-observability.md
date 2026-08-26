---
purpose: 通用产品数据采集与链路观测规范
content: 行为事件、API 请求日志、Task Trace、流程节点、保留周期、脱敏边界和新产品接入清单
source: REQ-0126-product-data-collection-observability-standard / add-product-data-collection-observability-standard
update_method: 数据采集、链路观测、日志审计、Task Trace 或保留周期规范变化时同步更新
created_at: 2026-08-26 10:58:47
updated_at: 2026-08-26 19:36:50
---

# 通用产品数据采集与链路观测规范

## 1. 目标

本规范用于指导新产品、新端和新模块从设计阶段接入产品数据采集与链路观测能力，确保用户行为、后端请求、任务链路和流程节点具备统一事实源、统一字段语义、统一脱敏边界和统一验收口径。

规范覆盖：

| 端 / 层 | 覆盖要求 |
|---|---|
| Web 管理端 | 采集管理端页面访问、业务点击、表单提交、日志审计查询和请求链路透传。 |
| 店主端 | 采集公开展示、搜索筛选、详情查看、收藏分享、询价等业务行为。 |
| 微信小程序 | 采集页面、组件曝光、点击、搜索、收藏、分享和业务 API 请求链路。 |
| App | 采集与 Web / 小程序等价的业务行为；离线缓存、重试和设备标识脱敏可按后续独立需求扩展。 |
| 后端 API | 所有业务 API 请求默认写入 `request_logs`，任务类请求按分级策略写入 `task_traces` 和 `task_trace_spans`。 |

如某产品、端或模块确实不适用其中某一层采集，需求、设计或 Change 验收必须记录 N/A 原因。

## 2. 四层链路模型

统一模型：

```text
usage_events
  -> request_logs
      -> task_traces
          -> task_trace_spans
```

| 层级 | 事实源 | 说明 |
|---|---|---|
| 行为事件 | `usage_events` | 记录页面访问、业务点击、搜索筛选、表单提交、保存、删除、上传、分享、收藏等可命名业务行为。 |
| 请求日志 | `request_logs` | 记录后端业务 API 请求摘要和服务端可信 `request_id`。 |
| 任务链路 | `task_traces` | 记录长耗时、多步骤、批量、异步、外部依赖或高风险操作的总体追踪。 |
| 流程节点 | `task_trace_spans` | 记录任务内部关键阶段；底层可沿用 span 命名，中文产品和管理端展示统一称为“流程节点”。 |

## 3. 两类入口

### 3.1 界面触发入口

```text
用户访问页面 / 点击业务按钮 / 搜索筛选 / 保存上传
  -> 客户端生成 behavior_trace_id
  -> 客户端生成 behavior_event_id
  -> 上报 usage_events
  -> 行为触发 API 请求携带 behavior_trace_id / behavior_event_id
  -> 后端 request_logs 保存 behavior_trace_id / parent_behavior_event_id
  -> 任务类请求：
       request_logs.request_id -> task_traces.parent_request_id
       task_traces.task_trace_id -> task_trace_spans.task_trace_id
```

规则：

- 同一次用户行为触发一个或多个 API 请求时，共享同一个 `behavior_trace_id`。
- `behavior_event_id` 标识单条行为事件。
- `parent_behavior_event_id` 记录请求来源行为事件，用于从请求日志回指行为事件。
- `request_id` 由后端生成，是服务端可信单次 HTTP 请求 ID。
- 行为采集失败不得阻断主业务流程。

### 3.2 直接 API 调用入口

```text
外部系统 / 脚本 / API 客户端 / 后台服务调用业务 API
  -> 不伪造 usage_events
  -> request_logs 记录服务端 request_id
  -> behavior_trace_id 允许为空
  -> 任务类请求：
       request_logs.request_id -> task_traces.parent_request_id
       task_traces.task_trace_id -> task_trace_spans.task_trace_id
```

规则：

- 直接 API 调用不要求存在 `usage_events`。
- 直接 API 调用允许 `behavior_trace_id` 和 `parent_behavior_event_id` 为空。
- 直接 API 调用仍必须能通过 `request_id` 进入任务链路和流程节点。

## 4. 字段语义与可信边界

| 字段 | 生成方 | 语义 | 可信边界 |
|---|---|---|---|
| `behavior_trace_id` | 客户端 helper / SDK | 一次用户行为链路，可关联同一行为触发的一个或多个 API 请求。 | 客户端字段，仅用于链路归因和排障；不得作为认证、授权、审计身份或租户隔离依据。 |
| `behavior_event_id` | 客户端 helper / SDK | 单条行为事件 ID。 | 客户端字段，必须校验长度、字符集和格式。 |
| `parent_behavior_event_id` | 后端从请求头或请求上下文提取 | 请求来源行为事件 ID。 | 仅用于回指行为事件；缺失时允许为空。 |
| `request_id` | 后端 | 服务端可信单次 HTTP 请求 ID。 | 可信请求日志主追踪 ID；客户端传入值不得覆盖。 |
| `client_request_id` | 客户端 | 客户端侧请求标识，用于跨端排障辅助。 | 不得作为认证、授权、审计身份或租户隔离依据。 |
| `task_trace_id` | 后端 Task Trace helper | 任务链路 ID，串联任务摘要和流程节点。 | 后端生成或由后端校验后接受；不得信任未校验客户端值。 |

所有客户端传入链路字段必须做长度、字符集和格式校验。非法、超长或含敏感值的字段应被忽略或返回文档化错误。

## 5. 标准数据结构

本规范定义跨产品最小标准字段。具体产品可以在不改变字段语义、关联关系、脱敏边界和保留周期的前提下扩展字段；物理类型、分区、归档表、枚举实现和索引名称由产品对应 SQLite / MySQL schema、迁移和数据库设计文档落地。

### 5.1 `usage_events`

`usage_events` 记录用户在客户端产生的可命名业务行为事件。

| 字段 | 中文注释 | 必填 | 可空 | 生成方 | 关联 / 用途 | 脱敏边界 |
|---|---|---|---|---|---|---|
| `id` | 行为事件内部主键 | 是 | 否 | 后端或数据层 | 行级唯一标识；不得作为跨系统链路 ID。 | 不含敏感信息。 |
| `behavior_trace_id` | 行为链路 ID，表示一次用户行为链路 | 是 | 否 | 客户端 helper / SDK | 同一次用户行为触发一个或多个 API 请求时复用；关联 `request_logs.behavior_trace_id`。 | 客户端字段，仅用于归因和排障。 |
| `behavior_event_id` | 单条行为事件 ID | 是 | 否 | 客户端 helper / SDK | 单条行为事件唯一标识；被 `request_logs.parent_behavior_event_id` 回指。 | 必须校验长度、字符集和格式。 |
| `event_name` | 稳定事件名 | 是 | 否 | 客户端事件字典 | 用于跨产品统计、漏斗和审计查询；不得使用临时文案或按钮标题直接拼接。 | 不包含用户输入原文。 |
| `event_category` | 行为分类 | 是 | 否 | 客户端事件字典 | 建议使用 `page`、`click`、`search`、`filter`、`form`、`upload`、`share`、`favorite`、`auth` 等稳定分类。 | 不含敏感信息。 |
| `client_type` | 客户端类型 | 是 | 否 | 客户端 / 后端归一化 | 建议枚举为 `web_admin`、`web_catalog`、`wechat_miniapp`、`app`、`backend` 或 `unknown`。 | 不含敏感信息。 |
| `page_path` | 页面路径 | 否 | 是 | 客户端 | 页面访问、点击、表单等行为的页面来源。 | 查询参数必须脱敏或截断。 |
| `page_code` | 页面稳定编码 | 否 | 是 | 客户端事件字典 | 跨端页面归一化统计；适用于小程序页面、App 页面或 Web 路由。 | 不含敏感信息。 |
| `session_id` | 会话或匿名会话标识 | 否 | 是 | 客户端 / 后端会话层 | 用于匿名访问归因、会话级排障和去重。 | 必须是脱敏或不可逆标识。 |
| `actor_user_id` | 操作者用户 ID | 否 | 是 | 后端鉴权上下文或客户端已知上下文 | 登录用户行为归因；匿名访问允许为空。 | 不存手机号、邮箱、姓名等直接 PII。 |
| `actor_role` | 操作者角色 | 否 | 是 | 后端鉴权上下文或客户端已知上下文 | 区分管理端、店主端、游客等角色。 | 不含敏感信息。 |
| `properties` | 行为属性摘要 | 否 | 是 | 客户端，上报后由后端过滤 | 记录业务对象类型、筛选条件摘要、结果数量等已脱敏 JSON。 | 禁止完整请求体、密码、Token、真实客户敏感数据。 |
| `result` | 行为结果 | 否 | 是 | 客户端或后端上报接口 | 建议枚举为 `success`、`failed`、`ignored`、`unknown`。 | 错误摘要必须脱敏。 |
| `created_at` | 行为发生时间 | 是 | 否 | 客户端采集时间或后端接收时间 | 行为时间线、保留周期和审计排序。 | 不含敏感信息。 |

建议索引：`(behavior_trace_id, created_at)`、`(behavior_event_id)`、`(event_name, created_at)`、`(client_type, created_at)`、`(actor_user_id, created_at)`。`behavior_event_id` 在同一产品数据域内应保持唯一或可通过唯一约束去重。

### 5.2 `request_logs`

`request_logs` 记录后端业务 API 请求摘要。所有业务 API 请求默认必须写入该表；可排除项见本规范 API 请求日志覆盖章节。

| 字段 | 中文注释 | 必填 | 可空 | 生成方 | 关联 / 用途 | 脱敏边界 |
|---|---|---|---|---|---|---|
| `id` | 请求日志内部主键 | 是 | 否 | 后端或数据层 | 行级唯一标识；不得替代 `request_id`。 | 不含敏感信息。 |
| `request_id` | 服务端可信单次 HTTP 请求 ID | 是 | 否 | 后端 request log middleware | 请求日志主追踪 ID；关联 `task_traces.parent_request_id`。 | 客户端传入值不得覆盖。 |
| `behavior_trace_id` | 来源行为链路 ID | 否 | 是 | 后端从请求头或上下文提取 | 界面触发入口用于关联 `usage_events.behavior_trace_id`；直接 API 调用允许为空。 | 客户端字段，仅用于归因和排障。 |
| `parent_behavior_event_id` | 来源行为事件 ID | 否 | 是 | 后端从请求头或上下文提取 | 回指 `usage_events.behavior_event_id`；一条行为事件可触发多个请求。 | 客户端字段，必须校验后保存。 |
| `client_request_id` | 客户端请求 ID | 否 | 是 | 客户端请求封装 | 辅助定位客户端重试、并发请求和网络问题；不得作为服务端可信 ID。 | 客户端字段，必须校验后保存。 |
| `method` | HTTP 方法 | 是 | 否 | 后端 middleware | 请求维度统计和排障。 | 不含敏感信息。 |
| `path` | 请求路径 | 是 | 否 | 后端 middleware | 原始路径摘要；用于日志审计查询。 | 查询参数必须脱敏或截断。 |
| `route_template` | 路由模板 | 否 | 是 | 后端路由层 | 归一化统计，例如 `/api/v1/products/{id}`。 | 不含敏感信息。 |
| `status_code` | HTTP 状态码 | 是 | 否 | 后端 middleware | 成功率、错误率和审计查询。 | 不含敏感信息。 |
| `result` | 请求结果 | 是 | 否 | 后端 middleware | 建议枚举为 `success`、`failed`、`error`、`cancelled`。 | 错误摘要必须脱敏。 |
| `duration_ms` | 请求耗时毫秒 | 是 | 否 | 后端 middleware | 性能分析和慢请求定位。 | 不含敏感信息。 |
| `client_type` | 调用端类型 | 是 | 否 | 请求头、鉴权上下文或后端归一化 | 区分 Web 管理端、店主端、小程序、App、后台服务和未知调用方。 | 不含敏感信息。 |
| `actor_user_id` | 操作者用户 ID | 否 | 是 | 后端鉴权上下文 | 已登录请求归因；系统调用或匿名请求允许为空。 | 不存手机号、邮箱、姓名等直接 PII。 |
| `actor_role` | 操作者角色 | 否 | 是 | 后端鉴权上下文 | 权限侧排障和审计查询。 | 不含敏感信息。 |
| `resource_type` | 业务资源类型 | 否 | 是 | 业务路由或服务层 | 例如 `tile`、`brand`、`upload`、`profile`。 | 不含敏感信息。 |
| `resource_id` | 业务资源 ID | 否 | 是 | 业务路由或服务层 | 精准定位单个业务对象相关请求。 | 不存对象存储完整 key 或敏感业务编号原文。 |
| `metadata` | 请求 / 响应脱敏摘要 | 否 | 是 | 后端脱敏 helper | 保存错误码、摘要、分页、对象类型、结果数量等安全 JSON。 | 禁止 Authorization、Cookie、Token、完整请求体、完整响应体。 |
| `created_at` | 请求开始或接收时间 | 是 | 否 | 后端 middleware | 时间线、保留周期和审计排序。 | 不含敏感信息。 |

建议索引：`(request_id)` 唯一或高选择性索引、`(behavior_trace_id, created_at)`、`(parent_behavior_event_id)`、`(client_request_id)`、`(route_template, created_at)`、`(status_code, created_at)`、`(client_type, created_at)`、`(actor_user_id, created_at)`。

### 5.3 `task_traces`

`task_traces` 记录任务类请求或后台任务的总体链路。是否接入 Task Trace 按本规范分级覆盖策略判断。

| 字段 | 中文注释 | 必填 | 可空 | 生成方 | 关联 / 用途 | 脱敏边界 |
|---|---|---|---|---|---|---|
| `id` | 任务链路内部主键 | 是 | 否 | 后端或数据层 | 行级唯一标识；不得替代 `task_trace_id`。 | 不含敏感信息。 |
| `task_trace_id` | 任务链路 ID | 是 | 否 | 后端 Task Trace helper | 任务链路主追踪 ID；关联 `task_trace_spans.task_trace_id`。 | 后端生成或后端校验后接受。 |
| `parent_request_id` | 来源请求 ID | 否 | 是 | 后端 Task Trace helper | 关联 `request_logs.request_id`；后台定时任务无来源 HTTP 请求时允许为空。 | 不含敏感信息。 |
| `task_type` | 任务类型 | 是 | 否 | 后端 Task Trace helper | 例如 `upload`、`import`、`export`、`batch_update`、`external_sync`。 | 不含敏感信息。 |
| `task_name` | 任务名称 | 是 | 否 | 后端 Task Trace helper | 人读任务名称；用于日志审计页和排障入口展示。 | 不使用用户输入原文直接拼接。 |
| `status` | 任务状态 | 是 | 否 | 后端 Task Trace helper | 建议枚举为 `running`、`success`、`failed`、`cancelled`、`timeout`。 | 不含敏感信息。 |
| `started_at` | 任务开始时间 | 是 | 否 | 后端 Task Trace helper | 任务时间线和耗时计算。 | 不含敏感信息。 |
| `finished_at` | 任务结束时间 | 否 | 是 | 后端 Task Trace helper | 任务完成、失败或取消时间；运行中允许为空。 | 不含敏感信息。 |
| `duration_ms` | 任务总耗时毫秒 | 否 | 是 | 后端 Task Trace helper | 性能分析；运行中可为空。 | 不含敏感信息。 |
| `actor_user_id` | 操作者用户 ID | 否 | 是 | 后端鉴权上下文 | 用户触发任务归因；系统任务允许为空。 | 不存手机号、邮箱、姓名等直接 PII。 |
| `client_type` | 任务来源端类型 | 否 | 是 | 请求上下文或任务上下文 | 区分界面触发、直接 API、后台服务或定时任务。 | 不含敏感信息。 |
| `metadata` | 任务脱敏摘要 | 否 | 是 | 后端 Task Trace helper | 保存任务参数摘要、资源数量、对象类型、批次号等安全 JSON。 | 禁止完整 payload、真实密钥、完整对象 key、真实客户敏感数据。 |
| `error_code` | 错误码 | 否 | 是 | 后端 Task Trace helper | 失败归因和节点联动。 | 不含敏感信息。 |
| `error_message` | 脱敏错误摘要 | 否 | 是 | 后端 Task Trace helper | 人读失败原因摘要。 | 必须脱敏和截断，不保存堆栈全文或本机路径。 |
| `created_at` | 记录创建时间 | 是 | 否 | 后端或数据层 | 保留周期和审计排序。 | 不含敏感信息。 |

建议索引：`(task_trace_id)` 唯一或高选择性索引、`(parent_request_id)`、`(task_type, status, created_at)`、`(actor_user_id, created_at)`。

### 5.4 `task_trace_spans`

`task_trace_spans` 记录任务内部流程节点。底层字段可继续使用 `span` 命名；面向中文产品、管理端和验收表达统一称为“流程节点”。

| 字段 | 中文注释 | 必填 | 可空 | 生成方 | 关联 / 用途 | 脱敏边界 |
|---|---|---|---|---|---|---|
| `id` | 流程节点内部主键 | 是 | 否 | 后端或数据层 | 行级唯一标识；不得替代 `span_id`。 | 不含敏感信息。 |
| `task_trace_id` | 所属任务链路 ID | 是 | 否 | 后端 Task Trace helper | 关联 `task_traces.task_trace_id`。 | 不含敏感信息。 |
| `span_id` | 流程节点 ID | 是 | 否 | 后端 Task Trace helper | 单个流程节点追踪 ID。 | 不含敏感信息。 |
| `parent_span_id` | 父流程节点 ID | 否 | 是 | 后端 Task Trace helper | 支持嵌套节点或子步骤；无父节点时为空。 | 不含敏感信息。 |
| `span_name` | 流程节点稳定名称 | 是 | 否 | 后端 Task Trace helper | 机器可读节点名，例如 `file_read`、`thumbnail_generate`、`external_sync`。 | 不使用用户输入原文直接拼接。 |
| `node_label` | 流程节点中文展示名 | 否 | 是 | 后端 Task Trace helper 或展示层映射 | 管理端或审计页展示，例如“读取文件”“生成缩略图”。 | 不含敏感信息。 |
| `sequence` | 节点顺序 | 是 | 否 | 后端 Task Trace helper | 同一任务内排序和流程还原。 | 不含敏感信息。 |
| `status` | 节点状态 | 是 | 否 | 后端 Task Trace helper | 建议枚举为 `running`、`success`、`failed`、`skipped`、`cancelled`、`timeout`。 | 不含敏感信息。 |
| `started_at` | 节点开始时间 | 是 | 否 | 后端 Task Trace helper | 节点时间线和耗时计算。 | 不含敏感信息。 |
| `finished_at` | 节点结束时间 | 否 | 是 | 后端 Task Trace helper | 节点完成、失败或跳过时间；运行中允许为空。 | 不含敏感信息。 |
| `duration_ms` | 节点耗时毫秒 | 否 | 是 | 后端 Task Trace helper | 定位慢节点和失败阶段。 | 不含敏感信息。 |
| `metadata` | 节点脱敏摘要 | 否 | 是 | 后端 Task Trace helper | 保存节点输入输出摘要、数量、对象类型、外部调用摘要等安全 JSON。 | 禁止完整 payload、真实密钥、完整对象 key、堆栈全文和本机路径。 |
| `error_code` | 节点错误码 | 否 | 是 | 后端 Task Trace helper | 节点失败归因和筛选。 | 不含敏感信息。 |
| `error_message` | 节点脱敏错误摘要 | 否 | 是 | 后端 Task Trace helper | 人读节点失败原因摘要。 | 必须脱敏和截断。 |
| `created_at` | 记录创建时间 | 是 | 否 | 后端或数据层 | 保留周期和审计排序。 | 不含敏感信息。 |

建议索引：`(task_trace_id, sequence)`、`(task_trace_id, span_id)`、`(span_name, status)`、`(status, created_at)`。

### 5.5 可空与关联规则

| 场景 | 必须满足 |
|---|---|
| 界面触发 API | `usage_events.behavior_trace_id` 与 `request_logs.behavior_trace_id` 保持一致；能识别来源事件时，`request_logs.parent_behavior_event_id` 等于 `usage_events.behavior_event_id`。 |
| 一次行为触发多个 API | 多条 `request_logs` 共享同一个 `behavior_trace_id`，并可共享同一个 `parent_behavior_event_id`。 |
| 直接 API 调用 | 不伪造 `usage_events`；`request_logs.behavior_trace_id` 和 `request_logs.parent_behavior_event_id` 允许为空。 |
| 任务类请求 | `task_traces.parent_request_id` 优先记录来源 `request_logs.request_id`；直接 API 和界面触发入口都通过该字段进入任务链路。 |
| 后台定时任务 | 若无来源 HTTP 请求，`task_traces.parent_request_id` 允许为空，但必须保留 `task_trace_id`、`task_type`、`task_name` 和节点信息。 |
| 流程节点 | `task_trace_spans.task_trace_id` 必须指向 `task_traces.task_trace_id`；复杂任务可使用 `parent_span_id` 表达嵌套节点。 |

### 5.6 产品扩展规则

- 产品可以新增业务维度字段、聚合表、分区表、归档表或搜索索引，但不得改变上述标准字段语义。
- 新增字段若进入 API 请求头、查询参数、响应体、Pydantic Schema、OpenAPI 或 Orval，必须在对应 Change 中同步 API 文档和前后端测试。
- 新增或调整 DB 字段、索引、约束、迁移或保留策略，必须同步 SQLite / MySQL schema、迁移、数据库设计文档和测试。
- 任何扩展字段默认适用安全与脱敏章节；不得保存完整请求体、完整响应体、凭据、密钥、Cookie、Token、本机绝对路径或真实客户敏感数据。

## 6. 行为事件采集口径

应采集的可命名业务行为：

| 分类 | 示例 |
|---|---|
| 页面 | 页面访问、Tab 切换、入口点击、详情查看。 |
| 查询 | 搜索、筛选、排序、加载更多、结果为空。 |
| 表单 | 表单提交、保存、删除、状态切换、登录成功 / 失败。 |
| 媒体 | 上传、预览、删除、上传失败、对象读取失败。 |
| 互动 | 收藏、分享、咨询、复制、快捷入口点击。 |

可排除的 UI 噪音：

- 纯视觉 hover。
- tooltip 关闭。
- 无业务含义的布局点击。
- 重复无状态点击。
- 不改变业务状态、查询条件或导航路径的临时交互。

行为事件必须使用稳定事件字典，避免每个产品自行创造不可复用的 `event_name`。事件属性必须脱敏和截断。

## 7. API 请求日志覆盖

所有业务 API 请求必须记录 `request_logs`。

`request_logs` 至少记录：

| 字段 | 说明 |
|---|---|
| `request_id` | 后端可信请求 ID。 |
| `method` / `path` | 请求方法和路径。 |
| `status_code` / `result` | HTTP 状态和成功 / 失败结果。 |
| `duration_ms` | 请求耗时。 |
| `client_type` | `web_admin`、`web_catalog`、`wechat_miniapp`、`app`、`backend` 或 `unknown`。 |
| `actor` | 可用的操作者上下文。 |
| `created_at` | 请求时间。 |
| `metadata` | 已脱敏摘要，不保存完整请求体或响应体。 |

可排除请求：

- 健康检查。
- 静态资源。
- OpenAPI / Swagger / Redoc 文档资源。
- 预检 OPTIONS。
- 内部探活。
- 等价低价值高频请求。

排除项必须写入规范或产品实现文档。请求日志写入失败必须降级处理，不得阻断主业务响应。

## 8. Task Trace 分级覆盖

所有业务 API 都必须有 request log；Task Trace 按分级覆盖。

满足以下任一条件的接口或任务必须接入 Task Trace：

| 条件 | 示例 |
|---|---|
| 长耗时 | 大文件处理、复杂查询、批量保存。 |
| 多步骤 | 保存时同时处理主记录、关联关系、媒体、索引或外部结果。 |
| 批量 / 异步 | 批量导入、批量删除、导出、后台 worker。 |
| 外部依赖 | 对象存储、第三方服务、外部 API。 |
| 失败需定位节点 | 单条 request log 无法说明慢节点或失败阶段。 |
| 高风险写操作 | 影响关键业务数据、权限、安全、发布状态或审计。 |

普通简单写操作可以只保留 `request_logs`，但需求、设计或实现文档必须说明不接入 Task Trace 的理由。

Task Trace 写入失败必须降级处理，不得覆盖主业务错误。`metadata` 必须经过统一脱敏、截断和安全 JSON 序列化。

## 9. 数据保留周期

默认保留周期：

| 数据 | 默认周期 | 处理方式 |
|---|---:|---|
| `request_logs` 明细 | 90 天 | 超期删除或匿名化。 |
| `usage_events` 明细 | 180 天 | 超期删除或匿名化。 |
| `task_traces` / `task_trace_spans` 明细 | 90 天 | 超期删除或匿名化。 |
| 聚合数据 | 1 年 | 可用于长期趋势分析。 |

调整保留周期时，必须记录：

- 调整原因。
- 影响范围。
- 审批依据。
- 明细数据和聚合数据的差异。
- 对存储成本、排障窗口、隐私和合规的影响。

不得为了长期趋势分析无限期保留敏感明细。

## 10. 安全与脱敏

禁止采集或展示：

- Authorization。
- Cookie。
- Token。
- 密码。
- 真实密钥。
- 数据库 DSN。
- MinIO AccessKey / SecretKey。
- 完整请求体。
- 完整响应体。
- 本机绝对路径。
- 完整内部对象 key。
- 真实客户敏感数据。

前端脱敏只能作为展示优化。后端在持久化前执行敏感字段过滤、长度截断和安全 JSON 序列化，才是安全边界。

采集字段不得放宽管理端、店主端、小程序、App 或后端 API 的权限边界。

## 11. 新产品接入清单

| 项 | 要求 |
|---|---|
| 行为事件字典 | 定义事件名、分类、必填属性、可选属性、禁止属性和 N/A 项。 |
| 前端 helper / SDK | 统一生成 `behavior_trace_id`、`behavior_event_id`，并在行为触发请求中透传。 |
| 后端 request log middleware | 统一生成 `request_id`，记录请求摘要、耗时、状态、客户端和脱敏 metadata。 |
| Task Trace helper | 通过封装写 `task_traces` 和 `task_trace_spans`，避免路由层直接拼 SQL。 |
| 标准数据结构 | 对照 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 最小标准字段，记录产品扩展字段、N/A 项和索引取舍。 |
| 直接 API 兼容 | `behavior_trace_id` 可空，不伪造 `usage_events`，从 `request_id` 进入任务链路。 |
| 脱敏 helper | 后端统一过滤敏感字段、截断长字段、安全序列化 JSON。 |
| DB / migration | 字段和索引变化同步 SQLite / MySQL schema、迁移、数据库设计文档和测试。 |
| API / Orval | 请求头、查询参数、响应字段或错误码变化同步 OpenAPI、Orval、API 文档和前后端测试。 |
| 保留周期 | 记录默认周期、超期删除或匿名化方式、周期调整审批依据。 |
| 验收 | 覆盖行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期和旧数据兼容。 |

## 12. 后续 Change 引用规则

后续以下类型需求、BUG 或 Change 应引用本规范：

- 观测类。
- 日志审计类。
- 行为埋点类。
- 上传、导入导出、批量处理类。
- 跨端请求封装类。
- Task Trace 或流程节点扩展类。

引用时必须说明：

- 哪些层级适用。
- 是否遵守标准数据结构最小字段、可空规则和索引建议。
- 哪些层级 N/A 及原因。
- 是否影响 API、DB、OpenAPI、Orval、Web、小程序、App 或测试。
- 是否需要新增或修改保留周期。
- 是否涉及敏感字段和脱敏验证。

## 13. 验证命令

规范文档和索引引用校验：

```bash
python scripts/validate-product-data-observability-standard.py
```

相关治理校验：

```bash
python scripts/validate-openspec-language.py
openspec validate add-product-data-collection-observability-standard --strict
```

## 14. 相关事实源

- `issues/requirements/review/REQ-0126-product-data-collection-observability-standard/`
- `openspec/changes/add-product-data-collection-observability-standard/`
- `docs/standards/task-trace-coverage.md`
- `docs/standards/api-governance.md`
- `docs/04-database-design.md`
- `openspec/specs/product-usage-logging/spec.md`
