---
requirement_id: REQ-0069-upload-observability-trace-logs
title: 任务链路追踪与审计日志查看
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0024-product-usage-logging
created_at: 2026-07-25 11:42:04
updated_at: 2026-07-26 11:56:45
related_bug: BUG-0085-admin-video-upload-stuck-at-99
---

# REQ-0069 任务链路追踪与审计日志查看

## 1. 需求背景

平台已经具备基础日志审计能力：后端有 `request_logs`、`usage_events`、`audit_logs` 三类日志事实源，管理端也已有日志审计列表与详情入口，可用于按日志类型、路径、状态、操作者、`request_id` 等条件查询。

但现有日志仍主要以“单次请求”或“单个审计事件”为中心。对于图片上传、视频上传、文件上传这类长耗时、多节点任务，用户一次操作通常会跨越前端进度、API 请求、后端校验、对象存储写入、数据库落库、后处理和响应返回等多个节点。仅靠单条请求日志，很难回答：

- 用户这一次任务卡在哪个节点；
- 从前端显示 99% 到后端完成响应之间耗时多少；
- 对象存储、数据库、后处理和前端状态反馈各自耗时多少；
- 同一次业务任务产生的多条请求日志、行为事件和审计操作如何串联；
- 系统管理员是否能在审计日志中直接查看任务时间线。

`BUG-0085-admin-video-upload-stuck-at-99` 暴露了这个缺口：视频上传长时间停留在 99% 时，需要可追踪的任务链路事实源来拆解耗时。图片/视频/文件上传是本需求的首批落地样例，但真实目标是建立通用 `Task Trace` 能力，后续可扩展到导入、导出、批量处理、发布、同步等所有多节点任务。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在审计日志中查看一次业务任务的完整时间线，判断任务是否成功、失败、超时或仍在处理中。 |
| 企业内部运营人员 | 上传或执行长耗时任务后，获得可解释的状态反馈，减少重复提交和盲目等待。 |
| 开发 / 运维人员 | 基于 `task_trace_id` 定位慢节点、失败节点、错误码和关联请求，支撑生产排障。 |
| 产品负责人 | 将上传等关键任务的耗时体验纳入可观测事实源，支持后续优化优先级判断。 |
| 安全 / 审计负责人 | 在不泄露敏感字段的前提下，追溯关键任务由谁发起、何时发生、影响了哪些资源。 |

## 3. 需求目标

- 建立通用任务链路追踪模型，为一次业务任务生成 `task_trace_id`。
- 将任务节点记录为可排序、可聚合、可查询的 `task span` 或等价结构。
- 上传场景必须首批覆盖图片、视频、文件三类上传。
- 审计日志列表必须支持按 `task_trace_id` 查询相关日志。
- 审计日志详情必须能展示任务时间线、节点耗时、节点结果、关联 `request_id` 和错误码。
- 任务追踪必须复用或扩展现有日志审计能力，不另建与审计日志割裂的孤立页面。
- 日志与任务追踪数据必须遵守脱敏、权限、保留周期和最小化采集原则。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 通用 Task Trace 模型 | 定义 `task_trace_id`、`task_type`、节点/span、状态、耗时、错误码和关联资源。 |
| 上传首批落地 | 覆盖图片上传、视频上传、文件上传，能拆解前端、后端、对象存储、数据库和后处理节点。 |
| 审计日志查询扩展 | 管理端日志审计支持按 `task_trace_id` 搜索，列表项展示任务标识或任务摘要。 |
| 审计日志详情时间线 | 日志详情中展示同一任务的节点时间线、耗时、结果、关联 request_id 和失败原因。 |
| 后端结构化记录 | 在 media 模块、对象存储适配层和关键业务服务中记录任务节点。 |
| 前端任务上下文 | 管理端上传组件需要携带或接收 `task_trace_id`，并上报关键前端节点。 |
| 安全脱敏 | 任务日志不得保存密钥、Authorization、Cookie、原始本地路径、完整敏感请求体或真实客户数据。 |
| API / DB / Orval 同步 | 如新增字段、接口或表结构，必须同步 OpenAPI、Orval、数据库文档和测试。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 完整 APM 平台 | 不建设跨服务分布式追踪系统、采样策略控制台或链路拓扑大屏。 |
| 外部日志系统接入 | 不接入 ELK、OpenTelemetry Collector、云日志等外部平台。 |
| 保存完整请求体/响应体 | 仅保存脱敏摘要和必要诊断字段。 |
| 视频转码能力增强 | 可记录后处理节点，但不在本需求中新增转码、压缩、多清晰度等能力。 |
| 所有历史任务回填 | 不要求为历史日志生成 `task_trace_id`。 |
| 非管理端展示入口 | 首期只要求管理端审计日志可查看；小程序或店主端不展示任务日志。 |

