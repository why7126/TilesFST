## ADDED Requirements

### Requirement: 测试证据与环境证据边界

测试治理 SHALL 区分自动化测试、开发环境 smoke、DevTools evidence、体验版 evidence 和生产 evidence 的证明范围。

#### Scenario: 自动化测试不得冒充生产验证
- **WHEN** pytest、Vitest、静态校验、开发 API smoke 或 DevTools 验证通过
- **THEN** 测试结果 MAY 作为开发阶段验收证据
- **AND** SHALL 记录覆盖边界和目标环境
- **AND** SHALL NOT 被表述为生产环境、体验版、真机或生产发布验证已通过。

#### Scenario: 生产环境不可用时记录后置
- **WHEN** 开发阶段无法访问生产环境、生产数据、生产对象存储、体验版入口或真机设备
- **THEN** 测试计划或验收记录 SHALL 将缺失证据标记为 `production_only_pending`、`environment_unavailable`、`follow_up` 或 `not_applicable_for_development`
- **AND** SHALL 说明该缺口阻塞的后续阶段，而不是默认阻塞开发归档。
