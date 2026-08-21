---
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: archived
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 15:07:32
source_bug: BUG-0131-miniapp-sku-detail-carousel-original-image-height
sprint: sprint-024
---

# 变更追踪

```yaml
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: archived
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 15:07:32
source_bug: BUG-0131-miniapp-sku-detail-carousel-original-image-height
sprint: sprint-024
related_specs:
  - miniapp-sku-detail-page
  - miniapp-product-list-page
  - media-acceptance-template
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-21 15:07:32 | `/release-prepare v1.1.2` | 修正归档 trace 状态一致性：归档目录、Sprint 与 BUG trace 均已记录 archived，本文件同步为 archived。 |
| 2026-08-21 13:52:48 | `/opsx-apply BUG-0131-miniapp-sku-detail-carousel-original-image-height` | 实现 SKU 详情图片高清展示 URL、小程序详情轮播高度调整、列表缩略图边界和聚焦回归测试；缺少 DevTools/真机 render evidence，已记录为发布前补证。 |
| 2026-08-21 13:43:10 | `/bug-opsx BUG-0131-miniapp-sku-detail-carousel-original-image-height` | 基于 `BUG-0131-miniapp-sku-detail-carousel-original-image-height` 创建修复 Change，状态为 proposed，待实现。 |
