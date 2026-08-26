---
created_at: 2026-08-25 17:20:27
updated_at: 2026-08-25 18:18:35
---

# AI Usage 矩阵 unknown 语义治理

## 迭代目标

优化 AI Usage Sprint 复盘矩阵，区分真实 `0` 与未采集或未归因的 workflow 阶段，并改善 post-command hook 在同分候选 run 中误选零 token turn 的风险。

## 变更摘要

- Sprint Usage Matrix 增加列级观测状态，未观测 workflow 列在数据层标记为 `unknown`，在复盘 Markdown 中渲染为 `-`。
- Fact Sheet Markdown 输出说明 `-` 不等价于真实 `0`。
- post-command hook 目标 run 选择在同等上下文匹配分数下优先选择有 token 或模型调用指标的 run。
- 回溯刷新 `sprint-025` AI usage snapshot，并重写复盘 Token 区。
- 扫描 `~/.codex/sessions`，按 `sprint-025` 时间窗、REQ/BUG/Change scope 与 workflow event 重新补齐 lifecycle token 归因。
- Sprint snapshot 聚合时裁剪到正式 Sprint scope，避免相关历史 REQ/BUG 被 Change 关联扩展成复盘矩阵对象行。
- 修复 Fact Sheet 时间测试 fixture，避免固定未来日期随时间漂移失效。

## 影响范围

- 脚本：AI usage extractor 与 Sprint Fact Sheet 生成器。
- 命令：`/sprint-exps` Token 分析章节语义。
- OpenSpec：`fix-ai-usage-message-content-token-count` 的 `agent-workflow-tooling` delta spec。
- 知识库：`sprint-025` 复盘 Token 区。

## 更新文件

- `.agents/skills/sprint-exps/SKILL.md`
- `docs/knowledge-base/retrospectives/sprint-025-retrospective.md`
- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/20260825172027-governance-ai-usage-matrix-unknown.md`
- `openspec/changes/fix-ai-usage-message-content-token-count/`
- `scripts/ai_usage.py`
- `scripts/generate-sprint-fact-sheet.py`
- `tests/test_ai_usage.py`
- `tests/test_generate_sprint_fact_sheet.py`
- `data/ai-usage/command-runs/sprints/sprint-025/backfill-sessions-20260825.json`
- `data/ai-usage/sprints/sprint-025.json`

## 关键决策

- 已采纳：保留固定 workflow 列，避免不同 Sprint 表格结构漂移。
- 已采纳：新增 `unknown` 语义，而不是删除未观测列；这样能同时暴露回溯缺口和真实消耗来源。
- 已采纳：用户可见矩阵单元使用 `-` 展示未观测阶段，避免 `unknown` 文本过长影响阅读；数据层继续保留 `status=unknown`。
- 已采纳：post hook 仅在同分候选中优先非零 run，避免跨 workflow 强行改写归因。
- 已采纳：sprint snapshot 对象覆盖与矩阵行只保留 Sprint 正式 scope；历史关联 issue 不进入该 Sprint 的复盘矩阵。
- 未采纳：把所有未观测列继续渲染为 `0`；原因是复盘读者会误判为真实零成本。
- 替代方案：后续可将本次 session 目录级回溯流程沉淀为正式脚本参数，替代临时扫描脚本。

## 验证结果

- `uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py`：通过，60 passed。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --summary`：通过，`fresh_gate.status=pass`，`unknown_columns_count=20`。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown`：通过，矩阵包含 `unknown` 与真实 `0`。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change fix-ai-usage-message-content-token-count --sprint sprint-026 --json`：通过，`status=ok`、`usage_mode=actual`、`warning_count=0`。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-026 --summary`：通过，`fresh_gate.status=pass`。
- `~/.codex/sessions` 目录级回溯扫描：完成，扫描 520 个 JSONL，选择 23 个 session、100 个唯一 command run，`sprint-025` total_tokens 更新为 8,039,162。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown`：通过，矩阵行裁剪为 `Total`、`sprint-025`、9 个 REQ 与 7 个 BUG，未观测 workflow 列数为 10。
- `/opsx-modify BUG-0141` 验收返修：通过，未观测 workflow 单元由 `unknown` 改为 `-`，真实 `0` 保持数字显示。

## 产品影响

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：更新治理脚本与 Fact Sheet 聚焦测试。

## 后续建议

后续可将本次临时目录级扫描流程产品化为 `extract-ai-usage.py` 的目录输入参数，增加 dry-run 候选报告、时间窗边界和 scope trim 明确开关。
