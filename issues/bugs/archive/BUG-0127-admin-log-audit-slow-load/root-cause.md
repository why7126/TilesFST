---
bug_id: BUG-0127-admin-log-audit-slow-load
created_at: 2026-08-11 08:50:48
updated_at: 2026-08-11 08:50:48
severity: medium
related_requirement:
related_bug:
---

# 根因分析

## 直接原因

管理后台日志审计列表接口在一次首屏加载中同时执行三类高成本查询：

1. 基于 `request_logs`、`usage_events`、`audit_logs` 的统一 UNION 日志源计算总数。
2. 基于同一个统一 UNION 日志源按 `created_at DESC` 排序并分页。
3. 同步聚合 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 摘要指标。

在日志表持续增长后，UNION 后外层过滤、计数、排序和指标聚合会放大查询成本。即使前端默认限制为最近 1 天，统一外层排序和摘要聚合仍可能让首屏变慢。

## 根本原因

本缺陷属于日志审计查询设计与数据增长治理不足，具体表现为：

- 查询条件下推不足：当前统一日志源先把三张表标准化为同一列集，再在外层拼接 `WHERE` 条件。`log_type`、`start_time`、`end_time`、`status_code`、`result`、`actor_user_id`、`task_trace_id` 等条件没有按日志类型充分下推到对应单表查询。
- 指定日志类型时仍可能承担统一查询成本：当 `log_type=request`、`usage_event` 或 `audit` 时，理论上可以直接查询单表；当前统一 UNION 形态不利于在所有数据库方言中稳定获得最优计划。
- 排序分页依赖 UNION 后临时排序：本地 SQLite `EXPLAIN QUERY PLAN` 已显示列表分页阶段出现 `USE TEMP B-TREE FOR ORDER BY`，说明单表 `created_at` 索引无法完全消除 UNION 后排序成本。
- 摘要指标与列表首屏强耦合：`LogService.list_logs()` 返回列表时同步调用 `get_metrics()`，而摘要指标会扫描三张日志表。摘要慢会直接拖慢列表首屏。
- 索引覆盖仍偏基础：已有 `created_at`、`actor_user_id + created_at`、`status_code + created_at`、`path + created_at`、`task_trace_id + created_at` 等索引，但常用组合如 `client_type + created_at`、`result + created_at`、`audit_logs(created_at)` 未完整覆盖；SQLite schema 与迁移、MySQL schema 之间也需要继续保持一致。

## 触发条件

- 管理员打开“日志审计”页面，触发默认列表加载。
- 系统已有较多 `request_logs` 和 `usage_events` 数据。
- 管理员使用最近 1 天、最近 7 天、状态、操作者、路径或 request_id / Task Trace ID 等筛选条件。
- 页面需要同时显示摘要指标、分页总数和列表数据。
- 生产 MySQL 数据量明显大于本地 demo 数据，或数据库缓存冷启动、磁盘 IO / CPU 资源受限。

## 分类

- 类型：performance / database-query / admin-observability
- 层级：后端 Repository 查询设计 + 数据库索引 + 管理端首屏加载策略
- 影响端：Web 管理端
- 关联模块：`admin_logs` API、`LogRepository`、`LogService`、日志审计页面

## 已确认事实

- 本地 `data/sqlite/tilesfst.db` 中 `request_logs` 约 2.3 万条、`usage_events` 约 1.5 万条、`audit_logs` 少量记录，已足以暴露查询计划风险。
- 列表分页查询的 SQLite `EXPLAIN QUERY PLAN` 显示 UNION 后外层排序使用临时 B-Tree。
- 摘要指标查询的 SQLite `EXPLAIN QUERY PLAN` 显示会扫描三张日志表。
- 前端默认时间范围为“最近1天”，说明已有基本时间窗口限制；当前问题更偏后端查询形态与指标聚合。

## 待验证项

- 生产 MySQL 中三张日志表的真实行数、近 1 天行数、近 7 天行数和慢查询日志。
- MySQL 对当前 UNION 列表查询、COUNT 查询和 metrics 查询的 `EXPLAIN` / `EXPLAIN ANALYZE` 结果。
- 指定 `log_type` 后是否仍扫描非目标日志表。
- 摘要指标拆分或异步加载后，首屏列表接口耗时可降低多少。
- 补充组合索引后，常用筛选条件在 SQLite 与 MySQL 中的计划是否稳定命中索引。
