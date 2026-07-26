## Why

`/opsx-archive <change-id>` 已能完成单个 Change 的 OpenSpec 归档，但 issue 子文档 reconcile 仍要求关联 Sprint 已 `completed`，导致已交付的 REQ/BUG 在 Sprint 未结束时无法迁入 `issues/**/archive/`。这会让 Change 已 archived、Issue trace 已 done、物理目录仍在 review/ 的状态长期不一致。

## What Changes

- 调整 issue archive promote 与子文档状态 reconcile 门禁：单个 REQ/BUG 只要求自身 trace 已闭环、关联的全部 Change 已 archived，不再要求所属 Sprint 已 completed。
- 保留 `/sprint-archive` 的整体门禁：Sprint 归档仍必须确认 Sprint scope、Change archive、tasks 与 issue promote 全部闭环。
- 更新 `rules/issues-lifecycle.md`、workflow sync / opsx archive Skill 文案和相关测试，明确区分“单 Issue 归档”和“Sprint 整体归档”。
- 修复当前 `promote-issues-for-archive.py --change <change-id>` 被未完成 Sprint 间接阻断的问题。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `agent-workflow-tooling`: 调整 Issue 归档子文档状态一致性门禁，使单 Issue 归档不依赖 Sprint completed，同时保留 Sprint archive 总门禁。

## Impact

- 影响脚本：`scripts/workflow_sync/issue_status_residuals.py`。
- 影响测试：`tests/test_issue_status_residuals.py`。
- 影响规范与技能：`rules/issues-lifecycle.md`、`.agents/skills/workflow-sync/SKILL.md`、`.agents/skills/opsx-archive/SKILL.md`。
- 不影响业务代码、API、数据库、Orval、Docker Compose、小程序或 Web 运行时代码。
