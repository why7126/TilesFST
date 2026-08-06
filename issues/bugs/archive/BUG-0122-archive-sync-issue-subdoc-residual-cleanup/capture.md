---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
status: done
created_at: 2026-08-06 11:29:58
updated_at: 2026-08-06 12:01:54
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

归档同步阶段未自动清理已确认安全的 Issue 子文档状态残留，导致 `promote-issues-for-archive` 被 `capture.md` 中残留的 `captured` 状态阻断。

# 复现步骤

1. 对已完成闭环且可归档的 Issue 执行归档同步流程。
2. Workflow Sync 已能识别 Issue 子文档中存在可安全同步的状态残留。
3. 继续执行 `promote-issues-for-archive`。

# 期望 vs 实际

- 期望：归档同步阶段自动处理已确认安全的子文档状态残留，或在 promote 前完成必要 reconcile，使已闭环 Issue 可继续物理归档。
- 实际：`capture.md` 仍残留 `status: captured`，`promote-issues-for-archive` 触发 Issue 子文档状态门禁并阻断归档。

# 附件

暂无。
