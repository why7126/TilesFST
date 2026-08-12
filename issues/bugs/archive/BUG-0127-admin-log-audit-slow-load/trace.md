---
bug_id: BUG-0127-admin-log-audit-slow-load
status: done
lifecycle_stage: archive
created_at: 2026-08-11 08:41:56
updated_at: 2026-08-11 23:53:31
severity: medium
related_requirement:
related_bug:
iteration: sprint-022
openspec_changes:
  - change_id: fix-admin-log-audit-slow-load
    type: fix
    status: archived
---

```yaml
bug_id: BUG-0127-admin-log-audit-slow-load
status: done
lifecycle_stage: review
severity: medium
related_requirement:
related_bug:
iteration: sprint-022
openspec_changes:
  - change_id: fix-admin-log-audit-slow-load
    type: fix
    status: archived
```

# Trace

## 摘要

管理后台日志审计表数据加载很慢，初步判断与日志列表统一 UNION 查询、全量计数排序和同步指标聚合有关。

## 线索

- `/api/v1/admin/logs` 通过 `LogRepository.list_logs()` 查询三类日志统一列表。
- 当前实现先构造 `request_logs`、`usage_events`、`audit_logs` 的 UNION 源，再在外层过滤、计数、排序和分页。
- 列表响应还同步计算 `today_logs`、`api_errors`、`slow_requests`、`sensitive_ops` 摘要指标。
- 前端默认最近 1 天时间范围已降低部分压力，但日志量增长后仍可能因查询下推不足、组合索引不足或指标聚合阻塞导致首屏慢。
- 本地 SQLite explain 已显示列表分页使用临时 B-Tree 排序，摘要指标扫描三张日志表。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:43:17 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-log-audit-slow-load） |
| 2026-08-11 23:43:10 | /opsx-archive | Change `fix-admin-log-audit-slow-load` 已归档，状态同步完成。 |
| 2026-08-11 23:37:35 | /opsx-modify | Change `fix-admin-log-audit-slow-load` 验收返修已同步，后续已归档。 |
| 2026-08-11 09:19:25 | /opsx-apply | Change `fix-admin-log-audit-slow-load` apply 完成，后续已归档。 |
| 2026-08-11 09:06:06 | /bug-opsx | 创建 OpenSpec 修复 Change `fix-admin-log-audit-slow-load`，后续已归档。 |
| 2026-08-11 09:01:25 | /sprint-propose --bug | 纳入 sprint-022 正式范围。 |
| 2026-08-11 08:55:11 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-11 08:54:48 | /bug-review --approve | 评审通过，确认进入后续 Sprint 与修复 Change 流程。 |
| 2026-08-11 08:50:48 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-08-11 08:48:00 | /bug-generate | 根据 capture 与 explore 结论生成 bug.md，状态推进为 draft。 |
| 2026-08-11 08:41:56 | /bug-capture | 记录管理后台日志审计表数据加载慢问题，初步线索来自 `/explore` 只读排查。 |

- 2026-08-11 23:43:10 workflow-sync：状态同步为 done（Change archived）
