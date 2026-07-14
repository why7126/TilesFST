## Context

REQ-0034 已在 `agent-workflow-tooling` 能力中定义 AI usage 事实源、command run 边界、Token 指标聚合、脱敏和 `/sprint-exps` 读取快照的要求。但 Sprint 006 复盘仍记录 `data/ai-usage/sprints/sprint-006.json` 不存在，导致复盘只能估算 token 风险。

REQ-0035 不重新设计事实源，而是补齐默认流程：Sprint close / archive 应先检查或生成 snapshot，`/sprint-exps` 应优先消费 snapshot，并在真实统计不可用时显式标注 fallback。

关联知识库证据：

- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`：AI usage snapshot 未生成导致精确 Token 统计缺失，行动项 A-001 要求纳入 Sprint close / exps 默认流程。

## Goals / Non-Goals

**Goals:**

- 在 Sprint close / archive 阶段提供 snapshot 检查、生成或刷新入口。
- 在 `/sprint-exps` 中强制区分 `actual` 与 `estimated_fallback`。
- 校验 snapshot 的存在性、新鲜度、覆盖范围和必要指标。
- 成功路径输出保持摘要化，避免 snapshot 检查本身扩大上下文消耗。
- 继承 REQ-0034 的脱敏与安全边界。

**Non-Goals:**

- 不改造 Codex Desktop 或底层 session 记录机制。
- 不新增 Web / 管理端 / 小程序 UI。
- 不做精确费用、账单或额度核算。
- 不强制一次性回填所有历史 Sprint。
- 不在本 Change 的 propose 阶段写 `src/` 或实现代码。

## Decisions

### D1. 以 `data/ai-usage/sprints/<sprint-id>.json` 作为 Sprint snapshot 默认路径

沿用 REQ-0034 的 `data/ai-usage/` 事实源，不新增顶层目录。Sprint 级聚合使用固定路径便于 `/sprint-archive` 和 `/sprint-exps` 查找。

备选方案：把 snapshot 写入 `iterations/<sprint>/`。该方案会把本地 AI usage 派生事实混入 Sprint 四件套，且更容易提交敏感或机器本地数据，因此不采用。

### D2. Sprint close / archive 负责检查和尽力生成，`/sprint-exps` 负责消费和显式降级

`/sprint-archive` 或未来 close 命令应在归档前检查 snapshot 状态，并在缺失时尝试生成或提示补跑。`/sprint-exps` 必须读取 snapshot；如果不可用，只能以 `estimated_fallback` 输出，并说明原因。

备选方案：只在 `/sprint-exps` 内生成 snapshot。该方案会把复盘命令变得过重，也不能在 close 阶段提前发现缺口。

### D3. 新鲜度与覆盖不足先 warning，不伪装 actual

snapshot 若缺少目标 Sprint、早于最近关键变更、关键指标为空或无法覆盖主要 scope，应标记 `stale` 或 warning，并降级为 `estimated_fallback` 或提示刷新。

备选方案：只按文件存在判断。该方案会误用旧 snapshot，不满足 REQ-0035 的防误读目标。

### D4. 输出摘要优先，详细明细留在 snapshot 文件

命令成功路径只输出状态、口径、路径、生成时间、warning 数和关键计数。失败或用户要求时再展开详细诊断。

备选方案：每次输出完整 command run 明细。该方案会增加上下文成本，也更容易暴露敏感内容。

## Risks / Trade-offs

- 本地 session 数据不可访问 -> 输出 `estimated_fallback` 和 recommended action，不阻断复盘文档生成。
- snapshot 过期判断可能不完整 -> 第一版基于 Sprint scope、trace/close 时间和 snapshot metadata 做保守 warning。
- 自动生成 snapshot 可能较慢 -> close 阶段可先检查，再按需生成；成功路径只显示摘要。
- 脱敏遗漏风险 -> 仅持久化统计、相对路径、hash、时间和 warning，不保存 prompt 或工具输出全文。

## Migration Plan

1. 在 apply 阶段实现 snapshot 检查/生成脚本或扩展现有 AI usage 生成脚本。
2. 更新 `/sprint-archive` 与 `/sprint-exps` 技能，把 snapshot 检查、生成和 fallback 标注纳入默认流程。
3. 补充测试，覆盖 present/missing/stale/failed 和 actual/estimated_fallback。
4. 更新 `data/README.md` 或相关文档，明确 snapshot 文件提交边界和脱敏规则。
5. 在后续 Sprint 中通过 `/sprint-archive` 或 `/sprint-exps` 验证真实 snapshot 路径。

## Open Questions

- `Sprint close` 是否长期作为独立命令存在，还是继续由 `/sprint-archive` 承担 close 语义？
- snapshot metadata 中“最近关键变更时间”的权威来源应优先使用 sprint.yaml、trace.md，还是 Workflow Sync event？
