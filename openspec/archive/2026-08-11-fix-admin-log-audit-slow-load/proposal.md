---
change_id: fix-admin-log-audit-slow-load
status: proposed
created_at: 2026-08-11 09:06:06
updated_at: 2026-08-11 09:06:06
source_bug: BUG-0127-admin-log-audit-slow-load
related_sprint: sprint-022
---

# 修复管理后台日志审计列表加载慢

## 背景

`BUG-0127-admin-log-audit-slow-load` 已确认管理后台“日志审计”页面首屏、筛选和翻页时加载偏慢。当前后端列表接口会基于 `request_logs`、`usage_events`、`audit_logs` 三张表构造统一 UNION 源，再在外层执行过滤、`COUNT(*)`、`ORDER BY created_at DESC` 和分页；同时列表响应同步计算 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 摘要指标。

本地 SQLite demo 数据已能暴露查询计划风险：列表分页阶段出现 `USE TEMP B-TREE FOR ORDER BY`，摘要指标查询扫描三张日志表。生产 MySQL 数据量更大时，该查询形态会放大管理员排障等待时间，并影响请求日志、行为事件、审计操作和 Task Trace 的定位效率。

## 变更内容

- 优化 `/api/v1/admin/logs` 列表查询路径，将高选择性筛选条件下推到对应日志表查询，减少 UNION 后外层过滤、计数和排序成本。
- 指定 `log_type=request`、`log_type=usage_event` 或 `log_type=audit` 时，优先走对应单表或等价低成本查询路径，避免无必要三表扫描。
- 调整摘要指标获取策略，使指标聚合不再明显阻塞日志列表首屏；可采用独立接口、异步加载、缓存或低成本聚合，但必须保持口径可解释。
- 补齐 SQLite 与 MySQL 的日志表索引、schema、迁移和数据库文档，覆盖 `client_type + created_at`、`result + created_at`、`audit_logs(created_at)` 等常用筛选场景。
- 补充后端查询结果等价测试、权限测试、索引或查询计划保护测试，并在验收中记录优化前后耗时与查询计划证据。

## 不做范围

- 不新增日志采集业务事件，不改变请求日志、行为事件或审计日志的写入语义。
- 不移除日志详情、Request Snapshot、Task Trace 关联、操作者筛选或现有分页字段。
- 不引入独立搜索引擎、日志中间件、数据仓库或外部 APM 产品。
- 不在本 Change 中实现日志保留周期、冷归档、分区表或异步离线统计系统；若生产数据规模需要这些能力，应另建 REQ/BUG。
- 不降低系统管理员权限边界，不向非管理员开放日志审计数据。

## 回滚方案

- 若单表查询或条件下推导致结果语义偏差，可临时回退到原统一 UNION 查询，但必须保留 BUG-0127 的验收阻塞记录。
- 若摘要指标拆分或缓存导致指标口径异常，可临时隐藏指标延迟态或回退同步指标计算，但列表首屏慢风险需重新评估。
- 若新增索引在生产 MySQL 造成迁移耗时或锁表风险，应先停止发布，回滚迁移计划或改为维护窗口执行，并保留现有 schema。
- 回滚后必须重新运行日志列表筛选、分页、权限和脱敏测试，确保排障入口仍可用。
