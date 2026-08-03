## Why

`/sprint-exps` 当前在 AI usage snapshot 缺失、过期或覆盖不足时会输出 `estimated_fallback`，导致 Sprint 复盘无法量化真实模型成本。需要在复盘生成前增加 fresh gate，把“必须刷新真实 snapshot”的问题前置暴露，避免最终经验沉淀只剩估算说明。

## What Changes

- 为 Sprint AI usage snapshot 增加 fresh gate：在 `/sprint-exps` 默认路径中，若 snapshot 不是 `present + actual + usage_matrices + scope coverage pass`，必须阻断真实成本分析输出并给出刷新命令。
- 复用 `scripts/extract-ai-usage.py --check-snapshot` 与 Fact Sheet summary 的 `ai_usage_snapshot`，统一 freshness、coverage、usage matrices 和 recommended action 的判断口径。
- 允许用户显式选择 fallback 复盘时继续生成估算章节，但必须标记为非成本量化结果，且不得宣称完成真实 token 成本分析。
- 补充测试覆盖 missing、stale、coverage-missing、usage-matrices-missing、present/actual 通过路径，防止 `/sprint-exps` 静默退回 fallback。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `agent-workflow-tooling`: 强化 `/sprint-exps` 对 Sprint AI usage snapshot 的 fresh gate，确保真实成本分析只基于新鲜、完整、可覆盖当前 Sprint scope 的 actual snapshot。

## Impact

- 影响脚本：`scripts/ai_usage.py`、`scripts/generate-sprint-fact-sheet.py`，以及可能新增的 snapshot gate 辅助函数或 CLI 参数。
- 影响技能文档：`.agents/skills/sprint-exps/SKILL.md`、`.agents/skills/sprint-archive/SKILL.md`（按实现实际影响同步）。
- 影响测试：AI usage snapshot 与 Fact Sheet summary 相关 pytest。
- 不影响业务 API、数据库表结构、Web 前端、小程序、管理端、Orval 或 Docker Compose。
