---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
root_cause_status: confirmed
category: workflow
created_at: 2026-08-22 21:24:15
updated_at: 2026-08-22 21:24:15
---

# Root Cause

## 根因状态

`confirmed`

在 `/bug-generate BUG-0136-workflow-sync-bug-generate-captured-draft` 执行中，`bug.md` 已生成且初始状态为 `draft`，随后运行 `bug.generate` Workflow Sync 后，脚本报告目标 `trace.md` 与 `_registry.yaml` 为 `Skipped (no delta)`，并且文件状态核对显示 `trace.md`、`issues/bugs/_registry.yaml`、`issues/bugs/CHANGELOG.md` 仍停留在 `captured`，`bug.md` 也被同步为 `captured`。该证据链能闭环解释“`bug.generate` 未主动从 `captured` 推进 `draft`”的现象。

## 直接原因

`scripts/sync-workflow-status.py --event bug.generate` 没有在目标 BUG 处于 `captured` 且 `bug.md` 已生成时，将 BUG 主状态推进为 `draft`。脚本还会根据未推进的主状态刷新 `bug.md` frontmatter，导致已生成的 `bug.md` 状态被拉回 `captured`。

## 根本原因

Workflow Sync 的事件到状态转换规则对 `bug.generate` 缺少完整状态推进契约，或只做了派生文档刷新而未把 `bug.generate` 视为主状态变更事件。`req.generate`、`bug.complete` 等相邻事件可能已有状态推进预期，但 `bug.generate` 的状态机映射没有覆盖 `captured -> draft`。

## 触发条件

1. 目标 BUG 已完成 capture，`trace.md` 主状态为 `captured`。
2. `/bug-generate` 已生成 `bug.md`，且 `bug.md` 语义上应为 `draft`。
3. Final Step 执行 `python scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`。
4. Workflow Sync 以当前 trace 主状态为准刷新子文档或索引，但未推进主状态。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `issues/bugs/archive/BUG-0136-workflow-sync-bug-generate-captured-draft/bug.md` | 复现 / 文件状态 | `/bug-generate` 创建了正式 `bug.md`；运行 Workflow Sync 后曾出现 `status: captured` | 子文档状态可被未推进的主状态反向覆盖 |
| `issues/bugs/archive/BUG-0136-workflow-sync-bug-generate-captured-draft/trace.md` | 文件状态 | `bug.generate` Workflow Sync 后未自动写入 `status: draft` 与 `lifecycle.generated`，需本命令链路手动修正 | 主状态推进缺失 |
| `issues/bugs/_registry.yaml` | 文件状态 | BUG-0136 在 `bug.generate` Workflow Sync 后仍为 `captured`，需手动修正为 `draft` | registry 未随生成事件推进 |
| `issues/bugs/CHANGELOG.md` | 文件状态 | BUG-0136 当前态看板在 `bug.generate` Workflow Sync 后仍建议 `/bug-generate`，需手动修正为 `/bug-complete` | 下一步推导依赖的状态事实源未更新 |
| `/bug-generate BUG-0136` 命令输出摘要 | 脚本输出 | Workflow Sync summary：`Event: bug.generate`、`Updated: 0`、`Subdocuments: checked=3, updated=1`；detail：trace 与 registry 均为 `Skipped (no delta)` | `bug.generate` 事件未将 trace/registry 作为主状态变更目标 |

## 人工补证步骤

当前根因已由本地命令复现闭环确认。后续实现阶段可补充以下证据以辅助定位代码级修复点：

1. 在 `scripts/sync-workflow-status.py` 或 `scripts/workflow_sync/` 中定位事件状态映射表，记录 `bug.generate` 是否缺少 `draft` 目标状态。
2. 增加或运行聚焦测试，构造 `captured` BUG + 已存在 `bug.md` 的 fixture，断言 `bug.generate` 后 trace、registry、CHANGELOG 和 `bug.md` 均为 `draft`。
3. 对比 `req.generate` 的同步路径，确认 REQ 与 BUG 生成事件的行为是否应保持一致。

## 验证方式

- 修复前：对 `captured` BUG 运行 `bug.generate` Workflow Sync，trace 和 registry 报告 no delta，状态仍为 `captured`，当前态看板仍建议 `/bug-generate`。
- 修复后：同样输入下，Workflow Sync 将 trace、registry、当前态看板和 `bug.md` 统一推进为 `draft`，并记录 `lifecycle.generated`；重复运行保持幂等。
