---
bug_id: BUG-0127-admin-log-audit-slow-load
status: done
created_at: 2026-08-11 08:41:56
updated_at: 2026-08-11 23:43:16
severity_hint: medium
environment: prod
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

管理后台日志审计表数据加载很慢，进入日志审计页面或切换筛选条件后首屏等待时间明显偏长。

# 复现步骤

1. 使用系统管理员账号进入管理后台。
2. 打开“日志审计”页面。
3. 保持默认筛选条件，或切换日志类型、时间范围、状态、操作者、Task Trace ID、路径 / Request ID 等筛选项。
4. 观察日志表格、摘要指标和分页数据的加载耗时。

# 期望 vs 实际

- 期望：日志审计页面在默认时间范围和常用筛选条件下能快速返回首屏数据，分页、筛选和摘要指标不应因日志量增长明显卡顿。
- 实际：日志审计表加载很慢；初步怀疑列表查询将 `request_logs`、`usage_events`、`audit_logs` 做 UNION 后再全量计数、排序和分页，同时列表接口还同步聚合摘要指标，导致首屏查询成本过高。

# 影响范围

- 管理后台日志审计页面首屏加载、筛选、分页体验。
- 管理员按 request_id、Task Trace ID、操作者、状态等条件排查问题的效率。
- 后端 `/api/v1/admin/logs` 日志列表接口与统一日志查询 Repository。
- SQLite 本地/demo 与 MySQL 生产环境的日志表索引、查询计划和数据增长策略。

# 初步线索

- `LogRepository.list_logs()` 先对 `request_logs`、`usage_events`、`audit_logs` 组成统一 UNION 源，再执行 `COUNT(*)` 和 `ORDER BY created_at DESC LIMIT/OFFSET`。
- UNION 源包含 `LEFT JOIN users` 与 `LEFT JOIN task_traces`，在日志量增长后容易放大计数和排序成本。
- `LogService.list_logs()` 每次返回列表时还会调用 `get_metrics()`，额外聚合今日日志、API 错误、慢请求和敏感操作摘要。
- 前端默认时间范围为最近 1 天，说明页面已经有基本限流，但仍可能因为查询下推不足、组合索引不足或指标聚合同步执行导致首屏慢。
- 日志审计页面加载自身也会产生请求日志，长期会继续增加 `request_logs` 数据量。

# 建议验收或复现要点

- [ ] 在接近生产日志量的数据集上复现默认打开日志审计页耗时，并记录 `/api/v1/admin/logs` 响应耗时。
- [ ] 分别采集 SQLite 与 MySQL 下默认查询、按日志类型、按时间范围、按状态、按 request_id / Task Trace ID 筛选的查询计划。
- [ ] 验证列表查询是否将 `log_type`、`start_time`、`end_time` 等高选择性条件下推到各日志表。
- [ ] 验证摘要指标是否仍阻塞首屏列表返回。
- [ ] 修复后默认首屏、筛选、分页在目标数据量下达到可接受响应时间，并补充回归测试或性能阈值测试。

# 附件

- 暂无。
