## ADDED Requirements

### Requirement: 媒体验收环境分层

媒体五联和媒体类 BUG 四联验收 SHALL 区分开发证据、体验版证据和生产证据，生产环境不可用时不得阻塞开发归档，但必须作为发布阶段或发布后待办记录。

#### Scenario: 开发阶段媒体 render 证据
- **WHEN** 媒体 BUG 或 Change 在开发阶段验证列表图、详情图、证书图、Logo、缩略图或受控 `/media` URL
- **THEN** 验收记录 MAY 使用开发 API smoke、对象存储审计摘要、DevTools 截图或 DevTools Network evidence
- **AND** 该结论 SHALL 标记为开发阶段通过或开发证据充分
- **AND** SHALL NOT 写作生产对象、生产域名、体验版或真机 Network 已通过。

#### Scenario: 生产媒体证据后置
- **WHEN** 生产对象、生产接口、生产 no-fallback、生产缩略图回填或生产真实用户路径只有发布或生产维护后才能验证
- **THEN** 开发阶段验收 SHALL 将该缺口记录为 `production_only_pending` 或发布阶段待办
- **AND** SHALL 记录重试条件、责任环境和后续承接命令
- **AND** SHALL NOT 将该缺口作为开发归档 blocker，除非 Change 目标明确是生产维护执行。

#### Scenario: 生产维护或生产发布强门禁
- **WHEN** Change 目标明确为生产维护执行，或发布对象声明 `release_target.environment=production`
- **THEN** 生产对象、生产 URL、生产 no-fallback 媒体、备份、dry-run/apply 和二次审计证据 SHALL 按范围参与强门禁
- **AND** 缺失时 SHALL 标记为 `blocked`、`environment_unavailable` 或 `publish_evidence_missing`。
