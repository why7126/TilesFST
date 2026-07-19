## ADDED Requirements

### Requirement: 首页品牌自定义导航栏
小程序首页 SHALL 将搜索框上方的品牌展示区域定义为首页品牌自定义导航栏，并在右侧使用微信小程序原生分享和关闭能力。

#### Scenario: 自定义导航栏展示品牌元素
- **WHEN** 用户打开微信小程序首页
- **THEN** 首页搜索框上方 SHALL 展示品牌自定义导航栏
- **AND** 导航栏 SHALL 包含品牌 Logo、门店名称和品牌副文案
- **AND** 品牌元素 SHOULD 对应当前首页 `brand-header` 中的 `store-logo`、`store-name`、`store-subtitle` 或等价元素
- **AND** 当 Logo、门店名称或副文案缺失时，页面 SHALL 使用安全本地 Logo 或“菲尚特瓷砖馆” / “专业选砖 · 品质生活”等品牌兜底。

#### Scenario: 门店信息入口不属于自定义导航栏
- **WHEN** 团队验收首页品牌自定义导航栏
- **THEN** 导航栏 SHALL NOT 包含 `store-link`、"门店信息"文案、门店信息箭头、多门店切换暗示或门店详情跳转
- **AND** 导航栏整体 SHALL NOT 默认绑定 `openStoreInfo`
- **AND** 如果首页仍需门店信息入口，该入口 SHALL 位于自定义导航栏之外或由后续需求定义。

#### Scenario: 右侧使用原生分享和关闭能力
- **WHEN** 首页展示品牌自定义导航栏
- **THEN** 导航栏右侧 SHALL 保留微信小程序原生分享和关闭两个操作的位置
- **AND** 页面 SHALL NOT 使用 WXML、WXSS 或自定义图片手绘模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件
- **AND** 分享 SHALL 使用微信小程序标准分享能力，例如 `onShareAppMessage` 或平台菜单能力
- **AND** 关闭 SHALL 使用微信小程序原生关闭能力。

#### Scenario: 搜索框保持在导航栏下方
- **WHEN** 用户查看首页顶部区域
- **THEN** 搜索框 SHALL 位于自定义导航栏下方
- **AND** 搜索框 SHALL NOT 被并入自定义导航栏内部
- **AND** 首页 SHALL NOT 因导航栏调整出现第二个同等主级搜索入口
- **AND** 搜索框点击后 SHALL 进入现有搜索页或搜索组件能力。

#### Scenario: 自定义导航栏与 REQ-0043 首页保持一致
- **WHEN** 团队验收 REQ-0042 实现
- **THEN** 首页 SHALL 继续使用 REQ-0043 的深色视觉基准
- **AND** Header、搜索、Banner、四入口、新品推荐、热销推荐、全部产品瀑布流和底部 TabBar SHALL NOT 因导航栏调整被移除、遮挡或恢复到旧结构
- **AND** 首页 SHALL NOT 恢复 REQ-0041 早期暖白背景、旧五入口或“我的”Tab 目标。

#### Scenario: 导航栏移动端安全区与状态稳定
- **WHEN** 团队在 320 到 430 pt 宽度范围、加载态、网络异常态和返回首页场景验收
- **THEN** 品牌 Logo、门店名称、副文案 SHALL NOT 与右侧原生分享 / 关闭区域重叠
- **AND** 页面 SHALL NOT 出现页面级横向滚动、导航栏高度异常、搜索框挤压、明显闪烁或品牌文案不可读
- **AND** 从搜索页、商品详情页、分类/找砖、收藏/证书占位页或分享返回首页后，导航栏 SHALL 保持稳定展示。

#### Scenario: 默认不新增接口和数据库
- **WHEN** 实现首页品牌自定义导航栏
- **THEN** 系统 SHALL 默认复用 REQ-0043 首页已有 store / brand 数据
- **AND** SHALL NOT 新增独立导航栏 API、数据库表、字段或后台配置
- **AND** 如果后续实现需要新增或调整 API contract，Change SHALL 同步 OpenAPI、Orval、docs 和测试
- **AND** 如果后续实现需要新增数据库字段，Change SHALL 同步 SQLite/MySQL 文档、schema / migration 和测试。
