---
created_at: 2026-08-30 12:45:20
updated_at: 2026-08-30 12:55:22
---

# 测试计划

## 聚焦测试

- 新增 `tests/test_environment_tiered_evidence_validation.py`，覆盖开发证据冒充生产通过、体验版/真机 Network 缺 evidence、`production_only_pending` 生产发布阻断和正常开发后置通过。
- Sprint readiness 和 release status 聚焦单测覆盖上层 validator 接入。
- 已运行 `uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_sprint_archive_readiness.py::test_environment_evidence_blocker_blocks_sprint_archive_readiness tests/test_release_validation.py::test_release_status_reclassifies_production_only_pending_for_production_target tests/test_release_validation.py::test_release_status_keeps_production_followups_non_blocking_for_development`：8 passed。
- 已运行 `uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_sprint_archive_readiness.py tests/test_release_validation.py`：47 passed, 3 failed；失败来自既有 usage-docs screenshot fixture 规则漂移，不属于本次环境分层 evidence 门禁。

## 治理校验

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate enforce-environment-tiered-evidence-gates`
- `python scripts/validate-sprint-scope.py sprint-028 --item enforce-environment-tiered-evidence-gates`
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`
