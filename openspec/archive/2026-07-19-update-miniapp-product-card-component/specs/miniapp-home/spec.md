## MODIFIED Requirements

### Requirement: 新品热销与全部产品承接
小程序首页 SHALL 在 Banner 与快捷入口后展示新品推荐、热销推荐和全部产品瀑布流，使用户可以连续浏览公开 SKU；首页商品卡片 SHALL 复用统一商品卡片核心结构，并根据模块传入展示密度、来源上下文和位置序号。

#### Scenario: 新品推荐商品卡片
- **WHEN** 首页展示新品推荐
- **THEN** 小程序 SHALL 使用横向滚动商品卡片展示 SKU 主图、SKU 编号或商品名称、规格和 `price_display`
- **AND** 商品图片区域 SHALL NOT 展示“新品”角标或标签
- **AND** 用户点击商品卡片 SHALL 进入商品详情页
- **AND** 点击 SHALL 携带 `skuId`、`sourcePage=home`、`sourceModule=new_products`、`index` 和可用 `requestId`。

#### Scenario: 热销推荐商品卡片
- **WHEN** 首页展示热销推荐
- **THEN** 小程序 SHALL 使用双列大卡片展示 SKU 主图、系列或商品名、空间或工艺标签和 `price_display`
- **AND** 用户点击卡片 SHALL 进入商品详情页
- **AND** 点击 SHALL 携带 `skuId`、`sourcePage=home`、`sourceModule=hot_products`、`index` 和可用 `requestId`
- **AND** 卡片内 SHALL NOT 展示收藏心形、分享、购物车、联系客服或询价快捷操作。

#### Scenario: 全部产品瀑布流展示
- **WHEN** 首页展示全部产品瀑布流
- **THEN** 小程序 SHALL 复用统一商品卡片核心结构展示公开 SKU
- **AND** 卡片 SHALL 支持图片失败、字段缺失、不可查看和防重复点击兜底
- **AND** 首页容器 SHALL 负责瀑布流、分页、加载态和空状态。
