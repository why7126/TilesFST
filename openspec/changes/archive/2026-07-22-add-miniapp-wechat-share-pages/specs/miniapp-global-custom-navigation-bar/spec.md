## ADDED Requirements

### Requirement: 分享直达导航兜底
支持微信分享的页面 SHALL 在分享直达场景继续遵守小程序自定义导航、微信原生胶囊避让、返回兜底和页面 offset 规则。

#### Scenario: 分享直达返回兜底
- **WHEN** 用户从微信朋友或朋友圈直达商品详情页、商品列表页或品牌详情页
- **AND** 页面栈没有上一页
- **THEN** 页面 SHALL 提供返回首页或等价安全入口
- **AND** 返回操作 SHALL NOT 报错、白屏或停留在无反馈状态。

#### Scenario: 分享直达胶囊避让
- **WHEN** 支持分享的页面从微信朋友或朋友圈直达
- **THEN** 自定义导航栏 SHALL 继续避让微信原生分享和关闭胶囊
- **AND** 标题、品牌信息、返回按钮、搜索入口或其他自定义元素 SHALL NOT 进入胶囊 reserve 区域
- **AND** 页面 SHALL NOT 在 WXML、WXSS 或自定义图片中手绘模拟微信分享按钮、关闭按钮或系统胶囊。

#### Scenario: 分享直达内容 offset
- **WHEN** 分享直达页面处于加载态、正常态、空状态、错误态或网络失败状态
- **THEN** 页面主体内容 SHALL 使用同一导航栏 offset
- **AND** 首屏内容、错误文案、重试入口和底部操作区域 SHALL NOT 被 fixed header、原生胶囊或底部安全区遮挡。
