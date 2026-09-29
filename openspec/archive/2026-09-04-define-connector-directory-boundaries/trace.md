---
change_id: define-connector-directory-boundaries
status: applied
lifecycle_stage: change
created_at: 2026-09-04 17:30:00
updated_at: 2026-09-04 17:30:00
---

# 变更追踪

## 基本信息

```yaml
change_id: define-connector-directory-boundaries
change_type: governance
status: applied
sprint: sprint-029
source_requirement: null
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 本 Change 只补充连接器目录边界、文档入口和目录校验脚本，不新增 API、DB、请求日志、Task Trace、端侧请求封装、媒体上传或管理端写操作。
  validation: OpenSpec、目录结构、上下文预算、Sprint scope、OpenSpec 文档语言、脚本编译和 Workflow Sync 校验通过。
```

## 归档验证摘要

```yaml
documentation_sync:
  status: done
  updated:
    - rules/directory-structure.md
    - AGENTS.md
    - docs/README.md
    - connectors/README.md
    - docs/spec-logs/CHANGELOG.md
    - docs/spec-logs/20260904171641-governance-connector-directory-boundaries.md
api: not_applicable
database: not_applicable
web: not_applicable
miniapp: not_applicable
admin: not_applicable
orval: not_applicable
docker_compose: not_applicable
tests:
  - python -m py_compile scripts/validate-directory-structure.py
  - python scripts/validate-directory-structure.py
  - python scripts/validate-agent-context-budget.py --change define-connector-directory-boundaries
  - python scripts/validate-sprint-scope.py sprint-029 --item define-connector-directory-boundaries
  - python scripts/validate-openspec-language.py
  - openspec validate define-connector-directory-boundaries --strict
evidence_source: local_cli
verification_boundary: 本地治理文档与脚本校验，不代表 WorkBuddy 连接器运行时已实现。
```
