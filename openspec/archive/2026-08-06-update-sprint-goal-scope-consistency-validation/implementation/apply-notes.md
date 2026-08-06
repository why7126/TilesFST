---
change_id: update-sprint-goal-scope-consistency-validation
created_at: 2026-08-06 12:03:32
updated_at: 2026-08-06 12:03:32
---

# 实现记录

## 影响范围

| 范围 | 结论 |
|---|---|
| API | 不涉及 |
| 数据库 | 不涉及 |
| Web | 不涉及 |
| 小程序 | 不涉及 |
| 管理端 | 不涉及 |
| Orval | 不需要 |
| Docker Compose | 不需要 |
| 工作流脚本 | 更新 `scripts/validate-sprint-scope.py` |
| 工作流规则 | 更新 `/sprint-propose`、Workflow Sync 与 Sprint 生命周期规则 |

## 验证证据

- `uv run pytest tests/test_validate_sprint_scope.py`
- `python scripts/validate-sprint-scope.py sprint-021 --item REQ-0102-sprint-goal-scope-consistency-validation`
- `python scripts/validate-sprint-scope.py sprint-020 --item REQ-0100-mintlify-docs-site-ia-content-experience`，预期失败并提示目标编号列表缺失
