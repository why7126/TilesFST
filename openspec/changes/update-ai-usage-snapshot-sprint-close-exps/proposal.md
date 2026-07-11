## Why

Sprint 006 复盘已经暴露 AI usage snapshot 未成为默认产物，导致 `/sprint-exps` 只能继续 estimated fallback，无法量化命令级 Token 成本。REQ-0035 需要把 snapshot 生成、校验和消费纳入 Sprint close / exps 默认流程，让真实统计成为常规路径，估算只作为显式降级。

## What Changes

- 在 Sprint close / archive 阶段默认检查目标 Sprint 的 AI usage snapshot 状态。
- 当 snapshot 缺失、过期或生成失败时，输出明确 warning、原因和 recommended action。
- 为 Sprint close / archive 提供默认生成或刷新 snapshot 的入口，复用 REQ-0034 的 `data/ai-usage/` 事实源与脱敏规则。
- `/sprint-exps` 优先消费真实 snapshot；无法使用真实数据时必须显式标记 `estimated_fallback`，不得静默估算。
- 增加 snapshot 新鲜度与覆盖范围校验，避免使用过期或覆盖不足的统计结果。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `agent-workflow-tooling`: 增强 Sprint close / archive 与 `/sprint-exps` 的 AI usage snapshot 默认生成、校验、消费与 fallback 显式化要求。

## Impact

- 影响脚本与流程命令：`scripts/` 中 AI usage snapshot 生成/校验入口、Sprint fact sheet 或复盘相关脚本。
- 影响项目技能：`.agents/skills/source-command-sprint-archive/SKILL.md`、`.agents/skills/source-command-sprint-exps/SKILL.md` 需要纳入默认步骤。
- 影响文档：`data/README.md` 或 AI usage 相关说明需要明确 snapshot 提交边界与安全约束。
- 影响测试：需要补充脚本级测试，覆盖 snapshot present/missing/stale/failed、actual/estimated_fallback、成功路径摘要输出和敏感内容不落盘。
- 不影响产品 API、数据库表结构、Web UI、小程序、MinIO 上传链路和 Orval。
