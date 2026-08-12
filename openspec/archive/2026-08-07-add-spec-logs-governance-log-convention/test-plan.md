---
created_at: 2026-08-07 10:32:44
updated_at: 2026-08-07 10:32:44
change_id: add-spec-logs-governance-log-convention
---

# 测试计划

## 校验命令

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `python scripts/validate-sprint-scope.py sprint-022 --item add-spec-logs-governance-log-convention`
- `openspec validate add-spec-logs-governance-log-convention`

## 业务测试

本变更仅修改治理资产和文档规范，不涉及 `src/` 业务运行时代码；后端、前端、小程序业务测试不适用。
