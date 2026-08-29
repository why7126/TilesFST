## MODIFIED Requirements

### Requirement: 日志详情抽屉

系统 SHALL 在右侧抽屉中展示日志详情和 Request Snapshot，且不丢失列表上下文。

#### Scenario: 打开详情抽屉

- **WHEN** admin 选择日志行详情操作
- **THEN** 页面 SHALL 打开右侧抽屉，并在抽屉背后保留可见列表上下文。

#### Scenario: 详情分组匹配原型

- **WHEN** 详情抽屉可见
- **THEN** 抽屉 SHALL 分组展示基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata JSON。

#### Scenario: Request Snapshot 结构化展示

- **WHEN** 详情抽屉展示包含 Request Snapshot 的日志
- **THEN** 抽屉 SHALL 结构化展示请求信息、输入摘要、业务资源、响应结果、操作者与客户端、环境与时间
- **AND** JSON 视图 SHALL 作为辅助查看方式，不得作为唯一展示方式
- **AND** 敏感字段被忽略或脱敏时 SHALL 展示脱敏状态摘要但不得展示敏感原文。

#### Scenario: 长链路字段不重叠

- **WHEN** 详情抽屉展示 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 或等价长 snake_case 排障字段
- **THEN** 字段名 SHALL NOT 侵入或遮挡字段值展示区域
- **AND** 字段值 SHALL NOT 被字段名或字段说明图标遮挡
- **AND** 基础信息、请求信息和 Request Snapshot SHALL 使用换行、截断、title、tooltip、响应式列宽、单列布局或等价可访问策略保持字段名和值可读
- **AND** 窄宽度视口下抽屉内容 SHALL 可滚动且不得导致页面整体横向失控滚动。

#### Scenario: Snapshot 空态与异常展示

- **WHEN** Snapshot 字段缺失、metadata 为空或 metadata JSON 解析失败
- **THEN** 日志详情抽屉 SHALL 继续展示核心日志字段
- **AND** 缺失 Snapshot 字段 SHALL 展示未采集、空值或等价空态
- **AND** 页面 SHALL NOT 崩溃。

#### Scenario: 关闭抽屉

- **WHEN** admin 点击关闭、点击遮罩或按下 Escape
- **THEN** 抽屉 SHALL 关闭，并保留当前筛选和分页状态。

#### Scenario: metadata 脱敏且可滚动

- **WHEN** 抽屉展示 metadata
- **THEN** metadata SHALL 使用等宽字体可滚动区域展示
- **AND** 敏感字段 SHALL 被脱敏或省略。

### Requirement: 客户端请求身份日志审计展示

系统 SHALL 在日志审计能力中展示客户端请求身份信息，支持排障而不泄露敏感字段。

#### Scenario: 日志列表展示请求身份摘要

- **WHEN** admin 查看 `/admin/logs` 日志列表
- **THEN** 表格 SHALL 展示客户端类型和后端可信 `request_id`
- **AND** 表格 MAY 展示短格式客户端请求标识
- **AND** 长 ID SHALL 截断展示，完整值 SHALL 可通过复制、详情抽屉或等价方式获取。

#### Scenario: 日志详情展示两类请求 ID

- **WHEN** admin 打开日志详情抽屉
- **THEN** 详情 SHALL 展示后端可信 `request_id`
- **AND** 详情 SHALL 展示客户端请求标识，若不存在则展示空值或等价缺省状态
- **AND** 字段命名或说明 SHALL 避免将客户端请求标识误读为服务端可信链路 ID。

#### Scenario: 日志详情请求身份字段可读

- **WHEN** 日志详情展示 `request_id`、`client_request_id`、`behavior_trace_id`、`parent_behavior_event_id` 或 `task_trace_id`
- **THEN** 详情 SHALL 区分服务端可信请求 ID、客户端请求标识、行为链路、来源行为事件和任务链路
- **AND** 长 ID 字段名和值 SHALL 同时保持可读或可复制
- **AND** 字段说明图标 SHALL 保留 hover、focus 和可访问名称。

#### Scenario: 客户端请求标识筛选策略

- **WHEN** 日志审计实现 `client_request_id` 筛选
- **THEN** 日志查询 API SHALL 使用索引或等价优化过滤该字段
- **AND** OpenAPI、Orval 和文档 SHALL 同步该查询参数
- **AND** 本 Change 若未修改筛选参数 SHALL 记录 API、OpenAPI 和 Orval 为 N/A。

