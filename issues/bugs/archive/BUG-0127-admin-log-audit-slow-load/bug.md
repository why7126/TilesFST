---
bug_id: BUG-0127-admin-log-audit-slow-load
title: 管理后台日志审计表数据加载很慢
severity: medium
status: done
owner:
discovered_at: 2026-08-11 08:41:56
environment: prod
related_requirement:
related_change: fix-admin-log-audit-slow-load
created_at: 2026-08-11 08:48:00
updated_at: 2026-08-11 23:43:10
lifecycle_stage: review
iteration: sprint-022
---

# 现象

管理后台“日志审计”页面的数据表加载很慢。进入页面、切换筛选条件或翻页时，日志表格、分页总数和摘要指标等待时间明显偏长，影响管理员定位请求日志、行为事件、审计操作和 Task Trace 的效率。

# 复现步骤

1. 使用系统管理员账号登录管理后台。
2. 打开“日志审计”页面。
3. 保持默认“最近1天”时间范围，观察首屏日志列表加载耗时。
4. 切换日志类型、状态 / 结果、操作者、Task Trace ID、路径 / Request ID 等筛选项。
5. 观察日志表格、总数、分页和摘要指标是否持续出现明显等待。

# 期望 vs 实际

## 期望

- 日志审计页面默认首屏能快速返回最近日志。
- 常用筛选和分页不应随着日志量增长出现明显卡顿。
- 摘要指标不应阻塞列表首屏数据返回。
- 管理员能在可接受时间内按 request_id、Task Trace ID、操作者、状态和路径排查问题。

## 实际

- 日志审计表数据加载慢，首屏和筛选后的等待时间偏长。
- 当前后端日志列表查询会先将 `request_logs`、`usage_events`、`audit_logs` 三张表组成统一 UNION 源，再在外层执行过滤、`COUNT(*)`、`ORDER BY created_at DESC` 和分页。
- 列表响应还同步计算 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 摘要指标，进一步放大首屏查询成本。

# 影响范围

- 管理后台日志审计页面首屏加载、筛选、分页和详情入口效率。
- 后端 `/api/v1/admin/logs` 列表接口。
- `LogRepository.list_logs()`、`LogRepository.get_metrics()` 和统一日志查询 SQL。
- SQLite 本地 / demo 环境与 MySQL 生产环境的日志表索引、查询计划和数据增长策略。
- 管理员排查 API 错误、慢请求、上传任务和用户操作行为的响应效率。

# 严重等级说明

严重等级：`medium`。

该问题影响管理端排障和运维效率，且日志表会随系统使用持续增长，具备累积放大风险。但当前没有证据表明核心业务写入、店主展示端或小程序用户链路不可用，因此暂定为中等严重度。若生产环境已出现日志审计页超时、无法完成排障或影响事故响应，可在评审阶段提升为 `high`。

# 初步证据

- 本地 `data/sqlite/tilesfst.db` 中已有 `request_logs=23387`、`usage_events=15350`、`audit_logs=13`，可用于轻量复现查询计划问题。
- 当前列表分页查询的 SQLite `EXPLAIN QUERY PLAN` 显示 UNION 后外层排序会使用临时 B-Tree：`USE TEMP B-TREE FOR ORDER BY`。
- 当前摘要指标查询的 SQLite `EXPLAIN QUERY PLAN` 显示会扫描 `request_logs`、`usage_events`、`audit_logs` 三张日志表。
- 前端 `LogAuditPage` 默认时间范围为最近 1 天，说明问题并非完全由无限时间范围导致；后端查询下推不足、统一排序和同步指标聚合仍是主要疑点。

# 初步修复方向

- 将高选择性筛选条件下推到各日志表子查询，减少 UNION 后外层过滤和排序的数据量。
- 根据 `log_type` 选择单表查询，避免已指定日志类型时仍执行三表 UNION。
- 将摘要指标拆成独立接口、异步加载或缓存，避免阻塞列表首屏。
- 补齐常用筛选组合索引，例如 `client_type + created_at`、`result + created_at`、`audit_logs(created_at)`，并同步 SQLite / MySQL schema、迁移和数据库文档。
- 补充查询结果等价测试、索引存在性测试或查询计划保护，防止性能回退。

# 验收要点

- [ ] 默认进入日志审计页时，`/api/v1/admin/logs` 在目标数据量下达到可接受响应时间。
- [ ] 按日志类型、时间范围、状态、操作者、request_id、Task Trace ID 筛选时，列表结果与当前语义一致。
- [ ] 指定 `log_type` 时避免无必要三表 UNION。
- [ ] 列表首屏不被摘要指标聚合明显阻塞。
- [ ] SQLite 与 MySQL schema / migration / docs 中的日志索引保持一致。
- [ ] 后端测试覆盖列表筛选、分页、摘要指标和性能相关查询形态。
