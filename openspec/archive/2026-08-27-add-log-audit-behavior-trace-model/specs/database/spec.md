## ADDED Requirements

### Requirement: 日志审计行为链路字段数据库支持

数据库能力 SHALL 在 SQLite demo 与生产 MySQL 中一致支持日志审计行为链路字段、请求来源字段、任务链路字段和流程节点查询索引。

#### Scenario: usage_events 行为链路字段一致

- **WHEN** 系统初始化或迁移 SQLite 与 MySQL schema
- **THEN** `usage_events` SHALL 支持 `behavior_trace_id`
- **AND** `usage_events` SHALL 支持 `behavior_event_id`
- **AND** 字段可空性、长度、类型和中文注释 SHALL 在 SQLite、MySQL 和数据库文档中保持一致。

#### Scenario: request_logs 行为来源字段一致

- **WHEN** 系统初始化或迁移 SQLite 与 MySQL schema
- **THEN** `request_logs` SHALL 支持 `behavior_trace_id`
- **AND** `request_logs` SHALL 支持 `parent_behavior_event_id`
- **AND** 直接 API 调用和历史日志 SHALL 能保存空行为来源字段。

#### Scenario: task traces 与 task trace spans 支持行为链路查询

- **WHEN** 系统初始化或迁移 Task Trace 相关 schema
- **THEN** `task_traces` SHALL 继续支持 `parent_request_id`
- **AND** `task_traces` SHOULD 支持 `behavior_trace_id`
- **AND** `task_trace_spans` MAY 支持 `behavior_trace_id` 和当前 `request_id`
- **AND** 字段设计 SHALL 支持从行为链路、请求 ID 和任务链路 ID 三种入口查询。

#### Scenario: 链路查询索引一致

- **WHEN** 数据库提供日志审计链路查询
- **THEN** SQLite 与 MySQL SHALL 提供按 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`parent_request_id`、`task_trace_id` 和 `created_at` 的索引或等价优化
- **AND** 后端 SHALL NOT 依赖扫描 metadata JSON 作为主要查询路径。

#### Scenario: 数据库文档同步

- **WHEN** 本 Change 实现完成
- **THEN** 数据库设计文档 SHALL 记录新增字段、中文注释、可空约束、索引、SQLite / MySQL 类型映射和旧日志兼容策略
- **AND** 发布或归档前 SHALL 记录 MySQL 目标路径验证、迁移幂等和回滚边界。
