---
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
title: 规则/Skill 已读摘要复用纳入命令上下文预算治理 - 业务流程
status: done
created_at: 2026-07-16 09:07:01
updated_at: 2026-07-18 09:18:43
---

# 业务流程

## 1. 背景链路

Sprint 007 复盘已记录：Token 成本已经通过 AI usage fact source 变得可见，但规则/技能重复读取、archive 历史检索风险、长测试日志和同步报告输出仍是中等浪费来源。复盘行动项 A-004 明确要求“将规则/Skill 已读摘要复用机制纳入命令上下文预算治理，减少连续命令重复读取”。

REQ-0040 承接该行动项，将现有 `rules/agent-context-budget.md` 中的原则化约束，完善为可被命令 Skill 和校验脚本执行的机制。

## 2. 目标流程

```text
用户触发工作流命令
        |
        v
识别命令类型与风险等级
        |
        v
检查同一会话已读摘要
        |
        +-- 文件未变更、摘要覆盖当前任务 --> 使用摘要承接
        |
        +-- 文件变更 / 任务升级 / 摘要不足 --> 分段补读必要片段
        |
        v
执行命令主体
        |
        v
输出短摘要：复用哪些摘要、补读哪些片段、是否有 warning
        |
        v
Workflow Sync / AI usage hook 等 Final Step 按原规则执行
```

## 3. 摘要复用判定

```text
                 ┌────────────────────────┐
                 │ 是否同一会话已读？      │
                 └───────────┬────────────┘
                             │
                     否      │      是
                     v       │      v
              读取必要片段   │  文件是否变化？
                             │      |
                             │  是  | 否
                             v      v
                        重新读取   摘要是否覆盖当前命令？
                                      |
                                  否  | 是
                                  v   v
                              补读片段 使用摘要
```

## 4. 与父级/相关 REQ 差异

| 维度 | REQ-0034 / REQ-0035 / REQ-0037 | REQ-0040 |
|---|---|---|
| 关注点 | 记录、生成、消费 AI usage / Token 事实源 | 减少工作流命令执行前后的重复读取成本 |
| 主要对象 | `data/ai-usage/`、post-command hook、Sprint snapshot | `rules/agent-context-budget.md`、命令 Skill、预算校验脚本 |
| 输出 | command run、Sprint snapshot、hook summary | 摘要复用规则、Skill 模板、校验增强 |
| 风险 | 原始 session 脱敏、归因准确性、snapshot coverage | 摘要过期、过度概括、绕过强门禁 |
| 是否涉及 UI | 否 | 否 |

## 5. 预期交付路径

1. `/req-review REQ-0040 --approve` 完成需求评审。
2. `/req-opsx REQ-0040` 创建 OpenSpec Change。
3. Change 设计中引用 `knowledge_base_refs`，特别是 sprint-007 复盘行动项 A-004。
4. 实现阶段更新规则、相关 Skill 模板和校验脚本。
5. 通过 `python scripts/validate-agent-context-budget.py` 验证命令 Skill 未回退。

## 6. 非 UI / 非业务端说明

本需求是 Agent 工作流治理能力，不涉及 Web 管理端、店主 Web、小程序、API、数据库或上传链路。无需 prototype。
