## REMOVED Requirements

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

## ADDED Requirements

### Requirement: 媒体验收证据来源声明

媒体五联和媒体类 BUG 四联验收 SHALL 说明媒体 evidence 的来源、覆盖对象和证明边界；开发工具、对象存储审计摘要、静态检查或本地 smoke 证据不得被表述为体验版、真机、线上或发布完成通过。

#### Scenario: 媒体 render 证据说明来源
- **WHEN** 媒体 BUG 或 Change 验证列表图、详情图、证书图、Logo、缩略图或受控 `/media` URL
- **THEN** 验收记录 MAY 使用开发 API smoke、对象存储审计摘要、DevTools 截图或 DevTools Network evidence
- **AND** 验收记录 SHALL 说明 `evidence_source`、`verification_boundary`、`evidence_ref` 或等价信息
- **AND** SHALL NOT 写作生产对象、生产域名、体验版或真机 Network 已通过。

#### Scenario: 当前不可验证媒体链路
- **WHEN** 线上对象、线上接口、线上 no-fallback、缩略图回填或真实用户路径当前不可验证
- **THEN** 验收记录 SHALL 说明当前已有证据来源、不可验证原因、后续承接方式或 N/A 理由
- **AND** `production_only_pending` SHALL 仅作为历史兼容字段解释，不作为新流程推荐分类
- **AND** SHALL NOT 将当前不可获得的证据写作已经通过。

#### Scenario: 发布确认消费媒体证据边界
- **WHEN** release 或 publish 材料引用媒体 evidence
- **THEN** 发布材料 SHALL 消费已记录的证据来源和证明边界
- **AND** 缺失的公开访问、对象回填或真实用户路径 evidence SHALL 按 release validator 的现有 blocker 分类处理，不得恢复发布目标分层门禁。
