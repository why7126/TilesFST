## ADDED Requirements

### Requirement: 小程序全局自定义导航栏
系统 SHALL 提供小程序全局自定义导航栏能力，使首页和主要非首页页面共享一致的顶部导航契约。

#### Scenario: 首页保留品牌导航形态
- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 保留当前品牌 `brand-header` 或等价品牌导航形态
- **AND** 首页 SHALL NOT 显示左侧返回按钮
- **AND** 首页品牌 Logo、门店名称和品牌副文案 SHALL 保持稳定展示
- **AND** 首页搜索框、Banner 和入口区 SHALL 从导航栏下方开始展示且不被遮挡。

#### Scenario: 非首页展示返回导航形态
- **WHEN** 用户打开 search、tile-detail、category、product-list、favorites、certificates 或 store-info 页面
- **THEN** 页面 SHALL 使用同一导航模块的非首页形态
- **AND** 左侧 SHALL 显示返回按钮
- **AND** 中间或左中区域 MAY 展示页面标题、品牌短标题或等价页面识别信息
- **AND** 首页形态和非首页形态 SHALL 由页面类型区分，不得在首页误显示返回按钮。

### Requirement: 非首页返回行为
系统 SHALL 为小程序非首页导航栏提供稳定返回能力。

#### Scenario: 有页面栈时返回上一页
- **WHEN** 非首页页面栈存在上一页且用户点击返回按钮
- **THEN** 小程序 SHALL 返回上一页
- **AND** 返回过程 SHALL NOT 破坏当前页面的分享、刷新或错误重试能力。

#### Scenario: 无页面栈时兜底返回首页
- **WHEN** 用户从分享卡片或外部入口直达非首页且页面栈无上一页
- **AND** 用户点击返回按钮
- **THEN** 小程序 SHALL 进入明确兜底路径
- **AND** 兜底路径 SHOULD 为首页
- **AND** 页面 SHALL NOT 报错、白屏或停留在无反馈状态。

#### Scenario: 返回按钮触控区域可用
- **WHEN** 用户在 320 到 430 pt 宽度范围操作非首页导航栏
- **THEN** 返回按钮有效点击区域 SHALL 不小于 44x44 pt
- **AND** 返回按钮 SHALL NOT 与品牌 Logo、页面标题、微信原生胶囊或页面内容重叠。

### Requirement: 微信原生胶囊与状态栏避让
系统 SHALL 在所有覆盖页面避让微信原生分享 / 关闭胶囊和状态栏安全区。

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

### Requirement: 范围与数据边界
系统 SHALL 保持本 Change 为小程序导航 UI refinement，不扩展后台配置、API、数据库或业务页面范围。

#### Scenario: 不新增业务页面
- **WHEN** 实现本 Change
- **THEN** 系统 SHALL NOT 因导航栏新增 search、tile-detail、category、product-list、favorites、certificates 或 store-info 之外的新业务页面
- **AND** 底部 TabBar 文案、图标和路由 SHALL NOT 因本 Change 调整。

#### Scenario: 默认不新增接口与数据库
- **WHEN** 实现本 Change
- **THEN** 系统 SHALL NOT 默认新增 API、数据库表或字段
- **AND** 若实现阶段发现必须调整接口 contract，SHALL 同步 OpenAPI、Orval、docs 和测试
- **AND** 若实现阶段新增字段，SHALL 同步 SQLite/MySQL schema、数据库文档和测试。

#### Scenario: 媒体与 Logo 安全边界
- **WHEN** 导航栏展示 Logo 或图片资源
- **THEN** 小程序 SHALL 使用后端返回的安全 URL 或本地安全资源
- **AND** SHALL NOT 直连未授权对象存储或暴露 raw object key。
