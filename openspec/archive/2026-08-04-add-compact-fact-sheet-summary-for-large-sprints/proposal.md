## 背景

10+ Change 的大型 Sprint 在复盘时需要依赖 Sprint Fact Sheet 控制上下文，但当前 summary 仍可能默认暴露完整 `usage_matrices`，导致 `/sprint-exps` 输出和模型上下文被大矩阵占满。现在需要让 Fact Sheet summary 默认提供 compact Token Usage Fact Sheet 摘要，只在明确请求时展开完整矩阵。

## 变更内容

- 为 `scripts/generate-sprint-fact-sheet.py --summary` 增加 compact AI usage 摘要口径，默认只输出 fresh gate、snapshot 状态、关键 totals、矩阵规模、warning_count 与 recommended_action。
- 对包含 10+ Change 的 Sprint，summary 默认不得输出完整 `usage_matrices.rows` 或四张 usage matrix 明细。
- 增加按需字段读取方式，使调用方可通过 `--fields ai_usage_snapshot.usage_matrices` 或等价参数获取完整矩阵。
- 更新 `/sprint-exps` Skill，使其默认使用 compact Token Usage Fact Sheet summary；只有用户明确要求矩阵或复盘文档确需写入矩阵时，才按需读取完整矩阵字段。
- 补充测试覆盖大型 Sprint summary 输出边界、字段模式读取完整矩阵、以及 `/sprint-exps` 规则不再默认消费完整矩阵。

## 能力范围

### 新增能力

无。

### 修改能力

- `agent-workflow-tooling`: 调整 Sprint Fact Sheet summary 与 `/sprint-exps` 对 AI usage matrices 的默认读取和输出边界。

## 影响范围

- 影响脚本：`scripts/generate-sprint-fact-sheet.py`。
- 影响技能：`.agents/skills/sprint-exps/SKILL.md`。
- 影响测试：`tests/test_generate_sprint_fact_sheet.py` 以及必要的技能文本校验。
- 不影响后端 API、数据库、Web 前端、小程序、MinIO、Docker Compose 或 Orval 生成物。
