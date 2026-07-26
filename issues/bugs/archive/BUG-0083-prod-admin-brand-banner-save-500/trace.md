---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
severity: high
created_at: 2026-07-23 10:35:53
updated_at: 2026-07-23 22:59:55
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-23 10:35:53
  generated: 2026-07-23 10:46:22
  completed: 2026-07-23 11:19:18
  reviewed: 2026-07-23 11:36:25
  approved: 2026-07-23 11:36:25
  done: 2026-07-23 22:56:30
iteration: sprint-011
openspec_changes:
  - change_id: fix-admin-banner-create-schema-drift
    type: fix
    status: archived
related_change: fix-admin-banner-create-schema-drift
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
captured_via: capture
classification_rationale: 项目已有管理端 Banner 配置与品牌类型投放能力，且历史 BUG-0075 已修复归档；生产环境创建品牌类型 Banner 时保存接口仍返回 500，属于既有能力在生产环境下的回归或残留偏差，按 BUG 记录。
---

# BUG Trace

```yaml
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
severity: high
created_at: 2026-07-23 10:35:53
updated_at: 2026-07-23 22:56:30
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-23 10:35:53
  generated: 2026-07-23 10:46:22
  completed: 2026-07-23 11:19:18
  reviewed: 2026-07-23 11:36:25
  approved: 2026-07-23 11:36:25
  done: 2026-07-23 22:56:30
iteration: sprint-011
openspec_changes:
  - change_id: fix-admin-banner-create-schema-drift
    type: fix
    status: archived
related_change: fix-admin-banner-create-schema-drift
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 22:59:55 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-banner-create-schema-drift） |
| 2026-07-23 22:59:21 | /opsx-archive | Change `fix-admin-banner-create-schema-drift` 已归档，状态同步完成。 |
| 2026-07-23 22:57:29 | /opsx-apply | Change `fix-admin-banner-create-schema-drift` apply 完成，待 archive。 |
| 2026-07-23 22:56:30 | production-confirm | 用户确认更新后端镜像并执行启动迁移后，生产创建品牌类型 Banner 保存已恢复。 |
| 2026-07-23 12:08:13 | /sprint-propose BUG-0083 sprint-011 | 纳入 sprint-011，状态推进为 in_sprint。 |
| 2026-07-23 11:46:14 | /bug-opsx BUG-0083 | 创建 OpenSpec Change `fix-admin-banner-create-schema-drift` |
| 2026-07-23 11:47:03 | workflow-sync-correction | BUG 尚未纳入 Sprint，保持 approved 状态并保留 Change 关联。 |
| 2026-07-23 11:37:16 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-23 11:36:25 | /bug-review --approve | 评审通过，允许 bug-opsx 与纳入 Sprint 规划。 |
| 2026-07-23 11:19:18 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-07-23 10:46:22 | /bug-generate | 生成正式 bug.md，状态推进为 draft。 |
| 2026-07-23 10:35:53 | /capture | 记录生产环境创建品牌类型 Banner 时 `POST /api/v1/admin/banners` 返回 500 的回归或残留缺陷。 |
