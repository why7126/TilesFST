---
requirement_id: REQ-0126-product-data-collection-observability-standard
title: 建立通用产品数据采集与链路观测规范
terminal: multi
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0124-log-audit-behavior-trace-model
created_at: 2026-08-26 10:02:25
updated_at: 2026-08-26 11:02:04
related_change: add-product-data-collection-observability-standard
---

# REQ-0126 建立通用产品数据采集与链路观测规范

## 1. 需求背景

REQ-0124 已在本项目中落地日志审计行为链路模型，将产品行为事件、后端接口请求、任务链路和流程节点串联为统一排障链路：

```text
用户行为事件 -> API 请求日志 -> 任务链路 -> 流程节点
```

该模型解决了“一次用户行为触发一个或多个 API 请求”与“直接 API 调用没有界面行为上下文”并存时的追踪问题。但目前它仍是本项目内的一次实现，尚未沉淀为可复用的跨产品规范。后续新产品或新端如果在开发时没有统一采集标准，就会重新讨论字段命名、请求日志覆盖、行为事件口径、Task Trace 接入条件、数据脱敏、保留周期和验收方式，容易产生重复设计和不一致实现。

本需求要求建立“通用产品数据采集与链路观测规范”，让小程序、店主端、App、Web 管理端和后端 API 从开发阶段开始按统一模型接入采集与观测能力。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 产品负责人 | 在产品设计阶段明确哪些行为、请求和任务必须采集，保证后续分析和排障有事实源。 |
| 研发负责人 | 为新产品和新模块提供统一接入规范，减少每个项目重复设计埋点、日志和 trace。 |
| 前端 / 小程序 / App 开发 | 明确行为事件、链路 ID、请求头透传、离线或失败场景的接入边界。 |
| 后端开发 | 明确所有 API 请求日志、直接 API 调用、Task Trace 分级覆盖和脱敏策略。 |
| QA / 验收人员 | 用统一验收清单检查行为事件、请求日志、任务链路、流程节点和保留周期。 |
| 运维 / 排障人员 | 能通过 `behavior_trace_id`、`request_id`、`task_trace_id` 定位用户行为、请求和任务失败节点。 |

## 3. 需求目标

- 建立通用产品数据采集与链路观测规范 v1。
- 规范覆盖小程序、店主端、App、Web 管理端和后端 API。
- 明确所有业务 API 请求必须记录 `request_logs`，并定义低价值高频请求的排除项。
- 明确用户行为事件采集口径，支持“所有可命名业务行为必须采集，纯 UI 噪音可排除”。
- 明确四层链路模型：`usage_events -> request_logs -> task_traces -> task_trace_spans`。
- 明确直接 API 调用不伪造行为事件，允许 `behavior_trace_id` 为空。
- 明确 Task Trace 分级覆盖策略。
- 明确默认数据保留周期和超期删除 / 匿名化原则。
- 明确敏感字段脱敏、禁止采集字段、OpenAPI / Orval / DB / 测试同步要求。
- 形成新产品开发阶段可执行的接入清单和验收门禁。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 通用规范正文 | 建立产品数据采集与链路观测标准，定义适用端、采集层级、字段语义和接入边界。 |
| 全端覆盖口径 | 覆盖 Web 管理端、店主端、小程序、App 和后端 API。 |
| API 请求日志标准 | 明确所有业务 API 请求 MUST 写入 `request_logs`，并列出可排除请求。 |
| 行为事件采集标准 | 明确页面访问、业务点击、搜索、筛选、详情、保存、删除、上传、分享、收藏等行为事件采集口径。 |
| 链路 ID 标准 | 规范 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`client_request_id`、`task_trace_id` 的语义和可信边界。 |
| Task Trace 分级覆盖 | 定义哪些接口 MUST 接入 Task Trace，哪些接口 MAY 只保留 request log。 |
| 数据保留周期 | 明确 `request_logs` 90 天、`usage_events` 明细 180 天、`task_traces/task_trace_spans` 90 天、聚合数据 1 年的默认周期。 |
| 安全与脱敏 | 明确禁止采集和禁止展示的敏感字段、请求体、响应体、Header、Cookie、Token、密钥、本机路径和客户敏感数据。 |
| 新产品接入清单 | 明确前端 helper、后端 middleware、DB migration、OpenAPI/Orval、测试模板、脱敏 helper 和验收清单。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 接入外部 APM / OpenTelemetry | 本规范不替代分布式追踪平台，也不要求本期接入第三方观测系统。 |
| 第三方埋点平台适配 | 不接入第三方数据平台、用户画像或复杂 BI。 |
| 实时告警和大屏 | 不建设实时告警、BI 大屏、漏斗分析或运营分析页面。 |
| 历史数据强制回填 | 不要求对历史日志批量补齐 `behavior_trace_id` 或 Task Trace。 |
| 具体业务页面实现 | 本需求沉淀规范，不直接新增某个业务页面或业务接口。 |
| 立即改造所有历史产品 | 后续产品或存量模块按 Sprint / Change 分批接入。 |

