---
change_id: fix-stale-scan-pending-business-word
type: fix
status: applied
created_at: 2026-08-06 12:07:29
updated_at: 2026-08-06 12:48:10
source_bug: BUG-0121-stale-scan-pending-business-word
source_sprint: sprint-021
related_bugs:
  - BUG-0121-stale-scan-pending-business-word
affected_capabilities:
  - agent-workflow-tooling
  - sprint-planning-governance
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  workflow_tooling: true
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-06 12:07:29 | bug.opsx | 从 BUG-0121 创建 OpenSpec Change，状态为 proposed |
| 2026-08-06 12:48:10 | opsx.apply | 已完成 stale scan 上下文识别修复、回归测试与 OpenSpec 校验；状态为 applied |
