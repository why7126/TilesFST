---
review_id: REV-REQ-0040-rule-skill-read-summary-reuse-context-budget-001
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
date: 2026-07-16
participants: []
result: approved
created_at: 2026-07-16 09:09:53
updated_at: 2026-07-16 09:09:53
---

# 需求评审

## 评审结论

评审通过。REQ-0040 聚焦将规则/Skill 已读摘要复用机制纳入命令上下文预算治理，来源清晰，承接 sprint-007 复盘行动项 A-004；范围限定在规则、命令 Skill 表述和上下文预算校验，不涉及产品端 UI、API、数据库或 OpenSpec 规格直接变更。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖规则定义、Skill 表述、校验增强、失效条件和安全边界。
- [x] 优先级与依赖合理，可作为 AI usage / Token 治理链路的后续改进。
- [x] 非 UI 类需求，不需要 prototype。
- [x] 与 REQ-0034、REQ-0035、REQ-0037 的关系已说明，不重复既有 AI usage fact source 能力。

## 条件通过项

- [ ] 后续 `/req-opsx` 生成 Change 时，design.md MUST 引用 `knowledge_base_refs` 中的 sprint-007 复盘行动项。
- [ ] 实现阶段 MUST 继续遵守 `rules/agent-context-budget.md`，优先用摘要、命中数和 diff stat 复核，不展开长 Skill 或长规则全文。
- [ ] 实现阶段若引入摘要落盘机制，MUST 先补充脱敏、生命周期、提交边界与清理策略。

## 后续动作

1. `/req-opsx REQ-0040-rule-skill-read-summary-reuse-context-budget`
2. 通过后纳入 Sprint，进入实现与验收。
