## ADDED Requirements

### Requirement: 小程序分享设备 evidence
小程序分享能力验收 SHALL 记录 DevTools、真机、静态测试、blocked 或 follow-up 结论，明确分享、返回、原生胶囊和运行入口同步的证据边界。

#### Scenario: 分享矩阵 evidence
- **WHEN** 团队验收首页、商品详情页、商品列表页和品牌详情页的微信分享
- **THEN** evidence SHALL 覆盖微信朋友分享和朋友圈分享
- **AND** evidence SHALL 记录页面路径、关键 query 参数、分享渠道、视口或设备来源和结论
- **AND** evidence SHALL 覆盖 DevTools 320、375、430 pt 或等价静态视口检查。

#### Scenario: 真机不可用时标记剩余风险
- **WHEN** 分享、返回、原生胶囊或页面滚动涉及真机体验但无法执行真机验收
- **THEN** evidence SHALL 标记 `blocked` 或 `follow_up`
- **AND** 验收报告、Change trace 或 release note SHALL NOT 写作真机通过
- **AND** remaining risk SHALL 说明缺少真机结论的影响和后续承接方式。

#### Scenario: 运行入口同步 evidence
- **WHEN** 小程序页面同时存在维护源码 `.ts` 与实际运行 `.js`
- **THEN** 静态测试或等价验收 SHALL 确认四个目标页面的运行 `.js` 包含对应分享配置
- **AND** `.ts` 包含 `onShareAppMessage` 或 `onShareTimeline` 但 `.js` 缺失对应逻辑时 SHALL 视为验收失败
- **AND** 静态测试通过 SHALL NOT 被表述为 DevTools 渲染通过或真机通过。
