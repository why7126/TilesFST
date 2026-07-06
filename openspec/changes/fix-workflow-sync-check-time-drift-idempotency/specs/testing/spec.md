## MODIFIED Requirements

### Requirement: Change 测试

New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, or governance scripts MUST include focused regression tests for the modified behavior. For `update-admin-superuser-protection`, backend tests MUST cover protected account identification and all protected operation guards; frontend tests SHOULD cover protected row disabled actions and ordinary user non-regression.

#### Scenario: 治理文档声明测试要求

- **WHEN** a developer reads `docs/standards/testing-governance.md`
- **THEN** MUST find a rule that OpenSpec Change implementations MUST add matching tests
- **AND** MUST NOT allow implementation-only changes without test coverage for new Services or Routers

#### Scenario: 受保护用户列表字段已测试

- **WHEN** backend tests run for this change
- **THEN** at least one test MUST assert that `GET /api/v1/admin/users` returns `is_protected=true` for `ADMIN_USERNAME`
- **AND** ordinary admin users MUST return `is_protected=false`

#### Scenario: 受保护破坏性操作已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST assert protected account edit returns HTTP 403 and leaves fields unchanged
- **AND** tests MUST assert reset-password returns HTTP 403 and leaves `password_hash` unchanged
- **AND** tests MUST assert status change returns HTTP 403 and leaves status unchanged
- **AND** tests MUST assert protected account self password change returns HTTP 403 and leaves `password_hash` and `token_version` unchanged

#### Scenario: 前端受保护行行为已测试

- **WHEN** frontend tests run for this change
- **THEN** tests SHOULD assert protected account row action buttons are disabled or inert
- **AND** tests SHOULD assert disabled actions use `protected_reason`
- **AND** tests SHOULD assert ordinary user edit/reset/status actions remain available and keep DS confirm behavior

#### Scenario: Orval 与 API 契约已检查

- **WHEN** this change modifies OpenAPI response schemas
- **THEN** generated client types MUST include `is_protected` and `protected_reason`
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
