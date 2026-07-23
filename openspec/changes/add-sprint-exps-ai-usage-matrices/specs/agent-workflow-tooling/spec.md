# agent-workflow-tooling Delta

## ADDED Requirements

### Requirement: Sprint 复盘 AI 使用量矩阵
`/sprint-exps` MUST 基于 `data/ai-usage` 的 Sprint snapshot 展示 AI 使用量矩阵，用于按 Sprint、REQ、BUG 与工作流命令交叉分析 token 与模型调用消耗。

#### Scenario: 输出四张指标矩阵
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** 对应 `data/ai-usage/sprints/<sprint-id>.json` 存在可用真实统计
- **THEN** 复盘文档 MUST 在 `## 模型 Token 使用分析` 中输出 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张矩阵表
- **AND** 四张表 MUST 使用相同的行列结构

#### Scenario: 矩阵行列顺序
- **WHEN** `/sprint-exps` 输出 AI 使用量矩阵
- **THEN** 表格最上方 MUST 包含 `Total` 汇总行
- **AND** 纵向对象行 MUST 按 Sprint、REQ、BUG 顺序排列
- **AND** Sprint 行 MUST 使用 `sprint-xxx` 或规范大写展示名，REQ/BUG 行 MUST 使用对应 canonical ID
- **AND** 横向命令列 MUST 按 `Capture`、`BUG-Capture`、`REQ-Capture`、`BUG-Explore`、`REQ-Explore`、`REQ-Generate`、`BUG-Generate`、`REQ-Complete`、`BUG-Complete`、`REQ-Review`、`BUG-Review`、`REQ-Opsx`、`BUG-Opsx`、`Opsx-Explore`、`Opsx-Propose`、`Opsx-Apply`、`Opsx-Archive`、`Sprint-Propose`、`Sprint-Explore`、`Sprint-Apply`、`Sprint-Archive` 的顺序展示

#### Scenario: 缺少矩阵统计
- **WHEN** Sprint snapshot 缺失、过期、覆盖不足或缺少矩阵字段
- **THEN** `/sprint-exps` MUST 标记 `ai_usage_mode: estimated_fallback` 或输出 warning
- **AND** `/sprint-exps` MUST 提示刷新 `data/ai-usage` snapshot
- **AND** `/sprint-exps` MUST NOT 编造矩阵数值

#### Scenario: 对象归因口径
- **WHEN** 同一 command run 同时关联多个 REQ 或 BUG
- **THEN** Sprint 行与 `Total` 行 MUST 按唯一 command run 汇总
- **AND** REQ/BUG 行 MAY 按对象归因分别计入同一 command run
- **AND** 复盘说明 SHOULD 提醒对象行用于归因分析，不代表可与 `Total` 行直接相加
