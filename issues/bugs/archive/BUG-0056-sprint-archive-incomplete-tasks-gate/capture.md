---
bug_id: BUG-0056-sprint-archive-incomplete-tasks-gate
status: captured
created_at: 2026-07-04 15:04:22
updated_at: 2026-07-04 15:04:22
severity_hint: high
environment: local
related_requirement:
related_bug:
---

# 现象

`/sprint-archive` 在 Sprint 内部分 OpenSpec Change 的 `tasks.md` 仍存在 `- [ ]` 未完成项时，仍然可以继续归档并关闭 Sprint。

# 复现步骤

1. 准备一个 Sprint，其 `sprint.yaml` `changes[]` 引用至少一个 `tasks.md` 含未完成项的 change。
2. 执行 `/sprint-archive <sprint-id>`。
3. 观察 change 可被归档，Sprint 也可被标记为 completed。

# 期望 vs 实际

- 期望：默认模式下，任何未完成 `tasks.md` 项都必须阻断 `/sprint-archive`；只有显式 `--force` 且逐项确认后才允许继续。
- 实际：流程说明存在文字门禁，但缺少可执行前置校验，导致未完成 tasks 也可归档。

# 附件

- sprint-004 归档后仍存在未完成 task 的历史样本：
  - `openspec/changes/archive/2026-07-03-add-product-usage-logging/tasks.md`
  - `openspec/changes/archive/2026-07-03-fix-admin-content-padding-too-large/tasks.md`