## 5. 核心概念

### 5.1 task_trace_id

`task_trace_id` 表示一次用户可感知的业务任务。它可能包含一个或多个 API 请求、行为事件、审计操作和后端内部节点。

示例：

```text
task_trace_id: task_20260725_upload_video_xxx
task_type: upload_video
actor_user_id: admin-user-id
resource_type: media
resource_id: media-id
status: success | failed | timeout | cancelled | processing
started_at: 2026-07-25 11:42:04
ended_at: 2026-07-25 11:42:18
duration_ms: 14000
```

### 5.2 task span

`task span` 表示任务中的一个节点。节点必须可排序，并能表达节点耗时、结果、错误和关联请求。

示例节点：

| span_name | 说明 |
|---|---|
| `frontend_select_file` | 用户选择文件。 |
| `frontend_upload_progress` | 前端上传进度变化，可按关键节点记录。 |
| `api_receive` | 后端接收上传请求。 |
| `validate_file` | 后端校验大小、MIME Type、扩展名。 |
| `storage_put_object` | 对象存储写入。 |
| `db_create_media` | 数据库创建媒体记录。 |
| `post_process` | 封面、元数据或后处理节点；无后处理时可标为 N/A。 |
| `api_response` | 后端响应返回。 |

### 5.3 与 request_id 的关系

`request_id` 表示一次 HTTP 请求，`task_trace_id` 表示一次业务任务。一个 `task_trace_id` 可以关联多个 `request_id`；单请求任务也可以让两者一一对应。

```text
task_trace_id
├── request_id A: 上传 API
├── request_id B: 查询任务状态 API
└── usage_event: 前端完成/失败事件
```

## 6. 功能要求

### FR-001 任务追踪标识生成与透传

- 系统 MUST 为需要追踪的业务任务生成 `task_trace_id`。
- `task_trace_id` MAY 由后端生成并返回前端；如果由前端预生成，后端 MUST 校验格式并可覆盖不可信值。
- 后端 MUST 在任务相关请求日志、行为事件、审计操作和任务节点中携带同一个 `task_trace_id`。
- 前端上传组件 MUST 能在任务开始后保留 `task_trace_id`，用于进度、完成、失败等事件上报。
- `task_trace_id` MUST 不包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。

### FR-002 任务节点记录

- 系统 MUST 记录任务开始、关键节点、任务结束或失败。
- 每个节点 MUST 至少包含：`task_trace_id`、`task_type`、`span_name`、`status`、`started_at`、`ended_at` 或 `duration_ms`。
- 节点 SHOULD 包含：`request_id`、`actor_user_id`、`client_type`、`resource_type`、`resource_id`、`error_code`、`summary`、脱敏 metadata。
- 节点顺序 MUST 可稳定排序，支持按时间线展示。
- 节点记录失败不得覆盖原业务错误；若任务追踪写入失败，主业务应按可观测性降级策略继续或返回明确错误。

### FR-003 上传首批场景

- 图片、视频、文件上传 MUST 作为首批 Task Trace 场景。
- 上传任务 MUST 区分以下阶段：前端选择文件、上传开始、请求体上传完成、后端接收、文件校验、对象存储写入、数据库记录、后处理、响应返回、前端完成或失败。
- 上传任务 MUST 记录文件大小、媒体类型、业务类型、对象 key 前缀或脱敏对象标识。
- 上传任务 MUST NOT 记录原始文件名作为对象存储 key；日志中如需展示文件名，必须脱敏或截断。
- 对 `BUG-0085` 的 99% 停留场景，必须能统计“前端请求体上传完成”到“后端响应完成”之间的耗时，并定位最慢节点。
- 视频上传可记录后处理节点，但若新增转码、压缩、多清晰度或封面生成增强能力，必须另走 OpenSpec Change。

### FR-004 审计日志列表查询

- 管理端日志审计列表 MUST 支持按 `task_trace_id` 查询。
- 日志列表 SHOULD 展示任务相关摘要，例如任务类型、任务结果、耗时或是否存在慢节点。
- 现有 `path_or_request_id` 筛选可以扩展为“路径 / request_id / task_trace_id”，或新增独立 `task_trace_id` 筛选项；实现方案在 OpenSpec design 中确定。
- 列表查询 MUST 保持分页和索引友好，避免对 metadata 做无界模糊扫描成为主路径。
- 仅系统管理员可访问任务追踪查询；其他角色不得通过直链查看。

### FR-005 审计日志详情时间线

