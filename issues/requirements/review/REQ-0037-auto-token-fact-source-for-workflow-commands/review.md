---
review_id: REV-REQ-0037-001
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
date: 2026-07-12 09:59:37
participants:
  - product
result: approved
created_at: 2026-07-12 09:59:37
updated_at: 2026-07-12 09:59:37
---

# REQ-0037 需求评审

## 评审结论

评审通过。该需求承接 REQ-0034 的 AI Token 使用量事实源能力和 REQ-0035 的 Sprint close / exps 默认流程接入，进一步把事实源构建前移到 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令后置步骤。范围边界清晰，验收标准覆盖自动触发、统一 hook、command run 明细、Sprint snapshot、脱敏安全、失败降级、技能规则同步和测试校验，可进入 `/req-opsx`。

## 评审检查清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 范围清晰，Out of Scope 明确 | 通过 | PRD 明确包含工作流命令后置 usage hook、command run 明细、Sprint snapshot 刷新、失败降级与 skill/rule 同步；明确排除 Codex 客户端改造、原始 session 入仓、费用核算、UI 和历史全量回填。 |
| 验收标准可测试 | 通过 | acceptance.md 已按自动触发、统一 hook、command run、snapshot、脱敏、失败降级、技能同步和测试校验分组，均可落到脚本、文档或测试验收。 |
| 优先级与依赖合理 | 通过 | P1 合理；依赖 REQ-0034 的事实源口径和 REQ-0035 的 snapshot close/exps 流程，目标是减少每个命令后的用量事实遗漏。 |
| UI 类原型或实现策略已决 | N/A | 非 UI 的 Agent 工作流 / 脚本治理需求，无需 prototype；knowledge-base gate 为 N/A。 |
| 无与现有 REQ 重复未说明 | 通过 | 与 REQ-0034、REQ-0035 关系已说明：REQ-0034 解决事实源能力，REQ-0035 解决 Sprint close/exps 默认消费，本需求解决每个工作流命令后的自动构建。 |

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md MUST 明确统一 post-command hook 与 Workflow Sync 的职责边界，避免让 Workflow Sync 直接持久化敏感 session 内容。
- [ ] 后续实现 MUST 保持自动构建失败默认不阻断主命令，并清晰区分 `actual`、`estimated_fallback`、`unavailable`。
- [ ] 后续实现 MUST 复用 REQ-0034 的脱敏边界，不得写入原始 prompt、系统/developer 指令、本机绝对路径或工具输出正文。
- [ ] 后续实现 MUST 避免在每个 source-command skill 中复制长逻辑，优先使用统一 hook 或共享规则入口。

## 下一步

1. `/req-opsx REQ-0037-auto-token-fact-source-for-workflow-commands`
2. 纳入 Sprint 前确认 REQ 与对应 Change 已进入正式 Sprint scope。
