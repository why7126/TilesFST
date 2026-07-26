## MODIFIED Requirements

### Requirement: 微信小程序首页首屏
系统 SHALL 提供原生微信小程序首页，用于面向终端客户展示菲尚特品牌、搜索入口、Banner、快捷业务入口、新品推荐、热销推荐、全部产品瀑布流和底部 TabBar。

#### Scenario: 首页首屏展示核心模块
- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 展示品牌 Logo、门店名称、品牌副文案、搜索入口、Banner、四个快捷业务入口和至少一个推荐模块
- **AND** 页面 SHALL 使用深色品牌视觉，页面背景、卡片/搜索框/模块底色、品牌金、主文字和辅助文字 SHALL 与 REQ-0043 验收标准一致
- **AND** 页面 SHALL NOT 展示新增、编辑、上下架、库存、订单或客户管理入口。

#### Scenario: 首页移动视口可用
- **WHEN** 团队在 375x812、390x844 和 320 到 430 pt 宽度范围验收首页
- **THEN** 页面 SHALL 无页面级横向滚动、明显内容截断、控件重叠或底部 TabBar 遮挡
- **AND** 所有主要点击区域 SHALL 不小于 44x44 pt。

#### Scenario: 首页运行入口执行业务逻辑
- **WHEN** 微信开发者工具预览 `pages/index/index`
- **THEN** 实际运行脚本 SHALL 初始化首页状态并触发首页聚合数据或全部产品首批数据加载
- **AND** 实际运行脚本 SHALL NOT 保持空模板 `Page({ data: {}, onLoad() {} })`
- **AND** 首页动态模块 SHALL 基于运行时数据或模块级降级策略展示。

#### Scenario: 首页真实小程序导航环境
- **WHEN** 首页使用微信原生导航栏
- **THEN** 页面内容 SHALL 从品牌 Header 或搜索入口开始，并避免与原生标题重复
- **AND** Header SHALL NOT 模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件。

### Requirement: Banner 与快捷入口
小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。

#### Scenario: Banner 跳转安全降级
- **WHEN** 用户点击 Banner 且跳转目标属于商品详情、搜索结果或门店信息
- **THEN** 小程序 SHALL 跳转到对应页面
- **AND** 当配置目标不可达或指向本期未实现能力时，小程序 SHALL 安全降级且不得出现空白页或路由错误。

#### Scenario: 四入口快捷导航
- **WHEN** 用户查看首页快捷导航
- **THEN** 小程序 SHALL 仅展示“选瓷砖”、“品牌馆”、“新品榜”和“热销榜”四个快捷入口
- **AND** 四个入口 SHALL 使用统一的图标在上、文案在下结构
- **AND** 每个入口点击区域 SHALL 不小于 72x72px 或小程序等效尺寸。

#### Scenario: 快捷入口点击策略
- **WHEN** 用户点击四个快捷入口之一
- **THEN** “选瓷砖” SHALL 进入分类 Tab、筛选页或已有分类能力
- **AND** “品牌馆” SHALL 安全降级到搜索、筛选或占位提示，直到完整品牌馆能力另行建设
- **AND** “新品榜” SHALL 进入搜索页并带入 `section=new` 或等价筛选参数
- **AND** “热销榜” SHALL 进入搜索页并带入 `section=hot` 或等价筛选参数
- **AND** 任一目标不可达时 SHALL 安全降级且不得出现白屏或路由错误。

### Requirement: 原型与范围控制
小程序首页实现 SHALL 参考 `issues/requirements/archive/REQ-0043-miniapp-home-style-optimization/prototype/miniapp/` 下的 HTML 和 context，以及用户附件 PNG；当原型、验收和既有 spec 冲突时，优先级 SHALL 为 HTML、PNG、context、acceptance、UI 设计规则、既有 spec。

#### Scenario: 收藏能力不进入本期
- **WHEN** 实现小程序首页或商品详情
- **THEN** 系统 SHALL NOT 提供收藏持久化 API、收藏列表、收藏统计或用户维度收藏状态
- **AND** 原型中的收藏心形 MAY 作为非持久化视觉反馈、建设中提示或占位展示
- **AND** 热销推荐排序 SHALL NOT 依赖收藏量。

