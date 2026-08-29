## MODIFIED Requirements

### Requirement: 微信小程序首页首屏
系统 SHALL 提供原生微信小程序首页，用于面向终端客户展示菲尚特品牌、高权重搜索入口、Banner、快捷业务入口、新品推荐、热销推荐、全部产品瀑布流和底部 TabBar，并 SHALL 为真实 DevTools / 真机设备验收保留可复核 evidence。搜索入口 SHALL 成为首页首屏主要找砖入口，视觉权重高于普通快捷入口但不得遮挡 Banner、快捷入口或推荐模块。

#### Scenario: 首页首屏展示核心模块
- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 展示品牌 Logo、门店名称、品牌副文案、高权重搜索入口、Banner、四个快捷业务入口和至少一个推荐模块
- **AND** 页面 SHALL 使用深色品牌视觉，页面背景、卡片/搜索框/模块底色、品牌金、主文字和辅助文字 SHALL 与 REQ-0043 验收标准一致
- **AND** 搜索入口 SHALL 支持用户从首屏进入 `/pages/search/index`
- **AND** 页面 SHALL NOT 展示新增、编辑、上下架、库存、订单或客户管理入口。

#### Scenario: 首页搜索入口来源参数
- **WHEN** 用户点击首页搜索入口
- **THEN** 小程序 SHALL 跳转 `/pages/search/index` 或等价完整搜索页
- **AND** 跳转参数 SHALL 携带 `sourcePage=home` 和 `scope=all` 或等价来源信息
- **AND** 搜索入口文案 SHALL 覆盖瓷砖名称、商品编号、品牌、规格等高频搜索意图。

#### Scenario: 首页移动视口可用
- **WHEN** 团队在 375x812、390x844 和 320 到 430 pt 宽度范围验收首页
- **THEN** 页面 SHALL 无页面级横向滚动、明显内容截断、控件重叠或底部 TabBar 遮挡
- **AND** 所有主要点击区域 SHALL 不小于 44x44 pt
- **AND** 搜索入口 SHALL NOT 遮挡自定义导航栏、Banner、快捷入口、新品推荐、热销推荐或全部产品区。
