## MODIFIED Requirements

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
