## ADDED Requirements

### Requirement: Runbook 必须说明媒体维护进度输出

Runbook MUST 说明媒体维护任务可选进度输出的使用方式、输出通道边界和生产日志采集注意事项。

#### Scenario: 记录进度参数用法

- **WHEN** Runbook 描述 `backfill-image-variants`、`backfill-brand-certificate-thumbnails` 或 `media-drift-reconcile` 的 dry-run / apply 命令
- **THEN** Runbook MUST 说明可选 `--progress` 或等价参数的用途
- **AND** Runbook MUST 说明未启用进度参数时 stdout JSON 行为保持兼容

#### Scenario: 记录 stdout 与 stderr 边界

- **WHEN** Runbook 提供带进度输出的生产命令示例
- **THEN** Runbook MUST 说明最终 JSON 输出到 stdout
- **AND** Runbook SHOULD 说明进度信息输出到 stderr，便于分别保存审计 JSON 与运行日志

#### Scenario: 记录脱敏与审计要求

- **WHEN** Runbook 展示进度输出样例或日志采集建议
- **THEN** 样例 MUST 不包含真实 object key、客户信息、私有 endpoint、密钥、连接串、`.env` 内容或本机绝对路径
- **AND** Runbook MUST 提醒最终审计事实仍以命令结束后的 JSON summary 与 acceptance summary 为准
