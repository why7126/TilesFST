# miniapp-brand-list-page Specification

## Purpose
TBD - created by archiving change add-brand-list-page. Update Purpose after archive.
## Requirements
### Requirement: 微信小程序品牌列表页入口
系统 SHALL 提供微信小程序品牌列表页入口，使用户可从小程序现有导航或首页入口进入品牌列表页，并 SHALL 将相关入口文案统一为“品牌”。

#### Scenario: 品牌入口进入品牌列表页
- **WHEN** 用户点击小程序中的“品牌”入口
- **THEN** 小程序 SHALL 进入品牌列表页
- **AND** 小程序 SHALL NOT 继续降级进入搜索页、分类页、找砖页或建设中提示。

#### Scenario: 品牌入口文案一致
- **WHEN** 小程序展示品牌相关入口、页面标题或导航标题
- **THEN** 入口文案、页面标题和导航标题 SHALL 使用“品牌”或等价品牌频道语义
- **AND** 小程序 SHALL NOT 将本品牌列表页入口展示为“找砖”。

#### Scenario: 品牌列表页入口失败可恢复
- **WHEN** 用户进入品牌列表页且页面数据加载失败
- **THEN** 小程序 SHALL 展示可恢复错误态和重试入口
- **AND** 页面 SHALL NOT 白屏、路由报错或丢失返回能力。

### Requirement: 品牌列表页轮播

品牌列表页 SHALL 在顶部提供品牌轮播区域，并 SHALL 与小程序首页轮播保持一致的基础交互体验。品牌轮播区域 SHALL NOT 展示开发、原型、验收或能力说明类文案作为正式用户可见内容。品牌轮播图属于首屏大图展示位，目标规格 SHALL 为 `display`；品牌轮播图片 SHALL 优先使用后端受控真实展示图，缺失或不可读时降级到缩略图或等价轻量字段；缩略图也缺失或加载失败时 SHALL 使用安全占位或品牌化兜底图，不得冷加载原图作为普通展示 fallback。

#### Scenario: 品牌轮播图片优先使用 display 展示图

- **WHEN** 品牌列表页展示品牌轮播图片
- **THEN** 小程序 SHALL 优先使用后端返回的展示图 URL，缺失或不可读时降级到缩略图 URL 或等价轻量展示 URL
- **AND** 缩略图对象 SHALL 真实存在，且字节数或像素尺寸应明显小于原图
- **AND** `.thumb` 或 `.display` URL 实际回退原图时 SHALL 记录为性能风险
- **AND** 页面 SHALL NOT 仅因 URL 包含 `.thumb` 或 `.display` 就判定图片性能验收通过
- **AND** 缺少轻量字段时 SHALL 展示安全占位或品牌化兜底图，不得请求原图或不存在的本地静态占位图。

### Requirement: 双列品牌卡片列表

品牌列表页 SHALL 在顶部轮播或品牌氛围 Hero 下方以每行一个品牌的信息卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目胶囊、不可用品牌和小屏视口提供稳定降级。品牌 Logo 或品牌图片小图 SHALL 优先使用后端受控真实缩略图；缩略图缺失或加载失败时 SHALL 使用安全占位、品牌首字或统一默认图，不得回退品牌 Logo 原图。非首屏品牌卡片图片 SHALL 启用小程序懒加载或等价延迟加载策略。

#### Scenario: 品牌卡片图片懒加载与缩略图收益验收

- **WHEN** 品牌列表页展示多条品牌卡片
- **THEN** 品牌卡片 Logo 或品牌图片 SHALL 优先使用真实轻量缩略图
- **AND** 非首屏品牌卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 首屏关键品牌图片 SHALL 保持可预期展示，不得因懒加载造成明显空白
- **AND** 图片加载失败时 SHALL 使用安全占位、品牌首字或统一默认图
- **AND** 图片加载失败或缩略图缺失 SHALL NOT 请求 `brand_logo_url` 原图作为普通展示 fallback
- **AND** 小程序 evidence SHALL 覆盖品牌卡片图片 URL、资源大小、耗时、占位和失败态。

