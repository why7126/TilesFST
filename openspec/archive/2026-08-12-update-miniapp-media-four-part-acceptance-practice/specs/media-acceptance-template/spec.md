## ADDED Requirements

### Requirement: 小程序媒体四联最佳实践

系统 SHALL 为小程序媒体性能相关需求、BUG、OpenSpec Change、Sprint 验收和发布检查提供小程序媒体四联最佳实践引用。该实践 SHALL 覆盖 `key`、`object`、`URL`、`render` 四个维度，并 SHALL 明确对象存在、`.thumb` URL 存在、接口测试通过或只读审计摘要均不能单独证明小程序媒体性能验收通过。该实践 SHALL 不替代媒体五联验收模板或媒体类 BUG 四联验收模板，而是补充小程序媒体场景的 Network evidence、真实轻量资源命中和端侧 render 证据要求。

#### Scenario: 四联证据链完整

- **WHEN** 团队验收小程序媒体性能相关需求或缺陷
- **THEN** 验收记录 SHALL 包含 `key`、`object`、`URL`、`render` 四个维度
- **AND** `key` SHALL 记录业务资源、媒体类型、脱敏 key 摘要、标准前缀、原图 / 缩略图 / 视频 / poster 关系
- **AND** `object` SHALL 记录 object 存在性、MIME、大小、扩展名、权限边界、缩略图收益或无收益原因
- **AND** `URL` SHALL 记录 URL 类型、入口接口或页面、HTTP 状态、业务错误码、受控 `/media` 访问、resolved / fallback 结论和缓存相关证据
- **AND** `render` SHALL 记录小程序页面路径、组件、DevTools / 真机 / 体验版 evidence、展示 / 预览 / 播放 / 占位 / 失败态结论。

#### Scenario: 非通过状态不得省略

- **WHEN** 任一小程序媒体四联维度为 `fail`、`n/a` 或 `blocked`
- **THEN** 记录 SHALL 包含原因、影响判断和后续处理方式
- **AND** `blocked` SHALL NOT 被视为通过
- **AND** 任一 `fail` 项 SHALL 包含实际结果、期望结果、复现入口、影响范围和排查线索。

#### Scenario: 自动化证据不替代 render

- **WHEN** 测试 helper、接口测试、静态测试或只读审计通过
- **THEN** 验收记录 MAY 引用其摘要作为辅助证据
- **AND** SHALL NOT 将其自动表述为小程序 render evidence 已通过
- **AND** 小程序受影响页面仍 SHALL 记录 DevTools、真机、体验版或明确的 blocked / follow-up 证据。
