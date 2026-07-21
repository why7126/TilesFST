## MODIFIED Requirements

### Requirement: 微信小程序商品列表页入口
系统 SHALL 提供微信小程序商品列表页，用于承接分类、搜索、品牌和首页推荐等入口的公开 SKU 浏览。分类入口 SHALL 显式支持一级分类聚合查询和二级分类精确查询。

#### Scenario: 一级分类入口进入商品列表
- **WHEN** 用户从分类页一级分类商品入口进入商品列表
- **THEN** 小程序 SHALL 打开 `pages/product-list/index?categoryId={primaryCategoryId}&categoryName={encodedName}&categoryLevel=primary&sourcePage=category` 或等价商品列表页
- **AND** 页面 SHALL 展示一级分类名称作为标题或主要上下文说明
- **AND** 页面 SHALL 请求并展示该一级分类下所有启用二级分类的公开 SKU 聚合结果
- **AND** 页面 SHALL NOT 错误地只展示直接挂载在一级分类下的 SKU。

#### Scenario: 二级分类入口进入商品列表
- **WHEN** 用户从分类页二级分类卡片进入商品列表
- **THEN** 小程序 SHALL 打开 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}&categoryLevel=secondary&sourcePage=category` 或等价商品列表页
- **AND** 页面 SHALL 展示二级分类名称作为标题或主要上下文说明
- **AND** 页面 SHALL 请求并展示当前二级分类下可公开 SKU。

#### Scenario: 搜索入口进入商品列表
- **WHEN** 用户从搜索结果 SKU Tab 或搜索结果入口进入商品列表
- **THEN** 页面 SHALL 保留当前关键词
- **AND** 筛选、排序和分页请求 SHALL 继续携带该关键词
- **AND** 页面 SHALL NOT 丢失搜索上下文。

#### Scenario: 品牌和推荐入口进入商品列表
- **WHEN** 用户从品牌相关页面、首页推荐、新品榜或热销榜进入商品列表
- **THEN** 页面 SHALL 使用 `brandId`、`source` 或等价上下文加载公开 SKU
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

### Requirement: 筛选与排序
商品列表页 SHALL 支持基础筛选和排序，使用户可以在当前上下文内缩小或调整 SKU 列表。分类入口上下文中的筛选项 SHALL 限制在当前分类层级结果相关范围内。

#### Scenario: 打开筛选
- **WHEN** 用户点击筛选入口
- **THEN** 页面 SHALL 打开底部筛选抽屉或等价小程序筛选面板
- **AND** 筛选面板 SHALL 支持品牌、分类、规格和价格区间中可用项
- **AND** 若当前为一级分类上下文，可用筛选项 SHALL 限制在该一级分类聚合结果相关范围内
- **AND** 若当前为二级分类上下文，可用筛选项 SHALL 限制在该二级分类结果相关范围内。

#### Scenario: 应用筛选
- **WHEN** 用户确认筛选
- **THEN** 页面 SHALL 更新筛选快照
- **AND** 页面 SHALL 重置分页并重新请求第一页
- **AND** 已选筛选项 SHALL 在列表顶部以紧凑标签展示
- **AND** 若当前为分类入口上下文，请求 SHALL 继续携带 `categoryId` 与 `categoryLevel`。

#### Scenario: 移除筛选
- **WHEN** 用户移除单个已选筛选项或点击重置
- **THEN** 页面 SHALL 更新筛选快照
- **AND** 页面 SHALL 重置分页并重新请求第一页
- **AND** 若当前为分类入口上下文，请求 SHALL 继续携带 `categoryId` 与 `categoryLevel`。

#### Scenario: 切换排序
- **WHEN** 用户选择默认、最新、价格升序或价格降序排序
- **THEN** 页面 SHALL 更新排序参数
- **AND** 页面 SHALL 回到列表顶部
- **AND** 页面 SHALL 重置分页并重新请求第一页
- **AND** 若当前为分类入口上下文，请求 SHALL 继续携带 `categoryId` 与 `categoryLevel`。

#### Scenario: 不支持复杂排序
- **WHEN** 团队验收 v1 商品列表
- **THEN** 页面 SHALL NOT 提供个性化推荐排序、人工置顶配置或复杂多字段排序编辑。

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
商品列表页 SHALL 根据上下文展示可恢复的空状态和异常状态。

#### Scenario: 一级分类无启用二级分类
- **WHEN** 一级分类上下文下没有启用二级分类
- **THEN** 页面 SHALL 展示“该分类暂未上架商品”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他分类。

#### Scenario: 一级分类聚合无商品
- **WHEN** 一级分类上下文下所有启用二级分类均没有可公开 SKU
- **THEN** 页面 SHALL 展示“该分类暂未上架商品”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他分类。

#### Scenario: 二级分类无商品
- **WHEN** 二级分类上下文下没有可公开 SKU
- **THEN** 页面 SHALL 展示“该分类暂未上架商品”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他分类。

#### Scenario: 搜索无结果
- **WHEN** 搜索上下文下没有匹配 SKU
- **THEN** 页面 SHALL 展示当前关键词
- **AND** 页面 SHALL 提示用户缩短关键词、替换品牌/规格或清空筛选。

#### Scenario: 筛选无匹配
- **WHEN** 当前筛选条件下没有匹配 SKU
- **THEN** 页面 SHALL 展示清空筛选入口
- **AND** 页面 SHALL 保留当前上下文。

#### Scenario: 分类或品牌不可用
- **WHEN** 入口携带的分类或品牌已下架、停用或不存在
- **THEN** 页面 SHALL 展示可恢复空状态或返回提示
- **AND** 页面 SHALL NOT 白屏、路由报错或展示内部错误。
