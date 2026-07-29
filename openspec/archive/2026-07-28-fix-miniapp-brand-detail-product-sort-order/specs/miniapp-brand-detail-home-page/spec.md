## MODIFIED Requirements

### Requirement: 品牌主页商品 Tab

商品 Tab SHALL 展示当前品牌下的公开 SKU 列表，并复用或对齐既有商品列表双列卡片、分页和状态机。商品 Tab SHALL 按 SKU 发布时间 `published_at` 升序、ID 升序展示当前品牌公开 SKU；历史数据 `published_at` 为空时，系统 SHALL 使用 SKU 创建时间 `created_at` 作为排序兜底。

#### Scenario: 当前品牌商品列表

- **WHEN** 用户查看品牌主页商品 Tab
- **THEN** 小程序 SHALL 仅展示当前品牌下可公开 SKU
- **AND** 商品卡片 SHALL 展示主图、商品名称、品牌或规格、参考价格和状态徽标
- **AND** 商品列表 SHALL 使用一行 2 个商品卡片布局
- **AND** 商品列表 SHALL 按发布时间升序展示
- **AND** 当多条 SKU 发布时间相同时，商品列表 SHALL 按 SKU ID 升序稳定展示。

#### Scenario: 商品 Tab 分页与跳转

- **WHEN** 用户刷新、上拉加载更多或点击商品卡片
- **THEN** 商品 Tab SHALL 支持首屏加载、下拉刷新、上拉加载更多、无更多和加载失败重试
- **AND** 加载更多追加后的整体列表 SHALL 继续保持发布时间升序、ID 升序，不得跨页重复、遗漏或顺序漂移
- **AND** 点击商品卡片 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 页面 SHOULD 携带 `brandId`、`sourcePage=brand_detail`、`sourceModule=brand_products`、`index` 和可用 `requestId`。

#### Scenario: 当前品牌无商品

- **WHEN** 当前品牌没有可公开 SKU
- **THEN** 商品 Tab SHALL 展示品牌上下文空态
- **AND** 页面 SHALL NOT 自动展示其他品牌商品。
