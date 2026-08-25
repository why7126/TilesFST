## ADDED Requirements

### Requirement: upgrade 命令必须遵守工作流输出契约
Agent workflow tooling SHALL support upgrade planning and validation commands with Workflow Sync, AI Usage, context budget, and safe output contracts.

#### Scenario: upgrade 命令成功输出摘要
- **WHEN** `/upgrade-plan`、`/upgrade-validate` 或等价命令成功完成
- **THEN** 命令输出 SHALL 包含目标版本、来源版本、支持级别、blocker 数、warning 数、证据摘要、计划路径和下一步
- **AND** 命令 SHALL 默认输出 compact summary，不输出完整 manifest、完整 env、完整日志或大体积历史归档内容。

#### Scenario: upgrade 命令接入审计钩子
- **WHEN** upgrade 命令完成并且主校验成功
- **THEN** 命令 SHALL 运行 Workflow Sync 或等价状态同步
- **AND** 命令 SHALL 运行 AI Usage post-command hook，并按 release version、from version、to version 或 upgrade plan 归因。

#### Scenario: upgrade 命令保持生产安全边界
- **WHEN** upgrade 命令生成计划、校验计划或提示人工步骤
- **THEN** 命令 SHALL NOT 自动修改真实生产 env、自动执行生产升级、自动执行数据库写入迁移或对象存储写入维护任务
- **AND** 需要人工确认时 SHALL 输出结构化选项、推荐项、阻塞项和风险说明。
