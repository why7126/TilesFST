# miniapp-product-list-page Specification

## Purpose
TBD - created by archiving change add-miniapp-product-list-component. Update Purpose after archive.
## Requirements
### Requirement: 微信小程序商品列表页入口
系统 SHALL 提供微信小程序商品列表页，用于承接分类、搜索、品牌和首页推荐等入口的公开 SKU 浏览。分类入口 SHALL 显式支持一级分类聚合查询和二级分类精确查询。商品列表页 SHALL 保留入口上下文用于初始查询、标题和空状态展示，但 SHALL NOT 在页面内提供二次搜索、筛选或排序控件。

#### Scenario: 一级分类入口进入商品列表
- **WHEN** 用户从分类页一级分类商品入口进入商品列表
- **THEN** 小程序 SHALL 打开 `pages/product-list/index?categoryId={primaryCategoryId}&categoryName={encodedName}&categoryLevel=primary&sourcePage=category` 或等价商品列表页
- **AND** 页面 SHALL 展示一级分类名称作为标题或主要上下文说明
- **AND** 页面 SHALL 请求并展示该一级分类自身直接挂载的公开 SKU，以及该一级分类下所有启用二级分类的公开 SKU 聚合结果
- **AND** 页面 SHALL NOT 错误地遗漏直接挂载在一级分类下的 SKU。

