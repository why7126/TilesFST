---
created_at: 2026-07-05 15:09:02
updated_at: 2026-07-10 00:15:41
---

# Tasks

## 1. Baseline

- [x] 1.1 确认 BUG-0058 的 `bug.md`、`root-cause.md`、`acceptance.md` 与 `trace.md` 已进入 review / in_sprint 状态。
- [x] 1.2 确认 drift 复现点为 archived Change 时间字段，而非 Sprint 范围或状态真实变化。

## 2. Implementation

- [x] 2.1 调整 workflow-sync archived Change 归档时间推导，移除 issue/change trace frontmatter `updated_at` 作为事实源的路径。
- [x] 2.2 为归档时间解析保留稳定来源优先级：lifecycle / 归档记录 / archive 目录日期。
- [x] 2.3 调整 Markdown 持久化逻辑，确保渲染结果与原文一致时不写文件、不刷新 `updated_at`。

## 3. Regression Tests

- [x] 3.1 增加可变 `updated_at` 晚于真实归档事实的 archived Change 测试。
- [x] 3.2 增加 `persist_markdown` 无正文变化时不 touch `updated_at` 的测试。
- [x] 3.3 增加连续 `workflow-sync --check` no delta 的回归验证。

## 4. Validation

- [x] 4.1 运行 `uv run pytest tests/test_workflow_sync_time_drift.py`。
- [x] 4.2 运行 `python scripts/sync-workflow-status.py --check`。
- [x] 4.3 再次运行 `python scripts/sync-workflow-status.py --check`，确认 no delta。
- [x] 4.4 运行 `python scripts/validate-directory-structure.py`。

## 5. Trace

- [x] 5.1 更新 BUG-0058 trace，记录本 Change 与回归验证结果。
- [x] 5.2 更新 sprint-005 验收报告，关联 `fix-workflow-sync-check-time-drift-idempotency`。
- [x] 5.3 若修复经验具备长期复用价值，补充 `docs/knowledge-base/incidents/` 或 Sprint 复盘行动项。