### Requirement: 品牌卡片点击与埋点
品牌列表页 SHALL 支持整行点击品牌信息行，并 SHALL 记录品牌页曝光、品牌轮播点击和品牌行点击事件。

#### Scenario: 品牌行点击跳转
- **WHEN** 用户点击可用品牌行
- **THEN** 小程序 SHALL 在用户点击品牌 Logo 或品牌名称时进入品牌详情页或品牌主页
- **AND** 跳转上下文 SHALL 包含可用品牌 ID、品牌名称、来源页面和位置索引
- **AND** 品牌 Logo 与品牌名称点击区域 SHALL 不小于 44x44 pt 并保留小程序原生按压反馈。

#### Scenario: 品牌类目点击跳转
- **WHEN** 用户点击品牌行右侧某个类目名称
- **THEN** 小程序 SHALL 进入商品列表页
- **AND** 商品列表页 SHALL 按当前品牌 ID 与当前类目 ID 过滤商品
- **AND** 跳转参数 SHALL 包含 `brandId`、`categoryId`、`categoryLevel`、`categoryName` 和 `sourcePage=brand-list-category`
- **AND** 类目点击 SHALL NOT 触发品牌详情页跳转。

#### Scenario: 不可用品牌点击
- **WHEN** 用户点击已下架、未公开或缺少有效跳转目标的品牌行
- **THEN** 小程序 SHALL 阻止无效跳转并展示轻量提示
- **AND** 小程序 SHALL NOT 打开空白页或错误路由。

#### Scenario: 品牌列表埋点
- **WHEN** 用户浏览品牌列表页或点击品牌轮播、品牌 Logo / 名称、品牌右侧类目
- **THEN** 系统 SHOULD 记录 `brand_list_page_view`、`brand_banner_click`、`brand_card_click`、`brand_list_category_click` 或等价事件
- **AND** 事件参数 SHOULD 包含品牌 ID、类目 ID、类目名称、轮播 ID、跳转类型、位置索引和来源入口中的可用字段
- **AND** 事件 SHALL NOT 记录手机号、地址、微信号、Authorization header、Cookie 或其他与品牌浏览无关的敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌列表展示、品牌行点击跳转或重试。

### Requirement: 品牌列表页小程序导航与设备验收

品牌列表页 SHALL 遵守小程序自定义导航和设备验收要求，确保顶部导航、微信原生胶囊、首屏 Hero 或轮播、品牌卡片、类目胶囊和底部 TabBar 在常见视口中可用。

#### Scenario: 导航和胶囊避让

- **WHEN** 品牌列表页使用自定义导航、fixed header 或 sticky header
- **THEN** 页面 SHALL 使用统一导航 offset、spacer 或等价布局 token
- **AND** 页面标题、返回按钮、品牌 Hero 或轮播、品牌卡片和首屏内容 SHALL NOT 与微信原生胶囊 reserve 重叠。

#### Scenario: 返回兜底

- **WHEN** 用户从分享、外部入口或无页面栈场景进入品牌列表页并点击返回
- **THEN** 小程序 SHALL 提供首页或安全入口兜底
- **AND** 返回按钮触控热区 SHALL 不小于 44x44 pt。

#### Scenario: 设备 evidence

- **WHEN** 团队验收品牌列表页
- **THEN** 验收 evidence SHALL 至少覆盖 DevTools 320 pt、375 pt、390 pt 和 430 pt 视口
- **AND** evidence SHALL 记录首屏 Hero 或轮播、品牌矩阵标题、品牌卡片、类目胶囊、胶囊避让、底部 TabBar、加载态、空态和错误态结论
- **AND** DevTools 通过 SHALL NOT 被表述为真机通过。

#### Scenario: 运行入口一致

- **WHEN** 品牌列表页存在 `.ts` 与 `.js` 文件
- **THEN** 微信开发者工具实际加载的 `.js` 逻辑 SHALL 与源 `.ts` 逻辑一致
- **AND** 运行脚本 SHALL NOT 保持空模板。

### Requirement: 品牌列表页新版 UI 与交互分区

