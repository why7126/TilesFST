## MODIFIED Requirements

### Requirement: 商品卡片

商品列表页 SHALL 使用统一商品卡片展示公开 SKU，并 SHALL 为商品主图、名称、品牌/规格、价格、状态标识、召回置顶标识、图片加载性能和失败降级提供稳定体验。公开 SKU 有真实主图时，列表接口返回给商品卡片的 `cover_image` SHALL 是可通过后端 `/media/{object_key}` 或等价受控链路读取的图片 URL。列表缩略图或等价轻量优化图片 SHALL 是真实轻量资源；系统 SHALL NOT 仅以 `.thumb` 对象存在但内容等同原图的资源作为图片加载性能优化完成标准。

#### Scenario: 实际生效置顶商品展示标识
- **WHEN** 小程序普通商品列表展示公开 SKU
- **AND** 后端响应标记该 SKU 为当前列表中实际生效的召回置顶商品
- **THEN** 商品卡片 SHALL 展示固定文案“置顶”
- **AND** “置顶”标识 SHALL 使用商品卡片轻量角标或等价轻量位置
- **AND** 标识 SHALL NOT 遮挡商品主图核心内容、商品名称、品牌、规格或参考价格
- **AND** 标识展示 SHALL NOT 改变整卡点击、曝光埋点、点击埋点、图片失败兜底、下拉刷新或加载更多行为。

#### Scenario: 非置顶商品不展示置顶标识
- **WHEN** 小程序普通商品列表展示公开 SKU
- **AND** 后端响应未标记该 SKU 为当前列表中实际生效的召回置顶商品
- **THEN** 商品卡片 SHALL NOT 展示“置顶”标识
- **AND** 小程序 SHALL NOT 根据列表位置、排序值或本地猜测自行展示“置顶”标识。

#### Scenario: 置顶标识优先级
- **WHEN** 普通商品列表中的同一 SKU 同时具备置顶展示状态和新品或热销展示状态
- **THEN** 商品卡片 SHALL 优先展示“置顶”标识
- **AND** 本 Change SHALL NOT 要求同一卡片同时展示多个角标。

### Requirement: 商品列表公开数据接口

系统 SHALL 为小程序商品列表提供公开 SKU 查询能力，并过滤不可公开数据、内部字段和敏感信息。分类查询 SHALL 支持 `categoryLevel=primary|secondary` 以区分一级分类聚合和二级分类精确查询。品牌查询、分类查询和普通搜索查询在未显式请求新品、热销、价格排序或搜索相关性排序时，SHALL 使用与品牌详情页商品 Tab 一致的默认排序：按 SKU 发布时间 `published_at` 升序、SKU ID 升序返回；历史数据 `published_at` 为空时 SHALL 使用 SKU 创建时间 `created_at` 作为排序兜底。响应 MAY 保留 SKU 编码作为内部兼容字段，但公开商品列表 UI SHALL NOT 渲染该编码。响应 SHALL 使用布尔字段表达商品是否为当前列表中实际生效的召回置顶展示商品。

#### Scenario: 商品列表响应字段

- **WHEN** 商品列表请求成功
- **THEN** 响应 SHALL 返回商品列表、分页信息、是否有更多数据和可用筛选项
- **AND** 每个商品 SHALL 至少包含公开 `skuId`、商品名称、品牌、规格、参考价格和安全主图 URL
- **AND** 每个商品 SHALL 包含等价于 `is_recall_pinned` 的布尔字段，用于表达该商品是否为当前列表中实际生效的召回置顶展示商品
- **AND** 该字段 SHALL 基于后端排序层的置顶生效判断生成，不得要求小程序端根据排序位置推断
- **AND** 响应 MAY 包含 `sku_code` 作为兼容字段，但公开端 UI SHALL NOT 展示该字段。

#### Scenario: 新品榜和热销榜不触发置顶标识
- **WHEN** 商品列表请求为新品商品列表或热销商品列表
- **THEN** 系统 SHALL NOT 应用召回置顶逻辑
- **AND** 商品响应中的置顶展示字段 SHALL 为 false 或不触发小程序展示“置顶”标识
- **AND** 新品榜和热销榜原有排序语义 SHALL NOT 因置顶标识能力改变。

#### Scenario: 缺省字段兼容
- **WHEN** 小程序商品卡片接收到旧接口数据或缺少置顶展示字段的数据
- **THEN** 小程序 SHALL 默认按非置顶商品处理
- **AND** 小程序 SHALL NOT 展示“置顶”标识。
