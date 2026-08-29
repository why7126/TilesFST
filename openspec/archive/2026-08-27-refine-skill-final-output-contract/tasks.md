## 1. OpenSpec 与 Sprint 范围

- [x] 1.1 创建 `refine-skill-final-output-contract` OpenSpec Change。
- [x] 1.2 将纯治理 Change 纳入 `sprint-026` 的 `changes[]` 和 `scope_estimates[]`。
- [x] 1.3 补齐 proposal、design、tasks、trace、acceptance、test-plan 和 delta spec。

## 2. 输出契约与技能文案

- [x] 2.1 批量更新 `.agents/skills/*/SKILL.md` 的 Final Output Contract，移除可被原样输出的尖括号占位模板和通用 BUG 示例。
- [x] 2.2 为 `/sprint-propose` 补强去重正反例，移除“下一步已列命令又要求确认是否执行同一命令”的示例。
- [x] 2.3 为 `/req-opsx` 与 `/bug-opsx` 补强 Sprint 已解析、Sprint 未确定、范围需拆分或 hotfix 路径需确认时的输出边界。
- [x] 2.4 为 `/upgrade-plan` 与 `/upgrade-validate` 补齐完整三态输出契约和人工复核边界。
- [x] 2.5 更新 `AGENTS.md`、`rules/agent-context-budget.md` 与 `docs/README.md` 的摘要说明。

## 3. 校验脚本

- [x] 3.1 扩展 `scripts/validate-agent-context-budget.py`，检查尖括号占位模板、通用 BUG 示例、重复诱因和规范语气泄漏风险。
- [x] 3.2 运行脚本自校验，确认新增规则能覆盖本次治理目标。

## 4. 治理日志与验证

- [x] 4.1 写入 `docs/spec-logs/YYYYMMDDhhmmss-governance-skill-output-contract.md`。
- [x] 4.2 更新 `docs/spec-logs/CHANGELOG.md`。
- [x] 4.3 运行 `python scripts/validate-agent-context-budget.py`。
- [x] 4.4 运行 `python scripts/validate-openspec-language.py` 和 `openspec validate refine-skill-final-output-contract --strict`。
- [x] 4.5 运行 `python scripts/validate-directory-structure.py`。
- [x] 4.6 运行 Workflow Sync 与 AI Usage Hook，确认 `refine-skill-final-output-contract` 与 `sprint-026` 状态一致。
