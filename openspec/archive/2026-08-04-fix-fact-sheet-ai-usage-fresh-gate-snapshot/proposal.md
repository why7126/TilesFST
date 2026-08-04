## 背景

`BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot` 记录了 Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致的问题：snapshot 已完成刷新后，Fact Sheet 仍可能输出 stale blocker，或将 usage mode 映射为 `estimated_fallback`、`skipped`、`unavailable` 等不符合实际刷新状态的值。

该问题会降低 Sprint Fact Sheet、`/sprint-exps` 与 workflow AI usage 证据的可信度。尤其在复盘和 Sprint 收尾时，如果 fresh gate 与 snapshot 状态契约不一致，系统可能误拦截真实 token 成本矩阵，或给出错误的刷新建议。

## 变更内容

- 统一 Fact Sheet fresh gate 使用的 snapshot 状态契约，明确 `present`、`stale`、`missing`、`failed`、`unavailable` 与 usage mode 的对应关系。
- 修正 fresh gate stale 判定，确保已刷新且覆盖当前 Sprint scope 的 snapshot 不会因为旧时间源、旧缓存或 mode fallback 被误判为 stale。
- 增强 fresh gate 输出，保留 compact 原因字段：snapshot status、usage mode、generated_at、coverage、usage matrices presence、warning_count 和 recommended_action。
- 补充回归测试覆盖 fresh snapshot、stale snapshot、缺失 snapshot、coverage 不足和 usage mode fallback。
- 同步相关 workflow 文档或技能说明，确保后续 `/sprint-exps`、Sprint close 与 Fact Sheet 消费端使用一致口径。

## 能力范围

### 新增能力

无。

### 修改能力

- `agent-workflow-tooling`: 修正 Sprint Fact Sheet AI usage fresh gate 与 snapshot 状态、usage mode 映射的一致性。

## 影响范围

- 影响脚本：`scripts/generate-sprint-fact-sheet.py`、必要时 `scripts/extract-ai-usage.py` 或共享 AI usage helper。
- 影响测试：`tests/test_generate_sprint_fact_sheet.py`、必要时 AI usage / workflow sync 相关 pytest。
- 影响文档：本 Change 的 `agent-workflow-tooling` spec delta；若实现调整技能提示，还需同步 `.agents/skills/sprint-exps/SKILL.md` 或相关 workflow 技能。
- 不影响后端 API、数据库、Web 前端、小程序、MinIO、Docker Compose 或 Orval 生成物。

## 回滚计划

- 若 fresh gate 修复导致真实 stale snapshot 被误放行，回滚本 Change 中的 fresh gate 判定调整与相关测试期望。
- 保留现有 snapshot 持久化结构，不进行不可逆数据迁移。
- 回滚后仍可通过重新刷新 `data/ai-usage/sprints/<sprint>.json` 并人工复核 snapshot 字段规避。
