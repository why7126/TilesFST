---
change_id: fix-admin-banner-create-schema-drift
status: archived
type: fix
created_at: 2026-07-23 11:46:14
updated_at: 2026-07-23 22:59:21
related_bug: BUG-0083-prod-admin-brand-banner-save-500
related_requirement: REQ-0062-admin-banner-placement-scope
iteration: sprint-011
---

# Change Trace

```yaml
change_id: fix-admin-banner-create-schema-drift
status: archived
type: fix
created_at: 2026-07-23 11:46:14
updated_at: 2026-07-23 22:59:21
related_bug: BUG-0083-prod-admin-brand-banner-save-500
related_requirement: REQ-0062-admin-banner-placement-scope
iteration: sprint-011
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 22:59:21 | /opsx-archive | Change 已归档到 `openspec/changes/archive/2026-07-23-fix-admin-banner-create-schema-drift/`，正式规格已同步。 |
| 2026-07-23 22:56:30 | production-confirm | 用户确认更新后端镜像并执行启动迁移后，生产创建品牌类型 Banner 保存已恢复。 |
| 2026-07-23 12:08:13 | /sprint-propose BUG-0083 sprint-011 | 纳入 sprint-011，允许后续按 Sprint 范围执行 `/opsx-apply`。 |
| 2026-07-23 11:46:14 | /bug-opsx BUG-0083 | 创建 OpenSpec Change，用于修复生产 Admin Banner 创建接口 MySQL schema drift 导致的 500。 |
