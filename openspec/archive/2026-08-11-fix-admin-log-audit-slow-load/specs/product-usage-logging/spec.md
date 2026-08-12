# product-usage-logging Delta

## MODIFIED Requirements

### Requirement: 管理端日志查询 API
系统 SHALL 提供仅管理员可用的日志列表与详情查询 API，并在日志详情中返回统一 Request Snapshot。日志列表查询 SHALL 在日志量增长后保持可接受的首屏、筛选和分页性能；系统 SHALL 使用索引友好的查询路径、条件下推、低成本计数和可解耦指标策略，避免默认首屏被无条件三表 UNION、全量排序、全量计数或同步摘要聚合明显阻塞。

#### Scenario: 管理员查询日志列表
- **WHEN** 已认证 admin 调用 `GET /api/v1/admin/logs`
- **THEN** 系统 SHALL 返回统一响应，包含分页日志项、total、page、page_size 和指标摘要或指标延迟态
- **AND** 日志列表数据 SHALL 可在指标聚合失败、延迟或独立加载时先行返回
- **AND** 响应 SHALL NOT 暴露 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径、完整请求体或完整响应体。

#### Scenario: 支持日志列表筛选
- **WHEN** admin 按日志类型、时间范围、操作者、client type、status code 或 result、resource id、path、keyword、request id 或 task trace id 筛选
- **THEN** 系统 SHALL 仅返回匹配日志，并按最新优先排序
- **AND** 可下推筛选条件 SHALL 在对应日志表查询阶段尽量生效
- **AND** 系统 SHALL NOT 在过滤前将全部 request logs、usage events 或 audit logs 加载到内存。

#### Scenario: 指定日志类型使用低成本查询路径
- **WHEN** admin 指定 `log_type=request`、`log_type=usage_event` 或 `log_type=audit`
- **THEN** 系统 SHALL 优先查询对应单表或等价低成本路径
- **AND** 不应继续无条件扫描另外两类日志表
- **AND** total、分页和 `created_at DESC` 排序 SHALL 与该日志类型的既有语义一致。

#### Scenario: 混合日志分页保持稳定
- **WHEN** admin 未指定日志类型并查询混合日志列表
- **THEN** 系统 SHALL 合并 request logs、usage events 和 audit logs 的匹配记录
- **AND** 结果 SHALL 按 `created_at DESC` 稳定排序
- **AND** total、page、page_size 和 items SHALL 与筛选条件保持一致
- **AND** 实现 SHALL 通过等价测试覆盖跨日志类型排序、分页边界、空结果和重复时间戳场景。

#### Scenario: 摘要指标不阻塞列表首屏
- **WHEN** 日志审计页需要展示 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops`
- **THEN** 系统 SHALL 使用缓存、独立接口、异步加载、索引友好聚合或等价策略获取指标
- **AND** 指标查询失败、超时或降级 SHALL NOT 阻断列表数据展示
- **AND** 指标口径、延迟态或错误态 SHALL 在 API、Web 页面和测试中保持一致。

#### Scenario: 日志查询性能证据
- **WHEN** BUG-0127 修复完成并进入验收
- **THEN** 团队 SHALL 记录 SQLite demo 数据下优化前后的列表接口耗时和 `EXPLAIN QUERY PLAN` 摘要
- **AND** 团队 SHALL 记录生产或生产等价 MySQL 的 `EXPLAIN`、慢查询摘要或无法获取时的原因与剩余风险
- **AND** 验收 SHALL 覆盖默认首屏、常用筛选、单日志类型筛选、混合分页、指标加载和非管理员访问拒绝。

### Requirement: 日志存储与保留
系统 SHALL 将 request logs、Request Snapshot 与 usage events 存储在关系型存储中，并提供可查询索引和保留周期治理。日志查询常用索引 SHALL 在 SQLite demo 与 MySQL production 之间保持兼容，并 SHALL 支持管理端日志审计页的时间范围、客户端、状态或结果、操作者、request id、path 和 Task Trace 查询。

#### Scenario: 常用筛选字段建立索引
- **WHEN** 日志按创建时间、日志类型、操作者、request id、status code 或 result、client type、path 或 task trace id 查询
- **THEN** 系统 SHALL 使用索引或等价优化的数据库访问方式
- **AND** SQLite schema、SQLite migration、MySQL schema 和 MySQL migration SHALL 保持兼容索引定义
- **AND** SHALL NOT 在过滤前将全部日志加载到内存。

#### Scenario: BUG-0127 日志索引一致性
- **WHEN** 修复管理端日志审计加载慢问题
- **THEN** 系统 SHALL 至少评估并按需补齐 `request_logs(client_type, created_at)`、`request_logs(result, created_at)`、`usage_events(client_type, created_at)`、`usage_events(result, created_at)` 和 `audit_logs(created_at)` 等常用查询索引
- **AND** 新增或调整索引 SHALL 同步到 SQLite / MySQL schema、迁移、数据库文档和测试
- **AND** 迁移 SHALL 幂等执行，不破坏既有日志数据。
