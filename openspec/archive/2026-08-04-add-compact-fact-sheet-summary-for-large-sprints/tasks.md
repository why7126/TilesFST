## 1. Fact Sheet summary 输出边界

- [x] 1.1 梳理 `scripts/generate-sprint-fact-sheet.py` 中 `ai_usage_snapshot` 的 summary 构建逻辑，确认完整 JSON、summary 与 fields 模式的字段差异。
- [x] 1.2 为 summary 模式增加 compact `usage_matrices_summary`，包含矩阵可用性、metrics、行列数量、省略状态和完整矩阵 fields 读取提示。
- [x] 1.3 调整 summary 模式，确保 10+ Change Sprint 默认不输出完整 `usage_matrices.rows` 或四张 usage matrix 明细。
- [x] 1.4 保证完整 JSON 与 `--fields ai_usage_snapshot.usage_matrices` 仍能按需返回完整矩阵结构。

## 2. `/sprint-exps` 规则同步

- [x] 2.1 更新 `.agents/skills/sprint-exps/SKILL.md`，明确默认使用 compact Token Usage Fact Sheet summary。
- [x] 2.2 在技能中说明仅当用户明确要求矩阵明细或复盘文档确需写入真实矩阵时，才通过 fields 模式读取完整 `usage_matrices`。
- [x] 2.3 确认技能仍保留 fresh gate、fallback、脱敏和上下文预算要求。

## 3. 测试与校验

- [x] 3.1 更新 `tests/test_generate_sprint_fact_sheet.py`，覆盖大型 Sprint summary 不包含完整矩阵 rows。
- [x] 3.2 补充 fields 模式读取完整 `ai_usage_snapshot.usage_matrices` 的回归测试。
- [x] 3.3 运行相关 pytest，至少覆盖 Fact Sheet 与 AI usage 相关测试。
- [x] 3.4 运行 `python scripts/validate-openspec-language.py`，修复 Change 文档语言问题。
- [x] 3.5 运行 `openspec status --change add-compact-fact-sheet-summary-for-large-sprints`，确认 Change 已 apply-ready。
