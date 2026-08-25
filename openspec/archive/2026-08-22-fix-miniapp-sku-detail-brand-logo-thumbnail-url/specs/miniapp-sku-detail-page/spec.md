## MODIFIED Requirements

### Requirement: 品牌入口与相关推荐

SKU 详情页 SHALL 支持进入品牌主页、同系列商品和同品牌推荐，使用户可以继续浏览相关瓷砖；SKU 详情页品牌卡 SHALL 使用微信小程序品牌卡片组件承载单品牌展示、Logo fallback、入口提示和点击跳转。SKU 详情接口返回的品牌入口路径 SHALL 指向对应品牌详情页，品牌卡片不得在存在有效品牌详情页入口时误跳搜索页。SKU 详情接口返回的品牌对象 SHALL 包含 `brand_logo_thumbnail_url` 或等价轻量 Logo URL，使商品详情页品牌卡普通展示可以优先使用缩略图。

#### Scenario: SKU 详情接口返回品牌详情页入口

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且当前 SKU 关联启用品牌
- **THEN** 后端 SHALL 在 `data.brand.brand_entry_path` 返回 `/pages/brand-detail/index?brandId=<brand_id>`
- **AND** `brand_id` SHALL 与当前 SKU 关联品牌一致
- **AND** 响应 SHALL NOT 将可访问品牌入口返回为 `/pages/search/index` 或搜索结果页路径
- **AND** 后端 SHALL 在 `data.brand.brand_logo_thumbnail_url` 返回品牌 Logo 缩略图或等价轻量 URL，缺少可用缩略图时 SHALL 返回空值而不是伪造不可读 URL。

#### Scenario: SKU 详情页使用品牌卡片组件

- **WHEN** SKU 详情页展示品牌卡
- **THEN** 页面 SHALL 使用微信小程序品牌卡片组件替换重复的内联品牌卡片结构
- **AND** 页面 SHALL 从 SKU 详情数据中提取品牌展示对象、`skuId` 和来源上下文传入组件
- **AND** 页面 SHALL 保留并传递 `brand_logo_thumbnail_url`
- **AND** 组件 SHALL 负责 Logo 缺失/失败、长品牌名、入口不可用和点击防重复等卡片级行为。

#### Scenario: SKU 详情页品牌卡 Logo 缩略图优先

- **WHEN** SKU 详情页品牌对象同时包含 `brand_logo_thumbnail_url` 与 `brand_logo_url`
- **THEN** 品牌卡普通展示 SHALL 优先请求 `brand_logo_thumbnail_url`
- **AND** `brand_logo_url` SHALL 仅作为兼容字段或高清语义引用，不得作为缩略图可用时的首选展示资源
- **AND** 验收 SHALL 记录小程序 DevTools、真机或体验版 Network evidence，覆盖品牌 Logo URL 类型、HTTP 状态、资源大小、耗时和渲染结果。
