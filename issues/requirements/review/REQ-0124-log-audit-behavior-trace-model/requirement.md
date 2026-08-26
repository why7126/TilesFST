---
requirement_id: REQ-0124-log-audit-behavior-trace-model
title: 日志审计补齐行为链路与任务链路采集模型
terminal: multi
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-08-25 22:24:23
updated_at: 2026-08-25 23:25:07
related_change: add-log-audit-behavior-trace-model
---

# REQ-0124 日志审计补齐行为链路与任务链路采集模型

## 1. 需求背景

当前平台已经基于 `REQ-0024-product-usage-logging` 建立了产品行为事件、接口请求日志与管理端日志审计基础能力，并通过 `REQ-0071-request-snapshot-logging`、`REQ-0073-task-trace-parent-request-model`、`REQ-0075-audit-log-task-trace-linking` 和 `REQ-0076-observability-dashboard` 逐步增强了请求快照、Task Trace、审计关联和链路观测能力。

现有模型已经能记录单次 API 请求的 `request_id`，也能通过 `task_traces.parent_request_id` 将任务型请求关联到来源请求。但用户界面行为与后端请求之间仍缺少明确的一等链路字段：一次页面访问、一次按钮点击或一次表单提交可能触发一个或多个 API 请求，当前仅靠 `request_id` 无法稳定表达“一次用户行为引发了哪些请求”。同时，直接 API 调用、外部系统调用或后台任务并不一定存在用户界面行为上下文，也需要保持从请求日志到任务流程节点的独立追踪能力。

本需求要求补齐行为链路采集模型，让日志审计能够同时支持“界面触发”和“直接 API 调用”两种入口，并将行为事件、接口请求、任务链路和任务流程节点串联为一致的排障、审计和产品分析数据模型。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 从一次用户操作快速追踪相关 API 请求、任务链路和失败节点，判断操作影响范围。 |
| 研发 / 运维人员 | 通过 `behavior_trace_id`、`request_id`、`task_trace_id` 定位慢请求、失败请求和异常任务节点。 |
| 产品负责人 | 基于用户行为事件与请求结果的关联，理解关键功能使用路径和失败分布。 |
| 企业内部运营人员 | 在授权范围内确认一次保存、上传、发布或批量操作是否成功，以及失败发生在哪个阶段。 |

## 3. 范围

### 3.1 本期包含

- 为用户行为事件建立行为链路字段，支持 `behavior_trace_id` 和 `behavior_event_id`。
- 为后端请求日志建立行为来源关联字段，支持 `behavior_trace_id` 和 `parent_behavior_event_id`。
- 前端请求封装在界面行为触发的 API 请求中统一透传 `behavior_trace_id` / `behavior_event_id`。
- 直接 API 调用保持 `behavior_trace_id` 可空，并继续以 `request_logs.request_id` 作为请求追踪入口。
- 任务类请求继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`。
- `task_trace_spans` 继续作为任务流程节点事实源，支持通过 `task_trace_id` 联动任务链路。
- 日志审计查询支持按 `behavior_trace_id`、`request_id`、`task_trace_id` 定位相关记录。
- 明确字段语义、采集边界、脱敏策略、索引建议、兼容旧日志和测试验收范围。

### 3.2 本期不包含

- 接入外部 APM、OpenTelemetry 全量分布式追踪、第三方埋点平台或日志平台。
- 运维级日志统一采集，例如 Nginx access log、容器 stdout、数据库慢查询日志。
- 默认保存完整请求体、完整响应体、Header、Cookie、Authorization、Token 或真实密钥。
- 对历史日志进行强制批量回填；历史日志应以空行为链路兼容展示。
- 建设复杂 BI、漏斗分析、实时大屏、告警推送或自动异常检测。
- 面向店主 Web 或微信小程序的完整独立分析页面；若纳入本期，仅复用同一链路字段与上报策略。

## 4. 数据采集模型

### 4.1 界面触发入口

界面触发适用于页面访问、按钮点击、搜索筛选、详情查看、表单提交、上传、发布、删除等由 Web 管理端或其他前端产生的用户行为。

```text
usage_events.behavior_trace_id
  -> request_logs.behavior_trace_id
      -> task_traces.parent_request_id
          -> task_trace_spans
