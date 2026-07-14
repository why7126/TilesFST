---
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
title: 工作流命令自动构建 AI Token 事实源 - 业务流程
status: pending_review
created_at: 2026-07-12 09:56:48
updated_at: 2026-07-12 09:56:48
---

# 业务流程

## 1. 流程总览

```text
用户执行工作流命令
    │
    ├─ /req-* /bug-* /opsx-* /sprint-*
    │
    ▼
主命令流程
    ├─ 读规则 / 读事实源
    ├─ 写 issues / iterations / openspec（按命令边界）
    └─ 输出主流程结果
    │
    ▼
Workflow Sync
    ├─ req.* / bug.* / opsx.* / sprint.*
    └─ 同步 trace / registry / sprint 派生块
    │
    ▼
AI Usage Fact Source Hook
    ├─ 定位本地 session 输入
    ├─ 解析 token_count / 工具事件 / 用户命令
    ├─ 归因 REQ / BUG / Change / Sprint / workflow_event
    ├─ 脱敏与安全校验
    ├─ 写 command-runs
    └─ 有 sprint_id 时刷新 sprint snapshot
    │
    ▼
短摘要输出
    ├─ generated / refreshed / skipped / failed
    ├─ actual / estimated_fallback / unavailable
    └─ warnings + recommended_action
```

## 2. 命令后置顺序

```text
主命令成功
    │
    ▼
Workflow Sync 成功
    │
    ▼
Usage Hook 尝试构建
    │
    ├─ 成功
    │    └─ 输出 generated/refreshed 摘要
    │
    ├─ 缺少本地 session
    │    └─ 输出 unavailable + recommended_action，不阻断主命令
    │
    ├─ 解析/归因不足
    │    └─ 输出 estimated_fallback 或 warning
    │
    └─ 敏感内容风险
         └─ 跳过文本持久化，只写 warning 和数字指标
```

## 3. 数据流

| 阶段 | 输入 | 输出 | 说明 |
|---|---|---|---|
| 命令执行 | 用户消息、命令参数、上下文文件 | 工作流产物 | 不改变既有主命令边界。 |
| Workflow Sync | event、REQ/BUG/Change/Sprint | trace、registry、Sprint 派生块 | Sync 成功后再触发 usage hook。 |
| Session 定位 | 显式参数、环境变量、本地配置、当前会话 | 本地 session 输入或 unavailable | 原始路径不得写入仓库事实源。 |
| 用量提取 | session JSONL、manual map、workflow event | command run 明细 | 聚合 `last_token_usage`，统计工具调用和重跑。 |
| 归因聚合 | REQ/BUG/Change/Sprint ID、scope | Sprint snapshot | 无 Sprint 时只写 command run，不伪造 snapshot。 |
| 输出摘要 | hook 结果 | 命令终端摘要 | 只输出计数、状态、warning 和 recommended action。 |

## 4. 状态流

```text
No usage fact
    │
    ▼
Hook skipped
    │  reason: no session input
    │
    ▼
Command run generated
    │
    ├─ no sprint_id
    │    └─ command-runs only
    │
    └─ sprint_id present
         └─ sprint snapshot refreshed
              │
              ├─ coverage pass + metrics non-empty
              │    └─ usage_mode: actual
              │
              └─ stale / missing coverage / empty metrics
                   └─ usage_mode: estimated_fallback
```

## 5. 与父 REQ 差异

| 项 | REQ-0034 | REQ-0037 |
|---|---|---|
| 核心目标 | 建立 AI Token 使用量事实源、字段口径、脱敏和 `/sprint-exps` 接入。 | 将事实源构建扩展为每个工作流命令后的默认自动步骤。 |
| 触发方式 | 显式运行 `extract-ai-usage` 或由 Sprint close/exps 消费 snapshot。 | `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 后置 hook 自动尝试构建。 |
| 关注重点 | 事实源格式、session 解析、聚合和安全边界。 | 统一 hook、命令族覆盖、失败降级、skill 最小改造和幂等复跑。 |
| Sprint 归属 | 以 Sprint 聚合快照为复盘输入。 | 无 Sprint 时也要记录 command run，有 Sprint 时再刷新 snapshot。 |

## 6. 知识库复盘输入

sprint-006 复盘指出：`data/ai-usage/sprints/sprint-006.json` 缺失导致模型 Token 分析只能 estimated fallback，后续行动项要求将 AI usage snapshot 纳入默认流程。

本 REQ 在该经验基础上进一步前移触发点：不仅在 Sprint close / exps 前生成 snapshot，也让每个工作流命令结束时尽早沉淀 command run 明细。

## 7. 异常处理

| 异常 | 处理 |
|---|---|
| 主命令失败 | usage hook 跳过，主命令按原错误返回。 |
| Workflow Sync 失败 | usage hook 跳过，先修复 sync drift。 |
| 无本地 session 输入 | 输出 `usage_mode: unavailable` 和 recommended action。 |
| JSONL 解析失败 | 输出 warning，必要时标记 `failed`，不打印原始行。 |
| 缺少 `token_count` | 写 warning，不编造 Token 数字。 |
| 无 Sprint 归属 | 只写 command run 明细，Sprint snapshot 标记 skipped。 |
| 覆盖不足或过期 | snapshot 不作为完整 actual 使用，提示刷新。 |
| 检测到敏感内容 | 跳过文本持久化，只保留数字指标或 redaction warning。 |
