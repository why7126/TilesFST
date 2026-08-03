## MODIFIED Requirements

### Requirement: 双列品牌卡片列表
品牌列表页 SHALL 在顶部轮播下方以每行一个品牌的信息行展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目汇总、不可用品牌和小屏视口提供稳定降级。

#### Scenario: 单行品牌列表展示
- **WHEN** 品牌列表页获取到公开品牌数据
- **THEN** 页面 SHALL 以每行一个品牌的信息行展示品牌
- **AND** 每个品牌行 SHALL 分为左侧品牌信息区和右侧类目汇总区
- **AND** 左侧品牌信息区 SHALL 展示品牌 Logo、品牌名称和该品牌公开商品数量
- **AND** 右侧类目汇总区 SHALL 展示该品牌所有上架/公开商品对应类目的最后一层级类目名称集合
- **AND** 品牌列表页 SHALL NOT 继续以一行 2 个品牌卡片作为本需求目标形态。

#### Scenario: 品牌公开过滤
- **WHEN** 小程序请求品牌列表数据
- **THEN** 系统 SHALL 仅返回或仅展示启用且公开可见的品牌
- **AND** 系统 SHALL NOT 展示未公开品牌、已停用品牌、内部备注或管理端专用字段。

#### Scenario: 商品数量与末级类目口径一致
- **WHEN** 系统计算品牌列表页的商品数量和末级类目集合
- **THEN** 商品数量 SHALL 统计该品牌下小程序公开可见商品
- **AND** 末级类目集合 SHALL 基于同一公开商品集合计算
- **AND** 已下架、禁用或不应公开展示的商品 SHALL NOT 计入商品数量或类目集合
- **AND** 页面 SHALL NOT 出现商品数量为 0 但仍展示类目的矛盾状态。

#### Scenario: 末级类目提取与去重
- **WHEN** 品牌下公开商品存在绑定类目路径
- **THEN** 系统 SHALL 取每个上架/公开商品类目路径的最后一层级类目名称用于品牌行右侧展示
- **AND** 商品只绑定一级或二级类目时 SHALL 取实际绑定路径中的最后一层名称
- **AND** 同一品牌下重复末级类目名称 SHALL 仅展示一次
- **AND** 类目名称展示顺序 SHALL 使用类目后台排序或实现阶段明确的稳定兜底排序。

#### Scenario: 品牌 Logo、长文案和类目多行展示
- **WHEN** 品牌 Logo 缺失、图片加载失败、品牌名称较长、类目名称较长或类目数量较多
- **THEN** 品牌行 SHALL 展示品牌名称首字、品牌占位或统一占位图
- **AND** 品牌名称 SHALL 按设计策略截断或换行
- **AND** 类目汇总 SHALL 全部折行展示，不使用“等 N 类”折叠或隐藏后续类目
- **AND** 品牌行 SHALL NOT 出现破图、文字重叠、横向滚动、布局跳动或右侧类目覆盖左侧品牌信息。

#### Scenario: 品牌列表空状态
- **WHEN** 没有公开可展示品牌
- **THEN** 页面 SHALL 展示品牌化空状态
- **AND** 页面 SHALL 保留返回、重试或其他安全导航能力。

#### Scenario: 品牌无公开商品
- **WHEN** 品牌存在但没有公开商品
- **THEN** 页面 SHALL 展示 0 款商品或等价空态值
- **AND** 右侧类目汇总区 SHALL 留空
- **AND** 右侧类目汇总区 SHALL NOT 重复展示左侧已有的“暂无商品”空态文案
- **AND** 页面 SHALL NOT 让用户误解为接口加载失败。

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
品牌列表页 SHALL 遵守小程序自定义导航和设备验收要求，确保顶部导航、微信原生胶囊、首屏轮播、品牌单行列表和底部 TabBar 在常见视口中可用。

#### Scenario: 导航和胶囊避让
- **WHEN** 品牌列表页使用自定义导航、fixed header 或 sticky header
- **THEN** 页面 SHALL 使用统一导航 offset、spacer 或等价布局 token
- **AND** 页面标题、返回按钮、品牌轮播、品牌单行列表和首屏内容 SHALL NOT 与微信原生胶囊 reserve 重叠。

#### Scenario: 返回兜底
- **WHEN** 用户从分享、外部入口或无页面栈场景进入品牌列表页并点击返回
- **THEN** 小程序 SHALL 提供首页或安全入口兜底
- **AND** 返回按钮触控热区 SHALL 不小于 44x44 pt。

#### Scenario: 设备 evidence
- **WHEN** 团队验收品牌列表页
- **THEN** 验收 evidence SHALL 至少覆盖 DevTools 320 pt、375 pt 和 430 pt 视口
- **AND** evidence SHALL 记录首屏轮播、品牌单行列表、左侧品牌信息、右侧类目汇总、胶囊避让、底部 TabBar 和加载/空/错态结论
- **AND** DevTools 通过 SHALL NOT 被表述为真机通过。

#### Scenario: 运行入口一致
- **WHEN** 品牌列表页存在 `.ts` 与 `.js` 文件
- **THEN** 微信开发者工具实际加载的 `.js` 逻辑 SHALL 与源 `.ts` 逻辑一致
- **AND** 运行脚本 SHALL NOT 保持空模板。
