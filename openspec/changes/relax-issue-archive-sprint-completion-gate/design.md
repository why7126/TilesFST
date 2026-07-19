## Context

当前 `promote-issues-for-archive.py --change <change-id>` 的主门禁已经按单 Issue 维度判断：issue 位于 `review/`，trace status 为 done，且关联 Change 全部 archived 即可 promote。但当子文档存在残留状态时，推荐的 `sync-workflow-status.py --event req.archive --reconcile-issue-status-residuals --apply-reconcile` 会调用 `issue_reconcile_blockers()`，其中额外检查所有关联 Sprint 必须 `completed`。

这个额外检查把 Sprint 容器生命周期混入了单 Issue 归档：一个 Sprint 包含多个 Change 时，已归档的 REQ/BUG 被未完成的同 Sprint 其他项阻断，造成物理目录与 trace 状态不一致。

## Goals / Non-Goals

**Goals:**

- 允许 `/opsx-archive <change-id>` 在关联 Issue 的所有 Change 已 archived 后，完成该 Issue 子文档 reconcile 与 `review/` → `archive/` promote。
- 保留 `/sprint-archive` 的整体 readiness gate，不放宽 Sprint 完成条件。
- 让 promote/reconcile 报告继续阻断未闭环 issue、未 archived change 和子文档非闭环残留。

**Non-Goals:**

- 不改变 Sprint 目录归档规则。
- 不改变 Change archive 的 OpenSpec CLI 行为。
- 不自动归档同 Sprint 中尚未完成的其他 REQ/BUG。

## Decisions

### D1. 从子文档 reconcile blocker 中移除 Sprint completed 检查

`issue_reconcile_blockers()` 只判断 issue trace 是否 closed、关联 Change 是否全部 archived。Sprint 是否 completed 是 `/sprint-archive` 的聚合门禁，不属于单 Issue 子文档状态修复的前置条件。

### D2. 保持 promote 脚本的多 Change Issue 保护

`promote-issues-for-archive.py` 已通过 `pending_change_ids()` 阻断仍有关联 active Change 的 Issue。这个检查足以防止多 Change REQ/BUG 提前归档。

### D3. 用测试固定未完成 Sprint 场景

新增测试覆盖：Issue trace 已 done、关联 Change 已 archived、存在 planning/in_progress Sprint 时，reconcile 仍可写入子文档残留状态。未闭环 issue 仍必须被阻断。

## Risks / Trade-offs

- [Risk] Sprint scope 表仍引用已迁入 archive 的 Issue 路径。→ Mitigation: Workflow Sync 和路径解析应通过 issue id 解析阶段目录；Sprint archive 后旧路径残留检查继续负责整 Sprint 收尾。
- [Risk] 多 Change Issue 被提前迁移。→ Mitigation: 保留“全部关联 Change 已 archived”门禁。
- [Risk] 子文档残留被错误改为 done。→ Mitigation: reconcile 仍要求 Issue 主 trace 已 closed，且 linked Change 已 archived。

## Migration Plan

1. 更新 OpenSpec delta spec。
2. 修改 reconcile blocker、规则和 Skill 文案。
3. 补充测试并运行 focused tests。
4. 对当前 REQ-0039 重跑 reconcile/promote，验证 Sprint 未 completed 时可完成单 Issue 归档。
