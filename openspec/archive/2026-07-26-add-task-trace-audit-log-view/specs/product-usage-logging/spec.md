## MODIFIED Requirements

### Requirement: API 请求日志采集

系统 SHALL 采集 API 请求日志摘要，用于运维排障和审计链路关联。对于属于同一次业务任务的请求，系统 SHALL 支持记录 `task_trace_id` 或等价任务追踪标识，使请求日志可与 task span、usage event 和 audit log 串联。

#### Scenario: 生成或透传 request_id
- **WHEN** 客户端发送 API 请求且未携带 request_id
- **THEN** 系统 SHALL 为该请求生命周期生成 request_id
- **AND** 请求日志 SHALL 存储该 request_id。

#### Scenario: 持久化请求摘要
- **WHEN** API 请求完成
- **THEN** 系统 SHALL 持久化 method、path、status code、毫秒级耗时、request id、client type、可用的操作者上下文、摘要和创建时间。

#### Scenario: 记录任务追踪标识
- **WHEN** API 请求属于一个可追踪业务任务
- **THEN** 请求日志 SHALL 存储 `task_trace_id` 或等价任务追踪标识
- **AND** 同一任务下的多个 request id SHALL 可通过该任务追踪标识关联。

#### Scenario: 异常请求存储脱敏错误上下文
- **WHEN** API 请求因应用错误或服务端错误失败
- **THEN** 请求日志 SHALL 存储 status code、可用的 error code、错误摘要、request id 和已脱敏 metadata
- **AND** SHALL NOT 存储原始密钥、密码、Authorization header、Cookie 或数据库连接串。

#### Scenario: 默认排除噪声路由
- **WHEN** 请求目标为健康检查、静态资源、Swagger/OpenAPI 文档或媒体直出路由
- **THEN** 系统 SHALL 将该请求排除在默认请求日志采集之外。

### Requirement: 管理端日志查询 API

系统 SHALL 提供仅管理员可用的日志列表与详情查询 API。日志查询 API SHALL 支持 Task Trace 任务追踪查询和详情展示。

#### Scenario: 管理员查询日志列表
- **WHEN** 已认证 admin 调用 `GET /api/v1/admin/logs`
- **THEN** 系统 SHALL 返回统一响应，包含分页日志项、total、page、page_size 和指标摘要。

#### Scenario: 支持日志列表筛选
- **WHEN** admin 按日志类型、时间范围、操作者、client type、status code 或 result、resource id、path、keyword、request id 或 task trace id 筛选
- **THEN** 系统 SHALL 仅返回匹配日志，并按最新优先排序。

#### Scenario: 日志列表返回任务摘要
- **WHEN** 日志记录存在 `task_trace_id`
- **THEN** 日志列表项 SHOULD 返回 `task_trace_id`、`task_type`、`task_status` 和 `task_duration_ms` 或等价任务摘要字段。

#### Scenario: 管理员查询日志详情
- **WHEN** 已认证 admin 针对已存在日志调用 `GET /api/v1/admin/logs/{id}`
- **THEN** 系统 SHALL 返回基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata 等详情分组。

#### Scenario: 日志详情返回任务时间线
- **WHEN** 日志记录存在 `task_trace_id`
- **THEN** 日志详情 SHALL 返回同一任务下的 task span 时间线
- **AND** 每个 span SHALL 包含节点名称、耗时、状态、错误码、关联 request id 和摘要。

#### Scenario: 无任务追踪日志保持兼容
- **WHEN** 日志记录不存在 `task_trace_id`
- **THEN** 日志详情 SHALL 保持既有详情结构
- **AND** SHALL NOT 因缺少任务时间线而返回错误。

#### Scenario: 拒绝非管理员访问
- **WHEN** employee、店主端客户端、小程序用户或匿名用户调用管理端日志 API
- **THEN** 系统 SHALL 使用已文档化的 forbidden 响应拒绝访问。

#### Scenario: 日志不存在返回 not found
- **WHEN** admin 请求不存在的 log id
- **THEN** 系统 SHALL 返回已文档化的 404 类错误响应。

