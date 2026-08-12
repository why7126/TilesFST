## MODIFIED Requirements

### Requirement: 日志存储与保留
系统 SHALL 将 request logs、Request Snapshot 与 usage events 存储在关系型存储中，并提供可查询索引和保留周期治理。系统 SHALL 将真实用户性能事件作为独立观测数据存储或等价结构化存储，并 SHALL 明确其与请求日志、Request Snapshot、usage events 的边界、索引和保留策略。

#### Scenario: 关系型存储支持 demo 与生产
- **WHEN** 应用运行在本地或 Docker demo 模式
- **THEN** 日志 SHALL 使用 SQLite 兼容 schema 存储
- **AND** 当应用运行在 MySQL 生产环境
- **THEN** 日志 SHALL 使用 MySQL 兼容 schema，且不得包含 SQLite-only DDL。

#### Scenario: 常用筛选字段建立索引
- **WHEN** 日志按创建时间、日志类型、操作者、request id、status code 或 path 查询
- **THEN** 系统 SHALL 使用索引或等价优化的数据库访问方式
- **AND** SHALL NOT 在过滤前将全部日志加载到内存。

#### Scenario: 定义保留周期策略
- **WHEN** 评估日志保留周期
- **THEN** request logs 与 usage events SHALL 遵循既有审计保留策略，或遵循明确文档化的专用保留配置。

#### Scenario: 性能事件存储边界
- **WHEN** 系统持久化真实用户性能事件
- **THEN** 性能事件 SHALL 与审计日志、请求日志和产品行为事件保持可区分的数据类型或表结构
- **AND** 性能事件 MAY 记录受控 `request_id`、`client_type` 或页面上下文用于排障关联
- **AND** 性能事件 SHALL NOT 替代审计日志、权限判断或用户行为漏斗事实源。
