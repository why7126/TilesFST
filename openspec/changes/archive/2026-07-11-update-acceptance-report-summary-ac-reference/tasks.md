## 1. Acceptance Report Structure

- [x] 1.1 Locate Sprint acceptance-report template/generation paths used by `/sprint-propose` and `/sprint-archive`.
- [x] 1.2 Update generated or maintained `acceptance-report.md` structure to include final acceptance summary, final archive check, human sign-off record, and raw AC reference sections.
- [x] 1.3 Ensure raw AC reference entries include source paths and unchecked-item semantics where applicable.

## 2. Workflow Sync And Fact Sheet

- [x] 2.1 Update `scripts/workflow_sync/patch.py` so acceptance-report refreshes derived note/status areas without overwriting manual final verdict, reviewer, or sign-off fields.
- [x] 2.2 Update `scripts/generate-sprint-fact-sheet.py` so acceptance signals prioritize final summary/archive-check content over raw AC reference text.
- [x] 2.3 Preserve no-delta behavior so Workflow Sync does not refresh `updated_at` solely due to derived time drift.

## 3. Documentation And Validation

- [x] 3.1 Update relevant workflow skill/rule documentation for `acceptance-report.md` section responsibilities.
- [x] 3.2 Add focused validation or regression fixtures covering final PASS with unchecked raw AC reference items.
- [x] 3.3 Run Workflow Sync check and relevant script tests after implementation.
- [x] 3.4 Decide whether Sprint 005 acceptance report needs one-off cleanup or remains historical evidence.

## 实现记录

- `iterations/change/sprint-006/acceptance-report.md` 已是分层结构；本次补齐 Workflow Sync 对新版 Scope 表状态列的刷新。
- `scripts/generate-sprint-fact-sheet.py` 已优先读取 `最终验收摘要` / `最终归档检查`，原始 AC 未勾选项仅作为证据提示。
- 已运行 `uv run pytest tests/test_workflow_sync_time_drift.py tests/test_generate_sprint_fact_sheet.py`。
- Sprint 005 报告保留为历史证据，不做一-off 清理。
