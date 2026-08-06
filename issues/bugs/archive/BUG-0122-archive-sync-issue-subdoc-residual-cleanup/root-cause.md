---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
created_at: 2026-08-06 11:41:58
updated_at: 2026-08-06 11:41:58
category: workflow-sync
---

# 直接原因

归档 promote 前的同步流程未把已确认可安全同步的 Issue 子文档状态残留自动清理到闭环态，导致 `capture.md` 中的 `status: captured` 被 `promote-issues-for-archive` 识别为非闭环状态。

# 根本原因

归档链路依赖两段动作串行闭环：先由 Workflow Sync 写入 Issue 主状态与子文档状态，再由 `promote-issues-for-archive` 执行物理归档门禁。当前流程对“可安全 reconcile 的子文档残留”仍偏向报告与人工处理，没有在归档同步阶段形成自动清理或明确的一键修复路径，因此安全残留会继续流入 promote 门禁。

# 触发条件

- Issue 已完成交付闭环，准备从 `review/` 迁移到 `archive/`。
- 子文档仍保留历史阶段状态，例如 `capture.md` 的 `status: captured`。
- Workflow Sync 能判定该残留可安全同步，但归档流程未自动应用 reconcile。
- 随后执行 `promote-issues-for-archive`。

# 分类

`workflow-sync` / `process-automation`。

# 影响判断

该问题不会改变业务数据或线上功能，但会让已闭环 Issue 无法自动归档，迫使操作者额外执行 residual reconcile 或手工排查，增加归档流程中断概率。