## 5. 核心概念

### 5.1 产品行为事件

产品行为事件指用户在界面上产生的可命名业务行为，例如页面访问、按钮点击、搜索、筛选、详情查看、保存、删除、上传、分享和收藏。行为事件由 `usage_events` 记录，并通过 `behavior_trace_id` 关联该行为触发的请求。

### 5.2 API 请求日志

API 请求日志指后端对每次业务 API 请求记录的结构化日志，由 `request_logs` 承载。`request_id` 由后端生成，是服务端可信的单次 HTTP 请求 ID。所有业务 API 请求默认必须写入 `request_logs`。

### 5.3 任务链路

任务链路指一个长耗时、多步骤、批量、异步、外部依赖或高风险操作的总体追踪记录，由 `task_traces` 承载。任务链路通过 `parent_request_id` 关联触发它的请求日志。

### 5.4 流程节点

流程节点指任务内部的关键阶段，由 `task_trace_spans` 承载。底层字段可沿用 span 命名，面向中文产品和管理端展示时统一称为“流程节点”。

### 5.5 直接 API 调用

直接 API 调用指不由界面行为触发的外部系统调用、脚本调用、后台服务调用或 API 客户端调用。直接 API 调用不需要伪造 `usage_events`，允许 `behavior_trace_id` 为空，并继续从 `request_logs.request_id` 进入任务链路。

## 6. 功能要求

### FR-001 规范适用范围

- 规范 MUST 覆盖 Web 管理端、店主端、小程序、App 和后端 API。
- 规范 MUST 明确每类客户端的行为事件生成、链路 ID 透传、请求日志和直接 API 调用边界。
- 规范 SHOULD 允许不同产品按自身端形态裁剪接入，但裁剪项必须记录 N/A 原因。
- 新产品或新模块在设计阶段 SHOULD 引用本规范作为数据采集与链路观测基准。
- 规范 MUST 明确本项目现有 REQ-0124 为参考实现，而不是唯一适用场景。

### FR-002 API 请求日志全量覆盖

- 所有业务 API 请求 MUST 写入 `request_logs`。
- `request_logs.request_id` MUST 由后端生成，不得被客户端传入值覆盖。
- `request_logs` MUST 至少记录 method、path、status_code、duration_ms、client_type、actor、result、created_at 和脱敏 metadata 摘要。
- 健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活和等价低价值高频请求 MAY 排除，但排除规则必须写入规范。
- 请求日志写入失败 MUST 降级处理，不得阻断主业务响应。
- 请求日志采集不得保存完整请求体、完整响应体、Authorization、Cookie、Token、真实密钥或本机绝对路径。

### FR-003 行为事件采集口径

- 规范 MUST 明确用户行为事件由 `usage_events` 或等价事实源承载。
- 页面访问、业务按钮点击、菜单切换、搜索、筛选、详情查看、表单提交、保存、删除、上传、分享、收藏、登录成功 / 失败等可命名业务行为 SHOULD 采集。
- 纯视觉交互、无业务含义的 hover、tooltip 关闭、布局点击、重复无状态点击等 UI 噪音 MAY 排除。
- 行为事件 MUST 包含事件名、客户端类型、页面路径或页面标识、会话标识、行为分类、脱敏属性和发生时间。
- 行为事件命名 SHOULD 使用稳定字典，避免每个产品自造无法复用的 `event_name`。
- 行为采集失败 MUST 不阻断主业务流程。

### FR-004 链路 ID 与可信边界

- `behavior_trace_id` MUST 表示一次用户行为链路，可关联同一次行为触发的一个或多个 API 请求。
- `behavior_event_id` MUST 表示单条行为事件。
- `parent_behavior_event_id` SHOULD 记录请求来源行为事件，方便从 request log 回指 usage event。
- `request_id` MUST 表示后端可信单次 HTTP 请求。
- `client_request_id` MAY 作为客户端排障辅助字段，但不得作为认证、授权、审计身份或租户隔离依据。
- `task_trace_id` MUST 表示任务链路，串联任务摘要和流程节点。
- 所有客户端传入的链路字段 MUST 做长度、字符集和格式校验；非法、超长或敏感值应被忽略或返回文档化错误。