- 管理端日志详情 MUST 能展示同一 `task_trace_id` 下的任务时间线。
- 时间线 MUST 展示节点名称、开始时间、耗时、状态、错误码、关联 `request_id` 和摘要。
- 慢节点 SHOULD 有视觉或文案标识，例如“耗时最高节点”“超过慢任务阈值”。
- 详情页 MUST 支持复制 `task_trace_id` 和关联 `request_id`。
- 若某条日志没有 `task_trace_id`，详情页 MUST 保持现有日志详情能力，不显示空时间线错误。
- metadata JSON 展示必须脱敏，并对解析失败提供安全兜底。

### FR-006 任务状态与慢任务识别

- 任务状态 MUST 至少支持：`processing`、`success`、`failed`、`timeout`、`cancelled`。
- 任务最终状态 MUST 能从节点结果或显式结束事件中推导。
- 系统 SHOULD 支持慢任务阈值配置或常量，例如上传超过指定耗时即标记为 slow。
- 慢任务指标 SHOULD 纳入日志审计指标摘要，或在详情中至少展示慢节点提示。
- 任务失败 MUST 关联统一错误码；缺少错误码时必须提供失败摘要。

### FR-007 数据模型与存储

- 实现阶段 MUST 选择一种结构化存储策略，并在 OpenSpec design 中说明取舍：
  - 扩展现有 `request_logs` / `usage_events` / `audit_logs`，增加 `task_trace_id`、`task_type` 等字段；
  - 新增 `task_traces` / `task_trace_spans` 表，并与现有日志通过 `task_trace_id` 关联；
  - 组合方案：日志表保存任务摘要，span 表保存节点明细。
- 无论采用哪种方案，MUST 为 `task_trace_id`、`task_type`、`created_at` 或等价字段建立索引。
- SQLite demo 与生产 MySQL 必须保持 schema 兼容。
- 数据访问 MUST 通过 Repository 或统一服务层，不得在路由层直接拼 SQL。
- 日志保留周期 MUST 与系统设置审计策略对齐，或明确新增任务追踪保留策略。

### FR-008 API 与契约

- 若新增任务追踪查询字段或详情时间线字段，MUST 同步 OpenAPI、Orval 和前端类型。
- 日志列表接口返回结构 SHOULD 增加任务摘要字段，例如 `task_trace_id`、`task_type`、`task_status`、`task_duration_ms`。
- 日志详情接口 SHOULD 增加任务时间线字段，例如 `task_trace` 或 `task_spans`。
- 如果新增任务状态查询或任务事件上报接口，必须说明请求、响应、错误码和鉴权边界。
- 所有新增接口和字段必须使用统一 `ApiResponse` 响应结构。

### FR-009 安全与脱敏

- 任务追踪 MUST 复用现有认证与权限模型，管理端查询仅系统管理员可用。
- 日志不得保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据或完整敏感请求体。
- 上传日志不得暴露内部绝对路径、临时文件路径、对象存储真实凭证或未授权直连地址。
- metadata 必须经过统一脱敏和长度限制。
- 前端传入的 `task_trace_id`、`task_type`、`resource_id` 等字段不得作为权限判断依据。

## 7. UI 约束

- 管理端入口复用现有日志审计页面，不新增独立营销式页面。
- 日志列表筛选区应保持现有管理端列表页结构，新增 `task_trace_id` 时不得造成筛选区拥挤或移动端溢出。
- 详情抽屉中任务时间线应作为一个清晰分组，优先展示节点、耗时、状态和关联 ID。
- 按钮应使用图标或图标+文字表达复制、查看详情等操作，复制反馈不得造成页面布局位移。
- UI 必须遵守 Design System semantic token，不得直接写裸 Hex。
- 如果后续确认需要复杂时间线原型，应在 `/req-complete` 阶段补 prototype。

## 8. 关联需求与缺陷

| 类型 | ID | 关系 |
|---|---|---|
| 父需求 | `REQ-0024-product-usage-logging` | 本需求扩展现有产品使用日志与日志审计能力，增加任务链路追踪维度。 |
| 关联缺陷 | `BUG-0085-admin-video-upload-stuck-at-99` | 首批上传场景必须支撑该缺陷的耗时分析。 |
| 关联缺陷 | `BUG-0081-prod-cos-video-upload-fails` | 同属上传链路生产排障场景，后续可复用任务追踪能力。 |

## 9. 状态块

```yaml
requirement_id: REQ-0069-upload-observability-trace-logs
status: done
lifecycle_stage: plan
readiness: Partially Ready
next_command: /req-opsx REQ-0069-upload-observability-trace-logs
notes:
  - 已补齐 user-stories、business-flow、acceptance、trace 和日志详情时间线原型策略。
  - 后续 OpenSpec design 必须明确 task trace 数据模型采用扩展日志表、新增 span 表或组合方案。
  - 上传是首批验收样例，需求主体是所有多节点任务的通用 Task Trace。
```
