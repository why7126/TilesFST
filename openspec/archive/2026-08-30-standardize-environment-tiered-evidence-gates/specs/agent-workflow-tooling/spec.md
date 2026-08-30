## ADDED Requirements

### Requirement: 环境分层 evidence 门禁

workflow 命令 SHALL 区分开发验收、体验版验证、生产发布和发布后跟进的 evidence 阻塞范围，避免生产专属证据误阻塞开发归档，同时禁止用开发证据声称生产通过。

#### Scenario: 开发归档不被生产专属证据阻塞
- **WHEN** Change、BUG 或 Sprint 的当前阶段是开发验收或开发归档
- **THEN** workflow 命令 SHALL 接受自动化测试、开发 API smoke、DevTools 截图、DevTools Network、静态校验或等价开发环境证据作为当前阶段证据
- **AND** 仅生产环境可获得的生产 env、生产备份、生产公开 API、生产 no-fallback 媒体、生产 smoke 或生产真实用户路径证据 SHALL NOT 阻塞 `opsx.archive` 或开发阶段 `sprint.archive`
- **AND** 这些缺口 SHALL 标记为 `production_only_pending`、`follow_up`、`not_applicable_for_development` 或发布阶段待办。

#### Scenario: 环境 evidence 字段可复核
- **WHEN** workflow 命令记录环境相关 evidence
- **THEN** evidence SHOULD 包含 `target_environment`、`phase`、`blocking_scope`、`classification` 和 `evidence_ref` 或等价表格列
- **AND** `blocking_scope` SHALL 明确证据缺口阻塞开发归档、体验版验收、生产发布还是发布后跟进
- **AND** evidence SHALL 使用脱敏路径、命令摘要、截图、报告或人工摘要，不得包含密钥、token、Cookie、Authorization header、`.env`、真实客户数据或未脱敏隐私。

#### Scenario: 不得扩大通过结论
- **WHEN** 当前只有开发环境或 DevTools evidence
- **THEN** workflow 输出 SHALL 仅声明开发阶段或 DevTools 结论
- **AND** SHALL NOT 写作生产环境、体验版、真机或生产发布已通过
- **AND** 缺少的目标环境证据 SHALL 记录剩余风险和后续承接命令或阶段。
