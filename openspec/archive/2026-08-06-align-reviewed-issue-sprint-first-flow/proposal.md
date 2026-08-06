---
change_id: align-reviewed-issue-sprint-first-flow
title: 统一评审后先纳入 Sprint 再创建 Change 的命令流
status: applied
created_at: 2026-08-06 00:00:00
updated_at: 2026-08-06 11:52:14
---

# 提案

## 背景

当前 REQ/BUG 工作流文档与部分技能仍表达「评审通过后先 `/req-opsx` 或 `/bug-opsx`，再 `/sprint-propose`」的旧顺序，和用户希望的“评审后先进行 Sprint 规划，再创建对应 OpenSpec Change”不一致。命令执行结束后的下一步引导也分散在各技能中，容易出现已完成命令后没有明确可执行下一步、或未突出待用户决策点的问题。

## 目标

- 将已评审 REQ/BUG 的推荐推进顺序统一为：`/req-review` 或 `/bug-review` 通过后，先 `/sprint-propose` 纳入 Sprint，再 `/req-opsx` 或 `/bug-opsx` 创建/回填 Change。
- 保留既有安全门禁：未评审不得进入 Sprint；来源于 REQ/BUG 的 Change 在 `/opsx-apply` 前必须已被 Sprint 机器事实源追踪。
- 要求 `.agents/skills/` 下每个命令技能在结束时输出明确可执行的下一步引导。
- 要求命令输出明确列出待用户决策或处理的点，并优先使用可直接复制执行的命令格式。
- 通过脚本校验技能文件是否具备统一的下一步与待决策输出契约。

## 非目标

- 不修改后端 API、数据库 schema、Web、小程序或管理端运行时行为。
- 不自动创建新的业务 REQ/BUG，不改变既有 Issue 编号规则。
- 不放宽 OpenSpec Change、Sprint scope、Workflow Sync 或归档门禁。
- 不直接修改 `openspec/specs/` 正式规格，归档阶段再合并 delta。

## 能力范围

### 新增能力

无。

### 修改能力

- `sprint-planning-governance`：补充“评审通过后先 Sprint 规划，再 req/bug-opsx”的流程约束。
- `agent-workflow-tooling`：补充命令技能结束输出必须包含下一步引导和待决策/待处理点的契约。

## 影响范围

- `AGENTS.md`、REQ/BUG/Sprint/文档治理规则中的流程说明。
- `.agents/skills/*/SKILL.md` 命令技能的 Next / Final Output 口径。
- `scripts/validate-agent-context-budget.py` 或等价技能校验脚本。
- 不影响 API、DB、Orval、Docker Compose、前端或小程序运行时。
