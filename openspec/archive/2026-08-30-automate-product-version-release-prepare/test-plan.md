---
title: PRODUCT_VERSION 发布准备自动同步测试计划
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 22:41:57
---

# Test Plan

## 自动化校验

- `python -m py_compile scripts/validate-release.py scripts/validate-image-build.py`
- `uv run pytest tests/test_release_validation.py::test_release_prepare_syncs_product_version_sources_and_metadata tests/test_release_validation.py::test_image_prepare_blocks_when_product_version_sources_are_not_aligned tests/test_release_validation.py::test_version_mismatch_blocks_release_even_with_rationale tests/test_release_validation.py::test_release_status_classifies_product_version_mismatch_as_prepare_gap tests/test_release_validation.py::test_image_input_candidates_include_user_visible_product_versions -q`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --sync-product-version`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage prepare`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish`
- `python scripts/validate-image-build.py prepare --release v1.2.2`
- `python scripts/validate-image-build.py validate-plan --release v1.2.2`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate automate-product-version-release-prepare`
- `python scripts/validate-sprint-scope.py sprint-029 --item automate-product-version-release-prepare`

## 人工复核

- 确认 `/release-prepare` 不再要求人工编辑 `PRODUCT_VERSION`。
- 确认 `/release-publish` 不会写版本源。
- 确认 `/image-prepare` 的版本源 blocker 指向 `/release-prepare <version>`。
