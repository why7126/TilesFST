---
bug_id: BUG-0058-workflow-sync-check-time-drift-idempotency
created_at: 2026-07-05 08:00:34
updated_at: 2026-07-05 08:00:34
---

# Root Cause

## 直接原因

`workflow-sync` 在推导 archived Change 的归档时间时，会从关联 issue trace 或 change trace 的 frontmatter `updated_at` 取值；同时普通同步写入会在正文无变化时刷新 `updated_at`。这两个行为叠加后，`--check` 会把上一次同步产生的更新时间误判为新的归档事实。

## 根本原因

归档时间和文档更新时间的语义边界不清晰：

- archived Change 的归档时间应来自稳定事实源，例如 lifecycle、变更记录或归档目录日期。
- `updated_at` 是文档维护时间，属于可变元数据，不适合作为归档事实。
- 写入辅助函数缺少“正文无变化则不 touch frontmatter”的幂等保护。

## 触发条件

- Sprint Scope 表包含 archived Change 的归档时间；
- 关联 issue trace / change trace 已处于 done 或 archived 状态；
- 执行 workflow sync 后刷新了 trace 或 Sprint 文档的 `updated_at`；
- 再次执行 `python scripts/sync-workflow-status.py --check`。

## 分类

workflow / tooling / document-metadata
