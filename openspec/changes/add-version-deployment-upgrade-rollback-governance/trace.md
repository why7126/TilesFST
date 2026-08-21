---
change_id: add-version-deployment-upgrade-rollback-governance
status: applied
lifecycle_stage: change
source_requirement: REQ-0114-version-deployment-upgrade-rollback-governance
source_sprint: sprint-025
change_type: add
created_at: 2026-08-21 18:48:30
updated_at: 2026-08-21 22:09:09
---

# Change 追踪

## 基本信息

```yaml
change_id: add-version-deployment-upgrade-rollback-governance
status: applied
lifecycle_stage: change
source_requirement: REQ-0114-version-deployment-upgrade-rollback-governance
source_sprint: sprint-025
change_type: add
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
  scripts: true
  workflow: true
capabilities:
  new:
    - version-deployment-upgrade-rollback-governance
  modified:
    - product-release-management
    - deployment
    - deployment-image-build
    - database
    - object-storage
    - agent-workflow-tooling
iteration: sprint-025
related_requirements:
  - REQ-0114-version-deployment-upgrade-rollback-governance
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 22:09:09 | `/opsx-modify` | 验收返修：将用户命令与 Skill 名称简化为 `upgrade-plan` / `upgrade-validate`，同步 AGENTS、rules、docs、REQ、OpenSpec delta、Sprint 验收文案和 Skill 目录；底层脚本 `scripts/validate-release-upgrade.py` 保持不改名 |
| 2026-08-21 19:11:55 | `/opsx-apply` | 完成实现与验证，任务 23/23 完成；Workflow Sync 已同步 REQ-0114、Change 与 sprint-025，待归档 |
| 2026-08-21 18:48:30 | `/req-opsx` | 从 REQ-0114 创建 OpenSpec Change，生成 proposal、design、specs、tasks 与 trace |
