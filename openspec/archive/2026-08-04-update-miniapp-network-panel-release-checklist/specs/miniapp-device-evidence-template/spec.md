## ADDED Requirements

### Requirement: 小程序 Network evidence
系统 SHALL 在小程序 evidence 模板中支持 Network evidence，用于记录 DevTools 网络面板和体验版网络链路验证，且 SHALL 与静态测试、生产接口 smoke、DevTools 预览和真机 evidence 区分。

#### Scenario: Network evidence 来源可区分
- **WHEN** 团队记录小程序 Network evidence
- **THEN** evidence source SHALL 支持 `network_devtools` 与 `network_trial`
- **AND** `network_devtools` SHALL 表示微信开发者工具网络面板验证
- **AND** `network_trial` SHALL 表示体验版或等价手机体验入口网络链路验证
- **AND** 两者 SHALL NOT 被静态测试或生产接口 smoke 自动标记为 `passed`。

#### Scenario: DevTools Network 字段完整
- **WHEN** 团队记录 `network_devtools` evidence
- **THEN** evidence SHALL 记录微信开发者工具版本或可识别版本摘要、小程序基础库版本、运行策略、`urlCheck` 状态、页面路径和关键 query
- **AND** SHALL 记录请求域名、关键 API HTTP 状态、业务响应状态、图片/视频/证书/静态资源加载结论
- **AND** 结论 SHALL 明确 DevTools Network 不等同于体验版或真机网络验收。

#### Scenario: 体验版 Network 字段完整
- **WHEN** 团队记录 `network_trial` evidence
- **THEN** evidence SHALL 记录体验版来源、最新版本确认方式、重新扫码或等价入口确认、页面路径和验证场景
- **AND** SHALL 记录体验版是否请求生产 API 域名
- **AND** SHALL 记录首页、至少一个列表页、至少一个详情或媒体资源页面的接口和资源加载结论
- **AND** 若体验版 Network 工具不可用，evidence SHALL 记录替代观察方式、阻塞原因、剩余风险和后续承接方式。

#### Scenario: Network evidence 状态与安全
- **WHEN** Network evidence 未完成、失败或不可用
- **THEN** 状态 SHALL 使用 `required`、`failed`、`blocked`、`not_applicable` 或 `follow_up` 表达
- **AND** 缺少体验版 Network evidence 时 SHALL NOT 写作 `passed`
- **AND** evidence SHALL NOT 记录 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据、未脱敏隐私或完整网络日志。
