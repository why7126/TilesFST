## ADDED Requirements

### Requirement: 发布目标环境分离
产品版本发布管理 SHALL 区分开发环境发布确认与生产发布确认，并根据目标环境选择发布门禁。

#### Scenario: 开发环境发布确认不受生产证据阻断
- **WHEN** 发布对象声明 `release_target.environment=development`
- **THEN** 发布确认 SHALL 表示开发环境部署或开发交付确认
- **AND** 生产真实 env、生产 MySQL 或对象存储备份、生产公开 API、生产 no-fallback 媒体证据和生产 smoke SHALL NOT 阻断该开发环境发布确认
- **AND** 这些生产事项 SHALL 作为后续生产发布待办、known issue 或 production release blocker 记录。

#### Scenario: 生产发布确认使用生产门禁
- **WHEN** 发布对象声明 `release_target.environment=production`
- **THEN** 发布确认 SHALL 要求生产部署相关证据
- **AND** 生产 env 显式版本、生产备份、生产 smoke、生产公开 API 和生产媒体证据 SHALL 按发布范围参与门禁或记录明确不适用理由。

#### Scenario: 发布对象记录目标环境
- **WHEN** 创建或更新发布对象
- **THEN** 发布对象 SHOULD 包含 `release_target.environment`、`release_target.deployment_scope`、`release_target.production_release_required` 和 `release_target.rationale`
- **AND** `environment` 与 `deployment_scope` SHALL 使用 `development` 或 `production`。
