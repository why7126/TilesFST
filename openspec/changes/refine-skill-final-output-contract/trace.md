---
change_id: refine-skill-final-output-contract
change_type: update
status: applied
source_sprint: sprint-026
created_at: 2026-08-26 20:52:46
updated_at: 2026-08-26 20:58:03
---

# Change 追踪

## 基本信息

```yaml
change_id: refine-skill-final-output-contract
change_type: update
status: applied
sprint: sprint-026
source_requirement: null
source_bug: null
affected_capabilities:
  - agent-workflow-tooling
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
orval_required: false
docker_compose_required: false
```

## 影响声明

| 范围 | 影响 |
|---|---|
| `.agents/skills` | 调整命令最终输出契约与命令族示例。 |
| `AGENTS.md` / `rules` / `docs` | 更新命令输出摘要，保持与技能契约一致。 |
| `scripts` | 扩展 `validate-agent-context-budget.py`。 |
| 业务 `src/` | 不涉及。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-26 20:52:46 | `/spec-opt` | 创建命令最终输出契约治理 Change，并纳入 `sprint-026`。 |
| 2026-08-26 20:58:03 | `/spec-opt` | 批量更新命令技能最终输出契约，补强 sprint-propose、req-opsx、bug-opsx、upgrade 命令族示例，并扩展上下文预算校验脚本。 |
