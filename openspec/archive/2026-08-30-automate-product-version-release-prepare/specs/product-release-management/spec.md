## MODIFIED Requirements

### Requirement: 产品版本号发布强门禁

发布准备 SHALL 自动同步用户可见产品版本号与目标发布版本；发布确认 SHALL 只校验版本号一致性，不得在确认阶段写入版本源或通过说明性 rationale 放行版本漂移。

#### Scenario: Release prepare synchronizes product version sources
- **WHEN** release prepare runs for `<version>`
- **THEN** it SHALL synchronize existing user-visible `PRODUCT_VERSION` sources to `<version>` before prepare validation
- **AND** the synchronized sources SHALL include `src/shared/product-version.ts`, `src/miniapp/utils/product-version.ts`, and `src/miniapp/utils/product-version.js` when present
- **AND** it SHALL record `release.json.gates.product_version` evidence and `release.json.product_version_sync` metadata.

#### Scenario: Release prepare refreshes derived announcement version status
- **WHEN** release prepare synchronizes product version sources
- **THEN** it MAY refresh release announcement title, heading, and version status copy that can be derived from `release.json`
- **AND** it SHALL NOT write final publish confirmation, tarball checksum, or manually authored feature/risk copy into `announcement.mdx`.

#### Scenario: Release publish confirms but does not write product version sources
- **WHEN** release publish validation runs for `<version>`
- **AND** any user-visible `PRODUCT_VERSION` source differs from `<version>`
- **THEN** publish SHALL be blocked and SHALL point back to `/release-prepare <version>`
- **AND** release publish SHALL NOT modify Web or miniapp product version source files.

#### Scenario: Image prepare requires aligned product version sources
- **WHEN** image prepare runs for `<version>`
- **AND** any existing user-visible `PRODUCT_VERSION` source differs from `<version>`
- **THEN** image prepare SHALL record a blocker that instructs the operator to run `/release-prepare <version>` first
- **AND** image prepare SHALL NOT modify product version source files itself.

#### Scenario: Version source change invalidates image evidence
- **WHEN** a product version source is changed after image prepare or image build evidence exists
- **THEN** the operator SHALL rerun `/release-prepare <version>`, `/image-prepare <version>`, and `/image-build <version>` before publishing
- **AND** release status or validation SHALL present those commands as the safe remediation path.
