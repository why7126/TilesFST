---
change_id: relax-issue-archive-sprint-completion-gate
status: applied
type: modify
created_at: 2026-07-16 09:34:00
updated_at: 2026-07-16 09:39:00
source_requirement: null
iteration: null
---

# Trace

## 影响分析

```yaml
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
  workflow_scripts: true
  openspec: true
capabilities:
  new: []
  modified:
    - agent-workflow-tooling
orval_required: false
docker_compose_required: false
```

## 验证摘要

```yaml
checks:
  openspec_change_validate:
    command: "openspec validate relax-issue-archive-sprint-completion-gate --strict"
    result: pass
  focused_tests:
    command: "python -m pytest tests/test_issue_status_residuals.py"
    result: "8 passed"
  real_issue_reconcile:
    issue: REQ-0039-xl-admin-page-layered-acceptance-template
    sprint: sprint-008
    sprint_status: planning
    result: "residual reconcile write succeeded; promote review -> archive succeeded"
runtime_impact:
  api: false
  database: false
  orval: false
  docker_compose: false
  web_runtime: false
  miniapp: false
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-16 09:39:00 | /opsx-apply | 修复单 Issue 归档不应被未完成 Sprint 阻断的 workflow 门禁，并验证 REQ-0039 可归档 |
