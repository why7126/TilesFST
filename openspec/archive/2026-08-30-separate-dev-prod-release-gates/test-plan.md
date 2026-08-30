---
created_at: 2026-08-30 09:50:00
updated_at: 2026-08-30 09:50:00
---

# Test Plan

- Validate OpenSpec change: `openspec validate separate-dev-prod-release-gates`.
- Validate release metadata: `python scripts/validate-release.py --release-dir releases/v1.2.1 --stage publish`.
- Validate development upgrade plan generation and validation for `fresh -> v1.2.1`.
- Validate development upgrade plan generation and validation for `v1.2.0 -> v1.2.1`.
- Validate governance scripts: `python scripts/validate-agent-context-budget.py`, `python scripts/validate-directory-structure.py`, `python scripts/validate-openspec-language.py`.
- Validate touched prose: `python scripts/validate-doc-prose-hygiene.py <focused paths>`.
