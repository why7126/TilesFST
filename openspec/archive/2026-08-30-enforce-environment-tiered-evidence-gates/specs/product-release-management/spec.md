## ADDED Requirements

### Requirement: 生产发布环境证据强门禁

发布状态与发布确认 SHALL 在生产目标下强制重新判定开发阶段遗留的 `production_only_pending`，不得让开发证据自动升级为生产发布证据。

#### Scenario: Development target 保留生产后置项
- **WHEN** release status 或 release validation 的目标为 `development`
- **THEN** 环境证据脚本发现 `production_only_pending` SHALL 作为 production follow-up 或非阻塞项输出
- **AND** 仅当文本把开发证据写作生产通过、体验版通过或真机通过时才作为 blocker。

#### Scenario: Production target 阻断未重判的后置项
- **WHEN** release status 或 release publish 的目标为 `production`
- **THEN** 仍残留的 `production_only_pending` SHALL 被视为未重新判定的生产证据缺口
- **AND** validation SHALL 将其归类为 `publish_evidence_missing` 或 `environment_unavailable`
- **AND** 发布确认 SHALL 阻断，直到该项被生产 evidence、明确 N/A 或具体 blocker 替代。
