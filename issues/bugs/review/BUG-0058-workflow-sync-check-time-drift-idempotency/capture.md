---
bug_id: BUG-0058-workflow-sync-check-time-drift-idempotency
status: captured
created_at: 2026-07-04 15:33:21
updated_at: 2026-07-04 15:33:21
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

执行 `python scripts/sync-workflow-status.py --check` 时，已归档 Sprint 的 Scope 表仍报告漂移，漂移内容集中在 archived Change 的归档时间字段。重复同步后，归档时间可能受 issue trace 的 `updated_at` 刷新影响而发生变化，导致 check 幂等性不足。

# 复现步骤

1. 在当前仓库执行 `python scripts/sync-workflow-status.py --check`。
2. 观察 `iterations/archive/sprint-004/sprint.md` 被报告为 drift。
3. 对比脚本渲染结果与现有 Scope 表，确认同一 archived Change 的归档时间在 `08:15:02`、`08:16:02` 等值之间漂移。

# 期望 vs 实际

- 期望：`workflow-sync --check` 只检查稳定衍生内容；已归档 Change 的时间来源应来自显式归档记录、变更记录或归档目录日期，不应受后续 `updated_at` touch 影响。
- 实际：归档时间解析会读取 issue trace 或 change trace 的 frontmatter `updated_at`，后续同步刷新 `updated_at` 后，`--check` 又报告新的时间漂移。

# 附件

- 复现命令：`python scripts/sync-workflow-status.py --check`
- 漂移文件：`iterations/archive/sprint-004/sprint.md`