```

字段语义：

| 字段 | 说明 |
|---|---|
| `behavior_trace_id` | 一次用户行为链路 ID。一次点击、一次页面访问或一次表单提交可触发多个 API 请求，这些请求共享同一个行为链路 ID。 |
| `behavior_event_id` | 一次具体行为事件 ID。用于标识 `usage_events` 中的单条行为事件，并可被请求日志通过 `parent_behavior_event_id` 引用。 |
| `parent_behavior_event_id` | 请求来源行为事件 ID。用于表达某条 `request_logs` 记录由哪条行为事件触发。 |
| `request_id` | 单次后端 HTTP 请求 ID，由后端生成，是服务端可信请求追踪 ID。 |
| `task_trace_id` | 任务链路 ID，用于串联任务摘要和任务流程节点。 |
| `span` | 任务流程节点。底层使用 `task_trace_spans` 存储，中文展示为“流程节点”。 |

### 4.2 直接 API 调用入口

直接 API 调用适用于 Postman / curl、外部系统、脚本、后端任务或无界面行为上下文的客户端请求。

```text
request_logs.request_id
  -> task_traces.parent_request_id
      -> task_trace_spans
```

直接 API 调用不需要伪造 `usage_events`。当请求缺少行为上下文时，`behavior_trace_id` 和 `parent_behavior_event_id` 可以为空；系统仍必须写入 `request_logs.request_id`，任务类请求仍通过 `task_traces.parent_request_id` 进入任务链路。

## 5. 数据结构要求

### 5.1 usage_events

产品行为事件表用于记录页面访问、按钮点击、搜索筛选、提交、上传等行为事件。

| 字段 | 说明 |
|---|---|
| `id` | 行为事件记录 ID，主键。 |
| `behavior_trace_id` | 用户行为链路 ID；一次用户行为触发多个请求时共享。 |
| `behavior_event_id` | 行为事件 ID；可由前端生成或后端生成，后续阶段确认生成方。 |
| `request_id` | 行为上报接口自身的请求 ID，保留现有语义；不得将其误用为用户行为链路 ID。 |
| `actor_user_id` | 登录用户 ID；匿名上报为空。 |
| `actor_role` | 用户角色，如 `admin`、`employee`、`store_owner`、`anonymous`。 |
| `client_type` | 客户端类型，如 `web_admin`、`web_catalog`、`wechat_miniapp`、`backend`、`unknown`。 |
| `event_name` | 事件名称，必须来自事件字典。 |
| `event_category` | 事件分类。 |
| `page_path` | 页面路径，不含敏感 query。 |
| `session_id` | 前端会话 ID，匿名场景可用。 |
| `result` | 行为结果，如 `success`、`failed`。 |
| `duration_ms` | 行为耗时，毫秒。 |
| `task_trace_id` | 行为事件关联的任务链路 ID，可为空。 |
| `task_type` | 任务类型摘要，可为空。 |
| `metadata` | 脱敏后的行为属性 JSON。 |
| `created_at` | 服务端写入时间。 |

### 5.2 request_logs

API 请求日志表用于记录所有后端接口请求，包括界面触发请求、直接 API 调用、外部系统调用和后端任务请求。

| 字段 | 说明 |
|---|---|
| `id` | 请求日志记录 ID，主键。 |
| `request_id` | 服务端可信请求 ID；每次 HTTP 请求唯一，由后端生成。 |
| `behavior_trace_id` | 用户行为链路 ID；界面行为触发的请求有值，直接 API 调用可为空。 |
| `parent_behavior_event_id` | 触发该请求的行为事件 ID。 |
| `client_request_id` | 客户端请求 ID，由前端、小程序或外部调用方生成，仅用于排障对齐。 |
| `actor_user_id` | 从鉴权上下文解析的用户 ID。 |
| `actor_role` | 用户角色。 |
| `client_type` | 客户端类型。 |
| `method` | HTTP 方法。 |
| `path` | 实际请求路径，不含 query。 |
| `route_template` | 路由模板，如 `/api/v1/admin/tile-skus/{id}`。 |
| `status_code` | HTTP 状态码。 |
| `duration_ms` | 请求耗时，毫秒。 |
| `result` | 请求结果，如 `success`、`failed`。 |
| `error_code` | 业务错误码或异常摘要码。 |
| `task_trace_id` | 如果该请求触发任务链路，则记录任务链路 ID。 |
| `task_type` | 任务类型摘要。 |
| `ip_address_masked` | 脱敏 IP。 |
| `user_agent_summary` | 截断后的 User-Agent 摘要。 |
| `summary` | 列表展示摘要。 |
| `metadata.request_snapshot` | 结构化请求快照，包含输入摘要、资源、响应、操作者与时间信息。 |
| `created_at` | 请求日志写入时间。 |

### 5.3 task_traces

任务链路表用于记录任务型接口或后台任务的总体状态。

| 字段 | 说明 |
|---|---|
| `id` | 任务记录 ID，主键。 |
| `task_trace_id` | 任务链路 ID。 |
| `parent_request_id` | 触发该任务的 HTTP 请求 ID，关联 `request_logs.request_id`。 |
| `behavior_trace_id` | 用户行为链路 ID；界面触发任务有值，直接 API / 后台任务可为空。 |
| `task_type` | 任务类型，如 `upload_image`、`sku_update`、`sku_publish`。 |
| `status` | 任务状态，如 `processing`、`success`、`failed`、`timeout`、`cancelled`、`skipped`。 |
| `actor_user_id` | 发起人 ID。 |
| `client_type` | 客户端类型。 |
| `resource_type` | 任务关联资源类型。 |
| `resource_id` | 任务关联资源 ID。 |
| `started_at` | 任务开始时间。 |
| `ended_at` | 任务结束时间。 |
| `duration_ms` | 任务总耗时。 |
| `slowest_span_name` | 最慢流程节点名称。 |
| `error_code` | 任务失败错误码。 |
| `summary` | 任务摘要。 |
| `metadata` | 脱敏后的任务上下文 JSON。 |
| `created_at` / `updated_at` | 创建和更新时间。 |

### 5.4 task_trace_spans

任务流程节点表用于记录任务内部每个处理节点，帮助定位异常发生在哪一步。

| 字段 | 说明 |
|---|---|
| `id` | 节点记录 ID，主键。 |
| `task_trace_id` | 所属任务链路 ID。 |
| `request_id` | 关联请求 ID。 |
| `behavior_trace_id` | 用户行为链路 ID，可冗余保存以便查询。 |
| `task_type` | 任务类型。 |
| `span_name` | 流程节点名称，如 `input_validate`、`storage_put_object`、`db_persist`、`api_response`。 |
| `sequence` | 节点顺序。 |
| `status` | 节点状态。 |
| `started_at` | 节点开始时间。 |
| `ended_at` | 节点结束时间。 |
| `duration_ms` | 节点耗时。 |
| `resource_type` | 节点处理资源类型。 |
| `resource_id` | 节点处理资源 ID。 |
| `error_code` | 节点失败错误码。 |
| `summary` | 节点摘要。 |
| `metadata` | 脱敏后的节点上下文 JSON。 |
| `created_at` | 创建时间。 |

## 6. 功能要求

### FR-001 行为链路字段采集

- 系统 MUST 支持在 `usage_events` 中写入 `behavior_trace_id` 与 `behavior_event_id`。
- `behavior_trace_id` MUST 表达一次用户行为链路，可被同一行为触发的多个 API 请求复用。
- `behavior_event_id` MUST 表达一条具体行为事件，可用于更精确地关联请求来源。
- `behavior_trace_id` 与 `behavior_event_id` 的生成方、格式、长度、字符集和幂等策略 MUST 在后续设计阶段明确。

### FR-002 前端请求透传

- Web 管理端 SHOULD 在页面访问、按钮点击、搜索筛选、表单提交、上传等行为中生成或复用 `behavior_trace_id`。
- 同一次用户行为触发的多个 API 请求 MUST 透传同一个 `behavior_trace_id`。
- 界面行为触发的 API 请求 SHOULD 透传 `behavior_event_id`，后端写入 `request_logs.parent_behavior_event_id`。
- 前端透传字段只能作为链路归因依据，MUST NOT 作为鉴权、权限或审计可信身份来源。

### FR-003 请求日志行为来源关联

- 后端请求日志中间件 MUST 在可用时采集 `behavior_trace_id` 与 `parent_behavior_event_id`。
- 直接 API 调用缺少行为上下文时，`behavior_trace_id` 与 `parent_behavior_event_id` MAY 为空。
- 所有可采集 API 请求仍 MUST 生成服务端可信 `request_id`，并写入 `request_logs.request_id`。
- `client_request_id` 继续用于客户端与服务端排障对齐，不得替代 `behavior_trace_id` 或 `request_id`。

### FR-004 任务链路关联

- 任务类请求 MUST 继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`。
- 当任务由界面行为触发时，`task_traces` SHOULD 同步记录 `behavior_trace_id`，便于从行为链路直接定位任务。
- `task_trace_spans` MUST 保持流程节点拆分，并通过 `task_trace_id` 关联任务链路。
- 任务流程节点 SHOULD 至少记录节点名称、顺序、状态、耗时、错误码和摘要。