### Requirement: 管理端日志审计页面

系统 SHALL 提供 Web 管理端日志审计页面，并对齐产品 v2 Golden Reference。页面 SHALL 支持 Task Trace 查询、复制和任务时间线展示。

#### Scenario: 管理员打开日志审计页

- **WHEN** 已认证 admin 打开 `/admin/logs`
- **THEN** 系统 SHALL 在既有 Admin Shell 内渲染日志审计页面
- **AND** SYSTEM sidebar SHALL 展示并激活 `日志审计`。

#### Scenario: 指标与筛选可见

- **WHEN** admin 查看日志审计页
- **THEN** 页面 SHALL 展示 TODAY LOGS、API ERRORS、SLOW REQUESTS 和 SENSITIVE OPS 指标卡
- **AND** 页面 SHALL 展示日志类型、时间范围、操作者、状态或结果、资源或 ID、路径或 request id 筛选。
- **AND** 状态或结果筛选 SHALL 使用下拉选择交互，支持成功、失败和常见 HTTP 状态码精确筛选，且 SHALL 至少包含 `422 参数校验错误`。

#### Scenario: Task Trace 筛选可见
- **WHEN** admin 查看日志审计筛选区
- **THEN** 页面 SHALL 提供 `task_trace_id` 筛选能力，或将路径 / request id 筛选明确扩展为路径 / request id / task trace id
- **AND** 筛选区 SHALL 保持管理端列表页布局，不造成移动端溢出。

#### Scenario: 日志表格支持排障

- **WHEN** admin 查看日志行
- **THEN** 表格 SHALL 展示时间、类型、事件或摘要、操作者、客户端、状态或结果、耗时、request id、复制操作和详情操作。
- **AND** 类型与状态或结果 SHALL 通过不同颜色或等价视觉样式区分不同值，便于管理员快速扫描异常日志。

#### Scenario: Task Trace 摘要可扫描
- **WHEN** 日志行存在 `task_trace_id`
- **THEN** 表格 SHOULD 展示任务类型、任务结果、任务耗时或是否存在慢节点的摘要
- **AND** admin SHALL 能从详情操作进入任务时间线。

#### Scenario: request_id 与 task_trace_id 可复制且不造成布局位移

- **WHEN** admin 复制带有 request id 或 task trace id 的日志记录
- **THEN** 系统 SHALL 优先将完整 ID 写入系统剪贴板
- **AND** 系统 SHALL 使用 fixed toast 或等价不造成布局位移的反馈展示成功、失败或兜底结果
- **AND** 当 Clipboard API 不存在、浏览器拒绝写入或写入失败时，系统 SHALL 不抛出未捕获错误
- **AND** 系统 SHALL 提供手动复制指引、可选中文本或等价兜底，使 admin 仍可获取完整 ID。

#### Scenario: employee 不可打开页面

- **WHEN** 已认证 employee 打开 `/admin/logs`
- **THEN** 系统 SHALL 按既有管理端授权模式展示 forbidden 状态或重定向
- **AND** 不暴露日志数据。

#### Scenario: 日志能力测试覆盖

- **WHEN** 实现完成
- **THEN** 后端测试 SHALL 覆盖日志记录、校验、脱敏、权限、筛选、task trace 查询、任务时间线和 not-found 行为
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、request_id / task_trace_id 复制成功、Clipboard API 不可用兜底、复制写入失败兜底、详情抽屉、任务时间线、forbidden 状态和分页结构。

### Requirement: 日志详情抽屉

系统 SHALL 在右侧抽屉中展示日志详情，且不丢失列表上下文。日志详情抽屉 SHALL 在存在 task trace 时展示任务时间线。

#### Scenario: 打开详情抽屉
- **WHEN** admin 选择日志行详情操作
- **THEN** 页面 SHALL 打开右侧抽屉，并在抽屉背后保留可见列表上下文。

