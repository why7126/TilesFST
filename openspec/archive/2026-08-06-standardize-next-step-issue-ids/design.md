---
change_id: standardize-next-step-issue-ids
title: 下一步命令参数标识规范设计
status: proposed
created_at: 2026-08-06 14:28:00
updated_at: 2026-08-06 14:28:00
---

# 设计

## 统一规则

最终输出中的“下一步”命令参数选择遵循：

| 来源对象 | 适用命令 | 下一步参数 |
|---|---|---|
| REQ 来源 | `/req-*`、后续 `/opsx-apply`、`/opsx-archive` | 原始 `REQ-xxxx-*` |
| BUG 来源 | `/bug-*`、后续 `/opsx-apply`、`/opsx-archive` | 原始 `BUG-xxxx-*` |
| 非 REQ/BUG Change | `/opsx-*` | `<change-id>` |

示例：

```text
/req-opsx REQ-0100-mintlify-docs-site-ia-content-experience
→ /opsx-apply REQ-0100-mintlify-docs-site-ia-content-experience
→ /opsx-archive REQ-0100-mintlify-docs-site-ia-content-experience
```

## 输入解析

`/opsx-apply` 与 `/opsx-archive` 的 `<target>` 支持三类输入：

- `REQ-*`：读取对应需求 `trace.md` 的 `openspec_changes[]`，选择当前应处理的 linked Change。
- `BUG-*`：读取对应缺陷 `trace.md` 的 `openspec_changes[]`，选择当前应处理的 linked Change。
- 其他：按 OpenSpec `<change-id>` 处理。

解析原则：

- apply 阶段优先选择 active Change，或状态为 `proposed` / `in_progress` / `applied` 但尚未 archived 的 Change。
- archive 阶段优先选择已 applied 且仍 active 的 Change。
- 若一个 REQ/BUG 关联多个候选 Change，必须列出候选并让用户明确选择，不得猜测。
- 成功解析后，内部执行仍使用真实 `<change-id>` 调用 OpenSpec CLI、Workflow Sync 和 AI Usage hook。
- 最终下一步展示继续使用原始 REQ/BUG ID。

## 校验

扩展 `scripts/validate-agent-context-budget.py`：

- 检查 `req-opsx` / `bug-opsx` 不再输出 `/opsx-apply <change>` 作为 REQ/BUG 来源的下一步模板。
- 检查 `opsx-apply` / `opsx-archive` 文档声明支持 REQ/BUG target 解析。

## 历史兼容

已有命令仍可接受真实 `<change-id>`，但下一步引导优先使用原始 REQ/BUG ID。历史 trace、archive 路径和 OpenSpec Change 名称不重写。
