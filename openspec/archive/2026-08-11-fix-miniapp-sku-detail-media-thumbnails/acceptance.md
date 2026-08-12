---
change_id: fix-miniapp-sku-detail-media-thumbnails
status: proposed
created_at: 2026-08-07 22:55:00
updated_at: 2026-08-07 22:55:00
source_bug: BUG-0125-miniapp-sku-detail-media-original-load
---

# 验收要求

## BUG 验收

- BUG-0125 的 `acceptance.md` 必须回填媒体四联验收。
- 验收结论不得仅凭接口字段非空或 object 存在通过。
- 小程序 evidence 缺失时必须标记 blocked，不得视为通过。

## 完成标准

- SKU 详情首屏图片使用 `.thumb` 缩略图。
- 图片预览仍使用原图。
- 视频封面优先使用缩略图，视频播放 URL 不变。
- API 文档和测试均同步。
