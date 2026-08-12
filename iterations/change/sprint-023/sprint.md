---
note: workflow-sync — workflow-sync 自动同步 — 0/1 Change archived；1 applied；Sprint `planning`
created_at: 2026-08-12 09:15:58
updated_at: 2026-08-12 09:20:06
---

# sprint-023 迭代规划

## 1. 目标

- `optimize-release-workflow-ux`：固化 v1.1.0 发布流程中的操作体验优化。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| Change | optimize-release-workflow-ux | optimize release workflow ux | applied | 0.25 人天 | apply 5/5；待 archive `optimize-release-workflow-ux` |

REQ：无 已纳入正式范围；BUG：无 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 0 个范围项关联 Change，另有 1 个纯 Change；0 archived，1 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量

| Change | Story Points | 人天 | 说明 |
|---|---:|---:|---|
| optimize-release-workflow-ux | 0.5 | 0.25 | 纯治理文档修改 |

## 4. 风险

- 仅修改治理资产，不触碰业务 `src/`，主要风险是命令契约表述不一致。

## 5. 验证

- `openspec validate optimize-release-workflow-ux`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
