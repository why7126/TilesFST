---
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:36:34
---

# 测试计划

## 聚焦验证

- `uv run pytest tests/test_release_validation.py::test_version_mismatch_blocks_release_even_with_rationale tests/test_release_validation.py::test_miniapp_product_version_mismatch_blocks_publish -q`
- `python scripts/validate-release.py --release-dir releases/v1.2.2 --stage publish --target development`

## 治理验证

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate enforce-product-version-release-gates`
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`

## 不适用

- API 测试不适用：未修改后端接口。
- DB 测试不适用：未修改 schema、migration 或数据模型。
- Orval 不适用：未修改 OpenAPI。
- Docker Compose 验证不适用：未修改 Compose 或镜像构建脚本。