### FR-005 四层链路模型

- 规范 MUST 采用统一四层模型：`usage_events -> request_logs -> task_traces -> task_trace_spans`。
- 界面触发入口 MUST 支持通过 `usage_events.behavior_trace_id` 关联同一行为下的多个 `request_logs.behavior_trace_id`。
- 任务类请求 MUST 通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`。
- 任务流程节点 MUST 通过 `task_trace_spans.task_trace_id` 关联任务链路。
- 直接 API 调用 MUST 支持 `request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans` 的链路。
- 历史数据或非界面来源缺少行为链路时，系统 MUST 兼容空值展示和查询，不得报错。

### FR-006 Task Trace 分级覆盖

- 规范 MUST 采用 Task Trace 分级覆盖策略。
- 所有 API 请求 MUST 有 request log。
- 满足以下任一条件的接口或任务 MUST 接入 Task Trace：长耗时、三步以上业务过程、批量处理、异步任务、导入导出、上传 / 对象存储、第三方服务调用、失败需定位具体节点、高风险写操作、影响关键业务数据或权限。
- 普通简单写操作 MAY 只保留 request log，除非产品或安全要求需要更细粒度追踪。
- Task Trace span 写入失败 MUST 降级，不得覆盖主业务错误。
- Task Trace metadata MUST 经过统一脱敏、截断和安全 JSON 序列化。
- 新增 Task Trace 场景 MUST 同步 API 文档、数据库文档和测试；若不新增外部 API，需记录不需要 Orval 的依据。

### FR-007 数据保留周期

- `request_logs` 明细默认保留 90 天。
- `usage_events` 明细默认保留 180 天。
- `task_traces` 与 `task_trace_spans` 明细默认保留 90 天。
- 聚合数据默认保留 1 年。
- 产品因合规、审计或业务分析需要调整保留周期时，MUST 在规范或产品实现文档中记录原因、范围和审批依据。
- 超期明细数据 MUST 删除或匿名化，不得无限期保留。
- 保留策略 MUST 区分明细数据和聚合数据，避免为了长期趋势分析而保留过多敏感明细。

### FR-008 安全、脱敏与禁止采集字段

- 采集 payload、metadata、错误摘要、请求摘要、响应摘要和流程节点摘要 MUST 使用敏感字段过滤、长度截断和安全序列化。
- 禁止采集或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO AccessKey / SecretKey、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 和真实客户敏感数据。
- IP、User-Agent、设备信息和会话信息 SHOULD 按规范脱敏或摘要化。
- 前端脱敏只能作为展示优化，后端脱敏 MUST 作为安全边界。
- 采集字段不得放宽管理端、店主端、小程序或 App 的权限边界。
- 规范 SHOULD 明确数据采集对用户隐私披露、内部审计和合规留存的影响。

### FR-009 新产品接入清单

- 规范 MUST 提供新产品接入清单。
- 前端 / 小程序 / App SHOULD 提供行为事件 helper 或 SDK，统一生成 `behavior_trace_id` 和 `behavior_event_id`。
- 后端 SHOULD 提供统一请求日志 middleware 或等价封装。
- 后端 SHOULD 提供 Task Trace helper 或等价服务，避免路由层直接拼 SQL 写 span。
- 数据库变更 MUST 同步 SQLite / MySQL schema、迁移、索引和数据库设计文档。
- API contract 变化 MUST 同步 OpenAPI、Orval、API 文档和前后端测试。
- 测试模板 SHOULD 覆盖行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期和旧数据兼容。

### FR-010 验收与治理落地

- 规范完成后 MUST 可被后续 REQ、BUG、OpenSpec Change 和 Sprint 验收引用。
- 新产品或新模块如不接入某层采集，MUST 标记 N/A 原因。
- 观测类、日志类、上传类、批量任务类需求 SHOULD 在 `req-complete` 或 OpenSpec design 阶段引用本规范。
- 规范 SHOULD 与既有 `docs/standards/task-trace-coverage.md`、`docs/standards/api-governance.md`、`docs/04-database-design.md` 和安全规范保持一致。
- 后续实现阶段 SHOULD 提供校验脚本或 checklist，降低规范只停留在文档层的风险。

## 7. UI / UE 约束

本需求本身不新增具体业务 UI，但规范应约束观测入口和日志审计类页面：

- 链路查询入口应至少支持 `behavior_trace_id`、`request_id` 和 `task_trace_id`。
- 长 ID 应使用截断、复制、tooltip/title 或详情展开，不得撑宽列表。
- 直接 API 调用、历史日志或无行为上下文记录应展示“无界面行为来源”或等价空态。
- 任务内部节点在中文界面应展示为“流程节点”，底层表结构可继续使用 span。
- 日志、观测和审计页面不得展示完整请求体、完整响应体、Header、Cookie、Authorization、Token、真实密钥、本机路径或完整内部对象 key。
- 管理端日志审计类列表应继续遵守 admin-list 一致性规范。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 标准本身不直接改表；后续实现或产品接入时可能要求 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 字段和索引符合规范。 |
| Pydantic Schema | 后续接口新增采集字段、查询参数或响应字段时需要同步。 |
| OpenAPI/Orval | 标准本身不生成 Orval；后续 API contract 变化时必须同步。 |
| Web 管理端 | 需要作为日志审计、行为采集和请求封装的标准来源。 |
| 店主端 / 小程序 / App | 需要定义行为事件 helper、链路 ID 透传和失败不阻断策略。 |
| 后端 API | 所有业务 API 请求日志、直接 API 兼容和 Task Trace 分级覆盖受规范约束。 |
| 测试 | 后续 req-complete 与 OpenSpec 阶段需补齐标准验收清单和测试模板。 |
| 数据治理 | 需要定义保留周期、超期删除 / 匿名化和敏感字段禁止清单。 |

## 9. 关联需求与现状参考

| 关联项 | 关系 |
|---|---|
| `REQ-0124-log-audit-behavior-trace-model` | 本需求来源与父需求，已在本项目落地行为链路模型。 |
| `REQ-0024-product-usage-logging` | 既有产品行为事件和请求日志基础能力。 |
| `REQ-0071-request-snapshot-logging` | 请求快照与请求摘要脱敏基础。 |
| `REQ-0073-task-trace-parent-request-model` | Task Trace 与来源请求关联基础。 |
| `REQ-0075-audit-log-task-trace-linking` | 审计日志与任务链路关联基础。 |
| `REQ-0076-observability-dashboard` | 链路观测聚合能力参考。 |
| `docs/standards/task-trace-coverage.md` | Task Trace 覆盖判定标准参考。 |
| `docs/standards/api-governance.md` | API 请求身份、OpenAPI / Orval 与契约治理参考。 |
| `rules/security.md` | 敏感信息、认证授权和安全边界参考。 |
| `rules/data-management.md` | 数据资产、运行时数据和真实客户数据边界参考。 |

## 10. 风险与待确认

| 风险 / 待确认 | 说明 |
|---|---|
| “全量点击采集”表述过宽 | 建议在后续 req-complete 中收敛为“所有可命名业务行为必须采集，纯 UI 噪音可排除”。 |
| App 离线上报 | App 端可能涉及离线缓存、重试上报、去重和设备标识脱敏，需要后续明确。 |
| 跨端 ID 格式 | 小程序、店主端、App 是否完全复用 Web 管理端 ID 格式，需要在规范中定稿。 |
| 数据保留审批 | 默认周期已确认，但不同产品是否允许上调 / 下调及审批流程仍需补齐。 |
| 聚合数据粒度 | 首版可先定义聚合数据保留 1 年，具体聚合表和粒度后续按产品分析需求扩展。 |
| 执行落地成本 | 如果没有 helper、middleware、测试模板和 checklist，规范可能难以在新产品中稳定执行。 |

## 11. 状态块

```yaml
requirement_id: REQ-0126-product-data-collection-observability-standard
status: in_sprint
priority: P1
readiness: Ready
parent_requirement: REQ-0124-log-audit-behavior-trace-model
terminal: multi
target_clients:
  web_admin: included
  web_catalog: included
  wechat_miniapp: included
  app: included
  backend_api: included
api_change_required: possible
database_change_required: possible
orval_required: conditional
prototype_required: false
next_step: /opsx-archive REQ-0126-product-data-collection-observability-standard
notes:
  - 已确认采用 Task Trace 分级覆盖。
  - 已确认默认保留周期为 request_logs 90 天、usage_events 180 天、task trace 90 天、聚合数据 1 年。
  - 首版标准不接入外部 APM、OpenTelemetry、第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。
```
openspec_changes:
  - change_id: add-product-data-collection-observability-standard
    type: add
    status: applied
