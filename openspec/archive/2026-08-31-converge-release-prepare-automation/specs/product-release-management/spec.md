## ADDED Requirements

### Requirement: 发布准备自动化产物决策
发布命令族 SHALL 将公告、产品使用文档和升级计划的产物决策写入发布计划，并 SHALL 由发布准备命令按计划生成或校验这些产物。

#### Scenario: release-propose 默认声明发布准备产物
- **WHEN** 操作者执行 `/release-propose <version>` 且未提供额外产物参数
- **THEN** 发布计划 SHALL 声明每次发布必须生成或更新 `announcement.mdx`
- **AND** 发布计划 SHALL 默认声明不生成或不更新 usage docs
- **AND** 发布计划 SHALL 默认声明 `fresh -> <version>` 与上一正式版本到 `<version>` 两条升级计划；若不存在上一正式版本，该相邻升级计划 SHALL 记录为不适用。

#### Scenario: release-propose 支持显式产物参数
- **WHEN** 操作者执行 `/release-propose <version> --usage-docs`
- **THEN** 发布计划 SHALL 将 `usage_docs.generation_decision.required` 记录为 `true`。
- **WHEN** 操作者执行 `/release-propose <version> --no-usage-docs`
- **THEN** 发布计划 SHALL 将 `usage_docs.generation_decision.required` 记录为 `false`。
- **WHEN** 操作者执行 `/release-propose <version> --upgrade-from <fresh|version>`
- **THEN** 发布计划 SHALL 将该来源版本追加到待生成升级路径，并与默认路径去重。

#### Scenario: release-prepare 按发布计划生成和校验产物
- **WHEN** 操作者执行 `/release-prepare <version>`
- **THEN** 发布准备流程 SHALL 自动同步 Web 与小程序用户可见 `PRODUCT_VERSION` 到发布版本。
- **AND** 发布准备流程 SHALL 生成或更新 `announcement.mdx`。
- **AND** 若 `usage_docs.generation_decision.required` 为 `true`，发布准备流程 SHALL 生成并校验 usage docs 与 Mintlify 投影。
- **AND** 若 `usage_docs.generation_decision.required` 为 `false`，发布准备流程 SHALL 保持 `usage_docs.status=skipped` 且不得创建空 `usage-docs/` 目录。
- **AND** 发布准备流程 SHALL 生成并校验默认和显式声明的升级计划。

#### Scenario: release-status 仅报告状态和安全下一步
- **WHEN** `/release-status <version>` 发现默认或显式声明的升级计划缺失
- **THEN** 状态面板 SHALL 作为只读结果报告缺口。
- **AND** 安全修复路径 SHALL 指向 `/release-prepare <version>`，由 prepare 阶段统一生成默认和声明产物。

#### Scenario: release-publish 只记录发布确认
- **WHEN** 操作者执行 `/release-publish <version>`
- **THEN** 发布确认流程 SHALL NOT 修改 Web 或小程序 `PRODUCT_VERSION` 源。
- **AND** 发布确认流程 SHALL NOT 生成或替换主发布公告。
- **AND** 发布确认流程 SHALL NOT 生成 usage docs、Mintlify 投影或 upgrade plan。
- **AND** 发布确认流程 SHALL 仅在发布门禁通过后写入发布确认字段。
