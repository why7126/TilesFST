---
bug_id: BUG-0129-miniapp-rum-app-version-production
status: done
severity: medium
created_at: 2026-08-12 09:21:24
updated_at: 2026-08-12 21:37:07
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-12 09:21:24
  generated: 2026-08-12 09:42:46
  completed: 2026-08-12 14:19:46
  reviewed: 2026-08-12 14:21:57
  approved: 2026-08-12 14:21:57
iteration: sprint-023
openspec_changes:
  - change_id: fix-miniapp-rum-performance-observability
    status: archived
related_requirement: null
related_change: fix-miniapp-rum-performance-observability
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0129-miniapp-rum-app-version-production
status: done
severity: medium
created_at: 2026-08-12 09:21:24
updated_at: 2026-08-12 14:29:16
lifecycle_stage: review
lifecycle:
  captured: 2026-08-12 09:21:24
  generated: 2026-08-12 09:42:46
  completed: 2026-08-12 14:19:46
  reviewed: 2026-08-12 14:21:57
  approved: 2026-08-12 14:21:57
iteration: sprint-023
openspec_changes:
  - change_id: fix-miniapp-rum-performance-observability
    status: archived
related_requirement: null
related_change: fix-miniapp-rum-performance-observability
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-12 21:36:56 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-rum-performance-observability） |
| 2026-08-12 21:36:48 | /opsx-archive | Change `fix-miniapp-rum-performance-observability` 已归档，状态同步完成。 |
| 2026-08-12 15:03:33 | /opsx-modify | Change `fix-miniapp-rum-performance-observability` 验收返修已同步，随后已归档闭环。 |
| 2026-08-12 14:40:43 | /opsx-apply | Change `fix-miniapp-rum-performance-observability` apply 完成，随后已归档闭环。 |
| 2026-08-12 14:29:16 | `/bug-opsx` | 创建 OpenSpec Change `fix-miniapp-rum-performance-observability`，覆盖小程序版本号、`request_id`、指标标签、空态和聚合完整分组键修复范围。 |
| 2026-08-12 14:26:26 | `/sprint-propose` | 纳入 `sprint-023` 正式范围，后续已创建并归档修复 Change。 |
| 2026-08-12 14:22:25 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-12 14:21:57 | `/bug-review --approve` | 用户确认 BUG-0129 需要修复，评审通过；进入 review 阶段后建议先纳入 Sprint。 |
| 2026-08-12 14:19:46 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态进入待评审。 |
| 2026-08-12 09:42:46 | `/bug-generate` | 生成 `bug.md`，将小程序版本号、request_id、指标标签、性能观测空态和聚合隐藏分组维度统一纳入 BUG-0129 正式缺陷范围。 |
| 2026-08-12 09:21:24 | `/bug-capture` | 记录小程序 RUM 将 `production` 环境名作为 `app_version` 上报，导致管理后台性能观测表版本号显示异常；用户补充小程序与 Web 管理后台应使用统一版本号。 |

- 2026-08-12 21:36:48 workflow-sync：状态同步为 done（Change archived）
