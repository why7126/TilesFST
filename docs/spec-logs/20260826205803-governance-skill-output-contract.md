---
purpose: 命令最终输出契约治理日志
content: 记录下一步与待用户决策处理去重、占位模板移除和校验脚本扩展
source: /spec-opt refine-skill-final-output-contract
update_method: 本日志为单次治理事实记录；后续同类调整新增日志并同步 CHANGELOG
created_at: 2026-08-26 20:58:03
updated_at: 2026-08-26 20:58:03
---

# 命令最终输出契约治理日志

## 迭代目标

降低命令最终回复中【下一步】与【待用户决策/处理】重复、尖括号占位模板被原样输出、通用 BUG 示例误导非 BUG 命令，以及规范语气泄漏到用户可见回复的风险。

## 变更摘要

- 批量更新 `.agents/skills/*/SKILL.md` 的 Final Output Contract：改为三态判定规则，移除可被照抄的最终输出占位模板和通用 BUG 示例。
- 补强 `/sprint-propose`、`/req-opsx`、`/bug-opsx`、`/upgrade-plan`、`/upgrade-validate` 命令族正反例，明确“有唯一下一步时待处理为无”“被用户决策阻塞时下一步为暂无可推进下一步”。
- 更新 `AGENTS.md`、`rules/agent-context-budget.md` 与 `docs/README.md` 的入口摘要，不再展示可复制占位模板。
- 扩展 `scripts/validate-agent-context-budget.py`，增加最终输出契约卫生校验，覆盖占位模板、通用 BUG 示例、重复诱因和规范语气泄漏风险。
- 回填 `openspec/changes/refine-skill-final-output-contract/` 的验收、测试计划和 trace。

## 影响范围

| 范围 | 影响 |
|---|---|
| `.agents/skills` | 仅调整命令技能说明和输出示例。 |
| `AGENTS.md` | 更新命令完成输出契约摘要。 |
| `rules/agent-context-budget.md` | 增加输出契约卫生与脚本校验说明。 |
| `docs/README.md` | 更新 AI 命令入口提示。 |
| `scripts/validate-agent-context-budget.py` | 增加契约卫生检查。 |
| OpenSpec / Sprint | `refine-skill-final-output-contract` 已纳入 `sprint-026`。 |

## 关键决策

- 已采纳统一三态输出规则：减少命令之间的文案漂移，同时保留命令族专属正反例。
- 已采纳脚本化拦截：避免后续技能更新重新引入旧模板和通用示例。
- 未采纳逐命令完全定制契约：维护成本高，且容易产生新的不一致。

## 验证结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `openspec validate refine-skill-final-output-contract --strict`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused governance files>`：通过并返回 7 条启发式 warning，未阻断。
- `python scripts/sync-workflow-status.py --event opsx.apply --change refine-skill-final-output-contract --sprint auto`：通过，解析到 `sprint-026`，无错误。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change refine-skill-final-output-contract --sprint sprint-026 --json`：通过，`usage_mode=actual`，`warning_count=0`。

## 影响声明

- API：不影响。
- DB：不影响。
- Web：不影响业务运行时代码。
- 小程序：不影响业务运行时代码。
- 管理端：不影响业务运行时代码。
- Orval：不需要。
- Docker Compose：不需要业务环境验证。

## 后续建议

后续新增或修改命令技能时，先运行 `python scripts/validate-agent-context-budget.py`，确认没有重新引入最终输出占位模板、通用 BUG 示例或【下一步】与【待用户决策/处理】重复诱因。
