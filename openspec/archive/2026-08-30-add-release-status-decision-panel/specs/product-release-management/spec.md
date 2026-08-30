## ADDED Requirements

### Requirement: 发布状态决策面板
产品版本发布管理 SHALL 提供只读发布状态决策面板，用于汇总 release、image、upgrade 和 publish 当前状态，并向操作者输出可执行的下一步。

#### Scenario: 状态面板区分决策与证据
- **WHEN** 操作者查看某个版本的发布状态
- **THEN** 状态面板 SHALL 分别列出需要用户选择的决策项、需要命令或人工补齐的证据项，以及不阻断当前目标的后续事项
- **AND** 每个阻塞项 SHALL 标明分类、影响阶段、阻塞目标、当前证据、建议动作和复核命令。

#### Scenario: 开发发布显示生产后续但不阻断
- **WHEN** 发布对象声明 `release_target.environment=development`
- **THEN** 状态面板 SHALL 将生产 env、生产备份、生产 no-fallback、公开 API 和生产 smoke 缺口归类为 `production_only_pending`
- **AND** 这些缺口 SHALL NOT 作为开发发布的阻塞项。

#### Scenario: 状态面板输出唯一下一步
- **WHEN** 状态面板能够推导出下一条安全动作
- **THEN** 输出 SHALL 提供一条可复制的下一步命令
- **AND** 若仍存在需要用户选择、补证或人工确认的事项，输出 SHALL 将其放入待用户处理区域而不是混入下一步命令。

### Requirement: 发布阻塞分类契约
产品版本发布管理 SHALL 使用统一阻塞分类表达 release、image、upgrade 和 publish 中的决策、证据、环境、范围和安全问题。

#### Scenario: 阻塞分类字段完整
- **WHEN** 发布命令、状态面板或 validator 报告发布阻塞项
- **THEN** 阻塞项 SHALL 使用 `decision_missing`、`prepare_evidence_missing`、`publish_evidence_missing`、`production_only_pending`、`input_drift`、`environment_unavailable`、`scope_incomplete`、`public_safety` 或 `schema_invalid` 等分类
- **AND** 阻塞项 SHOULD 包含 phase、blocks_target、owner、current_evidence、safe_remediation 和 rerun_check。

#### Scenario: 发布确认阶段不再重新发现普通下一步
- **WHEN** 发布状态面板已报告某版本未达到 publish ready
- **THEN** `/release-publish` SHOULD 只确认已就绪发布或报告状态面板已暴露的阻塞项
- **AND** 普通缺失的 image manifest、默认 upgrade plan 或用户决策 SHOULD 在 `/release-status` 或 `/release-prepare` 阶段提前暴露。
