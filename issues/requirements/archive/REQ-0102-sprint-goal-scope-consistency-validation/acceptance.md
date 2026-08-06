---
requirement_id: REQ-0102-sprint-goal-scope-consistency-validation
acceptance_status: passed
created_at: 2026-08-06 11:41:39
updated_at: 2026-08-06 17:17:37
source_change:
source_sprint:
---

# Acceptance

## 功能 AC

- [ ] AC-001 `validate-sprint-scope.py <sprint-id>` 校验 `sprint.md` 的 Sprint 目标编号列表覆盖 `sprint.yaml.requirements` 中的每个 REQ。
- [ ] AC-002 `validate-sprint-scope.py <sprint-id>` 校验目标编号列表覆盖 `sprint.yaml.bugs` 中的每个 BUG。
- [ ] AC-003 对纯 Change 的目标编号列表策略有明确规则：必须出现，或可由关联 REQ/BUG 表达，并在文档中说明。
- [ ] AC-004 校验支持完整 ID 与短编号等价，例如 `REQ-0100-mintlify-docs-site-ia-content-experience` 与 `REQ-0100`。
- [ ] AC-005 当 Scope 中的编号未出现在目标编号列表时，校验失败，并逐条输出具体缺失项。
- [ ] AC-006 缺失项失败信息至少包含 Sprint ID、缺失编号、缺失位置和建议修复方向。
- [ ] AC-007 `--item <id>` 聚焦校验时也必须检查目标编号列表，而不是只检查 `## 2. Scope`。
- [ ] AC-008 校验不得把 `## 2. Scope` 或后续章节中的编号误判为目标编号列表证据。
- [ ] AC-009 `/sprint-propose` 规则明确：新建、追加或修正正式 Scope 后，必须同步目标编号列表和必要要点段落。
- [ ] AC-010 Workflow Sync 规则明确目标编号列表维护边界；如果不自动维护，必须由增强校验兜底发现漂移。
- [ ] AC-011 使用 `sprint-020` / `REQ-0100` 历史案例可复现目标编号列表缺失校验失败。
- [ ] AC-012 目标编号列表完整的 Sprint 样例校验通过，成功路径输出保持摘要化。
- [ ] AC-013 Sprint 四件套中 `sprint.yaml` 仍作为机器事实源，不允许用目标编号列表反向覆盖正式 Scope。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: update-sprint-goal-scope-consistency-validation
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 横切 AC（knowledge-base）

无横切 AC：本需求为 Sprint 工作流与校验脚本治理，不涉及管理端列表、表单、弹窗或媒体上传 UI 场景。
