## ADDED Requirements

### Requirement: 发布命令主线下一步

发布命令 MUST 将变更型准备命令作为主线下一步，将只读状态面板作为按需排查入口，避免操作者把状态面板误解为准备阶段的必经步骤。

#### Scenario: release propose points to release prepare

- **GIVEN** `/release-propose <version>` 已创建或更新发布计划
- **WHEN** 命令输出下一步
- **THEN** 默认下一步 MUST 是 `/release-prepare <version>`
- **AND** 输出 MAY 提醒操作者可按需运行 `/release-status <version>` 查看只读状态面板

#### Scenario: release status remains read-only

- **GIVEN** 操作者运行 `/release-status <version>`
- **WHEN** 状态面板输出 release、image、upgrade 和 publish 状态
- **THEN** 它 MUST NOT 创建或修改 release、image、upgrade、公告、usage docs 或 publish confirmation
- **AND** 它 MUST 只汇总当前阶段、阻塞分类、默认 upgrade 路径和下一步
