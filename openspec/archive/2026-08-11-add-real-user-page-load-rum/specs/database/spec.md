## ADDED Requirements

### Requirement: 真实用户性能事件数据库支持
数据库 SHALL 支持真实用户性能事件在 SQLite demo 与生产 MySQL 中的兼容存储、索引和保留策略。

#### Scenario: 性能事件表兼容 SQLite 与 MySQL
- **WHEN** 系统新增性能事件存储
- **THEN** SQLite schema、SQLite migration、MySQL baseline 和 MySQL migration SHALL 均包含兼容字段
- **AND** 字段 SHALL 至少支持端类型、页面 key、版本、网络类型、设备类别、指标名、耗时、采样率、客户端事件时间和服务端接收时间
- **AND** MySQL DDL SHALL NOT 使用 SQLite-only 语法。

#### Scenario: 性能聚合索引
- **WHEN** 系统按时间范围、端类型、页面 key、版本、网络类型或设备类别查询性能事件
- **THEN** 数据库 SHALL 提供索引或等价查询优化
- **AND** 后端 SHALL NOT 在过滤前将全部性能事件加载到内存。

#### Scenario: 性能事件保留周期
- **WHEN** 性能事件进入生产存储
- **THEN** 系统 SHALL 明确保留周期、清理策略或后续运维任务边界
- **AND** 数据库文档 SHALL 说明性能事件与审计日志、请求日志、行为事件的保留差异。
