---
requirement_id: REQ-0102-sprint-goal-scope-consistency-validation
created_at: 2026-08-06 11:41:39
updated_at: 2026-08-06 11:41:39
---

# User Stories

## US-001 产品负责人查看完整 Sprint 目标编号

作为产品负责人，我希望 `sprint.md` 的 Sprint 目标编号列表覆盖正式 Scope 中的全部 REQ/BUG/必要 Change，以便快速理解当前 Sprint 的真实范围。

验收要点：

- 目标编号列表包含 `sprint.yaml.requirements` 中的每个 REQ。
- 目标编号列表包含 `sprint.yaml.bugs` 中的每个 BUG。
- 纯 Change 是否必须出现有明确规则，不靠人工猜测。

## US-002 评审者发现目标编号遗漏

作为评审者，我希望运行 `validate-sprint-scope.py` 时能发现 Scope 中存在、目标编号列表中缺失的编号，以便在 Sprint 提案或归档前修复人读文档。

验收要点：

- `sprint-020` / `REQ-0100` 的历史遗漏场景能被校验失败捕获。
- 失败信息列出具体缺失编号和缺失位置。
- `--item` 聚焦校验时也覆盖目标编号列表。

## US-003 AI Agent 在追加 Sprint Scope 后完成一致性闭环

作为 AI Agent，我希望 `/sprint-propose` 在新增或修正 Sprint Scope 后必须同步目标编号列表并运行增强校验，以便不留下机器 Scope 正确但人读摘要遗漏的文档漂移。

验收要点：

- `/sprint-propose` 规则要求新增/修正 Scope 后同步目标编号列表。
- Workflow Sync 规则清楚说明目标编号列表是否由 sync 自动维护。
- 校验失败时命令不能把 Sprint 规划视为完成。

## US-004 流程维护者保护 Sprint 四件套一致性

作为流程维护者，我希望 Sprint 四件套中的机器事实源和人读入口有清晰边界，以便后续维护校验脚本、Workflow Sync 和 Skill 时不会重复引入漂移。

验收要点：

- `sprint.yaml` 仍是机器事实源。
- `sprint.md` 目标编号列表、Scope 主表和派生分组表表达同一正式范围。
- `acceptance-report.md` 与 `release-note.md` 不承担目标编号列表职责，但不应与 Scope 冲突。
