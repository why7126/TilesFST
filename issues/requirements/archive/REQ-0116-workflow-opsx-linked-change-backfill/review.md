---
review_id: REV-REQ-0116-001
date: 2026-08-22
participants: []
result: approved
created_at: 2026-08-22 14:32:36
updated_at: 2026-08-22 14:32:36
---

# REQ-0116 需求评审

## 评审结论

评审通过。REQ-0116 范围清晰，聚焦 `req.opsx` 与 `bug.opsx` 两条 linked Change 自动回填链路，边界明确为 Workflow Sync / Issue 文档 / registry / Sprint scope 治理，不涉及业务端 UI、API 或 DB 结构变更。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖 REQ 与 BUG 两条链路、幂等性、registry、主文档、trace 和 Sprint scope。
- [x] 优先级合理，P1；该增强可降低后续 `/opsx-apply <REQ|BUG-id>` 解析和人工评审漂移风险。
- [x] 非 UI 需求，无原型或 UI 横切 AC 门禁。
- [x] 与 `REQ-0089-workflow-subdocument-status-sync` 的差异已说明：本需求聚焦 linked Change 回填一致性。

## 条件通过项

- [ ] 后续 `/req-opsx` 设计阶段需明确多 Change Issue 中 `related_change` 的主值选择策略。
- [ ] 后续实现需补充 REQ/BUG 两条链路的聚焦测试，避免只覆盖单一来源类型。

## 后续建议

1. 先通过 `/sprint-propose` 纳入目标 Sprint。
2. 再执行 `/req-opsx REQ-0116-workflow-opsx-linked-change-backfill` 创建 OpenSpec Change。
3. 实现阶段优先把回填逻辑沉到 Workflow Sync，而不是在 opsx Skill 中分散手工补字段。
