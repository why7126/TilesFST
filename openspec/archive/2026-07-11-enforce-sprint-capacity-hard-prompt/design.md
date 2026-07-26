## Context

`/sprint-propose` 负责把已评审的 REQ/BUG/Change 组合为 Sprint 四件套，并同步 trace 与 workflow 状态。现有 Capacity Gate 只有优先级、估算映射、fix 缓冲和“超限写入风险或延后项”的要求，缺少超过极限容量时的停止条件。

本变更属于流程治理增强，主要改动项目级 Codex skill 与相关校验/测试，不引入运行时服务、外部依赖、数据库迁移或 API 变更。

## Goals / Non-Goals

**Goals:**

- 在 `/sprint-propose` 中明确容量硬门槛：`estimated_person_days > capacity_person_days * 1.2` 时必须停止正式规划。
- 要求超限输出可操作提示：拆分 Sprint、移出低优先级项或替换范围。
- 保留 100% 到 120% 的弹性区间，但必须记录风险、缓冲与延后项。
- 通过文档和测试确保后续修改不会弱化该门禁。

**Non-Goals:**

- 不重新设计 Sprint 编号、四件套结构或 workflow sync marker。
- 不改变 REQ/BUG review gate、readiness gate 或 OpenSpec Change 准入条件。
- 不引入自动排期算法；范围替换仍由人或 Agent 根据优先级决策。
- 不修改后端 API、数据库、Web、小程序或部署配置。

## Decisions

1. 将 120% 定义为硬阻断阈值。
   - 理由：低于或等于 120% 仍可作为团队协商缓冲；超过 120% 通常意味着规划事实已失真，继续生成正式 Sprint 会污染 trace 和 Scope。
   - 备选：超过 100% 即阻断。该方案过于严格，容易阻断合理缓冲和紧急修复场景。

2. 阻断发生在生成正式四件套和 trace 更新之前。
   - 理由：如果先写 `sprint.yaml` 或更新 REQ/BUG trace，再要求拆分，会制造需要清理的半成品状态。
   - 备选：允许生成草稿四件套。当前命令已有 `--dry-run` 表达预览场景，正式 propose 应保持事实源干净。

3. sprint-propose skill 承载执行细则，OpenSpec spec 承载验收合同。
   - 理由：skill 是命令运行时入口，spec 是可归档的长期行为要求；两者分工清晰。
   - 备选：只改 skill。该方案缺少长期规格约束，归档后难以追踪门禁来源。

## Risks / Trade-offs

- [Risk] 估算缺失或容量字段缺失时无法计算 120% → Mitigation：实现时要求在 Capacity Gate 中先补齐容量和估算；无法计算时不得默认通过，应提示补充输入或使用项目默认容量。
- [Risk] 硬阻断可能让紧急 P0 修复无法一次性进入 Sprint → Mitigation：提示替换范围，优先保留 P0，移出 P1/P2 或拆分后续 Sprint。
- [Risk] skill 文案与脚本测试不同步 → Mitigation：补充面向 skill 文案/规则的测试或校验，确保出现 120% 阈值与阻断动作。
