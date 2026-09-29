## 背景

`BUG-0148-miniapp-product-list-card-image-fit` 已评审通过并纳入 `sprint-029`。用户反馈微信小程序商品列表中 `density="grid"` 商品卡片高度偏低，商品图使用填充裁切后无法完整显示整张图片，影响瓷砖选型时对纹理、边缘和主体完整性的判断。

当前根因已确认：`src/miniapp/components/product-card/` 的商品图使用填充裁切模式，且 grid 图片框比例偏矮；商品列表页、品牌详情商品 Tab 和首页全部产品等场景复用同一 grid 商品卡片，因此同一展示偏差会跨入口出现。

## 变更内容

- 调整小程序 `components/product-card/` 中 `density="grid"` 商品卡片的图片展示契约，优先完整显示整张商品图。
- 提高 grid 商品卡片图片区比例或等价高度，使双列卡片能自然承载完整方砖主体和商品信息。
- 为完整适配时的留白、占位背景、加载失败态和骨架屏比例建立稳定约束，避免破图、拉伸、突兀空白或布局跳动。
- 覆盖复用 grid 商品卡片的商品列表页、品牌详情商品 Tab 和首页全部产品场景。
- 同步小程序静态测试，更新 grid 图片比例、图片展示模式和骨架屏稳定性断言。

## 不变范围

- 不调整首页“新品推荐”“热销推荐”等 `density="compact"` 商品卡片。
- 不调整搜索页 `density="list"` 商品卡片。
- 不调整商品详情页轮播、图片预览、品牌图、证书图、Banner 图。
- 不变更 API 字段、数据库结构、媒体对象 key、对象存储策略、缩略图生成或图片 URL 策略。
- 商品列表、商品卡片和推荐位继续使用缩略图或等价轻量图片字段，不因完整显示整图而回退原图。

## 能力

### 修改能力

- `miniapp-product-list-page`: 补充 grid 商品卡片图片完整适配、图片区比例和复用场景验收要求。

### 新增能力

- 无。

## 影响范围

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
  deployment: false
capabilities:
  new: []
  modified:
    - miniapp-product-list-page
source_bug: BUG-0148-miniapp-product-list-card-image-fit
sprint: sprint-029
product_data_collection_observability:
  status: n/a
  affected_layers: []
  reason: 本变更仅调整小程序 grid 商品卡片的端侧展示样式和静态测试，不涉及 API、DB、请求封装、日志审计、行为埋点、Task Trace、对象存储或媒体 URL 策略。
  validation: 实现阶段通过静态测试和小程序渲染证据验证；无需运行 Orval、数据库迁移或产品数据采集门禁。
```

## 回滚方案

- 若完整适配导致 grid 双列卡片出现明显留白、文本遮挡、首屏浏览效率下降或性能回退，可回滚 `components/product-card/` 的 grid 图片比例和展示模式至变更前实现。
- 回滚时必须同步恢复 `tests/test_miniapp_static.py` 中对应静态断言，并在 BUG 验收记录中说明回滚原因、影响页面和后续替代方案。
- 回滚不得修改 API、DB、对象存储或媒体 URL 策略。
