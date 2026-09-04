## REMOVED Requirements

### Requirement: 环境证据脚本测试覆盖

测试治理 SHALL 覆盖环境分层 evidence 强脚本门禁，确保校验规则、CLI 输出和发布集成不会静默回退。

#### Scenario: 脚本聚焦测试覆盖误判
- **WHEN** 团队修改环境证据校验脚本或接入点
- **THEN** 测试 SHALL 覆盖开发证据冒充生产通过、DevTools 冒充体验版或真机通过、`production_only_pending` 在生产发布目标下阻断，以及开发目标下保留后置项不阻断
- **AND** 测试 SHALL 使用临时目录和脱敏样例，不读取真实生产数据或真实凭据。

#### Scenario: 发布与归档集成测试覆盖
- **WHEN** 环境证据脚本被接入 release 或 archive validator
- **THEN** 聚焦测试 SHALL 验证 validator 能消费脚本结果并返回对应错误分类
- **AND** 不得要求 Docker Compose、真实小程序体验版或生产环境才能运行脚本单测。

## ADDED Requirements

### Requirement: 证据来源诊断测试覆盖

测试治理 SHALL 覆盖证据来源诊断脚本和显式接入点，确保脚本仍能发现证据来源扩大表述，同时默认 release、opsx archive 和 sprint archive 链路不会静默恢复诊断阻断门禁。

#### Scenario: 脚本聚焦测试覆盖误判
- **WHEN** 团队修改证据来源诊断脚本或诊断规则
- **THEN** 测试 SHALL 覆盖开发证据冒充体验版、真机、线上或发布完成通过的误判
- **AND** 测试 MAY 覆盖 `production_only_pending` 历史兼容字段的诊断行为
- **AND** 测试 SHALL 使用临时目录和脱敏样例，不读取真实生产数据或真实凭据。

#### Scenario: 默认链路不恢复诊断阻断
- **WHEN** release、opsx archive 或 sprint archive 默认 validator 被修改
- **THEN** 聚焦测试 SHALL 验证默认 validator 不会因证据来源诊断脚本 findings 自动失败
- **AND** 只有显式接入诊断结果的独立门禁 MAY 将诊断 findings 转化为阻断项。
