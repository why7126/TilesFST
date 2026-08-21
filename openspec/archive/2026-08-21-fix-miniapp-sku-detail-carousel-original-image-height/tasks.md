---
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: implemented
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 13:52:48
---

# 任务清单

- [x] 复核 SKU 详情接口媒体字段生成逻辑，确认图片 `url`、`preview_url`、视频 `url`、`cover_url` 的现有语义和兼容风险。
- [x] 调整详情页图片首屏展示源，使商品详情页大图区域使用原图或详情级高清展示图。
- [x] 保持图片预览使用原图或等价高清 URL，视频播放 URL 和封面逻辑不被误改。
- [x] 保持商品列表、商品卡片、推荐位和 Banner 的 `.thumb` 或等价轻量图片策略。
- [x] 调整小程序商品详情页轮播高度，覆盖 320、375、430px 逻辑宽度，并保证首屏露出商品名称或关键商品信息。
- [x] 补充后端回归测试：SKU 详情高清展示 URL、预览高清 URL、列表/卡片缩略图策略。
- [x] 补充小程序静态或样式回归：详情页首屏图片绑定、图片预览绑定、轮播高度约束和首屏信息露出。
- [x] 更新 API 文档、OpenAPI/Orval 或说明无需更新的原因；若公开字段 schema 变化，必须执行 Orval 同步。
- [x] 回填媒体四联验收：key、object、URL、render；缺少 DevTools、真机或体验版证据时记录 blocked 或发布前补证。
- [x] 更新 `BUG-0131-miniapp-sku-detail-carousel-original-image-height` 验收回填和 trace，保留根因证据闭环。
- [x] 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若不需要，在归档前说明原因。

## 实现备注

- API schema 未新增字段，`media[].url` / `preview_url` 字段结构不变，仅调整 SKU 详情图片展示 URL 语义；本次无需 Orval。
- 当前缺少微信 DevTools、真机或体验版 render evidence，发布前需补充截图或人工验收摘要。
- 本缺陷属于清晰度与布局体验回退，已由 BUG/Change/验收材料记录，不单独沉淀 `docs/knowledge-base/incidents/`。
