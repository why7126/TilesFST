## ADDED Requirements

### Requirement: 产品版本号发布强门禁

发布准备与发布确认 SHALL 强制校验用户可见产品版本号与目标发布版本一致，不得通过说明性 rationale 放行版本漂移。

#### Scenario: Release prepare blocks product version mismatch
- **WHEN** release prepare validation runs for `<version>`
- **AND** `src/shared/product-version.ts`, `src/miniapp/utils/product-version.ts`, or `src/miniapp/utils/product-version.js` exists with `PRODUCT_VERSION` different from `<version>`
- **THEN** validation SHALL fail before marking prepare complete
- **AND** the failure SHALL identify the mismatched file and expected version.

#### Scenario: Release publish blocks user-visible version mismatch
- **WHEN** release publish validation runs for `<version>`
- **AND** any user-visible `PRODUCT_VERSION` source differs from `<version>`
- **THEN** publish SHALL be blocked even if `version_change_rationale` is present
- **AND** the release MUST NOT be marked published until the version sources are aligned.

#### Scenario: Version source change invalidates image evidence
- **WHEN** a product version source is changed after image prepare or image build evidence exists
- **THEN** the operator SHALL rerun `/image-prepare <version>` and `/image-build <version>` before publishing
- **AND** release status or validation SHALL present those commands as the safe remediation path.