品牌列表页 SHALL 按 REQ-0086 的新版设计稿优化视觉层级、品牌矩阵、品牌卡片和类目入口，并 SHALL 在品牌详情入口与类目商品入口之间提供明确触控分区。

#### Scenario: 新版品牌页首屏结构

- **WHEN** 用户进入微信小程序品牌列表页
- **THEN** 页面 SHALL 展示自定义导航、页面标题“品牌”、品牌氛围 Hero、品牌矩阵标题、品牌卡片列表和底部 TabBar
- **AND** Hero SHOULD 展示英文弱标签、品牌主标题和辅助文案
- **AND** 品牌矩阵标题 SHALL 展示“品牌矩阵”
- **AND** 品牌矩阵标题 SHALL NOT 展示“按类目快速识别”辅助提示
- **AND** 页面 SHALL NOT 遮挡微信原生胶囊、状态栏、底部 TabBar 或 Safe Area。

#### Scenario: 品牌卡片上下分区

- **WHEN** 品牌列表页展示单个品牌卡片
- **THEN** 卡片上行 SHALL 展示品牌 Logo 或首字母占位、品牌名称、公开商品数量和进入指示
- **AND** 卡片上行 SHALL 作为品牌详情入口
- **AND** 卡片下行 SHALL 展示末级类目胶囊标签
- **AND** 卡片下行 SHALL NOT 展示“全部类目 · 点击查看该品牌下的类目商品”等说明文案
- **AND** 卡片下行 SHALL 作为品牌下类目商品入口集合
- **AND** 卡片上下分区 SHALL 通过分隔线、间距或视觉层级明确区分。

#### Scenario: 类目胶囊独立点击

- **WHEN** 用户点击品牌卡片下行的任一类目胶囊
- **THEN** 小程序 SHALL 进入商品列表页
- **AND** 跳转参数 SHALL 包含当前品牌 ID 与当前类目 ID
- **AND** 小程序 SHALL 阻止该点击继续触发品牌详情页跳转
- **AND** 类目胶囊 SHALL 保留小程序端可感知的按压反馈。

#### Scenario: 新版暗色视觉与底部 TabBar

- **WHEN** 品牌列表页渲染新版 UI
- **THEN** 页面 SHALL 延续暗色旗舰风与品牌金强调
- **AND** 底部 TabBar 中“品牌”项 SHALL 呈现选中态
- **AND** 页面滚动内容 SHALL NOT 被底部 TabBar 或安全区遮挡
- **AND** 品牌 Logo 失败、品牌名较长、类目名较长和类目数量较多时 SHALL NOT 出现破图、文字重叠、横向溢出或主要入口不可点击。

### Requirement: 品牌列表搜索路径
品牌列表页 SHALL 支持在当前品牌列表页按品牌名称、品牌简称和品牌英文名过滤，并 SHALL 保持品牌卡片、品牌详情入口和品牌类目入口不回归。搜索态 SHALL 隐藏品牌 Banner 轮播和品牌 Hero 兜底，清空关键词后 SHALL 恢复完整品牌列表和 Banner 展示。

#### Scenario: 品牌关键词查找
- **WHEN** 用户在品牌列表页输入或提交品牌关键词
- **THEN** 页面 SHALL 请求公开品牌列表并携带 `keyword`
- **AND** 后端 SHALL 仅在品牌字段内匹配品牌名称、品牌简称和品牌英文名
- **AND** 搜索结果 SHALL 保持品牌列表页卡片布局、品牌卡片点击、品牌详情跳转和品牌类目入口行为
- **AND** 页面 SHALL 隐藏 Banner 轮播和品牌 Hero 兜底
- **AND** 空结果 SHALL 说明当前为品牌范围无结果，并提供调整关键词或清空当前搜索的路径。

#### Scenario: 品牌搜索清空
- **WHEN** 用户清空品牌列表页关键词
- **THEN** 页面 SHALL 重新请求不带 `keyword` 的公开品牌列表
- **AND** 页面 SHALL 恢复完整品牌列表、Banner 轮播或品牌 Hero 兜底
- **AND** 搜索入口 SHALL NOT 替代品牌卡片主点击区域。