#### Scenario: 详情分组匹配原型
- **WHEN** 详情抽屉可见
- **THEN** 抽屉 SHALL 分组展示基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata JSON。

#### Scenario: 展示任务时间线
- **WHEN** 详情日志存在 `task_trace_id`
- **THEN** 抽屉 SHALL 展示 Task Trace 分组
- **AND** 分组 SHALL 包含任务摘要、节点时间线、节点耗时、节点状态、错误码和关联 request id。

#### Scenario: 慢节点突出显示
- **WHEN** task span 超过慢任务阈值或为耗时最高节点
- **THEN** 抽屉 SHOULD 使用视觉标识或文案提示该慢节点
- **AND** SHALL NOT 遮挡基础信息、请求信息或 metadata JSON。

#### Scenario: 关闭抽屉
- **WHEN** admin 点击关闭、点击遮罩或按下 Escape
- **THEN** 抽屉 SHALL 关闭，并保留当前筛选和分页状态。

#### Scenario: metadata 脱敏且可滚动
- **WHEN** 抽屉展示 metadata
- **THEN** metadata SHALL 使用等宽字体可滚动区域展示
- **AND** 敏感字段 SHALL 被脱敏或省略。

## ADDED Requirements

### Requirement: 任务链路追踪

系统 SHALL 为可追踪业务任务提供 Task Trace 模型，支持任务标识、任务节点、状态、耗时、错误码、资源关联和安全脱敏。

#### Scenario: 生成任务追踪标识
- **WHEN** 用户发起需要追踪的业务任务
- **THEN** 系统 SHALL 生成或确认 `task_trace_id`
- **AND** `task_trace_id` SHALL NOT 包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。

#### Scenario: 记录任务节点
- **WHEN** 任务进入关键处理节点
- **THEN** 系统 SHALL 记录 task span
- **AND** span SHALL 至少包含 `task_trace_id`、`task_type`、`span_name`、`status`、开始时间和耗时或结束时间。

#### Scenario: 任务状态可推导
- **WHEN** 任务结束、失败、超时或取消
- **THEN** 系统 SHALL 将任务状态标记为 `success`、`failed`、`timeout` 或 `cancelled`
- **AND** 进行中的任务 SHALL 可标记为 `processing`。

#### Scenario: 任务节点关联请求
- **WHEN** task span 发生在某个 HTTP 请求生命周期中
- **THEN** span SHALL 关联对应 `request_id`
- **AND** 同一 `task_trace_id` MAY 关联多个 request id。

#### Scenario: 任务失败可诊断
- **WHEN** 任务节点失败
- **THEN** span SHALL 记录统一错误码或失败摘要
- **AND** SHALL NOT 暴露 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。

#### Scenario: 任务追踪持久化可查询
- **WHEN** 系统持久化 task trace 或 task span
- **THEN** 持久化结构 SHALL 支持按 `task_trace_id`、`task_type` 和创建时间查询
- **AND** SQLite demo 与 MySQL production SHALL 使用兼容 schema。

## MODIFIED Requirements

### Requirement: OpenAPI、Orval 与文档治理

系统 SHALL 保持产品使用日志相关 API、数据库、文档和生成客户端产物同步。

#### Scenario: 生成 API 契约
- **WHEN** 后端日志 API 被实现或变更
- **THEN** OpenAPI SHALL 暴露 response models、summaries、descriptions 和 tags
- **AND** Orval SHALL 生成对应 Web client methods。

#### Scenario: Task Trace 契约同步
- **WHEN** 日志列表、日志详情或上传响应新增 `task_trace_id`、任务摘要或任务时间线字段
- **THEN** OpenAPI SHALL 暴露这些字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: 文档保持同步
- **WHEN** 日志能力被实现
- **THEN** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用的错误码文档 SHALL 描述新增 endpoints、schemas、tables 和 errors。

#### Scenario: 校验与测试覆盖能力
- **WHEN** 实现完成
- **THEN** 后端和前端测试 SHALL 覆盖新增或修改的日志 API、任务时间线字段、权限、脱敏、筛选和错误场景。
