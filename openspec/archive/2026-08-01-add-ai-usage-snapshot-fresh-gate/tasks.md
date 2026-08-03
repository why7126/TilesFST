## 1. Snapshot Fresh Gate

- [x] 1.1 在 `scripts/ai_usage.py` 中实现可复用的 Sprint snapshot fresh gate 判定，覆盖 `present`、`actual`、`usage_matrices`、关键 totals 和 scope coverage。
- [x] 1.2 让 `scripts/extract-ai-usage.py --check-snapshot` 或等价 CLI 输出 compact gate 结果与 recommended_action，不输出原始 session、本机绝对路径或敏感内容。
- [x] 1.3 在 `scripts/generate-sprint-fact-sheet.py --summary` 中暴露 fresh gate compact 字段，保持默认 summary 不包含完整 evidence hints。

## 2. Sprint Experience Workflow

- [x] 2.1 更新 `.agents/skills/sprint-exps/SKILL.md`，要求默认先检查 fresh gate；未通过时输出 blocker 和刷新建议，不生成真实 token 成本矩阵。
- [x] 2.2 明确显式 fallback 复盘路径：仅当用户明确要求继续时输出 `ai_usage_mode: estimated_fallback`，并说明不能用于真实成本量化。
- [x] 2.3 复核 `.agents/skills/sprint-archive/SKILL.md` 是否需要同步 freshness 文案；如需同步，保持与 `/sprint-exps` 口径一致。

## 3. Tests And Validation

- [x] 3.1 补充 AI usage snapshot 单元测试，覆盖 missing、failed、stale、coverage-missing、usage-matrices-missing 和 present/actual 通过路径。
- [x] 3.2 补充 Fact Sheet summary 或 `/sprint-exps` 相关测试，确认 gate 未通过时不会静默输出真实成本矩阵。
- [x] 3.3 运行相关 pytest、`openspec validate add-ai-usage-snapshot-fresh-gate --strict` 和必要的目录/上下文预算校验。

## 4. Documentation Review

- [x] 4.1 复核是否需要更新 `rules/agent-context-budget.md` 或长期文档；若不需要，在实现输出中说明不适用原因。
- [x] 4.2 在实现完成输出中说明 API、数据库、Web、小程序、管理端、Orval 和 Docker Compose 均不受影响，除非实现阶段发现新的影响面。

## 归档验证摘要

| 项 | 结论 |
|---|---|
| 验证命令与结果 | `uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py`：51 passed；`openspec validate add-ai-usage-snapshot-fresh-gate --strict`：通过；`python scripts/validate-directory-structure.py`：通过；`python scripts/validate-agent-context-budget.py`：通过 |
| 验收结论 | 通过。Sprint AI usage snapshot fresh gate 已在脚本、Fact Sheet summary、`/sprint-exps` 与 `/sprint-archive` 技能中闭环；测试覆盖 missing、failed、stale、coverage-missing、usage-matrices-missing 与 present/actual pass 路径。 |
| 关联 Issue 或 Sprint 状态 | 无关联 REQ/BUG；未纳入 Sprint scope，属于纯技术治理 Change。Workflow Sync 在 `opsx.apply` 阶段返回 Sprint skipped/no-sprint 且无错误。 |
| 归档路径或归档时间 | 归档路径：`openspec/archive/2026-08-01-add-ai-usage-snapshot-fresh-gate/`；归档日期：`2026-08-01`。 |
