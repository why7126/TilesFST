---
title: workflow-sync check 时间漂移幂等性
created_at: 2026-07-10 00:15:41
updated_at: 2026-07-10 00:15:41
source: BUG-0058-workflow-sync-check-time-drift-idempotency
---

# 事件摘要

BUG-0058 暴露了 workflow-sync 的时间语义边界问题：已归档 Change 渲染到 Sprint Scope 表时，脚本可能把 issue trace 或 change trace 的 frontmatter `updated_at` 当作归档事实时间。由于 `updated_at` 会随文档维护刷新，连续执行 `workflow-sync --check` 可能在无业务变化时报告 drift。

# 根因

- 归档事实时间和文档维护时间混用。
- archived Change 时间推导曾允许读取可变 frontmatter `updated_at`。
- Markdown 持久化逻辑缺少“渲染结果与原文一致则不 touch”的幂等保护。

# 修复原则

- archived Change 归档时间只来自稳定事实源：trace lifecycle、归档/变更记录、archive 目录日期兜底。
- `updated_at` 只表示文档维护时间，不能作为业务事实或归档事实。
- Markdown 写入前比较最终内容；无正文变化时不写文件、不刷新 `updated_at`。
- workflow-sync 类脚本必须补连续 `--check` no delta 回归。

# 验证

- `uv run pytest tests/test_workflow_sync_time_drift.py`：4 passed。
- `python scripts/sync-workflow-status.py --check` 连续两次返回 0，均 no delta。
- `python scripts/validate-directory-structure.py` 通过。
