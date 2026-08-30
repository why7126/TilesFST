## ADDED Requirements

### Requirement: 生产证据后置承接

产品发布管理 SHALL 承接开发阶段留下的 `production_only_pending` 证据缺口，并在生产发布时重新判定阻塞状态。

#### Scenario: 开发阶段遗留生产待办
- **WHEN** REQ、BUG、Change 或 Sprint 验收记录存在 `production_only_pending`
- **THEN** 开发环境发布或开发归档 SHALL 可继续完成
- **AND** 发布状态面板 SHALL 将这些事项显示为生产发布待办或后续生产确认项
- **AND** SHALL NOT 将其混入开发阶段失败项。

#### Scenario: 生产发布重新收紧门禁
- **WHEN** 发布对象声明 `release_target.environment=production`
- **THEN** 生产证据待办 SHALL 重新按发布范围归类为 `publish_evidence_missing`、`environment_unavailable`、`schema_invalid` 或明确 N/A
- **AND** 缺少生产 env、备份、公开 API、生产 no-fallback 媒体、生产 smoke 或回滚准备证据时 SHALL 阻塞生产发布，除非该项对本次发布范围不适用。
