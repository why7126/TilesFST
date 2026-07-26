## MODIFIED Requirements

### Requirement: 微信小程序首页首屏
系统 SHALL 提供原生微信小程序首页，用于面向终端客户展示菲尚特品牌、搜索入口、Banner、快捷业务入口、新品推荐、热销推荐、全部产品瀑布流和底部 TabBar，并 SHALL 为真实 DevTools / 真机设备验收保留可复核 evidence。

#### Scenario: 首页首屏展示核心模块
- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 展示品牌 Logo、门店名称、品牌副文案、搜索入口、Banner、四个快捷业务入口和至少一个推荐模块
- **AND** 页面 SHALL 使用深色品牌视觉，页面背景、卡片/搜索框/模块底色、品牌金、主文字和辅助文字 SHALL 与 REQ-0043 验收标准一致
- **AND** 页面 SHALL NOT 展示新增、编辑、上下架、库存、订单或客户管理入口。

#### Scenario: 首页移动视口可用
- **WHEN** 团队在 375x812、390x844 和 320 到 430 pt 宽度范围验收首页
- **THEN** 页面 SHALL 无页面级横向滚动、明显内容截断、控件重叠或底部 TabBar 遮挡
- **AND** 所有主要点击区域 SHALL 不小于 44x44 pt。

#### Scenario: 首页运行入口执行业务逻辑
- **WHEN** 微信开发者工具预览 `pages/index/index`
- **THEN** 实际运行脚本 SHALL 初始化首页状态并触发首页聚合数据或全部产品首批数据加载
- **AND** 实际运行脚本 SHALL NOT 保持空模板 `Page({ data: {}, onLoad() {} })`
- **AND** 首页动态模块 SHALL 基于运行时数据或模块级降级策略展示。

#### Scenario: 首页真实小程序导航环境
- **WHEN** 首页使用微信原生导航栏
- **THEN** 页面内容 SHALL 从品牌 Header 或搜索入口开始，并避免与原生标题重复
- **AND** Header SHALL NOT 模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件。

#### Scenario: BUG-0068 首页设备验收 evidence 闭环
- **WHEN** 团队验收 `BUG-0068-miniapp-home-device-acceptance-followup`
- **THEN** 验收材料 SHALL 记录微信开发者工具或真机 evidence，至少包含页面路径、设备或模拟器、逻辑宽度、验收时间、截图/录屏/人工摘要和结论
- **AND** 验收宽度 SHALL 覆盖 320、375、390、430 pt 及 320-430 pt 常见宽度
- **AND** 首页品牌导航、搜索入口、Banner、快捷入口、新品推荐、热销推荐、全部产品区域和底部 TabBar SHALL 在 evidence 中可见或有明确降级说明
- **AND** 静态测试通过 SHALL NOT 被表述为 DevTools 或真机通过。

#### Scenario: BUG-0068 首页降级状态设备验收
- **WHEN** Banner 为空、商品为空、图片加载失败或首页请求失败
- **THEN** 首页 SHALL 展示品牌化降级、空状态或错误提示
- **AND** 降级状态 SHALL 继续满足 320-430 pt、无横向滚动、主要点击目标可用和底部 TabBar 不遮挡要求
- **AND** 错误诊断信息 SHALL NOT 泄露敏感路径、密钥、后台字段、Authorization header 或 Cookie。
