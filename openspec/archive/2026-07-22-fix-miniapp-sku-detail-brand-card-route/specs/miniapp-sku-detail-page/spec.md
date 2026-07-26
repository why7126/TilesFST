## MODIFIED Requirements

### Requirement: 品牌入口与相关推荐

SKU 详情页 SHALL 支持进入品牌主页、同系列商品和同品牌推荐，使用户可以继续浏览相关瓷砖；SKU 详情页品牌卡 SHALL 使用微信小程序品牌卡片组件承载单品牌展示、Logo fallback、入口提示和点击跳转。SKU 详情接口返回的品牌入口路径 SHALL 指向对应品牌详情页，品牌卡片不得在存在有效品牌详情页入口时误跳搜索页。

#### Scenario: 品牌入口

- **WHEN** 用户点击内容区品牌卡或“查看品牌主页”入口
- **THEN** 小程序 SHALL 使用 `brandId` 进入对应品牌主页或可用品牌承接页
- **AND** 可访问品牌的入口路径 SHALL 指向 `/pages/brand-detail/index?brandId=<brand_id>`
- **AND** 目标不可用时 SHALL 安全降级到可返回提示或搜索筛选结果
- **AND** 底部固定操作栏 SHALL NOT 显示品牌按钮或保留品牌按钮点击热区。

#### Scenario: SKU 详情接口返回品牌详情页入口

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且当前 SKU 关联启用品牌
- **THEN** 后端 SHALL 在 `data.brand.brand_entry_path` 返回 `/pages/brand-detail/index?brandId=<brand_id>`
- **AND** `brand_id` SHALL 与当前 SKU 关联品牌一致
- **AND** 响应 SHALL NOT 将可访问品牌入口返回为 `/pages/search/index` 或搜索结果页路径。

#### Scenario: SKU 详情页使用品牌卡片组件

- **WHEN** SKU 详情页展示品牌卡
- **THEN** 页面 SHALL 使用微信小程序品牌卡片组件替换重复的内联品牌卡片结构
- **AND** 页面 SHALL 从 SKU 详情数据中提取品牌展示对象、`skuId` 和来源上下文传入组件
- **AND** 组件 SHALL 负责 Logo 缺失/失败、长品牌名、入口不可用和点击防重复等卡片级行为。

#### Scenario: 品牌入口 fallback

- **WHEN** SKU 详情页品牌卡缺少 `brand_entry_path` 但品牌名称可用
- **THEN** 小程序 SHALL fallback 到品牌关键词搜索页或等价品牌承接页
- **AND** 小程序 SHALL 对品牌名称进行 URL 编码
- **AND** 品牌名称不可用或入口不可用时 SHALL 提示“品牌内容暂不可查看”或等价文案并阻止无效跳转。
