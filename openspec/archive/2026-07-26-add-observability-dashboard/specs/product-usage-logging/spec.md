## ADDED Requirements

### Requirement: 管理端链路观测聚合 API

系统 SHALL 提供仅管理员可用的链路观测聚合查询能力，用于按同一筛选口径返回请求日志、行为事件、审计操作和 Task Trace 的摘要、分布、排行与追踪结果。

#### Scenario: 管理员查询链路观测摘要
- **WHEN** 已认证 admin 使用时间范围、日志类型、客户端、任务类型、接口路径、状态或结果筛选链路观测数据
- **THEN** 系统 SHALL 返回统一响应 envelope
- **AND** 响应 SHALL 包含总日志量、API 错误数、API 错误率、慢请求数、任务成功率、慢任务数和审计操作数
- **AND** 所有摘要指标 SHALL 与同一组筛选条件保持一致。

#### Scenario: 返回 Task Trace 观测指标
- **WHEN** admin 查询链路观测数据且存在 Task Trace 数据
- **THEN** 系统 SHALL 返回任务状态分布、任务成功率、失败任务数量和任务耗时分布或等价分桶
- **AND** SHALL 返回慢任务排行，包含任务类型、耗时、状态、触发来源和 `task_trace_id`
- **AND** SHALL 返回最慢 span 排行，包含 span 名称、任务类型、耗时、结果和关联 `task_trace_id`。

#### Scenario: 返回请求与接口错误观测指标
- **WHEN** admin 查询链路观测数据且存在请求日志
- **THEN** 系统 SHALL 按接口路径、方法和状态码统计请求量、错误量和错误率
- **AND** SHALL 返回慢请求排行，包含路径、方法、状态码、耗时、客户端和 `request_id`
- **AND** SHALL 返回失败原因分布，优先使用错误码、异常摘要或业务失败原因。

#### Scenario: 返回客户端与行为分布
- **WHEN** admin 查询链路观测数据且存在行为事件或请求来源
- **THEN** 系统 SHALL 返回客户端分布，覆盖 `web_admin`、`web_catalog`、`miniapp`、`backend` 和未识别客户端
- **AND** 系统 SHALL 返回行为事件分布，包含事件类型、模块、结果和失败原因。

#### Scenario: 追踪 ID 精确查询
- **WHEN** admin 使用 `request_id` 或 `task_trace_id` 精确查询链路观测数据
- **THEN** 系统 SHALL 返回对应日志详情、Task Trace 时间线或相关记录集合所需的跳转 ID
- **AND** 未命中时 SHALL 返回空集合和可识别空态原因，而不是系统错误。

#### Scenario: 聚合查询权限与脱敏
- **WHEN** employee、店主端客户端、小程序用户或匿名用户调用链路观测聚合接口
- **THEN** 系统 SHALL 使用已文档化的 forbidden 响应拒绝访问
- **AND** 响应 SHALL NOT 暴露 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径、完整请求体或完整响应体。

#### Scenario: 聚合查询性能边界
- **WHEN** 系统计算链路观测摘要、分布或排行
- **THEN** 系统 SHALL 使用 Repository 或统一数据访问层执行数据库聚合、索引查询或分页 Top N 查询
- **AND** SHALL NOT 在过滤前将全部日志、行为事件、审计操作或 Task Trace 记录加载到内存
- **AND** SQLite demo 与 MySQL production SHALL 使用兼容查询和 schema。

### Requirement: 链路观测契约同步

系统 SHALL 在实现链路观测聚合 API 时同步维护 API、OpenAPI、Orval、文档、错误码、数据库说明和测试契约。

#### Scenario: OpenAPI 与 Orval 同步
- **WHEN** 新增或修改管理端链路观测聚合 API、响应 Schema 或查询参数
- **THEN** OpenAPI SHALL 暴露 response models、summaries、descriptions 和 tags
- **AND** Orval SHALL 生成对应 Web client methods 和 types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: API 与数据库文档同步
- **WHEN** 链路观测实现新增 endpoint、schema、索引、聚合字段或错误码
- **THEN** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用的错误码文档 SHALL 描述新增 endpoints、schemas、tables、indexes 和 errors。

#### Scenario: 测试覆盖
- **WHEN** 链路观测聚合 API 实现完成
- **THEN** 后端测试 SHALL 覆盖聚合摘要、筛选、权限、脱敏、空数据、追踪 ID 命中 / 未命中、SQLite 和 MySQL 兼容口径
- **AND** 若 Web 管理端页面消费该聚合接口，前端测试 SHALL 覆盖页面渲染、筛选刷新、排行下钻、复制反馈、加载失败、无权限、空态、分页结构、fixed toast 和移动端 smoke。
