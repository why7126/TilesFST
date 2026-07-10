---
bug_id: BUG-0056-sprint-archive-incomplete-tasks-gate
created_at: 2026-07-04 15:04:22
updated_at: 2026-07-04 15:04:22
---

# Workaround

在修复前，执行 `/sprint-archive` 前人工检查每个 `openspec/changes/<change-id>/tasks.md`：

```bash
rg "^- \\[ \\]" openspec/changes openspec/changes/archive
```

该规避方式不可靠，因为它无法限定当前 Sprint 范围，也不能统一处理 active / archived change 的路径解析。
