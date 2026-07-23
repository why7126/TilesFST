## MODIFIED Requirements

### Requirement: 品牌入口与相关推荐

SKU 详情页 SHALL 支持进入品牌主页、同系列商品和同品牌推荐，使用户可以继续浏览相关瓷砖；SKU 详情页品牌卡 SHALL 使用微信小程序品牌卡片组件承载单品牌展示、Logo fallback、入口提示和点击跳转。品牌主页入口 SHALL 由内容区品牌卡或等价“查看品牌主页”入口承载，底部固定操作栏 SHALL NOT 再提供重复的品牌按钮。

#### Scenario: 品牌入口

- **WHEN** 用户点击内容区品牌卡或“查看品牌主页”入口
- **THEN** 小程序 SHALL 使用 `brandId` 进入对应品牌主页或可用品牌承接页
- **AND** 目标不可用时 SHALL 安全降级到可返回提示或搜索筛选结果
- **AND** 底部固定操作栏 SHALL NOT 显示品牌按钮或保留品牌按钮点击热区。

#### Scenario: SKU 详情页使用品牌卡片组件

- **WHEN** SKU 详情页展示品牌卡
- **THEN** 页面 SHALL 使用微信小程序品牌卡片组件替换重复的内联品牌卡片结构
- **AND** 页面 SHALL 从 SKU 详情数据中提取品牌展示对象、`skuId` 和来源上下文传入组件
- **AND** 组件 SHALL 负责 Logo 缺失/失败、长品牌名、入口不可用和点击防重复等卡片级行为。

#### Scenario: 品牌入口 fallback

- **WHEN** SKU 详情页品牌卡缺少 `brand_entry_path` 但品牌名称可用
- **THEN** 小程序 SHALL fallback 到品牌关键词搜索页或等价品牌承接页
- **AND** 小程序 SHALL 对品牌名称进行 URL 编码
- **AND** 品牌名称不可用或入口不可用时 SHALL 提示“品牌内容暂不可查看”或等价文案并阻止无效跳转。

#### Scenario: 同系列推荐

- **WHEN** SKU 存在同系列其他公开 SKU
- **THEN** 页面 SHALL 展示同系列商品推荐
- **AND** 推荐 SHALL NOT 包含当前 SKU
- **AND** 用户点击推荐卡 SHALL 进入新的 SKU 详情页并重置滚动位置。

### Requirement: SKU 详情页视觉与可用性

SKU 详情页 SHALL 延续微信小程序首页 v6 深色企业轻奢风，并在主流小程序视口内保持可用。

#### Scenario: 深色视觉和大媒体区

- **WHEN** 用户查看 SKU 详情页
- **THEN** 页面 SHALL 使用与小程序首页 v6 一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 顶部媒体区 SHALL 采用大图布局
- **AND** 页面 SHALL NOT 使用电商红主按钮、纯白大背景或购物导向视觉。

#### Scenario: 移动视口可用

- **WHEN** 团队在 320 到 430px 逻辑宽度和常见底部安全区验收页面
- **THEN** 页面 SHALL 无横向滚动、内容重叠、按钮遮挡或关键文字截断
- **AND** 主要点击目标 SHALL 不小于 44x44px 或小程序等效尺寸。

#### Scenario: 底部操作栏

- **WHEN** SKU 详情页正常展示
- **THEN** 底部固定操作栏 SHALL 包含收藏和分享，且 SHALL NOT 包含品牌按钮
- **AND** 分享 SHALL 为主按钮
- **AND** 操作栏 SHALL 避让底部安全区
- **AND** 删除品牌按钮后 SHALL NOT 出现空白占位、错位、异常间距或残留点击热区。
