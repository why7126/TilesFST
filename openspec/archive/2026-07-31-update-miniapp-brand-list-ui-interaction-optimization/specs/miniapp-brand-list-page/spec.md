## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: 双列品牌卡片列表

品牌列表页 SHALL 在顶部轮播或品牌氛围 Hero 下方以每行一个品牌的信息卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目胶囊、不可用品牌和小屏视口提供稳定降级。

#### Scenario: 单行品牌列表展示

- **WHEN** 品牌列表页获取到公开品牌数据
- **THEN** 页面 SHALL 以每行一个品牌的信息卡片展示品牌
- **AND** 每个品牌卡片 SHALL 分为上行品牌信息区和下行类目汇总区
- **AND** 上行品牌信息区 SHALL 展示品牌 Logo 或首字母占位、品牌名称和该品牌公开商品数量
- **AND** 上行品牌信息区 SHOULD 展示轻量进入指示
- **AND** 下行类目汇总区 SHALL 展示该品牌所有上架/公开商品对应类目的最后一层级类目名称集合
- **AND** 下行类目 SHOULD 使用胶囊标签展示并自动换行
- **AND** 类目胶囊字号 SHOULD 比品牌名称字号小 2rpx
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

#### Scenario: 末级类目提取、ID 与去重

- **WHEN** 品牌下公开商品存在绑定类目路径
- **THEN** 系统 SHALL 取每个上架/公开商品类目路径的最后一层级类目用于品牌卡片下行展示
- **AND** 商品只绑定一级或二级类目时 SHALL 取实际绑定路径中的最后一层
- **AND** 同一品牌下重复末级类目 SHALL 仅展示一次
- **AND** 类目集合项 SHOULD 包含 `categoryId` 与 `categoryName`
- **AND** 类目名称展示顺序 SHALL 使用类目后台排序或实现阶段明确的稳定兜底排序。

#### Scenario: 品牌 Logo、长文案和类目多行展示

- **WHEN** 品牌 Logo 缺失、图片加载失败、品牌名称较长、类目名称较长或类目数量较多
- **THEN** 品牌卡片 SHALL 展示品牌名称首字、品牌占位或统一占位图
- **AND** 品牌名称 SHALL 按设计策略截断或换行
- **AND** 类目汇总 SHALL 全部折行展示，不使用“等 N 类”折叠或隐藏后续类目
- **AND** 品牌卡片 SHALL NOT 出现破图、文字重叠、横向滚动、布局跳动或类目标签覆盖品牌信息。

#### Scenario: 品牌列表空状态

- **WHEN** 没有公开可展示品牌
- **THEN** 页面 SHALL 展示品牌化空状态
- **AND** 页面 SHALL 保留返回、重试或其他安全导航能力。

#### Scenario: 品牌无公开商品

- **WHEN** 品牌存在但没有公开商品
- **THEN** 页面 SHALL 展示 0 款商品或等价空态值
- **AND** 类目汇总区 SHALL 留空或展示产品确认的轻量空态
- **AND** 页面 SHALL NOT 让用户误解为接口加载失败。

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
