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
品牌列表页 SHALL 在顶部提供品牌轮播区域，并 SHALL 与小程序首页轮播保持一致的基础交互体验。

#### Scenario: 品牌轮播展示
- **WHEN** 品牌列表页存在有效轮播数据
- **THEN** 页面 SHALL 展示品牌轮播图片、标题、副标题和指示点
- **AND** 轮播 SHALL 支持自动播放和循环播放
- **AND** 指示点激活态 SHALL 使用品牌金或等价品牌强调语义。

#### Scenario: 品牌轮播跳转
- **WHEN** 用户点击有效品牌轮播项
- **THEN** 小程序 SHALL 按配置跳转到品牌详情、品牌商品列表、商品详情、搜索或门店信息等可达目标
- **AND** 当目标不可达时，小程序 SHALL 安全降级并提示
- **AND** 小程序 SHALL NOT 打开空白页或无效路由。

#### Scenario: 品牌轮播图片安全
- **WHEN** 品牌轮播展示图片
- **THEN** 图片 URL SHALL 是公开安全 URL 或后端授权 URL
- **AND** 响应 SHALL NOT 暴露 MinIO 原始 object key、内部路径、Authorization header 或 Cookie。

#### Scenario: 无轮播数据降级
- **WHEN** 品牌列表页没有有效轮播数据或轮播图片加载失败
- **THEN** 页面 SHALL 隐藏异常轮播项或展示品牌化兜底
- **AND** 页面 SHALL NOT 展示破图。

### Requirement: 双列品牌卡片列表
品牌列表页 SHALL 以一行 2 个卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、不可用品牌和小屏视口提供稳定降级。

#### Scenario: 双列品牌列表展示
- **WHEN** 品牌列表页获取到公开品牌数据
- **THEN** 页面 SHALL 以一行 2 个品牌卡片展示品牌
- **AND** 每张卡片 SHALL 至少展示品牌 Logo 和品牌名称
- **AND** 品牌卡片 MAY 展示品牌简介、标语、商品数量或进入提示。

#### Scenario: 品牌公开过滤
- **WHEN** 小程序请求品牌列表数据
- **THEN** 系统 SHALL 仅返回或仅展示启用且公开可见的品牌
- **AND** 系统 SHALL NOT 展示未公开品牌、已停用品牌、内部备注或管理端专用字段。

#### Scenario: 品牌 Logo 和长文案降级
- **WHEN** 品牌 Logo 缺失、图片加载失败或品牌名称较长
- **THEN** 品牌卡片 SHALL 展示品牌名称首字、品牌占位或统一占位图
- **AND** 品牌名称 SHALL 按设计策略截断或换行
- **AND** 卡片 SHALL NOT 出现破图、文字重叠、横向滚动或布局跳动。

#### Scenario: 品牌列表空状态
- **WHEN** 没有公开可展示品牌
- **THEN** 页面 SHALL 展示品牌化空状态
- **AND** 页面 SHALL 保留返回、重试或其他安全导航能力。

### Requirement: 品牌卡片点击与埋点
品牌列表页 SHALL 支持整卡点击品牌卡片，并 SHALL 记录品牌页曝光、品牌轮播点击和品牌卡片点击事件。

#### Scenario: 品牌卡片点击跳转
- **WHEN** 用户点击可用品牌卡片
- **THEN** 小程序 SHALL 优先进入品牌详情页或品牌主页
- **AND** 如果品牌详情页尚未交付，小程序 MAY 进入品牌商品列表并携带品牌筛选参数
- **AND** 跳转上下文 SHALL 包含可用品牌 ID、品牌名称、来源页面和位置索引。

#### Scenario: 不可用品牌点击
- **WHEN** 用户点击已下架、未公开或缺少有效跳转目标的品牌卡片
- **THEN** 小程序 SHALL 阻止无效跳转并展示轻量提示
- **AND** 小程序 SHALL NOT 打开空白页或错误路由。

#### Scenario: 品牌列表埋点
- **WHEN** 用户浏览品牌列表页或点击品牌轮播、品牌卡片
- **THEN** 系统 SHOULD 记录 `brand_list_page_view`、`brand_banner_click` 和 `brand_card_click` 或等价事件
- **AND** 事件参数 SHOULD 包含品牌 ID、轮播 ID、跳转类型、位置索引和来源入口中的可用字段
- **AND** 事件 SHALL NOT 记录手机号、地址、微信号、Authorization header、Cookie 或其他与品牌浏览无关的敏感信息。

### Requirement: 品牌列表页小程序导航与设备验收
品牌列表页 SHALL 遵守小程序自定义导航和设备验收要求，确保顶部导航、微信原生胶囊、首屏轮播、双列品牌卡片和底部 TabBar 在常见视口中可用。

#### Scenario: 导航和胶囊避让
- **WHEN** 品牌列表页使用自定义导航、fixed header 或 sticky header
- **THEN** 页面 SHALL 使用统一导航 offset、spacer 或等价布局 token
- **AND** 页面标题、返回按钮、品牌轮播和首屏内容 SHALL NOT 与微信原生胶囊 reserve 重叠。

#### Scenario: 返回兜底
- **WHEN** 用户从分享、外部入口或无页面栈场景进入品牌列表页并点击返回
- **THEN** 小程序 SHALL 提供首页或安全入口兜底
- **AND** 返回按钮触控热区 SHALL 不小于 44x44 pt。

#### Scenario: 设备 evidence
- **WHEN** 团队验收品牌列表页
- **THEN** 验收 evidence SHALL 至少覆盖 DevTools 320 pt、375 pt 和 430 pt 视口
- **AND** evidence SHALL 记录首屏轮播、双列品牌卡片、胶囊避让、底部 TabBar 和加载/空/错态结论
- **AND** DevTools 通过 SHALL NOT 被表述为真机通过。

#### Scenario: 运行入口一致
- **WHEN** 品牌列表页存在 `.ts` 与 `.js` 文件
- **THEN** 微信开发者工具实际加载的 `.js` 逻辑 SHALL 与源 `.ts` 逻辑一致
- **AND** 运行脚本 SHALL NOT 保持空模板。

