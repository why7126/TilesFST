---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
acceptance_status: passed
created_at: 2026-08-22 21:24:15
updated_at: 2026-08-25 14:51:36
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | 对仅 `captured` 且已生成 `bug.md` 的 BUG 执行 `bug.generate` Workflow Sync 后，`trace.md` frontmatter 和 fenced YAML 均变为 `status: draft` | pass |
| AC-002 | `trace.md` 的 `lifecycle.generated` 与 `updated_at` 使用本次生成时间，且 `## 变更记录` 追加 `/bug-generate` 记录 | pass |
| AC-003 | `issues/bugs/_registry.yaml` 中目标 BUG 状态同步为 `draft`，不需要命令侧或人工额外修正 | pass |
| AC-004 | `issues/bugs/CHANGELOG.md` 中目标 BUG 当前态同步为 `draft`，下一步为 `/bug-complete <BUG-id>` | pass |
| AC-005 | `bug.md` frontmatter 的 `status` 保持 `draft`，不会被 Workflow Sync 反向覆盖为 `captured` | pass |
| AC-006 | 重复运行 `bug.generate` Workflow Sync 保持幂等，不重复写入异常变更记录，不破坏已生成文档 | pass |
| AC-007 | 若目标 BUG 缺少 `bug.md`，Workflow Sync 不误推进到 `draft`，并输出明确 warning 或 no-op 摘要 | pass |

## 测试建议

- 增加 `scripts/workflow_sync` 相关单元测试或回归测试，构造 `captured` BUG + 已生成 `bug.md` 的最小 fixture。
- 测试断言 trace、registry、CHANGELOG 与 `bug.md` frontmatter 的状态一致。
- 增加重复执行场景，确认没有重复或错位的 `## 变更记录`。
- 增加缺少 `bug.md` 的保护场景，确认不会凭空推进状态。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 21:55:26
accepted_by: workflow-sync
source_change: fix-workflow-sync-bug-generate-status-transition
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

