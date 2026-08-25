## ADDED Requirements

### Requirement: 对象存储影响必须纳入跨版本升级和回滚
对象存储能力 SHALL 为跨版本升级计划提供媒体对象、bucket、prefix、object key、缩略图和维护任务影响证据。

#### Scenario: 跨版本对象存储影响聚合
- **WHEN** 系统生成跨版本升级计划
- **THEN** 计划 SHALL 聚合中间版本涉及对象存储 provider、bucket、prefix、object key、缩略图、历史媒体维护任务和受控读取策略的影响
- **AND** 写入型维护任务 SHALL 要求 dry-run、备份确认和人工授权。

#### Scenario: 对象存储回滚边界明确
- **WHEN** 升级或维护任务可能写入、复制、删除或重生成对象
- **THEN** 回滚计划 SHALL 记录对象存储备份、只读确认或不可逆风险
- **AND** 缺少对象存储恢复证据 SHALL 使升级计划 blocked 或 requires manual review。
