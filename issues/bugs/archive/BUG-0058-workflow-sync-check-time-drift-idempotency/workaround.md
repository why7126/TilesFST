---
bug_id: BUG-0058-workflow-sync-check-time-drift-idempotency
created_at: 2026-07-05 08:00:34
updated_at: 2026-07-05 08:00:34
---

# Workaround

修复前可临时规避：

1. 避免在无正文变化时手动运行会刷新大量 `updated_at` 的 workflow sync。
2. 如果 `--check` 只报告 archived Change 时间字段漂移，可先对比 issue trace 的 lifecycle / 变更记录和 archive 目录日期，确认是否为元数据漂移。
3. 必要时运行一次非 `--check` 的 `python scripts/sync-workflow-status.py` 收敛衍生文档，再立即运行 `python scripts/sync-workflow-status.py --check` 验证。

该规避方式不可靠，因为它依赖人工判断 drift 是否仅为时间元数据污染，仍可能掩盖真实的 Scope 表漂移。
