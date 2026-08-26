## MODIFIED Requirements

### Requirement: 日志审计请求身份交互

Web 管理端 SHALL 在日志审计列表和详情中展示请求身份字段，并保持管理端列表页横切一致性。

#### Scenario: 日志审计筛选支持行为链路

- **WHEN** admin 打开日志审计页
- **THEN** Web 客户端 SHALL 提供按 `behavior_trace_id` 查询的入口
- **AND** SHALL 保持按 `request_id` 和 `task_trace_id` 查询的入口
- **AND** 筛选变化 SHALL 重置分页并调用后端日志审计 API
- **AND** 页面 SHALL NOT 在前端全量拉取后切片伪分页。

#### Scenario: 日志详情展示链路关系

- **WHEN** admin 打开日志详情
- **THEN** Web 客户端 SHALL 展示服务端可信 `request_id`
- **AND** SHALL 展示可用的 `behavior_trace_id`
- **AND** SHALL 展示可用的 `parent_behavior_event_id`
- **AND** SHALL 展示可用的 `task_trace_id`
- **AND** SHALL 将 task trace spans 展示为“流程节点”。

#### Scenario: 长链路 ID 展示不破坏列表

- **WHEN** 日志列表展示 `behavior_trace_id`、`request_id`、`client_request_id` 或 `task_trace_id`
- **THEN** 字段 SHALL 使用单行、截断、tooltip/title、复制按钮或等价可访问策略
- **AND** SHALL NOT 撑宽整表、遮挡操作列或破坏分页 DOM
- **AND** 复制成功或失败 SHALL 使用 fixed toast 或等价不造成布局位移的反馈。

#### Scenario: 无行为来源展示空态

- **WHEN** 日志记录来自直接 API 调用、外部系统、脚本或历史数据且没有 `behavior_trace_id`
- **THEN** Web 客户端 SHALL 展示“无界面行为来源”、未采集或等价空态
- **AND** SHALL 继续允许 admin 查看请求详情、任务链路和流程节点。

#### Scenario: 日志审计行为链路测试覆盖

- **WHEN** 实现日志审计行为链路查询
- **THEN** 前端测试 SHALL 覆盖 `behavior_trace_id`、`request_id`、`task_trace_id` 三类查询入口
- **AND** SHALL 覆盖空行为来源、长 ID 截断、复制反馈、分页结构和敏感字段不展示。
