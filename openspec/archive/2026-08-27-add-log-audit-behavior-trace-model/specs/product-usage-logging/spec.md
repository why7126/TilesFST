## MODIFIED Requirements

### Requirement: API 请求日志采集

系统 SHALL 采集 API 请求日志摘要与统一 Request Snapshot，用于运维排障、审计链路关联和跨端请求上下文还原。

#### Scenario: 请求日志记录行为来源字段

- **WHEN** API 请求由已采集的界面行为触发
- **THEN** 请求日志 SHALL 保存 `behavior_trace_id`
- **AND** 请求日志 SHALL 保存 `parent_behavior_event_id` 或等价结构化来源行为事件标识
- **AND** 同一次界面行为触发的多个 API 请求 SHALL 能通过同一个 `behavior_trace_id` 查询关联。

#### Scenario: 直接 API 调用行为链路为空

- **WHEN** 请求来自直接 API 调用、外部系统、脚本或无界面行为上下文的客户端
- **THEN** 请求日志 SHALL 允许 `behavior_trace_id` 为空
- **AND** 请求日志 SHALL 允许 `parent_behavior_event_id` 为空
- **AND** 系统 SHALL 继续生成服务端可信 `request_id`
- **AND** 直接 API 调用 SHALL NOT 为通过行为链路校验而伪造 `usage_events`。

#### Scenario: 行为来源字段不替代可信请求 ID

- **WHEN** 客户端携带 `behavior_trace_id`、`behavior_event_id` 或 `client_request_id`
- **THEN** 系统 SHALL 将这些字段视为链路归因或排障辅助字段
- **AND** 系统 SHALL NOT 使用这些字段覆盖服务端可信 `request_id`
- **AND** 系统 SHALL NOT 将这些字段作为鉴权、权限或操作者身份来源。

### Requirement: 产品使用行为事件采集

系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、分类页、商品列表页、商品详情、搜索、收藏列表、品牌详情页、商品卡片组件和品牌卡片组件的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互、收藏交互、品牌入口、卡片曝光、卡片点击和安全降级事件，用于小程序热销推荐统计、分类入口效果分析、搜索体验分析、收藏行为分析、品牌入口效果分析和后续产品优先级判断。

#### Scenario: 行为事件包含行为链路字段

- **WHEN** 客户端提交页面访问、按钮点击、搜索筛选、详情查看、表单提交、上传、发布或删除等可追踪行为事件
- **THEN** usage event SHALL 包含 `behavior_trace_id`
- **AND** usage event SHALL 包含 `behavior_event_id`
- **AND** `behavior_trace_id` SHALL 表示一次用户行为链路
- **AND** `behavior_event_id` SHALL 表示单条行为事件。

#### Scenario: 行为链路字段格式受控

- **WHEN** usage event 接收 API 收到 `behavior_trace_id` 或 `behavior_event_id`
- **THEN** 系统 SHALL 校验字段格式、长度和字符集
- **AND** 非法、超长或包含敏感信息的链路字段 SHALL 被拒绝或按文档化策略忽略
- **AND** 埋点失败 SHALL NOT 中断主用户流程。

### Requirement: 日志存储与保留

系统 SHALL 将 request logs、Request Snapshot 与 usage events 存储在关系型存储中，并提供可查询索引和保留周期治理。日志查询常用索引 SHALL 在 SQLite demo 与 MySQL production 之间保持兼容，并 SHALL 支持管理端日志审计页的时间范围、客户端、状态或结果、操作者、request id、path、行为链路和 Task Trace 查询。

#### Scenario: 行为链路字段索引

- **WHEN** 系统新增或迁移日志链路字段
- **THEN** SQLite schema、SQLite migration、MySQL schema 和 MySQL migration SHALL 支持 `usage_events.behavior_trace_id`
- **AND** SHALL 支持 `usage_events.behavior_event_id`
- **AND** SHALL 支持 `request_logs.behavior_trace_id`
- **AND** SHALL 支持 `request_logs.parent_behavior_event_id`
- **AND** SHALL 按 `behavior_trace_id`、`behavior_event_id`、`request_id`、`task_trace_id`、`parent_request_id` 和创建时间的常用查询建立索引或等价优化。

#### Scenario: 历史日志兼容空行为链路

- **WHEN** 系统读取历史 request logs、usage events、Task Trace 或 task spans
- **THEN** 缺少 `behavior_trace_id`、`behavior_event_id` 或 `parent_behavior_event_id` 的记录 SHALL 以空值、未采集状态或等价兼容方式返回
- **AND** 日志审计列表、详情和聚合查询 SHALL NOT 因空行为链路报错。

### Requirement: 管理端日志查询 API

