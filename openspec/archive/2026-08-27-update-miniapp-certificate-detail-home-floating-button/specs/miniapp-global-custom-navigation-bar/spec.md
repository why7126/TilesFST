## ADDED Requirements

### Requirement: 证书详情页返回首页覆盖

系统 SHALL 将小程序证书详情页纳入非首页返回首页悬浮按钮覆盖范围。证书详情页 SHALL 继续遵守小程序自定义导航 best-practice 的分享直达、返回兜底、页面 offset、原生胶囊避让和设备 evidence 规则，并 SHALL 复用 `home-floating-button` 组件作为明确的首页入口。

#### Scenario: 证书详情页纳入覆盖范围

- **WHEN** 团队实现或验收非首页返回首页悬浮按钮覆盖页面
- **THEN** 覆盖范围 SHALL 包含 `pages/certificate-detail/index`
- **AND** 证书详情页 SHALL 与商品详情页、品牌详情页、商品列表页等深层页面使用一致的首页入口语义。

#### Scenario: 证书详情页分享直达兜底

- **WHEN** 用户从微信分享卡片、扫码或外部入口直达证书详情页
- **THEN** 自定义导航左上返回 SHALL 在无页面栈时兜底到首页或等价安全入口
- **AND** 返回首页悬浮按钮 SHALL 可直接进入首页
- **AND** 页面 SHALL NOT 报错、白屏、无反馈或停留在不可恢复状态。

#### Scenario: 证书详情页不扩展全局组件契约

- **WHEN** 实现证书详情页返回首页覆盖
- **THEN** 系统 SHALL NOT 修改 `home-floating-button` 的全局视觉、offset 枚举、首页路由、导航锁或失败提示契约
- **AND** 系统 SHALL NOT 因该覆盖新增 API、数据库字段、后台配置、对象存储策略、埋点报表或 Web 端能力。
