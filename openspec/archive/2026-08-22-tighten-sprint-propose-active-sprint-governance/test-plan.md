---
created_at: 2026-08-22 14:12:50
updated_at: 2026-08-22 14:12:50
---

# 测试计划

- 运行 `python scripts/validate-sprint-selection.py` 验证当前仓库默认选择。
- 运行 `uv run pytest tests/test_sprint_selection_validation.py` 验证 Sprint 选择规则函数。
- 运行 `python scripts/validate-agent-context-budget.py`。
- 运行 `python scripts/validate-openspec-language.py`。
- 运行 `python scripts/validate-directory-structure.py`。
- 运行 `openspec validate tighten-sprint-propose-active-sprint-governance`。
