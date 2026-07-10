---
bug_id: BUG-0056-sprint-archive-incomplete-tasks-gate
title: /sprint-archive 未完成 tasks 仍可归档
severity: high
status: draft
created_at: 2026-07-04 15:04:22
updated_at: 2026-07-04 15:04:22
owner: AI
discovered_at: 2026-07-04 15:04:22
environment: local
related_requirement:
related_change:
---

# 缺陷说明

`/sprint-archive` 应在归档 Sprint 前确认 `sprint.yaml` 中所有 change 的 `tasks.md` 均已完成。当前流程只有文档文字说明，没有可执行脚本作为硬门禁，实际执行时可能遗漏未完成任务并继续归档。

# 影响范围

- Sprint 归档质量门禁失效。
- `openspec/changes/archive/` 与 `iterations/archive/` 可能记录尚未完成的 change。
- 后续 `/sprint-exps` 与发布判断会基于错误的 completed 状态沉淀经验或发布依据。

# 严重等级说明

严重等级为 high：该缺陷不直接影响业务运行时，但会破坏 OpenSpec/Sprint 工作流的质量闭环，并可能把未完成开发误判为已完成。
