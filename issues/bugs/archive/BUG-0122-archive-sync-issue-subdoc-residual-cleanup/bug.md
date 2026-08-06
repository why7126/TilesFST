---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
title: 归档同步阶段未自动清理安全 Issue 子文档状态残留
severity: medium
status: done
owner:
discovered_at: 2026-08-06 11:29:58
environment: local
related_requirement:
related_change: fix-archive-sync-issue-subdoc-residual-cleanup
created_at: 2026-08-06 11:50:22
updated_at: 2026-08-06 12:01:48
---

# 现象

归档同步阶段未自动清理已确认安全的 Issue 子文档状态残留，导致 `promote-issues-for-archive` 被 `capture.md` 中残留的 `captured` 状态阻断。

# 复现

1. 对已完成闭环且可归档的 Issue 执行归档同步流程。
2. Workflow Sync 已能识别 Issue 子文档中存在可安全同步的状态残留。
3. 继续执行 `promote-issues-for-archive`。
4. 观察归档 promote 结果。

# 期望

归档同步阶段应自动处理已确认安全的子文档状态残留，或在 promote 前完成必要 reconcile，使已闭环 Issue 可继续物理归档。

# 实际

`capture.md` 仍残留 `status: captured`，`promote-issues-for-archive` 触发 Issue 子文档状态门禁并阻断归档。

# 影响范围

- 影响 `/opsx-archive` 或 `/sprint-archive` 后的 Issue 物理归档流程。
- 影响已闭环 REQ/BUG 从 `review/` 迁移到 `archive/` 的自动化可靠性。
- 不直接影响业务前后端功能，但会导致流程文档状态与归档目录状态不一致。

# 严重等级说明

严重等级为 `medium`。该问题不阻断业务运行，但会阻断已闭环 Issue 的自动归档，使归档操作者必须手动运行 reconcile 或排查子文档状态残留，增加发布/归档流程风险。