系统 SHALL 提供仅管理员可用的日志列表与详情查询 API，并在日志详情中返回统一 Request Snapshot。日志列表查询 SHALL 在日志量增长后保持可接受的首屏、筛选和分页性能；系统 SHALL 使用索引友好的查询路径、条件下推、低成本计数和可解耦指标策略，避免默认首屏被无条件三表 UNION、全量排序、全量计数或同步摘要聚合明显阻塞。

#### Scenario: 按 behavior_trace_id 查询链路

- **WHEN** admin 使用 `behavior_trace_id` 查询日志审计数据
- **THEN** 系统 SHALL 返回匹配行为链路的 usage events
- **AND** SHALL 返回同一 `behavior_trace_id` 下的 request logs
- **AND** SHALL 返回可通过 request logs 关联到的 Task Trace 摘要和流程节点入口
- **AND** 查询 SHALL 使用索引友好路径，不得在过滤前全量加载日志。

#### Scenario: 按 request_id 查询直接 API 链路

- **WHEN** admin 使用 `request_id` 查询直接 API 调用
- **THEN** 系统 SHALL 返回该请求日志
- **AND** 若存在 `task_traces.parent_request_id` 指向该 `request_id`，系统 SHALL 返回任务链路摘要和流程节点入口
- **AND** 若请求没有行为来源，系统 SHALL 返回无界面行为来源的空态，而不是错误。

#### Scenario: 按 task_trace_id 查询任务链路

- **WHEN** admin 使用 `task_trace_id` 查询日志审计数据
- **THEN** 系统 SHALL 返回任务摘要
- **AND** SHALL 返回对应 task trace spans
- **AND** SHALL 能回溯到 `task_traces.parent_request_id` 对应的 request log
- **AND** 对有行为链路的任务 SHALL 同时展示 `behavior_trace_id`。

### Requirement: 管理端日志审计页面

系统 SHALL 提供 Web 管理端日志审计页面，并对齐产品 v2 Golden Reference。

#### Scenario: 日志审计支持三类链路查询入口

- **WHEN** admin 打开 `/admin/logs`
- **THEN** 页面 SHALL 支持按 `behavior_trace_id`、`request_id` 和 `task_trace_id` 查询
- **AND** 筛选项 SHALL 与时间范围、日志类型、状态或结果、操作者和路径筛选协同工作
- **AND** 筛选变化 SHALL 重置分页并使用后端真实分页结果。

#### Scenario: 日志详情展示行为到流程节点链路

- **WHEN** admin 打开包含行为链路的日志详情
- **THEN** 详情 SHALL 展示行为事件、API 请求、任务链路和流程节点之间的关系
- **AND** 流程节点底层 MAY 来自 `task_trace_spans`
- **AND** 用户可见文案 SHALL 使用“流程节点”描述任务内部 span。

#### Scenario: 无行为来源空态

- **WHEN** admin 查看直接 API 调用、历史日志或后台脚本调用产生的日志详情
- **THEN** 页面 SHALL 显示无界面行为来源、未采集或等价空态
- **AND** request log、Task Trace 和流程节点展示 SHALL 继续可用。

### Requirement: 任务链路追踪

系统 SHALL 为可观测任务记录可关联的 Task Trace，包含任务类型、阶段 spans、状态、开始时间、结束时间或耗时、请求关联标识、失败摘要，并支持按任务或请求上下文查询。

#### Scenario: 任务链路继承行为链路

- **GIVEN** 任务由带 `behavior_trace_id` 的 API 请求触发
- **WHEN** 系统创建或更新 Task Trace
- **THEN** Task Trace SHALL 记录 `parent_request_id`
- **AND** Task Trace SHOULD 记录同一个 `behavior_trace_id`
- **AND** task trace spans MAY 冗余记录 `behavior_trace_id` 以支持链路查询。

#### Scenario: 任务链路支持直接 API 请求

- **GIVEN** 任务由无行为上下文的 API 请求触发
- **WHEN** 系统创建 Task Trace
- **THEN** Task Trace SHALL 记录 `parent_request_id`
- **AND** `parent_request_id` SHALL 关联 `request_logs.request_id`
- **AND** Task Trace SHALL NOT 要求存在 `behavior_trace_id`。

### Requirement: 客户端请求身份日志审计展示

系统 SHALL 在日志审计能力中展示客户端请求身份信息，支持排障而不泄露敏感字段。

#### Scenario: 请求身份与行为链路身份分离

- **WHEN** 日志审计详情展示请求身份
- **THEN** 详情 SHALL 区分服务端可信 `request_id`
- **AND** SHALL 区分客户端请求标识 `client_request_id`
- **AND** SHALL 区分行为链路 `behavior_trace_id`
- **AND** SHALL 区分来源行为事件 `parent_behavior_event_id`
- **AND** 页面 SHALL NOT 将任一客户端提供字段展示为可信操作者身份。
