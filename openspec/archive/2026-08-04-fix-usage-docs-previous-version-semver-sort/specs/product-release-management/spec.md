## MODIFIED Requirements

### Requirement: 版本化产品使用文档
产品版本发布管理能力 SHALL 支持按产品版本维护公开产品使用文档源文件，并 SHALL 将产品文档是否生成或更新作为发布准备阶段的显式决策。

#### Scenario: 发布准备先确认是否生成产品文档
- **WHEN** `/release-prepare <version>` 准备产品发布材料
- **THEN** 发布准备流程 SHALL 确认本次是否需要生成或更新产品使用文档。
- **AND** 在确认前 SHALL NOT 自动创建新的 `releases/<version>/usage-docs/` 文档版本。

#### Scenario: 用户确认不需要生成产品文档
- **WHEN** 用户确认某个版本不需要生成或更新产品使用文档
- **THEN** 发布对象 SHALL 记录 `usage_docs.status` 为 `skipped` 或等价状态。
- **AND** 发布对象 SHALL 记录确认来源、确认时间和跳过原因。
- **AND** 流程 SHALL NOT 创建空的当前版本 `usage-docs/` 目录或把空文档加入 Mintlify 当前版本导航。

#### Scenario: 用户确认需要生成产品文档
- **WHEN** 用户确认某个版本需要生成或更新产品使用文档
- **THEN** 流程 SHALL 生成或更新 `releases/<version>/usage-docs/**`。
- **AND** 流程 SHALL 生成或更新 `releases/<version>/usage-docs/manifest.json`。
- **AND** 流程 SHALL 将 `usage_docs.status` 标记为 `generated` 或等价状态。

#### Scenario: 自动选择前一个已生成 usage docs 版本
- **WHEN** 用户确认某个版本需要生成产品使用文档
- **AND** 发布对象未显式指定 `usage_docs.source_version`
- **AND** 历史 release 中存在一个或多个已生成 `usage-docs/manifest.json` 的版本
- **THEN** 流程 SHALL 按 SemVer 语义解析候选版本并选择小于当前目标版本的最近版本作为 `source_version`
- **AND** 流程 SHALL 排除当前目标版本自身
- **AND** 若相邻上一版本未生成 usage docs，流程 SHALL 继续向更早的已生成 usage docs 版本查找
- **AND** 流程 SHALL NOT 使用字符串字典序作为版本先后判断依据。