### FR-005 日志审计查询与详情

- 日志审计接口 SHOULD 支持按 `behavior_trace_id` 查询相关行为事件、请求日志和任务链路。
- 日志审计接口 MUST 继续支持按 `request_id` 和 `task_trace_id` 查询。
- 日志详情 SHOULD 展示行为链路、请求链路和任务流程节点之间的关系。
- 历史日志缺少行为链路字段时，页面 MUST 以空值或未采集状态展示，不得报错。

### FR-006 直接 API 调用兼容

- 直接 API 调用不要求生成 `usage_events`。
- 直接 API 调用 MUST 能从 `request_logs.request_id` 开始追踪。
- 若直接 API 调用触发任务，系统 MUST 通过 `task_traces.parent_request_id` 与 `task_trace_spans` 完成任务链路排障。
- 外部系统或脚本调用可提供 `client_request_id`，但后端仍以 `request_id` 作为可信请求 ID。

### FR-007 安全与脱敏

- 所有 metadata MUST 采用字段白名单、敏感字段过滤、长度截断和 JSON 序列化保护。
- 系统 MUST NOT 保存密码、Token、Authorization、Cookie、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、完整请求体、完整响应体、内部绝对路径或真实客户敏感数据。
- 前端脱敏只能作为体验优化，后端脱敏与过滤才是安全边界。
- 日志审计查询与详情 MUST 保持管理端权限边界，不得对普通店主或匿名用户开放。

