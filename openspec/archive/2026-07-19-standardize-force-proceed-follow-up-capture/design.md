## Context

项目工作流将 REQ/BUG、OpenSpec Change、Sprint 和 Workflow Sync 作为事实源链路。`force-proceed` 的价值是让命令在非阻断风险下继续完成当前目标，但它不应绕过用户确认，把新的后续需求或缺陷直接写入 `issues/`。

当前规则已明确 `/capture`、`/req-capture`、`/bug-capture` 是 Issue 入口；本变更补充命令在发现 follow-up 时的默认输出边界，避免 `force-proceed` 与自动 capture 混用。

## Goals / Non-Goals

**Goals:**

- 明确 `force-proceed` 场景默认只输出标准 capture 文案。
- 明确自动创建 follow-up Issue 必须有用户在当前命令中的显式授权。
- 统一 follow-up capture 文案字段，降低后续 `/capture` 或人工评审成本。
- 为技能文件和校验脚本补充可测试门禁。

**Non-Goals:**

- 不改变 `/capture`、`/req-capture`、`/bug-capture` 的 Issue 创建流程。
- 不改变 Workflow Sync 的状态机和 Sprint 解析逻辑。
- 不引入业务 API、数据库、Web、小程序或 MinIO 行为变更。
- 不要求对历史已生成 Issue 做迁移。

## Decisions

1. `force-proceed` 与 follow-up capture 分离。

   默认行为为继续当前命令并输出 follow-up 文案；不得因为 `force-proceed` 自动写入 `issues/`。替代方案是允许自动生成 Issue 后标记 `needs_review`，但这仍会污染正式 Issue registry，且与“未评审不得进入 Sprint”的边界不够清晰。

2. 使用标准 `/capture` 文案作为兜底输出。

   文案应可直接复制给 `/capture`，包含类型倾向、标题、背景、影响、建议验收或复现、来源对象。替代方案是只输出一句建议，但缺少结构会导致后续 capture 质量不稳定。

3. 显式授权必须来自当前用户意图。

   只有用户在同一命令中明确要求“自动创建/帮我记录/生成 follow-up issue”等等价授权，命令才可创建 REQ/BUG 并运行对应 Workflow Sync。历史偏好、命令内部推断或 `force-proceed` 本身都不构成授权。

4. 校验优先覆盖技能文本约束。

   初期实现以更新相关 `.agents/skills/*` 和轻量校验为主；若未来出现脚本化 `force-proceed` 参数，再扩展脚本测试。这样能先守住 Agent 行为入口，避免为尚未存在的代码路径设计过重机制。

## Risks / Trade-offs

- [Risk] 用户希望全自动记录后续事项时，多一步确认会降低速度。
  Mitigation: 支持显式授权自动 capture，并让默认文案可直接用于 `/capture`。
- [Risk] 不同命令输出的 capture 文案风格不一致。
  Mitigation: 在共享 workflow tooling 规格和技能守则中定义最低字段。
- [Risk] 校验只看技能文本，无法证明每次模型行为都完全一致。
  Mitigation: 将规范写入 OpenSpec 与技能入口，并在任务中补充人工可复核示例或脚本校验。
