---
bug_id: BUG-0148-miniapp-product-list-card-image-fit
status: done
created_at: 2026-09-04 16:52:03
updated_at: 2026-09-07 22:58:30
severity_hint: medium
environment: miniapp
related_requirement: REQ-0049-miniapp-product-card-component
related_bug:
lifecycle_stage: plan
---

# 现象

微信小程序商品列表页双列商品卡片高度偏低，商品主图区域使用填充裁切展示，导致用户无法在列表卡片中完整看到整张商品图片。用户补充期望优先完整显示整图，并提供参考截图：商品卡片应能露出完整方砖主体，允许图片区域通过留白或背景承接完整适配效果。

# 复现步骤

1. 打开微信小程序。
2. 进入商品列表页，例如全部商品、分类商品、品牌商品或从首页榜单进入的商品列表。
3. 查看双列商品卡片中的商品图片展示。
4. 对比附件参考图，观察商品图是否能完整显示整张图片，以及卡片高度是否足以承载完整图和商品名称。

# 期望 vs 实际

- 期望：商品列表双列卡片优先完整显示整张商品图，图片主体不被上下或左右裁切；卡片图片区高度应适当提高或使用更合适的比例，商品名称、品牌、规格和参考价格仍保持可读且不互相遮挡。商品列表、品牌商品列表等复用 `product-card` 的 `grid` 场景应保持一致。
- 实际：当前卡片高度偏低，`grid` 商品图片区比例较扁，图片使用填充裁切策略展示，部分商品图片在列表中无法完整露出。

# 影响范围

- 微信小程序商品列表页 `pages/product-list/index.*`。
- 微信小程序品牌详情商品 Tab 等复用 `components/product-card/` 且使用 `density="grid"` 的商品卡片场景。
- 商品卡片 `grid` / `compact` 密度下的图片比例、图片展示模式、占位背景和卡片整体高度。
- 小程序静态测试中与商品卡片比例、图片模式、双列布局稳定性相关的断言。

# 初步线索

- 只读探索已定位：`pages/product-list/index.wxml` 使用 `<product-card density="grid" />` 渲染商品列表双列卡片。
- `components/product-card/index.wxml` 中商品图片使用 `mode="aspectFill"`，该模式会为了铺满容器裁切图片。
- `components/product-card/index.wxss` 中 `grid` / `compact` 图片框使用 `aspect-ratio: 1 / 0.86`，在双列卡片中图片区偏矮。
- 历史 `REQ-0049-miniapp-product-card-component` 与 `REQ-0056-product-list-card-only-layout` 要求固定比例、防布局跳动和双列稳定，但未要求图片必须完整显示；本次用户反馈明确将“完整显示整图”作为优先级。

# 建议验收或复现要点

- [ ] 商品列表页双列商品卡片中的商品图优先完整显示整张图片，主体不被裁切。
- [ ] 商品卡片图片区高度或比例调整后，卡片整体高度更接近附件参考效果，不再显得过低。
- [ ] 图片完整适配时的留白或背景视觉可接受，不出现破图、拉伸变形或明显空白突兀。
- [ ] 品牌详情商品 Tab 等复用 `density="grid"` 的商品卡片场景同步验证。
- [ ] 320 / 375 / 430 pt 视口下双列卡片不横向溢出、不互相遮挡，名称、品牌、规格和价格仍可读。
- [ ] 商品列表、商品卡片和推荐位仍保持轻量图片字段策略，不因完整显示整图而改用原图导致加载性能回退。
- [ ] 更新小程序静态测试中卡片图片比例与展示模式相关断言。

# 附件

- 用户参考截图：`screenshots/reference-product-card-image-fit.png`
