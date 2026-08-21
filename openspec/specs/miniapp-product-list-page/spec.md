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

商品列表页 SHALL 使用统一商品卡片展示公开 SKU，并 SHALL 为商品主图、名称、品牌/规格、价格、状态标识、图片加载性能和失败降级提供稳定体验。公开 SKU 有真实主图时，列表接口返回给商品卡片的 `cover_image` SHALL 是可通过后端 `/media/{object_key}` 或等价受控链路读取的图片 URL。列表缩略图或等价轻量优化图片 SHALL 是真实轻量资源；系统 SHALL NOT 仅以 `.thumb` 对象存在但内容等同原图的资源作为图片加载性能优化完成标准。从品牌列表页进入的品牌分类商品列表页、首页推荐、搜索结果、收藏列表和普通商品列表 SHALL 继续复用商品卡片缩略图优先策略。

#### Scenario: 商品列表保持缩略图优先

- **WHEN** 用户从品牌列表页、首页推荐、搜索结果、收藏列表或普通商品列表查看商品卡片
- **THEN** 商品卡片 SHALL 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 商品卡片 SHALL NOT 因 SKU 详情页改用高清展示图而直接回退原图字段
- **AND** 非首屏商品卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 商品详情、图片预览或分享场景 SHALL 保留原图或安全高清 URL。

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

### Requirement: 商品列表页微信分享
商品列表页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前搜索、分类、品牌和榜单上下文。

#### Scenario: 商品列表分享给微信朋友
- **WHEN** 用户在商品列表页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享标题 SHALL 反映当前搜索、分类、品牌、榜单或全部商品语义
- **AND** 分享路径 SHALL 指向商品列表页并保留可恢复当前列表的白名单 query 参数
- **AND** 白名单参数 SHOULD 包含 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section` 和 `sourcePage` 中适用字段。

#### Scenario: 商品列表分享到朋友圈
- **WHEN** 用户在商品列表页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 点击朋友圈入口后 SHALL 进入商品列表页
- **AND** 页面标题、筛选结果、空状态和错误态 SHALL 与分享参数语义一致
- **AND** 缺失可选参数时 SHALL 降级为可浏览列表或明确错误态，不得白屏。

#### Scenario: 商品列表分享参数编码
- **WHEN** 商品列表分享路径包含中文分类名、品牌名或搜索词
- **THEN** 小程序 SHALL 对 query 参数进行安全编码
- **AND** 被分享用户打开页面后 SHALL 正确解码并恢复列表语义
- **AND** 分享路径 SHALL NOT 包含 raw payload、Authorization header、Cookie、手机号、raw object key 或未授权素材路径。

#### Scenario: 商品列表分享埋点非阻断
- **WHEN** 商品列表页记录分享行为
- **THEN** 事件 SHOULD 包含页面路径、分享渠道、分类、品牌、关键词、榜单和结果上下文中的可用字段
- **AND** 埋点失败 SHALL NOT 阻断分享
- **AND** 分享行为 SHALL NOT 影响下拉刷新、加载更多、商品卡片点击或错误重试。

### Requirement: 商品列表召回置顶排序

小程序普通商品列表公开查询 MUST 支持少量召回 SKU 置顶排序。普通商品列表包括分类商品、品牌商品、普通关键词商品和非榜单推荐入口；首页无筛选全部产品瀑布流 MUST 保持既有首页排序，不应用本能力。后端 MUST 先应用公开条件和当前请求筛选，再计算召回置顶资格，并在分页前对完整结果集排序。每次请求默认最多 4 个生效召回 SKU 进入置顶区；超过上限时按 `recall_pin_sort_order` 升序、既有排序兜底和 SKU ID 升序裁定。小程序端 MUST 按接口返回顺序展示，不得做跨页本地重排，也不得展示召回置顶 UI 标识。

#### Scenario: 普通商品列表置顶排序

- **GIVEN** 当前普通商品列表存在多个可公开 SKU
- **AND** 其中部分 SKU 的 `recall_pin_sort_order` 小于 `9999` 且当前时间处于有效期内
- **WHEN** 小程序请求 `/api/v1/miniapp/products`
- **THEN** 生效召回 SKU MUST 排在非召回 SKU 之前
- **AND** 生效召回 SKU MUST 按 `recall_pin_sort_order` 升序排列
- **AND** 非召回 SKU MUST 保持该入口既有排序规则。

#### Scenario: 筛选条件先于置顶资格

- **GIVEN** 某 SKU 配置了生效召回置顶
- **WHEN** 该 SKU 不满足当前关键词、品牌、类目、规格、价格区间或公开展示条件
- **THEN** 系统 MUST 排除该 SKU
- **AND** MUST NOT 将其强行插入列表顶部。

#### Scenario: 置顶上限裁定

- **GIVEN** 当前请求内有 5 个或更多生效召回候选 SKU
- **WHEN** 后端计算商品列表排序
- **THEN** 仅排序值最靠前的 4 个 SKU MUST 进入置顶区
- **AND** 其余召回候选 MUST 按普通商品排序参与结果。

#### Scenario: 分页前排序稳定

- **WHEN** 用户刷新商品列表或加载更多
- **THEN** 后端 MUST 在分页前完成召回置顶排序
- **AND** 多页合并后 MUST NOT 出现重复、漏项或已加载商品顺序跳动。

#### Scenario: 榜单和价格排序不受影响

- **WHEN** 商品列表请求为 `section=new`、`section=hot`、价格升序或价格降序
- **THEN** 后端 MUST 跳过召回置顶排序
- **AND** 结果 MUST 保持新品榜、热销榜或价格排序原有语义。

#### Scenario: 不应用置顶逻辑的入口无置顶标识

- **WHEN** 小程序展示新品榜、热销榜、价格排序结果或后端未标记为当前列表实际生效置顶的 SKU
- **THEN** 商品卡片 MUST NOT 展示“置顶”“推荐”“召回”等置顶角标、标签或说明文案
- **AND** 页面 MUST NOT 新增排序说明、筛选控件或列表控件。

