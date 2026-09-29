---
bug_id: BUG-0148-miniapp-product-list-card-image-fit
title: 小程序商品列表 grid 卡片图片无法完整显示
severity: medium
status: done
owner:
discovered_at: 2026-09-04 16:52:03
environment: miniapp
related_requirement: REQ-0049-miniapp-product-card-component
related_change: fix-miniapp-product-grid-image-fit
created_at: 2026-09-04 17:30:56
updated_at: 2026-09-07 22:58:19
---

# 现象

微信小程序中使用 `density="grid"` 的商品卡片高度偏低，商品主图区域采用填充裁切展示，导致列表卡片无法完整显示整张商品图片。用户反馈期望优先完整显示整图，并提供参考截图：双列商品卡片应能露出完整方砖主体，允许图片区域通过留白或背景承接完整适配效果。

# 复现步骤

1. 打开微信小程序。
2. 进入商品列表页，例如全部商品、分类商品、品牌商品或从首页榜单查看更多进入的商品列表。
3. 查看双列 `grid` 商品卡片中的商品图片。
4. 进入品牌详情页的商品 Tab，查看同样使用 `grid` 商品卡片的列表效果。
5. 对比附件参考图，观察商品图片主体是否完整露出，以及卡片高度是否足以承载完整图片与商品名称。

# 期望结果

- `grid` 商品卡片优先完整显示整张商品图，图片主体不被上下或左右裁切。
- `grid` 商品卡片图片区域高度或比例更适合完整露出方形瓷砖图，整体高度不再显得过低。
- 图片完整适配时，留白或背景承接自然，不出现破图、拉伸变形或突兀空白。
- 商品名称、品牌、规格和参考价格在 320 / 375 / 430 pt 视口下保持可读，不互相遮挡、不横向溢出。
- 商品列表、商品卡片和推荐位仍保持轻量图片字段策略，不因完整显示整图而改用原图导致加载性能回退。

# 实际结果

- `grid` 商品卡片图片框比例偏扁，卡片整体视觉高度偏低。
- 商品图片使用填充裁切策略展示，部分商品图在卡片中无法完整露出。
- 用户需要通过详情页或其他入口才能看到完整商品图，列表快速识别商品的效率下降。

# 影响范围

## In Scope

- 微信小程序商品列表页 `pages/product-list/index.*` 中的双列 `grid` 商品卡片。
- 微信小程序品牌详情页商品 Tab 等复用 `components/product-card/` 且传入 `density="grid"` 的商品卡片场景。
- 首页“全部产品”瀑布/双列区域中传入 `density="grid"` 的商品卡片。
- `components/product-card/` 的 `grid` 图片比例、图片展示模式、占位背景和卡片整体高度。
- 与 `grid` 商品卡片比例、图片模式、骨架屏稳定性相关的小程序静态测试。

## Out of Scope

- 首页“新品推荐”“热销推荐”等横向滑动 `density="compact"` 商品卡片。
- 搜索页 `density="list"` 商品卡片。
- 商品详情页轮播大图、推荐位图片、品牌图、证书图和 Banner 图。
- API 字段、数据库结构、对象存储 key、缩略图生成策略、原图/展示图/缩略图派生能力。

# 严重等级说明

严重等级建议为 `medium`。该问题不阻断商品列表加载、点击详情或基础浏览流程，但直接影响小程序商品列表的视觉识别效率和用户对瓷砖图片完整性的判断。由于商品图片是瓷砖选型的核心信息，本 BUG 应作为常规修复进入后续 Sprint，不建议作为紧急 hotfix，除非实际验收发现主图裁切导致关键商品信息大面积不可辨识。

# 关联与证据

- 关联需求：`REQ-0049-miniapp-product-card-component`
- 用户参考截图：`screenshots/reference-product-card-image-fit.png`
- 初步代码线索：`components/product-card/index.wxml` 当前图片使用填充展示；`components/product-card/index.wxss` 当前 `grid` 图片框比例偏扁；`pages/product-list/index.wxml` 与 `pages/brand-detail/index.wxml` 均复用 `density="grid"`。
openspec_changes:
  - change_id: fix-miniapp-product-grid-image-fit
    type: fix
    status: archived
