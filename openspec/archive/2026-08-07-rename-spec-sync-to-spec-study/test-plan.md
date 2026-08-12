---
created_at: 2026-08-07 09:48:49
updated_at: 2026-08-07 09:48:49
change_id: rename-spec-sync-to-spec-study
---

# 测试计划

## 校验命令

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `python scripts/validate-sprint-scope.py sprint-022 --item rename-spec-sync-to-spec-study`
- `openspec validate rename-spec-sync-to-spec-study`

## 业务测试

本变更仅修改治理资产和技能命名，不涉及 `src/` 业务运行时代码；后端、前端、小程序业务测试不适用。
