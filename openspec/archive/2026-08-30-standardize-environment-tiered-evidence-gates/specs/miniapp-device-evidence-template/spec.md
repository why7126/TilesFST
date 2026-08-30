## ADDED Requirements

### Requirement: 小程序环境分层 evidence

小程序设备与 Network evidence 模板 SHALL 支持开发、体验版、生产发布和发布后跟进的目标环境字段，并按阶段确定证据缺口是否阻塞当前命令。

#### Scenario: DevTools 支撑开发验收但不等同体验版或生产
- **WHEN** 小程序 Change 在开发阶段记录 DevTools 截图、DevTools 预览或 DevTools Network evidence
- **THEN** evidence SHALL 可用于支撑 `dev_acceptance` 或开发归档结论
- **AND** `target_environment` SHALL 记录为 `development`
- **AND** 结论 SHALL 明确不等同于体验版、真机或生产发布通过。

#### Scenario: 体验版或生产入口不可用时后置
- **WHEN** 当前命令处于开发归档，且体验版入口、真机、生产域名或生产接口只有发布后才能验证
- **THEN** 相关 evidence 缺口 SHALL 标记为 `production_only_pending`、`follow_up` 或 `not_applicable_for_development`
- **AND** SHALL 记录重试条件、后续承接阶段和剩余风险
- **AND** SHALL NOT 因此阻塞开发阶段 `opsx.archive`。

#### Scenario: 生产发布重新校验小程序证据
- **WHEN** 发布目标为 `production`，且范围包含小程序页面、Network 或媒体资源链路
- **THEN** 发布阶段 SHALL 单独记录生产或生产等价入口 evidence
- **AND** 缺少生产域名、体验版或真机 Network 证据时 SHALL 阻塞生产发布，除非记录明确 N/A 理由。
