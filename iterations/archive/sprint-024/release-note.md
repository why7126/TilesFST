---
created_at: 2026-08-21 08:18:18
updated_at: 2026-08-21 14:42:16
publish_status: published
---

# sprint-024 发布说明

本 Sprint 包含治理资产更新与 2 个小程序展示缺陷修复范围，5 个 Change 均已归档。

## 已纳入范围

| 类型 | 编号 | 说明 | 发布影响 |
|---|---|---|---|
| Change | apply-moonbox-governance-quality-learnings | MoonBox 治理质量能力应用 | 不产生产品运行时发布内容 |
| BUG | BUG-0130-miniapp-home-no-jump-banner-internal-title | 小程序首页无跳转轮播图不应显示内部标题 | 已实现公开 Banner 标题净化与小程序兜底防泄露；验收返修移除首页 Banner 渐变遮罩、图片透明化和无跳转点击占位提示 |
| BUG | BUG-0131-miniapp-sku-detail-carousel-original-image-height | 小程序商品详情页轮播图清晰度不足且高度偏小 | 已实现详情页高清展示图、轮播高度和列表 `.thumb` 性能边界修复 |

## 发布提示

- BUG-0130 已归档；发布前建议补小程序 DevTools、真机或体验版 render evidence。
- BUG-0131 已归档；发布前建议补商品详情页清晰度、高度和首屏信息露出 render evidence。
- 本次修复未改变公开 Banner API schema，不需要 Orval；已同步 API 语义文档与小程序回归。
- 若确认内部标题已写入存量图片对象，需要记录素材替换或清理摘要。
