# miniapp-brand-detail-home-page Specification

## Purpose
TBD - created by archiving change add-miniapp-brand-detail-home-page. Update Purpose after archive.
## Requirements
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
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。品牌主页顶部品牌图位 SHALL 作为首屏 Hero 大图展示位，普通展示 SHALL 优先使用后端受控 `display` 规格；品牌列表、品牌卡、商品详情品牌入口和证书详情品牌入口等小 Logo 场景 SHALL 继续优先使用后端受控真实缩略图。品牌主页信息区 SHALL 区分 Hero 展示 URL、小 Logo 展示 URL、高清预览或分享 URL，避免首屏直接加载原图。

#### Scenario: 品牌详情顶部 Hero 展示使用 display 规格

- **WHEN** 用户进入品牌主页/详情页且品牌存在 Logo 或品牌图片
- **THEN** 页面上半部分顶部 Hero SHALL 优先请求 `brand_hero_display_url` 或等价 `display` 规格 URL
- **AND** `display` 规格缺失、为空或加载失败时 SHALL 降级请求 `brand_hero_thumbnail_url` 或等价轻量缩略图
- **AND** `display` 与 `thumbnail` 均不可用时 SHALL 展示安全视图占位、品牌名占位或可理解失败态
- **AND** 品牌主页顶部 Hero SHALL NOT 通过 `brand_logo_url`、`original_url`、`preview_url`、旧 `url`、语义不明 `image_url` 或不存在的本地静态资源冷加载原图或失败占位。

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

商品 Tab SHALL 展示当前品牌下的公开 SKU 列表，并复用或对齐既有商品列表双列卡片、分页和状态机。商品 Tab SHALL 按 SKU 发布时间 `published_at` 升序、ID 升序展示当前品牌公开 SKU；历史数据 `published_at` 为空时，系统 SHALL 使用 SKU 创建时间 `created_at` 作为排序兜底。商品 Tab 的商品卡片图片 SHALL 复用商品列表缩略图优先策略，且非首屏商品图片 SHALL 启用懒加载或等价延迟加载。

#### Scenario: 品牌详情商品 Tab 使用商品卡片缩略图策略

- **WHEN** 用户查看品牌详情页商品 Tab
- **THEN** 商品卡片图片 SHALL 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 非首屏商品卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 商品详情、图片预览或分享场景 SHALL NOT 被强制降级为列表缩略图
- **AND** 缩略图缺失回退原图时 SHALL 记录为性能风险。

### Requirement: 品牌主页证书 Tab

证书 Tab SHALL 展示当前品牌关联且可公开的证书列表，并过滤不可展示证书和内部字段。证书 Tab 图片小图 SHALL 优先使用后端受控真实缩略图、卡片专用小图或等价轻量图片 URL；图片预览、证书详情或文件打开 SHALL 使用原图、原文件或等价安全引用。证书 Tab SHALL 对非首屏图片类证书启用懒加载或等价延迟加载策略，并在缩略图缺失、不可读或加载失败时展示统一占位或受控失败态，SHALL NOT 在卡片图片 `src` 中 fallback 到 `file_url`、原图或原始文件 URL。

#### Scenario: 证书图片使用缩略图且预览保留原图

- **WHEN** 用户查看品牌详情页证书 Tab 且证书为图片类资源
- **THEN** 证书列表小图 SHALL 优先使用同目录 `.thumb` 缩略图或等价轻量图片 URL
- **AND** 缩略图缺失、不可读、为空或图片加载失败时 SHALL 展示统一证书占位或受控失败态
- **AND** 卡片图片 SHALL NOT 使用 `file_url`、原图或原始文件 URL 作为默认 fallback
- **AND** 图片预览或证书详情 SHALL 使用原图、原文件或等价受控高清 URL
- **AND** 非首屏证书图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略。

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

### Requirement: 品牌详情页微信分享
品牌详情页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前品牌参数、标题兜底和分享直达异常态。

#### Scenario: 品牌详情分享给微信朋友
- **WHEN** 用户在品牌详情页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享路径 SHALL 指向当前品牌详情页并携带有效 `brandId` 和 `source=share` 或等价来源参数
- **AND** 分享标题 SHALL 优先使用品牌名称，品牌数据未加载完成时 SHALL 使用稳定兜底标题
- **AND** 用户点击分享卡片后 SHALL 进入对应品牌详情页。

#### Scenario: 品牌详情分享到朋友圈
- **WHEN** 用户在品牌详情页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 朋友圈入口 SHALL 保留当前 `brandId`
- **AND** 被分享用户打开后 SHALL 进入对应品牌详情页
- **AND** 品牌不存在、不可公开或参数无效时 SHALL 展示可返回或可重试状态而不是白屏。

#### Scenario: 品牌分享埋点与安全
- **WHEN** 品牌详情页记录分享行为
- **THEN** 事件 SHOULD 包含页面路径、分享渠道和 `brandId`
- **AND** 埋点失败 SHALL NOT 阻断分享
- **AND** 分享路径和埋点 SHALL NOT 包含 Authorization header、Cookie、真实客户隐私、内部字段或本机绝对路径。

