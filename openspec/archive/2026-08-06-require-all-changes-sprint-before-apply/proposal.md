---
change_id: require-all-changes-sprint-before-apply
title: 所有 Change 执行前必须纳入 Sprint
status: proposed
created_at: 2026-08-06 14:01:45
updated_at: 2026-08-06 14:01:45
---

# 提案

## 背景

当前 `/opsx-apply` 门禁只强制来源于 REQ/BUG 的 OpenSpec Change 必须纳入 Sprint，允许无 REQ/BUG 来源的纯治理 Change 绕过 Sprint Inclusion Gate。`add-spec-opt-governance-command` 就是在未纳入 Sprint 的情况下完成 apply 和 archive 的典型例子。

这会造成两类治理断层：

- 直接 `/opsx-propose` 创建的 Change 可以跳过迭代容量、范围和优先级管理。
- 治理类 Change 虽然不改业务代码，但仍会改变工作流、规范、脚本或文档，应被纳入 Sprint 事实源追踪。

## 目标

- 将 `/opsx-apply` Sprint Inclusion Gate 从“仅 REQ/BUG 来源 Change 必须纳入 Sprint”提升为“所有 Change 必须纳入 Sprint”。
- 明确 `/opsx-propose` 直接创建的非 REQ/BUG Change，也必须先通过 `/sprint-propose` 或等价 scope 修复流程纳入 Sprint 后才能 `/opsx-apply`。
- 删除 `/spec-opt` 中“纯治理 Change 可豁免 Sprint Gate”的规则。
- 更新 AGENTS、rules、skills、docs 和必要校验脚本说明，避免后续再次产生同类漏洞。

## 非目标

- 不修改业务 `src/` 代码。
- 不改变 REQ/BUG 的评审门禁。
- 不要求非 REQ/BUG Change 自动创建 REQ/BUG。
- 不归档历史上已经完成但未纳入 Sprint 的 Change；历史偏差作为已知事实保留。

## 影响范围

- `AGENTS.md`
- `rules/document-governance.md`
- `rules/iterations-lifecycle.md`
- `rules/agent-context-budget.md`（按需）
- `docs/README.md`
- `.agents/skills/opsx-apply/SKILL.md`
- `.agents/skills/spec-opt/SKILL.md`
- `.agents/skills/workflow-sync/SKILL.md`
- `scripts/validate-agent-context-budget.py` 或新增/修改的治理校验脚本（按需）
- `openspec/archive/2026-08-06-require-all-changes-sprint-before-apply/`

不影响 API、数据库、Orval、Docker Compose、Web、小程序和管理端运行时。
