## ADDED Requirements

### Requirement: 微信小程序品牌入口页
系统 SHALL 提供微信小程序品牌入口页，用于集中展示可公开访问的品牌、品牌轮播和品牌卡片列表。

#### Scenario: 品牌入口页展示结构
- **WHEN** 用户进入品牌入口页
- **THEN** 小程序 SHALL 展示顶部品牌轮播和下方品牌列表
- **AND** 页面 SHALL 支持加载中、空状态、错误状态和重试
- **AND** 页面 SHALL NOT 展示管理端新增、编辑、启用、停用、删除或上传入口。

#### Scenario: 品牌轮播对齐首页轮播
- **WHEN** 品牌入口页存在可展示轮播数据
- **THEN** 小程序 SHALL 使用与首页轮播一致的 swiper 视觉、图片比例、指示器和滑动交互
- **AND** 轮播图片加载前后 SHALL NOT 造成明显布局跳动
- **AND** 轮播项点击 SHOULD 进入对应品牌主页/详情页。

#### Scenario: 品牌轮播无数据降级
- **WHEN** 品牌入口页没有可展示轮播数据或轮播加载失败
- **THEN** 小程序 SHALL 展示与首页轮播一致的品牌化降级视觉或隐藏轮播区
- **AND** 页面 SHALL 继续展示品牌列表或可恢复状态
- **AND** 页面 SHALL NOT 白屏。

### Requirement: 微信小程序品牌列表卡片
系统 SHALL 在品牌入口页以一行 2 个品牌卡片展示公开品牌，并支持进入品牌主页/详情页。

#### Scenario: 双列品牌卡片
- **WHEN** 品牌入口页返回公开品牌列表
- **THEN** 小程序 SHALL 以一行 2 个品牌卡片展示
- **AND** 每张品牌卡片 SHALL 展示品牌图片或 Logo、品牌名称
- **AND** 品牌卡片 MAY 展示品牌简称、英文名、商品数量或简短介绍
- **AND** 辅助信息 SHALL NOT 挤压品牌主图和品牌名称。

#### Scenario: 品牌卡片图片和长文本兜底
- **WHEN** 品牌图片缺失、图片加载失败或品牌名称过长
- **THEN** 品牌卡片 SHALL 展示统一占位图、品牌首字或等价深色占位
- **AND** 品牌名称 SHALL 截断或限制行数
- **AND** 卡片 SHALL NOT 展示破图、空字符串、`null`、`undefined` 或接口字段名。

#### Scenario: 品牌卡片进入详情
- **WHEN** 用户点击可用品牌卡片
- **THEN** 小程序 SHALL 携带 `brandId` 进入对应品牌主页/详情页
- **AND** 小程序 SHOULD 携带 `sourcePage`、`sourceModule`、`index` 和可用 `requestId`
- **AND** 连续点击 SHALL NOT 重复打开多个品牌主页。

### Requirement: 微信小程序品牌主页信息区
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。

#### Scenario: 品牌主页加载公开信息
- **WHEN** 用户通过 `brandId` 访问品牌主页/详情页
- **THEN** 小程序 SHALL 加载该品牌的公开信息
- **AND** 页面上半部分 SHALL 展示品牌图片或 Logo、品牌名称和品牌介绍
- **AND** 响应 SHALL NOT 暴露后台内部字段、对象存储原始 key、内部备注、Authorization header、Cookie 或敏感配置。

#### Scenario: 品牌信息降级
- **WHEN** 品牌主图缺失、Logo 缺失或品牌介绍为空
- **THEN** 小程序 SHALL 使用统一占位、回退到可用图片、隐藏区域或展示简短兜底文案
- **AND** 页面 SHALL NOT 展示破图、异常空字段或错误字段名。

#### Scenario: 品牌不可访问
- **WHEN** `brandId` 缺失、非法、品牌不存在、品牌禁用、品牌下架或品牌不可公开
- **THEN** 小程序 SHALL 展示可恢复错误态
- **AND** 页面 SHALL 提供返回或回首页能力
- **AND** 页面 SHALL NOT 白屏。

### Requirement: 微信小程序品牌主页 Tab 内容
品牌主页/详情页 SHALL 在品牌信息区下方通过 Tab 展示当前品牌关联内容，首期包含商品和证书。

#### Scenario: 商品和证书 Tab
- **WHEN** 用户进入品牌主页/详情页
- **THEN** 页面 SHALL 展示“商品”和“证书”Tab
- **AND** 默认 Tab SHALL 为“商品”
- **AND** 切换 Tab 时上方品牌信息 SHALL 保持可见或可返回查看
- **AND** Tab 切换 SHALL NOT 清空品牌基础信息。

