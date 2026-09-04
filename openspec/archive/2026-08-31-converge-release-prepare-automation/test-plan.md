---
created_at: 2026-08-31 09:10:00
updated_at: 2026-08-31 09:10:00
---

# 测试计划

- 运行 `python -m py_compile scripts/validate-release.py scripts/validate-release-upgrade.py scripts/generate-usage-docs.py`。
- 运行 `uv run pytest tests/test_release_validation.py tests/test_release_upgrade_validation.py`，覆盖 release status、usage docs 和升级计划校验契约。
- 运行 `python scripts/validate-agent-context-budget.py`、`python scripts/validate-openspec-language.py`、`python scripts/validate-directory-structure.py`。
- 运行 `openspec validate converge-release-prepare-automation`。
- 针对本次触达的技能、规则、OpenSpec 和治理日志运行 `python scripts/validate-doc-prose-hygiene.py <focused-paths>`。
