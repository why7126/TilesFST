## REMOVED Requirements

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

### Requirement: 环境证据强脚本门禁

workflow 治理 SHALL 将原环境证据强脚本门禁降级为证据来源诊断工具，用于手动排查验收或发布材料中证据来源描述是否混淆，但该脚本 SHALL NOT 作为 release、opsx archive 或 sprint archive 默认阻断门禁自动应用。

#### Scenario: 默认工作流不自动应用证据来源诊断

- **WHEN** release、opsx archive 或 sprint archive 默认校验运行
- **THEN** validator SHALL NOT automatically fail because `validate-environment-tiered-evidence.py` reports diagnostic findings
- **AND** operators MAY run `python scripts/validate-environment-tiered-evidence.py --change <change-id>`、`--sprint <sprint-id>` 或 `--release-dir releases/<version>` for focused diagnostics.

#### Scenario: 新流程不推荐生产待补字段

- **WHEN** new governance docs、Skill instructions 或 acceptance templates describe evidence source handling
- **THEN** they SHALL prefer evidence source fields such as `evidence_source`、`evidence_ref`、`network_summary` and `executed_at`
- **AND** they SHALL treat `production_only_pending` as historical compatibility wording only, not a recommended new-flow classification.

## ADDED Requirements

### Requirement: 证据来源声明边界

workflow 命令 SHALL 要求验收、归档和发布材料说明证据来源与证明边界，避免用开发工具、静态测试、本地 smoke 或 DevTools 证据扩大表述为体验版、真机、线上或发布完成结论。

#### Scenario: 当前证据只证明当前范围
- **WHEN** Change、BUG、Sprint 或 Release 记录自动化测试、开发 API smoke、DevTools 截图、DevTools Network、静态校验或本地验证 evidence
- **THEN** workflow 输出 SHALL 说明该 evidence 的来源和证明边界
- **AND** SHALL NOT 写作体验版、真机、线上或发布完成已经通过。

#### Scenario: 缺失证据按来源边界承接
- **WHEN** 当前流程无法获得体验版入口、真机设备、线上公开域名、线上接口或真实用户路径 evidence
- **THEN** workflow 输出 SHALL 记录当前已有证据来源、不可验证原因、后续承接阶段或 N/A 理由
- **AND** 新记录 SHOULD 使用 `evidence_source`、`verification_boundary`、`evidence_ref`、`network_summary`、`executed_at` 或等价字段
- **AND** `production_only_pending` SHALL 仅作为历史兼容字段解释，不作为新流程推荐分类。

#### Scenario: 证据记录保持可审计
- **WHEN** workflow 命令记录证据来源
- **THEN** evidence SHALL 使用脱敏路径、命令摘要、截图、报告或人工摘要
- **AND** evidence SHALL NOT 包含密钥、token、Cookie、Authorization header、`.env`、真实客户数据或未脱敏隐私。

### Requirement: 证据来源诊断工具

workflow 治理 SHALL 保留证据来源诊断脚本作为手动排查工具，用于发现验收或发布材料中的证据来源描述混淆；该脚本 SHALL NOT 作为 release、opsx archive 或 sprint archive 默认阻断门禁自动应用。

#### Scenario: 默认工作流不自动应用证据来源诊断
- **WHEN** release、opsx archive 或 sprint archive 默认校验运行
- **THEN** validator SHALL NOT automatically fail because `validate-environment-tiered-evidence.py` reports diagnostic findings
- **AND** operators MAY run `python scripts/validate-environment-tiered-evidence.py --change <change-id>`、`--sprint <sprint-id>` 或 `--release-dir releases/<version>` for focused diagnostics.

#### Scenario: 新流程不推荐生产待补字段
- **WHEN** new governance docs、Skill instructions 或 acceptance templates describe evidence source handling
- **THEN** they SHALL prefer evidence source fields such as `evidence_source`、`verification_boundary`、`evidence_ref`、`network_summary` and `executed_at`
- **AND** they SHALL treat `production_only_pending` as historical compatibility wording only, not a recommended new-flow classification.
