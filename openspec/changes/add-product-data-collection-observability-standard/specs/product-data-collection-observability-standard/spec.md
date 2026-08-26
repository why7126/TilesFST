## ADDED Requirements

### Requirement: 通用采集规范适用范围
系统 SHALL 提供通用产品数据采集与链路观测规范，覆盖小程序、店主端、App、Web 管理端和后端 API。

#### Scenario: 新产品设计阶段引用规范
- **WHEN** 新产品或新模块进入需求、设计或 OpenSpec Change 阶段
- **THEN** 团队 SHALL 引用通用产品数据采集与链路观测规范
- **AND** 明确适用客户端、行为事件、API 请求日志、Task Trace 和数据保留策略
- **AND** 对不适用的采集层级记录 N/A 原因。

#### Scenario: 规范覆盖所有终端类型
- **WHEN** 团队阅读通用规范
- **THEN** 规范 SHALL 覆盖 Web 管理端、店主端、小程序、App 和后端 API
- **AND** SHALL 明确每类客户端的行为事件生成、链路 ID 透传、请求日志和直接 API 调用边界。

### Requirement: 行为事件采集口径
系统 SHALL 定义产品行为事件采集口径，并区分可命名业务行为和纯 UI 噪音。

#### Scenario: 采集可命名业务行为
- **WHEN** 用户在界面产生页面访问、业务按钮点击、菜单切换、搜索、筛选、详情查看、表单提交、保存、删除、上传、分享、收藏、登录成功或登录失败等可命名业务行为
- **THEN** 客户端 SHALL 按规范记录 `usage_events` 或等价行为事实源
- **AND** 行为事件 SHALL 包含事件名、客户端类型、页面路径或页面标识、会话标识、行为分类、脱敏属性和发生时间。

#### Scenario: 排除纯 UI 噪音
- **WHEN** 用户只产生纯视觉交互、无业务含义 hover、tooltip 关闭、布局点击或重复无状态点击
- **THEN** 规范 SHALL 允许产品将该类交互排除在行为事件采集之外
- **AND** 排除规则 SHALL 不影响可命名业务行为采集。

#### Scenario: 行为采集失败不阻断主流程
- **WHEN** 行为事件上报、校验或持久化失败
- **THEN** 客户端和服务端 SHALL 不阻断用户主业务流程
- **AND** 失败处理 SHALL 不泄露敏感字段。

### Requirement: API 请求日志全量覆盖
系统 SHALL 要求所有业务 API 请求记录 `request_logs`，并定义可排除的低价值高频请求。

#### Scenario: 业务 API 请求写入 request_logs
- **WHEN** 后端收到业务 API 请求
- **THEN** 系统 SHALL 记录 `request_logs`
- **AND** `request_id` SHALL 由后端生成并作为服务端可信单次 HTTP 请求 ID
- **AND** 日志 SHALL 至少记录 method、path、status_code、duration_ms、client_type、actor、result、created_at 和脱敏 metadata 摘要。

#### Scenario: 排除低价值高频请求
- **WHEN** 请求目标为健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活或等价低价值高频请求
- **THEN** 规范 SHALL 允许将该请求排除在默认 `request_logs` 采集之外
- **AND** 排除项 SHALL 在规范或产品实现文档中明确记录。

#### Scenario: 请求日志写入失败降级
- **WHEN** `request_logs` 写入失败
- **THEN** 系统 SHALL 降级处理
- **AND** SHALL NOT 用日志写入失败覆盖或阻断主业务响应。

### Requirement: 链路 ID 与两类入口
系统 SHALL 定义 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`client_request_id` 和 `task_trace_id` 的语义、生成方和可信边界。

#### Scenario: 界面触发入口串联行为与请求
- **WHEN** 一个用户行为触发一个或多个 API 请求
- **THEN** 客户端 SHALL 为该行为链路生成或复用 `behavior_trace_id`
- **AND** 单条行为事件 SHALL 使用 `behavior_event_id`
- **AND** 行为触发的 API 请求 SHALL 透传 `behavior_trace_id` 和可用的 `behavior_event_id`
- **AND** 后端 `request_logs` SHALL 记录 `behavior_trace_id` 与 `parent_behavior_event_id` 或等价来源行为字段。

