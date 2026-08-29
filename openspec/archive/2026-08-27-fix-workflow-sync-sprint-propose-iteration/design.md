---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 设计说明

## 方案

Workflow Sync 已在 `derive_issue(issue, derived_changes, sprint)` 中根据 `sprint.requirements` / `sprint.bugs` 将已纳入 Sprint 的 Issue 状态推导为 `in_sprint`。本次只在写回 `trace.md` 时补齐机器事实字段：

- `patch_issue_trace()` 增加可选 `sprint_id` 参数。
- 当当前 Issue 存在于已解析 Sprint 的正式范围中时，将 frontmatter 与 fenced YAML block 的 `iteration` 写成该 Sprint ID。
- 当 Issue 不属于 Sprint 正式范围时，不新增或覆盖 `iteration`，避免把 skipped/unresolved 的自动解析误写为事实。

## 取舍

- 不把 `sprint.propose` 加入 `ISSUE_SCOPED_EVENTS`，因为该事件的事实源是 Sprint scope，不应通过 focused Issue 反向解析 Sprint。
- 不在 `add-sprint-scope-item.py` 中写 Issue trace；该脚本只维护 `sprint.yaml` 机器范围，状态派生仍由 Workflow Sync 统一处理。

## 验证责任

- 回归测试覆盖 REQ trace 的 `status` 与 `iteration` 同步。
- `validate-sprint-scope.py` 继续负责确认 Sprint 人读视图和机器范围一致。

