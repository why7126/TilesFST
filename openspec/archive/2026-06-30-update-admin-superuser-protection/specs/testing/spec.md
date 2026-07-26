---
change_id: update-admin-superuser-protection
capability: testing
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
---

## MODIFIED Requirements

### Requirement: Change tests

New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, or user-facing UI MUST include focused regression tests for the modified behavior. For `update-admin-superuser-protection`, backend tests MUST cover protected account identification and all protected operation guards; frontend tests SHOULD cover protected row disabled actions and ordinary user non-regression.

#### Scenario: Governance documentation states requirement

- **WHEN** a developer reads `docs/standards/testing-governance.md`
- **THEN** MUST find a rule that OpenSpec Change implementations MUST add matching tests
- **AND** MUST NOT allow implementation-only changes without test coverage for new Services or Routers

#### Scenario: Protected user list fields tested

- **WHEN** backend tests run for this change
- **THEN** at least one test MUST assert that `GET /api/v1/admin/users` returns `is_protected=true` for `ADMIN_USERNAME`
- **AND** ordinary admin users MUST return `is_protected=false`

#### Scenario: Protected destructive operations tested

- **WHEN** backend tests run for this change
- **THEN** tests MUST assert protected account edit returns HTTP 403 and leaves fields unchanged
- **AND** tests MUST assert reset-password returns HTTP 403 and leaves `password_hash` unchanged
- **AND** tests MUST assert status change returns HTTP 403 and leaves status unchanged
- **AND** tests MUST assert protected account self password change returns HTTP 403 and leaves `password_hash` and `token_version` unchanged

#### Scenario: Frontend protected row behavior tested

- **WHEN** frontend tests run for this change
- **THEN** tests SHOULD assert protected account row action buttons are disabled or inert
- **AND** tests SHOULD assert disabled actions use `protected_reason`
- **AND** tests SHOULD assert ordinary user edit/reset/status actions remain available and keep DS confirm behavior

#### Scenario: Orval and API contract checked

- **WHEN** this change modifies OpenAPI response schemas
- **THEN** generated client types MUST include `is_protected` and `protected_reason`
- **AND** generated files MUST NOT be hand-edited
