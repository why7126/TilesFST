---
created_at: 2026-08-31 14:06:32
updated_at: 2026-08-31 14:06:32
---

# 测试计划

## 校验命令

```bash
openspec validate rename-evidence-source-specs
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
python scripts/validate-agent-context-budget.py
python scripts/validate-sprint-scope.py sprint-029 --item rename-evidence-source-specs
python scripts/validate-doc-prose-hygiene.py openspec/changes/rename-evidence-source-specs docs/spec-logs/CHANGELOG.md docs/spec-logs/20260831140632-governance-evidence-source-specs.md
```

## 测试说明

本次只修改治理规格与治理日志，不触达业务 `src/`、API、DB、Web、小程序运行时代码、管理端代码或 Docker Compose 配置，因此不需要业务单元测试、Orval 生成或 Compose 验证。
