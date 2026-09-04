## REMOVED Requirements

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

## ADDED Requirements

### Requirement: 小程序证据来源声明

小程序设备与 Network evidence 模板 SHALL 说明证据来源、执行方式、覆盖入口和证明边界；DevTools 预览、DevTools Network、静态校验或开发 API smoke 证据不得被表述为体验版、真机、线上或发布完成通过。

#### Scenario: DevTools 支撑当前范围验收
- **WHEN** 小程序 Change 记录 DevTools 截图、DevTools 预览或 DevTools Network evidence
- **THEN** evidence SHALL 可用于支撑其实际覆盖范围内的开发验收或问题排查结论
- **AND** 记录 SHALL 包含 `evidence_source`、`verification_boundary`、`evidence_ref`、`network_summary` 或等价信息
- **AND** 结论 SHALL 明确不等同于体验版、真机、线上或发布完成通过。

#### Scenario: 小程序入口或设备当前不可验证
- **WHEN** 体验版入口、真机设备、线上域名、线上接口或真实用户路径当前不可验证
- **THEN** 记录 SHALL 说明当前已有证据来源、不可验证原因、后续承接方式或 N/A 理由
- **AND** `production_only_pending` SHALL 仅作为历史兼容字段解释，不作为新流程推荐分类
- **AND** SHALL NOT 因当前不可获得证据而扩大通过结论。
