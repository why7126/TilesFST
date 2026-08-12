---
created_at: 2026-08-07 11:22:49
updated_at: 2026-08-07 11:22:49
change_id: avoid-duplicate-spec-study-reports
---

# 测试计划

## 治理校验

- `openspec validate avoid-duplicate-spec-study-reports`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `python scripts/validate-sprint-scope.py sprint-022 --item avoid-duplicate-spec-study-reports`

## 业务测试

不适用。本 Change 只修改治理 Skill、规则和文档，不修改业务 `src/`。
