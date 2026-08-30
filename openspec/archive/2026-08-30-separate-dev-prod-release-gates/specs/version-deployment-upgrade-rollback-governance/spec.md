## ADDED Requirements

### Requirement: 升级计划目标环境分离
版本部署升级与回滚治理 SHALL 支持开发环境和生产环境两类升级计划目标，并避免把生产实施门禁误用为开发部署门禁。

#### Scenario: 开发环境升级计划
- **WHEN** 系统生成 `deployment_target=development` 的升级计划
- **THEN** 计划 SHALL 表达开发部署、开发验证和开发回滚边界
- **AND** 生产真实 env、生产 MySQL 或对象存储备份、生产 smoke 和生产公开证据 SHALL NOT 作为开发计划 blocker
- **AND** 生产实施要求 MAY 作为后续生产发布提醒记录。

#### Scenario: 生产环境升级计划
- **WHEN** 系统生成 `deployment_target=production` 的升级计划
- **THEN** 计划 SHALL 保留生产 env、备份、MySQL、对象存储、smoke 和回滚证据要求
- **AND** 不得凭开发环境部署计划宣称生产升级路径已验证。

#### Scenario: 常规发布默认升级计划跟随发布目标
- **WHEN** 正常发布需要生成默认升级计划
- **THEN** `fresh -> <to-version>` 和 `<previous-release-version> -> <to-version>` 的默认计划 SHALL 使用发布对象声明的目标环境
- **AND** 若后续单独生产发布，生产发布 SHALL 生成或校验生产目标升级计划。
