---
created_at: 2026-08-31 10:23:00
updated_at: 2026-08-31 10:23:00
---

# 测试计划

## 聚焦测试

- `uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_release_validation.py tests/test_sprint_archive_readiness.py`
- `python scripts/validate-environment-tiered-evidence.py --change deactivate-environment-tiered-evidence-gates`

## 治理校验

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate deactivate-environment-tiered-evidence-gates`
- `python scripts/validate-doc-prose-hygiene.py <focused paths>`
