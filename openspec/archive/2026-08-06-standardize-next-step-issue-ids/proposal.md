---
change_id: standardize-next-step-issue-ids
title: 统一下一步命令参数标识
status: proposed
created_at: 2026-08-06 14:28:00
updated_at: 2026-08-06 14:28:00
---

# 提案

## 背景

当前 REQ/BUG 流程中，`/req-opsx` 或 `/bug-opsx` 创建 OpenSpec Change 后，后续 `/opsx-apply`、`/opsx-archive` 的下一步引导常使用 `<change-id>`。这会让用户在同一条 REQ/BUG 链路中切换标识，例如 REQ-0100 后续变成 `improve-mintlify-docs-site`，降低可读性和可追溯性。

用户期望：

- BUG 链路中，不论是 `/bug-*` 还是后续 `/opsx-*`，下一步可执行命令都使用 `BUG-xxxx-*`。
- REQ 链路中，不论是 `/req-*` 还是后续 `/opsx-*`，下一步可执行命令都使用 `REQ-xxxx-*`。
- 非 BUG/REQ 的直接 Change，`/opsx-*` 继续使用 `<change-id>`。

## 目标

- 规范所有命令最终输出中的下一步参数选择。
- 让 `/opsx-apply` 和 `/opsx-archive` 明确支持以 REQ/BUG ID 作为输入，并解析到关联 Change。
- 更新 `req-opsx`、`bug-opsx` 的下一步示例，不再把 REQ/BUG 来源的后续操作引导为 `<change-id>`。
- 用校验脚本阻止下一步规范回退。

## 非目标

- 不修改业务 `src/` 代码。
- 不改变 OpenSpec Change 的真实目录名或 spec 归档路径。
- 不要求用户为非 REQ/BUG Change 创建 Issue。
- 不修改 API、数据库、Orval、Docker Compose、Web、小程序或管理端运行时。

## 影响范围

- `.agents/skills/req-opsx/SKILL.md`
- `.agents/skills/bug-opsx/SKILL.md`
- `.agents/skills/opsx-apply/SKILL.md`
- `.agents/skills/opsx-archive/SKILL.md`
- `.agents/skills/req-generate|req-complete|req-review|bug-review` 等下一步说明（按需）
- `AGENTS.md`
- `rules/agent-context-budget.md`
- `rules/requirement-management.md`
- `rules/bug-management.md`
- `docs/README.md`
- `scripts/validate-agent-context-budget.py`
- `openspec/archive/2026-08-06-standardize-next-step-issue-ids/`
