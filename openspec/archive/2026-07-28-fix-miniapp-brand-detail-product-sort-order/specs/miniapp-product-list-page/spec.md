## MODIFIED Requirements

### Requirement: 商品列表公开数据接口

系统 SHALL 为小程序商品列表提供公开 SKU 查询能力，并过滤不可公开数据、内部字段和敏感信息。分类查询 SHALL 支持 `categoryLevel=primary|secondary` 以区分一级分类聚合和二级分类精确查询。品牌查询 SHALL 支持按 `brandId` 召回当前品牌公开 SKU，并在品牌过滤场景下默认按 SKU 发布时间 `published_at` 升序、ID 升序返回；历史数据 `published_at` 为空时 SHALL 使用 `created_at` 作为排序兜底。响应 MAY 保留 SKU 编码作为内部兼容字段，但公开商品列表 UI SHALL NOT 渲染该编码。

#### Scenario: 商品列表查询参数

- **WHEN** 小程序请求商品列表
- **THEN** 请求 SHALL 支持 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 中适用参数
- **AND** `categoryLevel` 有值时 SHALL 仅允许 `primary` 或 `secondary`
- **AND** 服务端 SHALL 校验参数合法性
- **AND** 非法参数 SHALL 返回统一错误或可恢复空状态所需信息。

#### Scenario: 品牌过滤查询默认排序

- **WHEN** 商品列表请求携带 `brandId={brandId}` 且未请求新品、热销、搜索相关性或价格排序
- **THEN** 服务端 SHALL 仅查询当前品牌下可公开 SKU
- **AND** 服务端 SHALL 继续过滤不可公开、停用、下架或删除的 SKU、品牌、分类和规格
- **AND** 服务端 SHALL 按发布时间升序返回 SKU
- **AND** 当多条 SKU 发布时间相同时，服务端 SHALL 按 SKU ID 升序返回
- **AND** 响应 SHALL 保持分页、是否有更多数据和可用筛选项语义
- **AND** 服务端 SHALL NOT 改变搜索页相关性排序、新品榜召回规则或热销榜热度优先排序。

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
