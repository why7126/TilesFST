## MODIFIED Requirements

### Requirement: Change 测试

New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, or governance scripts MUST include focused regression tests for the modified behavior. For password-policy feedback changes, tests MUST cover both backend policy failure detail and frontend user-facing error rendering.

#### Scenario: 治理文档声明测试要求

- **WHEN** a developer reads `docs/standards/testing-governance.md`
- **THEN** MUST find a rule that OpenSpec Change implementations MUST add matching tests
- **AND** MUST NOT allow implementation-only changes without test coverage for new Services or Routers

#### Scenario: 修改密码策略失败详情已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST assert password change policy failures expose distinguishable failure details for length, uppercase, lowercase, digit, and special-character requirements
- **AND** tests MUST assert failures do not update `password_hash`
- **AND** tests MUST assert responses do not include plaintext passwords

#### Scenario: 修改密码弹窗具体错误提示已测试

- **WHEN** frontend tests run for this change
- **THEN** tests MUST assert policy failure details render as concrete user-facing messages
- **AND** tests MUST assert new-password policy failures are not displayed under the old-password field
- **AND** tests MUST assert old-password, weak-password, same-as-old, protected-account, and success paths do not regress

#### Scenario: Orval 与 API 契约已检查

- **WHEN** this change modifies OpenAPI response schemas
- **THEN** generated client types MUST include the password policy failure detail shape
- **AND** generated files MUST NOT be hand-edited

#### Scenario: workflow-sync 归档时间漂移已测试

- **WHEN** a Change modifies workflow-sync archived Change timestamp derivation
- **THEN** regression tests MUST cover an archived Change whose related issue or change trace frontmatter `updated_at` is newer than the stable archive fact
- **AND** the rendered archive timestamp MUST come from lifecycle, archive records, or archive directory date rather than mutable `updated_at`

#### Scenario: workflow-sync Markdown 持久化幂等已测试

- **WHEN** a Change modifies workflow-sync Markdown persistence behavior
- **THEN** regression tests MUST cover a Markdown document whose rendered content is identical to the current file
- **AND** persistence MUST NOT rewrite the file or refresh frontmatter `updated_at`
- **AND** consecutive `python scripts/sync-workflow-status.py --check` runs MUST remain no delta after a normal sync.