#### Scenario: 直接 API 调用不伪造行为事件
- **WHEN** 外部系统、脚本、API 客户端或后台服务直接调用业务 API
- **THEN** 系统 SHALL 不要求伪造 `usage_events`
- **AND** `behavior_trace_id` SHALL 允许为空
- **AND** 排障 SHALL 从 `request_logs.request_id` 进入后续任务链路。

#### Scenario: 客户端链路字段不可作为安全边界
- **WHEN** 客户端传入 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id` 或 `client_request_id`
- **THEN** 后端 SHALL 校验长度、字符集和格式
- **AND** 非法、超长或敏感值 SHALL 被忽略或返回文档化错误
- **AND** 这些字段 SHALL NOT 作为认证、授权、审计身份或租户隔离依据。

### Requirement: 四层链路模型
系统 SHALL 采用 `usage_events -> request_logs -> task_traces -> task_trace_spans` 四层链路模型。

#### Scenario: 行为触发任务链路
- **WHEN** 界面行为触发 API 请求且该请求产生任务
- **THEN** 系统 SHALL 支持通过 `usage_events.behavior_trace_id` 关联 `request_logs.behavior_trace_id`
- **AND** SHALL 通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`
- **AND** SHALL 通过 `task_trace_spans.task_trace_id` 关联任务流程节点。

#### Scenario: 直接 API 进入任务链路
- **WHEN** 直接 API 调用触发任务
- **THEN** 系统 SHALL 支持 `request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans` 的排障链路
- **AND** SHALL 在 `behavior_trace_id` 为空时兼容展示和查询。

### Requirement: 标准数据结构
系统 SHALL 在通用产品数据采集与链路观测规范中定义 `usage_events`、`request_logs`、`task_traces` 和 `task_trace_spans` 的最小标准字段、中文注释、可空规则、生成方、关联关系、索引建议和脱敏边界。

#### Scenario: 数据结构作为规范组成部分
- **WHEN** 团队阅读或引用通用采集规范
- **THEN** 规范 SHALL 提供 `usage_events`、`request_logs`、`task_traces` 和 `task_trace_spans` 的字段级结构说明
- **AND** 每类字段 SHALL 说明中文注释、必填性、可空性、生成方、关联或用途和脱敏边界
- **AND** 规范 SHALL 说明这些字段是跨产品最小标准字段，具体产品可以在不改变字段语义和安全边界的前提下扩展。

