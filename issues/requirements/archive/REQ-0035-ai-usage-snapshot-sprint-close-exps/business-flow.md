---
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
title: AI usage snapshot 纳入 Sprint close / exps 默认流程 - 业务流程
status: done
created_at: 2026-07-11 23:46:16
updated_at: 2026-07-15 13:14:04
---

# 业务流程

## 1. 默认收尾流程

```text
Sprint 进入 close / archive
        |
        v
解析目标 sprint_id、scope、REQ/BUG/Change
        |
        v
检查 data/ai-usage/sprints/<sprint_id>.json
        |
        +-- present 且 fresh --------+
        |                            |
        v                            v
标记 usage_mode=actual        输出 snapshot 状态摘要
        |                            |
        +----------------------------+
        |
        v
进入 /sprint-exps
        |
        v
优先读取 snapshot 并生成 Token 使用分析
```

## 2. 缺失或异常流程

```text
检查 snapshot
        |
        +-- missing / stale / failed
        |
        v
尝试默认生成或刷新 snapshot
        |
        +-- 生成成功 ----------------+
        |                            |
        v                            v
标记 usage_mode=actual        进入 /sprint-exps
        |
        +-- 生成失败 / 无法访问 session
        |
        v
输出 warning + recommended_action
        |
        v
允许 estimated_fallback，但必须显式标注原因
```

## 3. 与父 REQ 的差异

| 项 | REQ-0034 | REQ-0035 |
|---|---|---|
| 关注点 | 建立 AI usage 事实源、解析、脱敏、聚合和复盘接入能力 | 将 snapshot 生成与消费纳入 Sprint close / exps 默认流程 |
| 主要产物 | command run 明细、Sprint 聚合快照、解析与脱敏规则 | close / archive 检查、默认生成入口、fallback 显式化、复盘消费门禁 |
| 核心风险 | 原始 session 敏感、归因不准确、Token 口径误用 | snapshot 缺失、过期或失败时继续静默 estimated fallback |
| 验收重点 | 数据字段、聚合口径、脱敏策略、sprint-exps 可读取 | 默认流程、状态报告、新鲜度检查、warning 与补救建议 |

## 4. 状态与口径

| 状态 | 说明 | 后续动作 |
|---|---|---|
| `present` | snapshot 存在且可读取 | 校验新鲜度与覆盖范围 |
| `missing` | snapshot 不存在 | 尝试生成或提示补跑 |
| `stale` | snapshot 早于关键 scope / trace 更新 | 提示刷新 |
| `failed` | 生成或读取失败 | 输出 warning 和失败原因 |
| `actual` | 使用真实 snapshot 统计 | 可进入复盘分析 |
| `estimated_fallback` | 未使用真实统计，只能估算 | 必须显式标注并建议补跑 |

## 5. 知识库输入

sprint-006 复盘已记录：`data/ai-usage/sprints/sprint-006.json` 不存在导致复盘只能估算 token 风险，并提出行动项“将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程”。本需求承接该行动项，目标是把一次性复盘建议固化为默认流程。