### FR-008 数据库与性能

- SQLite 与 MySQL schema MUST 保持字段和索引一致。
- 行为链路查询 SHOULD 建立 `behavior_trace_id` 相关索引，避免无界 metadata 模糊扫描作为主查询路径。
- `request_id`、`task_trace_id`、`parent_request_id`、`created_at` 等既有追踪和时间字段索引 MUST 保持可用。
- 大日志量场景下，列表和聚合查询 MUST 使用分页、条件下推和索引友好查询。

## 7. UI 约束

- 管理端日志审计页 MUST 复用现有管理端 Shell、列表页、筛选区、详情抽屉和 Task Trace 时间线模式。
- UI 文案可将 `task_trace_spans` 展示为“流程节点”，但底层字段继续使用 `span` 命名。
- 筛选区 SHOULD 支持 `behavior_trace_id`、`request_id`、`task_trace_id` 的查询入口；具体是独立输入框还是复用现有“路径 / request_id”搜索框，后续阶段确认。
- 详情抽屉 SHOULD 清晰展示“行为事件 -> API 请求 -> 任务链路 -> 流程节点”的关系。
- 页面不得展示敏感字段原值；脱敏字段以 `******`、`已脱敏` 或等价方式呈现。
- 空数据、历史日志无行为链路、直接 API 无行为上下文、无匹配追踪 ID 等状态 MUST 有清晰反馈。

## 8. 关联需求

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0024-product-usage-logging` | 已建立产品使用行为埋点、接口请求日志详情和管理端日志审计基础能力。 |
| 关联需求 | `REQ-0071-request-snapshot-logging` | 已增强请求日志的结构化 Request Snapshot，本需求应复用其脱敏和快照策略。 |
| 关联需求 | `REQ-0073-task-trace-parent-request-model` | 已建立 Task Trace 与主请求关联模型，本需求继续使用 `parent_request_id`。 |
| 关联需求 | `REQ-0075-audit-log-task-trace-linking` | 已补齐审计操作日志与任务链路关联，本需求应保持同一 trace 语义。 |
| 关联需求 | `REQ-0076-observability-dashboard` | 已定义日志审计与链路观测仪表，本需求补齐行为链路查询维度。 |

## 9. 状态

```yaml
requirement_id: REQ-0124-log-audit-behavior-trace-model
priority: P1
status: in_sprint
owner: product
iteration: sprint-026
openspec_change: add-log-audit-behavior-trace-model
readiness: Ready
next: /opsx-apply REQ-0124-log-audit-behavior-trace-model
```
openspec_changes:
  - change_id: add-log-audit-behavior-trace-model
    type: add
    status: applied
