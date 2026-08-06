---
change_id: require-all-changes-sprint-before-apply
title: 所有 Change 纳入 Sprint 后才能 apply 的设计
status: proposed
created_at: 2026-08-06 14:01:45
updated_at: 2026-08-06 14:01:45
---

# 设计

## 规则变化

将 `/opsx-apply` 的准入条件统一为：

```text
任意 OpenSpec Change
→ 必须存在于某个 iterations/change|archive/<sprint>/sprint.yaml 的 changes[]
→ Workflow Sync dry-run 能通过 --sprint auto 解析到该 Sprint
→ 才允许 /opsx-apply
```

若 Change 关联 REQ/BUG，还需继续保持原有双向一致要求：

- `requirements[]` 或 `bugs[]` 包含对应 Issue。
- Issue `trace.md` 的 `iteration` 指向同一 Sprint。
- Issue 状态为 `in_sprint` 或后续交付态。

若 Change 不关联 REQ/BUG，则只要求：

- `changes[]` 包含该 Change。
- `scope_estimates[]` 中有以该 Change 为 `id` 或 `change` 的估算项。
- `/sprint-propose` 或 `scripts/add-sprint-scope-item.py --change <change-id>` 完成后通过 `validate-sprint-scope.py`。

## 命令行为

### `/opsx-apply`

- 删除“无 REQ/BUG 的 Change 可绕过门禁”。
- 对所有 Change 先运行 `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run`。
- dry-run 若返回 `change <id> not in sprint scope`，必须阻断实现。
- 对非 REQ/BUG Change，下一步提示应指向 `/sprint-propose` 或明确的 `scripts/add-sprint-scope-item.py --change <change-id> ...` 修复路径。

### `/spec-opt`

- 删除纯治理 Change 的 Sprint Gate 豁免。
- `/spec-opt` 创建或复用 Change 后，也必须在输出中提示先纳入 Sprint，再 `/opsx-apply`。

### Workflow Sync

- 文档说明中将 `opsx.apply` skipped/unresolved 从“只阻断 REQ/BUG 来源 Change”改为“阻断所有 Change”。
- 脚本已有 `find_sprints_for_change()` 解析能力；本次优先改规范和技能，不强制改同步引擎。

## 历史兼容

`add-spec-opt-governance-command` 已经在本规则生效前未纳入 Sprint 并完成归档。该历史事实不回滚、不补写到 Sprint；从本 Change apply 之后，新 Change 必须遵守新门禁。

## 校验

完成前运行：

```bash
python scripts/validate-agent-context-budget.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
openspec validate require-all-changes-sprint-before-apply
```

如扩展校验脚本，还需运行对应脚本验证。
