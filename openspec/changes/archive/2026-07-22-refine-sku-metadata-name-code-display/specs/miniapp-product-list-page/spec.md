## MODIFIED Requirements

### Requirement: 商品卡片

商品列表页 SHALL 使用统一商品卡片展示用户选砖所需的公开 SKU 信息，并支持进入 SKU 详情页。商品列表页双列卡片 SHALL 参照首页热销推荐展示主图、商品名称、品牌或规格信息、参考价格和状态徽标；SKU 编码 SHALL NOT 在小程序/店主端商品卡片中展示。

#### Scenario: 商品卡片字段

- **WHEN** 商品列表接口返回 SKU 数据
- **THEN** 商品卡片 SHALL 展示主图、商品名称、品牌或规格信息、参考价格和状态徽标
- **AND** 商品卡片 SHALL NOT 展示 SKU 编码、`sku_code` 字段名、内部编号或等价内部识别字段
- **AND** 辅助信息 SHALL NOT 挤压商品名称、主图、品牌或规格信息、参考价格和状态徽标。

#### Scenario: 图片稳定展示

- **WHEN** 商品主图加载中或加载完成
- **THEN** 商品图片区域 SHALL 使用稳定比例
- **AND** 加载前后 SHALL NOT 导致列表明显跳动。

#### Scenario: 图片加载失败

- **WHEN** 商品主图加载失败
- **THEN** 商品卡片 SHALL 展示统一占位图或占位背景
- **AND** 页面 SHALL NOT 展示破图图标
- **AND** 其他商品信息 SHALL 保持可浏览。

#### Scenario: 商品卡片进入详情

- **WHEN** 用户点击商品卡片任意主要区域
- **THEN** 小程序 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 目标不可达时 SHALL 展示可恢复提示
- **AND** 页面 SHALL 保留返回能力。

#### Scenario: 卡片不提供交易操作

- **WHEN** 团队验收商品列表卡片
- **THEN** 商品卡片 SHALL NOT 展示收藏、加入询价、购物车、立即购买、在线下单或联系商家快捷按钮。

### Requirement: 商品列表公开数据接口

系统 SHALL 为小程序商品列表提供公开 SKU 查询能力，并过滤不可公开数据、内部字段和敏感信息。分类查询 SHALL 支持 `categoryLevel=primary|secondary` 以区分一级分类聚合和二级分类精确查询。响应 MAY 保留 SKU 编码作为内部兼容字段，但公开商品列表 UI SHALL NOT 渲染该编码。

#### Scenario: 商品列表查询参数

- **WHEN** 小程序请求商品列表
- **THEN** 请求 SHALL 支持 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 中适用参数
- **AND** `categoryLevel` 有值时 SHALL 仅允许 `primary` 或 `secondary`
- **AND** 服务端 SHALL 校验参数合法性
- **AND** 非法参数 SHALL 返回统一错误或可恢复空状态所需信息。

#### Scenario: 一级分类聚合查询

- **WHEN** 商品列表请求携带 `categoryId={primaryCategoryId}` 且 `categoryLevel=primary`
- **THEN** 服务端 SHALL 查询该一级分类下所有启用二级分类关联的可公开 SKU
- **AND** 服务端 SHALL 继续过滤不可公开、停用、下架或删除的 SKU、品牌、分类和规格
- **AND** 服务端 SHALL NOT 只返回直接挂载在一级分类下的 SKU
- **AND** 响应 SHALL 保持分页、是否有更多数据和可用筛选项语义。

#### Scenario: 二级分类精确查询

- **WHEN** 商品列表请求携带 `categoryId={secondaryCategoryId}` 且 `categoryLevel=secondary`
- **THEN** 服务端 SHALL 仅查询该二级分类关联的可公开 SKU
- **AND** 服务端 SHALL 继续过滤不可公开、停用、下架或删除的 SKU、品牌、分类和规格
- **AND** 响应 SHALL 保持分页、是否有更多数据和可用筛选项语义。

#### Scenario: 商品列表响应字段

- **WHEN** 商品列表请求成功
- **THEN** 响应 SHALL 返回商品列表、分页信息、是否有更多数据和可用筛选项
- **AND** 每个商品 SHALL 至少包含公开 `skuId`、商品名称、品牌、规格、参考价格和安全主图 URL
- **AND** 响应 MAY 包含 `sku_code` 作为兼容字段，但公开端 UI SHALL NOT 展示该字段。

#### Scenario: 公开字段过滤

- **WHEN** 服务端返回商品列表数据
- **THEN** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置。

#### Scenario: 不可公开 SKU 过滤

- **WHEN** SKU、品牌、分类或规格处于不可公开、停用、下架或删除状态
- **THEN** 商品列表 SHALL 过滤相关 SKU
- **AND** 页面 SHALL NOT 展示不可公开商品。
