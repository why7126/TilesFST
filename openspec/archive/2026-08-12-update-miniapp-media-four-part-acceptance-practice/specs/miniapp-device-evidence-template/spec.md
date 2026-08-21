## ADDED Requirements

### Requirement: 小程序媒体 Network evidence

系统 SHALL 在小程序设备 evidence 模板中支持媒体资源 Network evidence，用于记录图片、视频、Logo、证书图片、缩略图、封面图和受控 `/media` URL 的真实请求链路。媒体 Network evidence SHALL 与静态测试、接口 smoke、DevTools 预览和真机 render evidence 区分。

#### Scenario: 媒体 Network 字段完整

- **WHEN** 团队记录小程序媒体资源 Network evidence
- **THEN** evidence SHALL 记录页面路径、验证场景、请求域名、HTTP 状态、业务响应状态、资源类型、资源大小或耗时摘要
- **AND** SHALL 记录媒体 URL 类型、受控 `/media` 访问方式、resolved / fallback 结论或等价观测摘要
- **AND** SHALL 记录该 evidence 来源为 `network_devtools`、`network_trial`、`real_device` 或明确的替代来源
- **AND** DevTools Network 结论 SHALL 明确不等同于体验版或真机网络验收。

#### Scenario: 缺少体验版或真机证据时不能写通过

- **WHEN** 小程序媒体性能变更影响真实用户体感但缺少体验版或真机 Network evidence
- **THEN** evidence SHALL 使用 `required`、`blocked` 或 `follow_up` 表达
- **AND** SHALL 记录阻塞原因、责任环境、重试条件和发布前承接方式
- **AND** SHALL NOT 写作体验版或真机媒体 Network 验收已通过。

#### Scenario: 媒体 Network evidence 安全

- **WHEN** 团队记录小程序媒体 Network evidence
- **THEN** evidence SHALL NOT 包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据、未脱敏 object key 全量值或完整网络日志
- **AND** 截图、录屏或报告包含敏感信息时 SHALL 先脱敏或记录不可公开原因。
