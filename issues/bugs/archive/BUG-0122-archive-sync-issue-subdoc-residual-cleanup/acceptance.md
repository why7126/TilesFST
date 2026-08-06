---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
acceptance_status: passed
created_at: 2026-08-06 11:41:58
updated_at: 2026-08-06 17:17:37
---

# 验收标准

## AC-001 自动处理安全残留

给定 Issue 已完成闭环且 Workflow Sync 可确认子文档状态残留可安全同步，当执行归档同步或归档 promote 前置流程时，应自动将安全残留同步为闭环态，或输出明确且可执行的一键 apply-reconcile 步骤。

## AC-002 保留人工判断门禁

给定子文档状态残留缺少闭环证据、验收结论或语义不明，当执行归档同步时，系统不得自动修改该残留，应报告 warning/blocker 并阻断 promote。

## AC-003 promote 不再被已安全确认的 captured 残留阻断

给定 `capture.md` 仅残留可安全同步的 `status: captured`，当完成归档同步后再次执行 `promote-issues-for-archive`，应不再因该残留触发 Issue Subdocument Status Gate。

## AC-004 幂等性

对同一已闭环 Issue 重复执行归档同步或 residual reconcile，不应重复写入无意义变更；再次执行应报告 no delta 或等价摘要。

## AC-005 审计输出

同步报告应保留可安全同步、需人工判断、缺验收结果、缺 trace/交付证据、不建议自动修复项的分类摘要，便于归档操作者判断风险。

# 验收结果回填

待修复后回填。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-archive-sync-issue-subdoc-residual-cleanup
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

