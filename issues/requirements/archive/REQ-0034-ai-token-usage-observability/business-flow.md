---
requirement_id: REQ-0034-ai-token-usage-observability
title: AI 命令 Token 使用量观测与 Sprint 复盘接入 - 业务流程
status: archived
created_at: 2026-07-11 17:06:13
updated_at: 2026-07-11 20:10:50
---

# 业务流程

## 1. 流程总览

```text
用户一轮消息
    │
    ▼
Codex session JSONL
~/.codex/sessions/**/rollout-*.jsonl
    │
    │  本地只读输入，不入仓库
    ▼
Token usage 提取脚本
    │
    ├─ 识别用户消息边界
    ├─ 聚合 token_count.last_token_usage
    ├─ 统计工具调用 / 工具输出 / 失败重跑
    ├─ 关联 REQ / BUG / Change / Sprint
    └─ 执行脱敏和路径归一化
    │
    ▼
data/ai-usage/
    ├─ command run 明细
    └─ Sprint 聚合快照
    │
    ▼
/sprint-exps
    │
    ▼
docs/knowledge-base/retrospectives/<sprint>-retrospective.md
```

## 2. 命令运行边界

命令运行边界按“用户一轮消息”定义。

```text
User message: /req-complete REQ-0034
    ├─ model call #1 -> token_count.last_token_usage
    ├─ tool call/read -> tool_output_chars
    ├─ model call #2 -> token_count.last_token_usage
    ├─ tool call/apply_patch
    ├─ workflow sync
    └─ final response

=> 归并为 1 条 command run
```

若同一轮用户消息处理多个对象，例如同时提到 `REQ-0034` 和 `BUG-0062`，command run 应保留多值关联，并降低或标记归因置信度。

## 3. 数据生命周期

| 阶段 | 输入 | 输出 | 说明 |
|---|---|---|---|
| 本地读取 | `~/.codex/sessions/**/rollout-*.jsonl` | 解析事件流 | 只读，不提交原始文件。 |
| 命令聚合 | 用户消息、turn、token_count、工具事件 | command run | 使用 `last_token_usage` 求和。 |
| 关联归因 | 命令文本、Workflow Sync 参数、Issue trace、Sprint scope | REQ/BUG/Change/Sprint 关联 | 允许多值和置信度。 |
| 脱敏输出 | command run 原始候选数据 | `data/ai-usage/` 事实源 | 不写 prompt、系统指令、绝对路径和工具输出全文。 |
| Sprint 聚合 | command run 明细、Sprint scope | Sprint 快照 | 供 `/sprint-exps` 读取。 |
| 复盘展示 | Sprint 快照 | Token 使用分析章节 | 按命令环节维度展示。 |

## 4. 关联规则

```text
显式命令 ID
    优先级最高
    /req-complete REQ-0034
        -> requirements: [REQ-0034]

Workflow Sync 参数
    python scripts/sync-workflow-status.py --event req.complete --req REQ-0034
        -> workflow_event: req.complete

Sprint scope 反查
    iterations/change/<sprint>/sprint.yaml
        -> sprint_id

时间窗口 / trace 变更记录
    作为辅助证据
        -> attribution_confidence: medium|low
```

## 5. 与现有流程的关系

| 现有流程 | 关系 |
|---|---|
| `trace.md` | 继续作为流程事实源，不承载完整 Token 明细。 |
| Workflow Sync | 提供事件名和 Issue/Sprint 关联线索，但不负责实时写 Token。 |
| `generate-sprint-fact-sheet.py` | 后续可合并 AI usage 聚合快照，减少 `/sprint-exps` 读取成本。 |
| `/sprint-exps` | 使用聚合快照生成命令环节维度分析。 |
| `rules/agent-context-budget.md` | 用 Token 事实反哺预算规则和高消耗来源优化。 |

## 6. 状态流

```text
No usage data
    │
    ▼
Session parsed
    │
    ▼
Command runs generated
    │
    ├─ attribution_confidence: high
    │       -> 可直接用于复盘
    │
    ├─ attribution_confidence: medium
    │       -> 可用于趋势分析，复盘需标注
    │
    └─ attribution_confidence: low
            -> 仅作风险提示或人工复核
```

## 7. 异常处理

| 异常 | 处理 |
|---|---|
| 缺少 `token_count` | 记录 warning，command run 标记无精确 token。 |
| JSONL 单行解析失败 | 跳过该行并记录 warning，不中断整个 Sprint。 |
| 无法归因到 Issue | 保留 command run，`requirements/bugs` 为空，置信度 low。 |
| 发现本机绝对路径 | 转相对路径、hash 或脱敏为 `<local-path-redacted>`。 |
| 工具输出疑似敏感 | 不保存原文，只保存字符数和 warning。 |
| 重复提取同一 session | 应尽量幂等，避免重复累计。 |

## 8. 父 REQ 差异

本需求暂无父 REQ。它属于流程治理和 Agent 观测能力，区别于业务功能需求、UI 需求和 API 治理需求；其主要产物是规则、脚本事实源和 Sprint 复盘输入，而不是用户可见产品功能。