#### Scenario: 证书与品牌馆完整能力不进入本期
- **WHEN** 用户点击证书 Tab、品牌馆入口、新品榜入口或热销榜入口
- **THEN** 小程序 SHALL 跳转到已有可用页面、搜索筛选结果或占位提示
- **AND** 系统 SHALL NOT 在本 Change 中新增完整证书聚合页、证书详情页、品牌馆独立页、品牌详情页、新品榜独立页或热销榜独立页。

#### Scenario: 不做项不被误纳入
- **WHEN** 团队验收本 Change
- **THEN** 验收 SHALL 确认收藏持久化、证书聚合页、品牌馆独立页、榜单独立页、快捷入口后台配置、订单、库存、新增、编辑、上下架和客户管理未被实现。

## ADDED Requirements

### Requirement: 新品热销与全部产品承接
小程序首页 SHALL 在 Banner 与快捷入口后展示新品推荐、热销推荐和全部产品瀑布流，使用户可以连续浏览公开 SKU。

#### Scenario: 新品推荐商品卡片
- **WHEN** 首页展示新品推荐
- **THEN** 小程序 SHALL 使用横向滚动商品卡片展示 SKU 主图、SKU 编号或商品名称、规格和 `price_display`
- **AND** 商品图片区域 SHALL NOT 展示“新品”角标或标签
- **AND** 用户点击商品卡片 SHALL 进入商品详情页。

#### Scenario: 热销推荐商品卡片
- **WHEN** 首页展示热销推荐
- **THEN** 小程序 SHALL 使用双列大卡片展示 SKU 主图、系列或商品名、空间或工艺标签和 `price_display`
- **AND** 用户点击卡片 SHALL 进入商品详情页
- **AND** 收藏心形如出现，SHALL 仅作为非持久化视觉反馈或占位。

#### Scenario: 全部产品瀑布流展示
- **WHEN** 用户浏览热销推荐下方区域
- **THEN** 首页 SHALL 展示“全部产品”模块
- **AND** 全部产品 SHALL 使用双列瀑布流布局，图片高度允许错落
- **AND** 首页 SHALL NOT 使用固定等高双列网格冒充瀑布流。

#### Scenario: 全部产品分页加载
- **WHEN** 首页首次加载全部产品
- **THEN** 小程序 SHALL 加载 10 到 20 个公开商品，默认分页大小 SHOULD 为 12
- **AND** 页面滚动接近底部 200 到 300px 且 `has_more=true` 时 SHALL 自动加载下一页
- **AND** 请求期间 SHALL 防止重复触发并发请求。

#### Scenario: 全部产品追加去重
- **WHEN** 下一页商品加载成功
- **THEN** 小程序 SHALL 将新商品追加到已有列表
- **AND** SHALL NOT 覆盖已有商品
- **AND** SHALL 按 `product_id` 或等价商品 ID 去重。

#### Scenario: 全部产品状态降级
- **WHEN** 全部产品返回 `has_more=false` 或前端推导没有更多
- **THEN** 小程序 SHALL 展示“已经到底了”或等价状态，并停止继续请求
- **WHEN** 下一页加载失败
- **THEN** 小程序 SHALL 展示可重试状态，并保留已加载商品
- **WHEN** 首页没有商品
- **THEN** 搜索、Banner、快捷入口等非商品模块 SHALL 继续可见。

### Requirement: 小程序首页 TabBar 目标与安全降级
小程序首页 SHALL 以“首页、分类、找砖、收藏、证书”为目标 TabBar 文案，并保证未完成页面可安全降级。

#### Scenario: TabBar 文案与选中态
- **WHEN** 用户查看小程序底部 TabBar
- **THEN** TabBar SHALL 展示“首页”、“分类”、“找砖”、“收藏”和“证书”目标文案
- **AND** 选中态 SHALL 使用品牌金或等价高亮
- **AND** “我的”Tab SHALL NOT 作为首页目标导航出现。

#### Scenario: 未完成 Tab 安全降级
- **WHEN** 用户点击收藏或证书 Tab 且完整页面未实现
- **THEN** 小程序 SHALL 展示“功能建设中”或等价提示，或跳转到可返回的占位页
- **AND** 页面 SHALL NOT 白屏、路由报错或丢失返回能力。