#### Scenario: 链路字段可空和关联规则清晰
- **WHEN** 界面触发 API、直接 API 调用、任务类请求或后台定时任务进入采集链路
- **THEN** 规范 SHALL 明确 `behavior_trace_id`、`parent_behavior_event_id`、`parent_request_id` 和 `task_trace_id` 的可空规则和关联关系
- **AND** 直接 API 调用 SHALL NOT 因缺少行为事件而伪造 `usage_events`
- **AND** 任务类请求 SHALL 优先通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`。

#### Scenario: 索引和实现扩展边界清晰
- **WHEN** 产品落地采集表、迁移或数据库设计文档
- **THEN** 规范 SHALL 提供关键查询维度的索引建议
- **AND** 产品 SHALL 在对应 Change 中同步 SQLite / MySQL schema、迁移、数据库设计文档和测试
- **AND** 物理类型、分区、归档表、枚举实现和索引名称 MAY 由产品实现自行确定。

### Requirement: Task Trace 分级覆盖
系统 SHALL 对 Task Trace 采用分级覆盖策略。

#### Scenario: 高价值任务必须接入 Task Trace
- **WHEN** 接口或任务满足长耗时、三步以上业务过程、批量处理、异步任务、导入导出、上传或对象存储、第三方服务调用、失败需定位具体节点、高风险写操作、影响关键业务数据或权限中的任一条件
- **THEN** 该接口或任务 SHALL 接入 `task_traces`
- **AND** 关键流程节点 SHALL 写入 `task_trace_spans`。

#### Scenario: 普通简单写操作可只保留请求日志
- **WHEN** 接口是普通简单写操作且不满足强制 Task Trace 条件
- **THEN** 规范 SHALL 允许该接口只保留 `request_logs`
- **AND** 需求、设计或实现文档 SHALL 说明不接入 Task Trace 的理由。

#### Scenario: Task Trace 写入失败降级
- **WHEN** `task_traces` 或 `task_trace_spans` 写入失败
- **THEN** 系统 SHALL 降级处理
- **AND** SHALL NOT 覆盖主业务错误。

### Requirement: 数据保留周期
系统 SHALL 定义日志、行为事件、任务链路和聚合数据的默认保留周期。

#### Scenario: 默认保留周期生效
- **WHEN** 产品接入数据采集与链路观测规范
- **THEN** `request_logs` 明细 SHALL 默认保留 90 天
- **AND** `usage_events` 明细 SHALL 默认保留 180 天
- **AND** `task_traces` 与 `task_trace_spans` 明细 SHALL 默认保留 90 天
- **AND** 聚合数据 SHALL 默认保留 1 年。

#### Scenario: 调整保留周期需要依据
- **WHEN** 产品因合规、审计或业务分析需要调整默认保留周期
- **THEN** 产品实现文档 SHALL 记录原因、范围和审批依据
- **AND** SHALL 区分明细数据和聚合数据。

#### Scenario: 超期明细删除或匿名化
- **WHEN** 明细数据超过保留周期
- **THEN** 系统 SHALL 删除或匿名化超期明细
- **AND** SHALL NOT 无限期保留敏感明细数据。

### Requirement: 安全脱敏与禁止采集字段
系统 SHALL 定义采集、持久化和展示过程中的敏感字段禁止清单，并将后端脱敏作为安全边界。

#### Scenario: 禁止采集或展示敏感字段
- **WHEN** 系统采集 payload、metadata、错误摘要、请求摘要、响应摘要或流程节点摘要
- **THEN** 系统 SHALL NOT 采集或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO AccessKey、MinIO SecretKey、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 或真实客户敏感数据。

#### Scenario: 后端脱敏是安全边界
- **WHEN** 客户端已经对字段做展示级脱敏
- **THEN** 后端 SHALL 仍在持久化前执行敏感字段过滤、长度截断和安全 JSON 序列化
- **AND** SHALL NOT 将前端脱敏作为唯一安全边界。

### Requirement: 新产品接入清单与后续引用
系统 SHALL 提供新产品接入 checklist，并允许后续 REQ、BUG、OpenSpec Change 和 Sprint 验收引用该规范。

#### Scenario: 新产品接入 checklist 完整
- **WHEN** 团队阅读通用规范
- **THEN** 规范 SHALL 提供新产品接入 checklist
- **AND** checklist SHALL 覆盖前端 helper 或 SDK、后端 request log middleware、Task Trace helper、DB migration、OpenAPI / Orval、脱敏 helper、测试模板和验收清单。

#### Scenario: 后续 Change 引用规范
- **WHEN** 后续观测类、日志类、上传类、批量任务类或跨端采集类需求进入 OpenSpec Change
- **THEN** Change 设计或验收 SHALL 引用通用产品数据采集与链路观测规范
- **AND** 若某层采集不适用，SHALL 记录 N/A 原因。

#### Scenario: Contract 变更同步治理
- **WHEN** 后续具体接入新增 API 字段、查询参数、响应字段、DB 字段或索引
- **THEN** 对应 Change SHALL 同步 Pydantic Schema、OpenAPI、Orval、API 文档、SQLite / MySQL schema、迁移、数据库设计文档和测试
- **AND** 若不需要 Orval 或 DB 变更，SHALL 在设计或验收记录中说明原因。
