---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
severity: high
created_at: 2026-08-01 07:12:45
updated_at: 2026-08-01 08:07:11
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-01 07:12:45
  generated: 2026-08-01 07:22:02
  completed: 2026-08-01 07:25:02
  reviewed: 2026-08-01 07:31:13
  approved: 2026-08-01 07:31:13
iteration: sprint-016
openspec_changes:
  - change_id: fix-public-sku-main-image-pending-path
    type: fix
    status: archived
related_requirement: null
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
severity: high
created_at: 2026-08-01 07:12:45
updated_at: 2026-08-01 08:07:11
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-01 07:12:45
  generated: 2026-08-01 07:22:02
  completed: 2026-08-01 07:25:02
  reviewed: 2026-08-01 07:31:13
  approved: 2026-08-01 07:31:13
iteration: sprint-016
openspec_changes:
  - change_id: fix-public-sku-main-image-pending-path
    type: fix
    status: archived
related_requirement: null
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-01 08:06:32 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-public-sku-main-image-pending-path） |
| 2026-08-01 08:06:04 | /opsx-archive | Change `fix-public-sku-main-image-pending-path` 已归档，状态同步完成。 |
| 2026-08-01 07:58:44 | /opsx-apply | Change `fix-public-sku-main-image-pending-path` apply 完成，待 archive。 |
| 2026-08-01 07:43:29 | `/sprint-propose sprint-016` | 纳入 sprint-016 正式范围，同步关联 Change `fix-public-sku-main-image-pending-path`。 |
| 2026-08-01 07:35:40 | `/bug-opsx BUG-0099` | 创建 OpenSpec Change `fix-public-sku-main-image-pending-path`。 |
| 2026-08-01 07:32:07 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-01 07:31:13 | `/bug-review --approve` | 评审通过，确认修复；可进入 /bug-opsx 或纳入 Sprint 正式范围。 |
| 2026-08-01 07:25:02 | `/bug-complete` | 补齐 root-cause.md、workaround.md、acceptance.md，状态推进为 pending_review，等待评审确认是否修复。 |
| 2026-08-01 07:22:02 | `/bug-generate` | 基于 capture 与 explore 证据生成正式缺陷稿 bug.md，状态推进为 draft。 |
| 2026-08-01 07:12:45 | `/capture` | 记录公开商品主图对象 key 长期停留在 `images/default/tiles/pending/...` 的问题，分类为 BUG。 |
