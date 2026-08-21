---
bug_id: BUG-0131-miniapp-sku-detail-carousel-original-image-height
status: done
severity: medium
created_at: 2026-08-21 13:00:43
updated_at: 2026-08-21 14:42:16
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-21 13:00:43
  generated: 2026-08-21 13:06:39
  completed: 2026-08-21 13:08:22
  reviewed: 2026-08-21 13:11:55
  approved: 2026-08-21 13:11:55
iteration: sprint-024
openspec_changes:
  - change_id: fix-miniapp-sku-detail-carousel-original-image-height
    type: fix
    status: archived
related_requirement: null
related_bug: BUG-0125-miniapp-sku-detail-media-original-load
---

# BUG Trace

```yaml
bug_id: BUG-0131-miniapp-sku-detail-carousel-original-image-height
status: done
severity: medium
created_at: 2026-08-21 13:00:43
updated_at: 2026-08-21 14:42:16
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-21 13:00:43
  generated: 2026-08-21 13:06:39
  completed: 2026-08-21 13:08:22
  reviewed: 2026-08-21 13:11:55
  approved: 2026-08-21 13:11:55
iteration: sprint-024
openspec_changes:
  - change_id: fix-miniapp-sku-detail-carousel-original-image-height
    type: fix
    status: archived
related_requirement: null
related_bug: BUG-0125-miniapp-sku-detail-media-original-load
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 14:42:16 | /sprint-archive | Sprint close stale scan 修正历史中间态描述；BUG-0131 当前状态为 done，Change 已归档。 |
| 2026-08-21 14:38:23 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-carousel-original-image-height） |
| 2026-08-21 14:38:18 | /opsx-archive | Change `fix-miniapp-sku-detail-carousel-original-image-height` 已归档，状态同步完成。 |
| 2026-08-21 14:38:18 | workflow-sync | 状态同步为 done（Change archived）。 |
| 2026-08-21 13:54:57 | /opsx-apply | Change `fix-miniapp-sku-detail-carousel-original-image-height` apply 完成，后续已归档。 |
| 2026-08-21 13:43:10 | `/bug-opsx BUG-0131-miniapp-sku-detail-carousel-original-image-height` | 创建修复 Change `fix-miniapp-sku-detail-carousel-original-image-height`，后续已实现并归档。 |
| 2026-08-21 13:16:46 | `/sprint-propose --bug BUG-0131-miniapp-sku-detail-carousel-original-image-height` | 纳入 `sprint-024` 正式范围，后续已创建并归档修复 OpenSpec Change。 |
| 2026-08-21 13:12:57 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-21 13:11:55 | `/bug-review --approve` | 用户确认批准修复，状态推进为 `approved`，准备纳入 Sprint。 |
| 2026-08-21 13:08:22 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；根因状态为 probable，媒体四联验收待修复后补证，状态推进为 `pending_review`。 |
| 2026-08-21 13:06:39 | `/bug-generate` | 基于 capture、探索结论和用户补充截图生成正式 `bug.md`，状态推进为 `draft`。 |
| 2026-08-21 13:00:43 | `/bug-capture` | 记录小程序商品详情页轮播首屏使用 `.thumb` 导致大图清晰度不足，且固定 `680rpx` 高度不符合瓷砖详情展示预期的问题；建议详情页展示改用原图或详情级展示图，列表仍保留 `.thumb`。 |
