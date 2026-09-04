## MODIFIED Requirements

### Requirement: 测试证据与环境证据边界

测试治理 SHALL 要求验收材料说明证据来源和证明边界，并保留手动证据来源诊断工具；该诊断工具 SHALL NOT 作为默认 release、opsx archive 或 sprint archive 阻断门禁自动应用。

#### Scenario: 证据来源声明

- **WHEN** a test plan、acceptance record 或 workflow trace cites screenshots、network summaries、smoke checks or manual verification
- **THEN** it SHALL state the evidence source or provide an evidence reference when available
- **AND** it SHALL NOT describe development-only evidence as trial、real-device or production proof.

#### Scenario: 手动诊断工具

- **WHEN** an operator wants to inspect evidence source wording
- **THEN** they MAY run `python scripts/validate-environment-tiered-evidence.py --change <change-id>`、`--sprint <sprint-id>` 或 `--release-dir releases/<version>`
- **AND** findings SHALL be treated as diagnostic output unless a separate active gate explicitly adopts them.