#### Scenario: Tab 独立状态
- **WHEN** 商品 Tab 或证书 Tab 加载、为空、失败或重试
- **THEN** 对应 Tab SHALL 独立展示加载中、空状态、错误状态和重试
- **AND** 一个 Tab 的失败 SHALL NOT 破坏另一个 Tab 已加载内容
- **AND** Tab 状态文案 SHOULD 包含当前品牌上下文。

### Requirement: 品牌主页商品 Tab
商品 Tab SHALL 展示当前品牌下的公开 SKU 列表，并复用或对齐既有商品列表双列卡片、分页和状态机。

#### Scenario: 当前品牌商品列表
- **WHEN** 用户查看品牌主页商品 Tab
- **THEN** 小程序 SHALL 仅展示当前品牌下可公开 SKU
- **AND** 商品卡片 SHALL 展示主图、商品名称、品牌或规格、参考价格和状态徽标
- **AND** 商品列表 SHALL 使用一行 2 个商品卡片布局。

#### Scenario: 商品 Tab 分页与跳转
- **WHEN** 用户刷新、上拉加载更多或点击商品卡片
- **THEN** 商品 Tab SHALL 支持首屏加载、下拉刷新、上拉加载更多、无更多和加载失败重试
- **AND** 点击商品卡片 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 页面 SHOULD 携带 `brandId`、`sourcePage=brand_detail`、`sourceModule=brand_products`、`index` 和可用 `requestId`。

#### Scenario: 当前品牌无商品
- **WHEN** 当前品牌没有可公开 SKU
- **THEN** 商品 Tab SHALL 展示品牌上下文空态
- **AND** 页面 SHALL NOT 自动展示其他品牌商品。

### Requirement: 品牌主页证书 Tab
证书 Tab SHALL 展示当前品牌关联且可公开的证书列表，并过滤不可展示证书和内部字段。

#### Scenario: 当前品牌证书列表
- **WHEN** 用户查看品牌主页证书 Tab
- **THEN** 小程序 SHALL 仅展示当前品牌关联且可公开的证书
- **AND** 证书项 SHALL 展示证书图片、证书名称、证书类型和必要有效状态
- **AND** 证书响应 SHALL NOT 暴露后台内部字段、审计字段、内部备注、对象存储原始 key、Authorization header、Cookie 或敏感配置。

#### Scenario: 证书预览或详情
- **WHEN** 用户点击可公开证书项
- **THEN** 小程序 SHALL 支持预览证书图片或进入证书详情
- **AND** 证书文件 SHALL 使用受控读取 URL 或等价安全引用
- **AND** 证书加载失败 SHALL 展示稳定错误提示。

#### Scenario: 当前品牌无证书
- **WHEN** 当前品牌没有可公开证书
- **THEN** 证书 Tab SHALL 展示品牌上下文空态
- **AND** 页面 SHALL NOT 展示其他品牌证书。

### Requirement: 品牌主页导航、设备验收与埋点
品牌入口页和品牌主页/详情页 SHALL 遵守小程序导航、设备视口、运行入口和埋点质量门禁。

#### Scenario: 小程序导航与视口验收
- **WHEN** 团队验收品牌入口页和品牌主页/详情页
- **THEN** 验收证据 SHALL 覆盖 DevTools 320、375 和 430 pt 宽度
- **AND** 品牌轮播、品牌卡片、Tab、商品卡片、证书卡片、自定义导航、原生胶囊 reserve 和底部 TabBar SHALL 不重叠
- **AND** 真机验收不可用时 SHALL 标记 blocked 或 follow_up
- **AND** 静态测试通过 SHALL NOT 被表述为 DevTools 或真机通过。

#### Scenario: 小程序运行入口一致
- **WHEN** 品牌入口页和品牌主页/详情页同时存在 `.ts` 与 `.js`
- **THEN** 微信开发者工具实际加载的 `.js` SHALL 包含对应页面的关键业务数据、生命周期和交互方法
- **AND** 项目 SHALL 通过静态测试、构建同步命令或等价机制发现 `.ts` 有业务逻辑但 `.js` 为空模板的脱节状态。

#### Scenario: 品牌页行为埋点
- **WHEN** 用户浏览品牌入口页、点击品牌轮播、点击品牌卡片、浏览品牌主页、切换 Tab、点击商品或点击证书
- **THEN** 小程序 SHOULD 记录对应行为事件
- **AND** 事件参数 SHOULD 包含 `sourcePage`、`sourceModule`、`brandId`、`brandName`、`tab`、`page`、`pageSize`、`resultCount`、`index` 和可用 `requestId`
- **AND** 埋点失败 SHALL NOT 阻断页面加载、Tab 切换、预览或详情跳转。
