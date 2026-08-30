## ADDED Requirements

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
