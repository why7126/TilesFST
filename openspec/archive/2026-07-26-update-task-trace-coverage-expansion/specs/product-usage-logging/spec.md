## MODIFIED Requirements

### Requirement: 任务链路追踪

系统 SHALL 为可追踪业务任务提供 Task Trace 模型，支持任务标识、任务节点、状态、耗时、错误码、资源关联、安全脱敏，并覆盖上传之外的长耗时、多步骤、跨服务、异步、批量、媒体处理、复杂保存和复杂查询类任务型业务接口。

#### Scenario: 生成任务追踪标识
- **WHEN** 用户发起需要追踪的业务任务
- **THEN** 系统 SHALL 生成或确认 `task_trace_id`
- **AND** `task_trace_id` SHALL NOT 包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。

#### Scenario: 记录任务节点
- **WHEN** 任务进入关键处理节点
- **THEN** 系统 SHALL 记录 task span
- **AND** span SHALL 至少包含 `task_trace_id`、`task_type`、`span_name`、`status`、开始时间和耗时或结束时间。

#### Scenario: 任务状态可推导
- **WHEN** 任务结束、失败、超时、取消或批量任务部分成功
- **THEN** 系统 SHALL 将任务状态标记为 `success`、`failed`、`timeout`、`cancelled` 或 `partial_success`
- **AND** 进行中的任务 SHALL 可标记为 `processing`。

#### Scenario: 任务节点关联请求
- **WHEN** task span 发生在某个 HTTP 请求生命周期中
- **THEN** span SHALL 关联对应 `request_id`
- **AND** 同一 `task_trace_id` MAY 关联多个 request id。

#### Scenario: 子请求和异步任务继承任务上下文
- **WHEN** 一个用户操作触发子请求、后台 worker 或异步任务
- **THEN** 子请求、后台 worker 或异步任务 SHALL 继承原始用户操作的 `task_trace_id`
- **AND** 无法继承时 SHALL 记录降级 span 或明确的关联缺失原因。

#### Scenario: 任务失败可诊断
- **WHEN** 任务节点失败
- **THEN** span SHALL 记录统一错误码或失败摘要
- **AND** SHALL NOT 暴露 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。

#### Scenario: 批量任务部分成功可诊断
- **WHEN** 批量任务出现部分成功
- **THEN** 系统 SHALL 记录成功数、失败数和失败分类摘要
- **AND** 任务最终状态 SHALL 可表达为 `partial_success` 或等价可查询状态。

#### Scenario: 任务追踪持久化可查询
- **WHEN** 系统持久化 task trace 或 task span
- **THEN** 持久化结构 SHALL 支持按 `task_trace_id`、`task_type` 和创建时间查询
- **AND** SQLite demo 与 MySQL production SHALL 使用兼容 schema。

## ADDED Requirements

### Requirement: 任务型接口 Task Trace 覆盖策略

系统 SHALL 定义任务型接口判定标准，并为首批接入 Task Trace 的业务接口输出可执行清单。

#### Scenario: 生成首批任务型接口清单
- **WHEN** 实现 REQ-0074
- **THEN** 系统 SHALL 输出首批 Task Trace 接入接口清单
- **AND** 清单 SHALL 至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。

#### Scenario: 首批清单包含接入信息
- **WHEN** 某个候选接口被列入首批清单
- **THEN** 清单 SHALL 标注任务类型、接入优先级、关键步骤、预期 span、是否异步、是否批量、是否涉及对象存储或外部依赖。

#### Scenario: 未纳入首批的候选接口有后续排期
- **WHEN** 候选接口未纳入首批接入范围
- **THEN** 清单 SHALL 记录未接入原因和后续排期建议。

#### Scenario: 同步任务记录关键步骤
- **WHEN** 同步任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录请求接收、输入校验、业务处理、持久化或外部调用、响应或任务结束 span。

#### Scenario: 异步任务记录关键步骤
- **WHEN** 异步任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录 `async_dispatch`、`worker_start`、`worker_process`、`worker_persist_result`、`worker_finished` 或 `worker_failed` 等等价 span。

#### Scenario: 批量任务记录关键步骤
- **WHEN** 批量任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录批量解析、批量校验、单项处理、成功 / 失败计数、失败分类摘要和最终结果 span。

#### Scenario: Task Trace helper 封装接入
- **WHEN** 业务服务写入任务 span
- **THEN** 系统 SHALL 通过 Task Trace helper、service 或等价封装生成、透传、绑定上下文和写入 span
- **AND** 路由层 SHALL NOT 直接拼 SQL 或直接持久化 task span。

### Requirement: 管理端复杂任务追踪反馈

系统 SHALL 在管理端复杂任务成功、失败、处理中或部分成功反馈中展示或提供可复制的 `task_trace_id`，并允许管理员进入日志审计查看任务时间线。

#### Scenario: 复杂任务反馈展示追踪标识
- **WHEN** 管理端复杂任务返回 `task_trace_id`
- **THEN** 页面 SHALL 在任务反馈区域展示该追踪标识或复制入口
- **AND** 展示 SHALL 不挤占主要业务表单区域。

#### Scenario: 复制追踪标识不造成布局位移
- **WHEN** 管理员复制 `task_trace_id`
- **THEN** 页面 SHALL 使用 fixed toast 或等价固定层展示成功、失败或兜底反馈
- **AND** 反馈 SHALL NOT 造成页面布局位移。

#### Scenario: 无追踪标识保持兼容
- **WHEN** 复杂任务响应中没有 `task_trace_id`
- **THEN** 页面 SHALL 保持原有交互
- **AND** SHALL NOT 显示空追踪组件或空错误态。

#### Scenario: 失败摘要安全展示
- **WHEN** 管理端展示复杂任务失败反馈
- **THEN** 页面 SHALL 只展示安全错误码、脱敏摘要和可复制追踪标识
- **AND** SHALL NOT 展示内部路径、堆栈、原始请求体或敏感 metadata。

#### Scenario: 日志审计入口可达
- **WHEN** 管理员从复杂任务反馈进入日志审计
- **THEN** 日志审计 SHALL 可按 `task_trace_id` 查询或展示同一任务的时间线。

