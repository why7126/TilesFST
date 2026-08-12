---
change_id: fix-admin-log-audit-slow-load
status: proposed
created_at: 2026-08-11 09:06:06
updated_at: 2026-08-11 09:06:06
source_bug: BUG-0127-admin-log-audit-slow-load
---

# 设计说明

## 根因分析

日志审计列表慢主要来自列表查询与指标聚合耦合，以及统一 UNION 查询在数据增长后难以稳定命中低成本计划：

1. `LogRepository.list_logs()` 先构造三张表的统一日志源，再在外层追加筛选、全量计数、排序和分页，导致数据库需要处理比当前筛选命中更多的数据。
2. 指定 `log_type` 时仍可能承担统一 UNION 查询成本，不能稳定利用单表 `created_at`、`actor_user_id`、`status_code`、`result` 或 `task_trace_id` 索引。
3. `created_at DESC` 排序发生在 UNION 后，本地 SQLite 已出现临时 B-Tree 排序，随着 `request_logs` 与 `usage_events` 增长会放大首屏等待。
4. `LogService.list_logs()` 同步调用摘要指标聚合，指标扫描三类日志表；指标慢会直接拖慢列表数据返回。
5. SQLite schema、SQLite migration 与 MySQL schema 的索引覆盖仍偏基础，常用组合筛选缺少一致的索引治理。

## 修复方案

1. 查询路径拆分：
   - 当请求指定 `log_type` 时，Repository 优先构造对应单表查询，并只保留与该类型兼容的筛选字段。
   - 当请求未指定 `log_type` 时，三类日志子查询应先下推时间范围、操作者、客户端、状态或结果、request id、Task Trace ID、路径或关键字等可下推条件，再合并排序分页。
   - 列表 `items`、`total`、`page`、`page_size`、`created_at DESC` 顺序和现有响应字段保持兼容。
2. 计数与分页成本控制：
   - `COUNT(*)` 应使用与列表相同的下推筛选语义，避免对无关日志类型或无关时间范围计数。
   - 默认首屏和常用筛选不得因为无条件全表 UNION 排序而退化；必要时可按日志类型分别取候选窗口后归并，但必须通过测试证明排序与分页语义一致。
3. 摘要指标解耦：
   - 列表首屏不得被 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 的全量聚合明显阻塞。
   - 可选实现路径包括独立 metrics endpoint、前端异步加载、短 TTL 缓存、基于时间窗口和索引的轻量聚合，或列表返回指标延迟态。
   - 指标失败或超时不得影响列表数据展示，且前端应有加载态、错误态或占位态。
4. 索引与 schema：
   - SQLite schema、SQLite migration、MySQL schema 和 MySQL migration 应同步补齐日志查询常用索引。
   - 优先评估 `request_logs(client_type, created_at DESC)`、`request_logs(result, created_at DESC)`、`usage_events(client_type, created_at DESC)`、`usage_events(result, created_at DESC)`、`audit_logs(created_at DESC)`，并保留既有 actor、status、path、request id、Task Trace 索引语义。
   - 新增索引必须幂等，不破坏既有日志数据。
5. 管理端体验：
   - 日志审计页继续复用管理端列表页一致性：筛选、分页、空态、加载态、错误反馈、详情入口和 fixed toast 不应退化。
   - 若指标改为异步加载，页面应允许列表先展示，指标区独立进入加载或失败状态。

## 风险与约束

- UNION 查询优化容易引入分页总数、排序稳定性或筛选语义差异，必须用等价测试覆盖混合日志与单类型日志。
- 指标拆分可能改变前端加载顺序，但不得改变管理员权限边界或泄露脱敏 metadata。
- MySQL 生产索引迁移可能造成锁表或耗时风险；需要在文档和发布步骤中说明迁移验证方式。
- 查询计划测试在 SQLite 与 MySQL 上表达不同，测试可采用索引存在性、查询语义、SQLite `EXPLAIN QUERY PLAN` 或生产等价 `EXPLAIN` evidence 的组合。

## 验证计划

- 运行日志审计后端接口测试，覆盖列表默认首屏、时间范围、日志类型、状态或结果、操作者、request id、Task Trace ID、路径或关键字筛选、分页和详情入口。
- 增加查询结果等价测试，确保优化前后混合日志排序与单类型筛选语义一致。
- 增加 SQLite/MySQL 索引存在性或迁移幂等测试，覆盖新增日志索引。
- 记录 SQLite demo 数据下的优化前后 `EXPLAIN QUERY PLAN` 与响应耗时摘要；生产或生产等价 MySQL 应补充 `EXPLAIN` / 慢查询摘要。
- 运行 OpenSpec 校验、语言校验、相关后端 pytest；若 API schema 或前端调用变化，运行 OpenAPI/Orval 生成与 Web 测试。
