---
change_id: fix-archive-sync-issue-subdoc-residual-cleanup
status: proposed
created_at: 2026-08-06 11:52:40
updated_at: 2026-08-06 11:52:40
related_bug: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
iteration: sprint-021
---

# 提案

## 背景

`BUG-0122-archive-sync-issue-subdoc-residual-cleanup` 记录了一个归档链路缺陷：Issue 已完成闭环且 Workflow Sync 可确认子文档状态残留可安全同步时，归档同步阶段没有自动处理该残留，导致 `promote-issues-for-archive` 被 `capture.md` 的 `captured` 状态阻断。

该问题不会影响线上业务运行，但会让已闭环 REQ/BUG 无法顺畅从 `review/` 迁入 `archive/`，迫使操作者额外执行 residual reconcile 或手工排查。

## 变更内容

- 在归档同步或 promote 前置流程中处理已确认安全的 Issue 子文档状态残留。
- 保留人工判断门禁：缺少闭环证据、验收结论或语义不明的残留不得自动写入。
- 确保 `promote-issues-for-archive` 不再被已安全确认的 `capture.md status: captured` 残留误阻断。
- 补充幂等、审计摘要和聚焦回归测试。

## 影响范围

- 影响 `scripts/sync-workflow-status.py`、`scripts/promote-issues-for-archive.py` 或其共享 workflow sync helper 的归档状态处理。
- 影响 Issue 子文档 drift / residual reconcile 报告与摘要。
- 不涉及 API、数据库、Web、小程序、管理端运行时代码、Orval 或 Docker Compose。

## 回滚方案

- 若自动 reconcile 行为引入误写风险，回滚自动 apply 部分，保留 dry-run 与明确报告。
- 保留现有 `--reconcile-issue-status-residuals --dry-run` / `--apply-reconcile` 手动路径作为退路。
- 回滚后必须重新运行归档门禁相关测试，确认不会绕过未闭环 Issue。

## 追溯

- BUG：`issues/bugs/archive/BUG-0122-archive-sync-issue-subdoc-residual-cleanup/`
- Sprint：`iterations/archive/sprint-021/`