#### Scenario: 二级分类入口进入商品列表
- **WHEN** 用户从分类页二级分类卡片进入商品列表
- **THEN** 小程序 SHALL 打开 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}&categoryLevel=secondary&sourcePage=category` 或等价商品列表页
- **AND** 页面 SHALL 展示二级分类名称作为标题或主要上下文说明
- **AND** 页面 SHALL 请求并展示当前二级分类下可公开 SKU。

#### Scenario: 搜索入口进入商品列表
- **WHEN** 用户从搜索结果 SKU Tab 或搜索结果入口进入商品列表
- **THEN** 页面 SHALL 保留当前关键词用于初始结果查询、标题或空状态文案
- **AND** 分页请求 SHALL 继续携带该关键词
- **AND** 页面 SHALL NOT 丢失搜索上下文
- **AND** 页面 SHALL NOT 展示商品列表页内二次搜索、筛选或排序控件。

#### Scenario: 品牌和推荐入口进入商品列表
- **WHEN** 用户从品牌相关页面、首页推荐、新品榜或热销榜进入商品列表
- **THEN** 页面 SHALL 使用 `brandId`、`source`、`section` 或等价上下文加载公开 SKU
- **AND** 目标入口不可用时 SHALL 安全降级到可返回提示或已有可用页面。

### Requirement: 商品列表容器与状态机
商品列表页 SHALL 提供可复用列表容器，统一处理查询上下文、分页、刷新、加载更多、无更多、空状态和错误状态。

#### Scenario: 首屏加载
- **WHEN** 商品列表页首次进入
- **THEN** 页面 SHALL 请求第一页商品数据
- **AND** 首屏 SHALL 展示与最终商品卡片比例一致的骨架屏或等价加载状态
- **AND** 页面 SHALL NOT 白屏或展示破碎布局。

#### Scenario: 下拉刷新
- **WHEN** 用户触发下拉刷新
- **THEN** 页面 SHALL 清空旧分页游标
- **AND** 页面 SHALL 重新请求第一页
- **AND** 刷新成功后 SHALL 使用新结果替换旧列表
- **AND** 若当前为分类入口上下文，请求 SHALL 继续携带 `categoryId` 与 `categoryLevel`。

#### Scenario: 上拉加载更多
- **WHEN** 用户滚动接近列表底部且仍有更多数据
- **THEN** 页面 SHALL 请求下一页
- **AND** 请求期间 SHALL 防止重复并发请求
- **AND** 新结果 SHALL 追加到已有列表并按 SKU ID 或等价 ID 去重
- **AND** 若当前为分类入口上下文，请求 SHALL 继续携带 `categoryId` 与 `categoryLevel`。

#### Scenario: 无更多数据
- **WHEN** 接口返回无更多数据或前端确认没有更多数据
- **THEN** 页面 SHALL 展示统一无更多状态
- **AND** 页面 SHALL 停止继续请求下一页。

#### Scenario: 加载失败
- **WHEN** 首屏或加载更多请求失败
- **THEN** 页面 SHALL 展示可理解错误状态和重试入口
- **AND** 加载更多失败 SHALL 保留已加载商品
- **AND** 页面 SHALL NOT 清空已有可浏览内容。

### Requirement: 商品卡片
商品列表页 SHALL 使用统一商品卡片展示用户选砖所需的公开 SKU 信息，并支持进入 SKU 详情页。商品列表页双列卡片 SHALL 参照首页热销推荐展示主图、商品名称、品牌或规格信息、参考价格和状态徽标；SKU 编码 MAY 在空间允许时展示，但不得挤压主图、名称、品牌/规格和价格。

#### Scenario: 商品卡片字段
- **WHEN** 商品列表接口返回 SKU 数据
- **THEN** 商品卡片 SHALL 展示主图、商品名称、品牌或规格信息、参考价格和状态徽标
- **AND** 商品卡片 MAY 展示 SKU 编码、分类名称或适用空间等辅助信息
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
系统 SHALL 为小程序商品列表提供公开 SKU 查询能力，并过滤不可公开数据、内部字段和敏感信息。分类查询 SHALL 支持 `categoryLevel=primary|secondary` 以区分一级分类聚合和二级分类精确查询。

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
- **AND** 每个商品 SHALL 至少包含公开 `skuId`、商品名称、SKU 编码、品牌、规格、参考价格和安全主图 URL。

#### Scenario: 公开字段过滤
- **WHEN** 服务端返回商品列表数据
- **THEN** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置。

#### Scenario: 不可公开 SKU 过滤
- **WHEN** SKU、品牌、分类或规格处于不可公开、停用、下架或删除状态
- **THEN** 商品列表 SHALL 过滤相关 SKU
- **AND** 页面 SHALL NOT 展示不可公开商品。

### Requirement: 商品列表空状态与异常状态
商品列表页 SHALL 根据上下文展示可恢复的空状态和异常状态。商品列表页不提供筛选控件，因此空状态 SHALL NOT 依赖清空筛选入口恢复。

#### Scenario: 一级分类无可公开商品
- **WHEN** 一级分类自身及其所有启用二级分类均没有可公开 SKU
- **THEN** 页面 SHALL 展示“该分类暂未上架商品”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他分类。

#### Scenario: 二级分类无商品
- **WHEN** 二级分类上下文下没有可公开 SKU
- **THEN** 页面 SHALL 展示“该分类暂未上架商品”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他分类。

#### Scenario: 搜索无结果
- **WHEN** 搜索上下文下没有匹配 SKU
- **THEN** 页面 SHALL 展示当前关键词
- **AND** 页面 SHALL 提示用户可返回搜索页调整关键词或搜索条件。

#### Scenario: 商品列表无匹配
- **WHEN** 当前入口上下文下没有可公开 SKU
- **THEN** 页面 SHALL 展示与分类、品牌、推荐或关键词上下文匹配的空状态
- **AND** 页面 SHALL NOT 展示清空筛选入口。

#### Scenario: 分类或品牌不可用
- **WHEN** 入口携带的分类或品牌已下架、停用或不存在
- **THEN** 页面 SHALL 展示可恢复空状态或返回提示
- **AND** 页面 SHALL NOT 白屏、路由报错或展示内部错误。

### Requirement: 商品列表视觉与移动可用性
商品列表页 SHALL 延续微信小程序深色企业轻奢风，并在主流小程序视口保持可用。商品列表页 SHALL 使用一行 2 个的双列商品卡片布局，首屏主要空间 SHALL 用于商品浏览。

#### Scenario: 深色视觉
- **WHEN** 用户查看商品列表页
- **THEN** 页面 SHALL 使用与小程序首页一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 页面 SHALL NOT 使用电商红主按钮、纯白大背景或购物导向视觉。

#### Scenario: 双列触控与视口
- **WHEN** 团队在 320、375 和 430px 逻辑宽度及常见底部安全区验收商品列表页
- **THEN** 页面 SHALL 每行展示 2 个商品卡片
- **AND** 页面 SHALL 无横向滚动、内容重叠、卡片互相遮挡、关键文字截断、底部 TabBar 遮挡或底部露白
- **AND** 商品卡片主要点击目标 SHALL 不小于 44x44px 或小程序等效尺寸。

#### Scenario: 原型验收
- **WHEN** 团队验收商品列表页视觉和交互
- **THEN** 验收 SHALL 优先参考 `issues/requirements/archive/REQ-0056-product-list-card-only-layout/prototype/miniapp/prototype.html`
- **AND** `issues/requirements/archive/REQ-0056-product-list-card-only-layout/prototype/miniapp/context.md` SHALL 作为交互补充说明
- **AND** 后续实现验收 SHALL 补充 320、375 和 430px 视口 evidence。

### Requirement: 商品列表页轻量双列浏览
商品列表页 SHALL 作为轻量商品浏览页，直接展示当前入口上下文下的公开 SKU，并避免搜索、筛选和排序控件占用首屏浏览空间。

#### Scenario: 商品列表页不展示搜索筛选排序控件
- **WHEN** 用户打开 `pages/product-list/index` 商品列表页
- **THEN** 页面 SHALL NOT 展示搜索框、搜索按钮、跳转搜索页的搜索入口、筛选按钮、筛选 chips、筛选抽屉入口或排序 tabs
- **AND** 页面 SHALL 保留标题、入口上下文、状态反馈、商品卡片列表和必要的加载/错误/空态操作。

#### Scenario: 商品列表页展示双列卡片
- **WHEN** 商品列表页存在可浏览 SKU
- **THEN** 页面 SHALL 使用一行 2 个商品卡片的双列布局展示商品
- **AND** 商品卡片 SHALL 使用与首页热销推荐一致的信息结构和视觉密度
- **AND** 单数商品数量时最后一张卡片 SHALL 保持左侧自然排列且不得拉伸为整行。

#### Scenario: 搜索页能力不受影响
- **WHEN** 团队验收 REQ-0056 商品列表页收敛
- **THEN** 微信小程序搜索页 SHALL 继续保留自身搜索、筛选、结果展示和相关埋点能力
- **AND** 商品列表页的控件移除 SHALL NOT 删除或破坏搜索页代码路径。

