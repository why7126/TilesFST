## MODIFIED Requirements

### Requirement: 微信原生胶囊与状态栏避让
系统 SHALL 在所有覆盖页面避让微信原生分享 / 关闭胶囊和状态栏安全区，并 SHALL 在小程序首页设备验收中补齐可复核 evidence。

#### Scenario: 右侧避让微信原生胶囊
- **WHEN** 页面渲染自定义导航栏
- **THEN** 导航栏右侧 SHALL 为微信原生分享 / 关闭胶囊预留不可占用区域
- **AND** 品牌信息、页面标题、返回按钮、搜索入口或其他自定义元素 SHALL NOT 进入该区域。

#### Scenario: 禁止手绘系统胶囊
- **WHEN** 团队实现或验收自定义导航栏
- **THEN** 页面 SHALL NOT 在 WXML / WXSS 中自绘模拟微信分享按钮、关闭按钮或系统胶囊
- **AND** 支持分享的页面 SHALL 保留微信小程序原生分享能力。

#### Scenario: 状态栏高度动态适配
- **WHEN** 页面在不同机型、不同状态栏高度或 320 到 430 pt 宽度范围渲染
- **THEN** 导航栏 SHALL 使用微信小程序可获得的系统信息、菜单按钮信息或等价安全区信息计算布局
- **AND** 页面 SHALL NOT 依赖单一机型硬编码高度完成验收。

#### Scenario: BUG-0068 首页胶囊与状态栏 evidence 闭环
- **WHEN** 团队验收首页品牌自定义导航栏
- **THEN** evidence SHALL 覆盖 320、375、390、430 pt 及 320-430 pt 常见宽度下的微信原生胶囊、状态栏和品牌导航布局
- **AND** 品牌 Logo、门店名称、品牌副文案、返回区域、搜索入口或其他自定义元素 SHALL NOT 进入原生胶囊区域
- **AND** 胶囊区域 SHOULD 在截图中可辨认且未被页面内容覆盖
- **AND** 若真机无法验收，材料 SHALL 标记 `blocked` 或 `follow_up`，不得写作真机通过。

### Requirement: fixed header 内容避让
系统 SHALL 确保所有覆盖页面的主体内容、状态页和滚动区域不被 fixed header 遮挡。

#### Scenario: 首屏内容避让导航栏
- **WHEN** search、tile-detail、category、product-list、favorites、certificates 或 store-info 页面加载
- **THEN** 页面主体内容 SHALL 从导航栏下方开始展示
- **AND** 搜索框、媒体轮播、分类列表、商品列表、收藏列表、证书列表和门店信息首屏内容 SHALL NOT 被 fixed header 遮挡。

#### Scenario: 状态页与下拉刷新避让导航栏
- **WHEN** 页面处于加载态、空状态、错误态、骨架屏或下拉刷新状态
- **THEN** 对应内容 SHALL 使用同一导航栏 offset
- **AND** SHALL NOT 被 fixed header 遮挡或与导航栏重叠。

#### Scenario: 统一顶部 offset 策略
- **WHEN** 团队验收页面布局实现
- **THEN** 覆盖页面 SHOULD 使用统一变量、工具函数或 layout class 承接导航栏高度
- **AND** 页面 SHALL NOT 散落互相冲突的顶部 padding 硬编码。

#### Scenario: BUG-0068 首页 fixed header 与底部 TabBar evidence 闭环
- **WHEN** 团队检查首页首屏、滚动中段和页面底部
- **THEN** fixed header SHALL 通过 spacer、offset 或等价方式为内容让位
- **AND** 底部 TabBar 与安全区 SHALL 不遮挡商品卡片、加载状态、空状态或主要点击目标
- **AND** 主要点击目标 SHOULD 不小于 44x44 pt
- **AND** evidence SHALL 明确记录结论、截图/录屏/人工摘要和剩余风险。
