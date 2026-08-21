---
purpose: review 命令默认通过治理优化日志
content: 调整 req-review 与 bug-review 无 flag 默认 approve，并同步正向命令提示
source: /spec-opt default-review-approve-command
update_method: 本日志作为单次治理迭代事实源；后续同类优化新建日志并维护 CHANGELOG
created_at: 2026-08-21 13:45:41
updated_at: 2026-08-21 13:52:00
---

# review 命令默认通过治理优化日志

## 迭代目标

降低 `/req-review` 与 `/bug-review` 高频正向评审路径的输入成本，将无 flag 调用定义为默认通过，反向评审结果继续要求显式 flag。

## 变更摘要

- `/req-review REQ-xxxx` 默认等价于评审通过，`--reject` 与 `--defer` 仍为显式反向结果。
- `/bug-review BUG-xxxx` 默认等价于评审通过，`--reject`、`--defer` 与 `--wont-fix` 仍为显式反向结果。
- 正向命令示例从带 `--approve` 调整为无 flag，避免后续输出继续要求重复参数。
- OpenSpec Change 和 `sprint-024` scope 已承载本次纯治理变更。

## 影响范围

| 维度 | 影响 |
|---|---|
| API | 无 |
| DB | 无 |
| Web | 无 |
| 小程序 | 无 |
| 管理端 | 无 |
| Orval | 无 |
| Docker | 无 |
| 治理资产 | `.agents/skills/{req-review,bug-review}/SKILL.md`、相关 Skill 示例、`AGENTS.md`、`rules/{requirement-management,bug-management,issues-lifecycle}.md`、`openspec/changes/default-review-approve-command/`、`iterations/change/sprint-024/sprint.yaml`、`docs/spec-logs/` |

## 更新文件

- `.agents/skills/req-review/SKILL.md`
- `.agents/skills/bug-review/SKILL.md`
- `.agents/skills/*/SKILL.md` 中的正向评审示例
- `AGENTS.md`
- `rules/requirement-management.md`
- `rules/bug-management.md`
- `rules/issues-lifecycle.md`
- `openspec/changes/default-review-approve-command/`
- `iterations/change/sprint-024/sprint.yaml`
- `docs/spec-logs/CHANGELOG.md`

## 关键决策

| 决策项 | 结论 |
|---|---|
| 已采纳原因 | 评审命令的高频正向路径通常就是通过，默认 approve 可减少重复参数与追问。 |
| 未采纳原因 | 未移除 `--approve` 兼容别名，避免历史提示或人工习惯立即失效。 |
| 替代方案或取舍 | 可完全删除 `--approve`，但会降低旧命令兼容性；本次选择默认通过并保留兼容别名。 |
| 验证责任 | 通过上下文预算、OpenSpec 语言、目录结构、目标 Change、Sprint scope 和文档表达卫生校验。 |
| 后续触发条件 | 若评审误通过风险上升，可恢复无 flag 追问或要求高风险 REQ/BUG 显式确认。 |

## 验证结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate default-review-approve-command`：通过。
- `python scripts/validate-sprint-scope.py sprint-024 --item default-review-approve-command`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：通过并报告 2 条既有规则文案 warning，不阻塞本次治理变更。

## 后续建议

- 后续命令输出的正向下一步使用 `/req-review REQ-xxxx` 或 `/bug-review BUG-xxxx`。
- 需要拒绝、延后或不修复时，继续显式追加反向 flag。
