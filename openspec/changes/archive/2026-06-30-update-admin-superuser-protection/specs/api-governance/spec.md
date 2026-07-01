---
change_id: update-admin-superuser-protection
capability: api-governance
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
---

## MODIFIED Requirements

### Requirement: Error code registry

Business and authentication errors MUST use stable codes documented in `docs/standards/error-codes.md` and implemented in `src/backend/app/core/error_codes.py`. This registry MUST include a stable business error for protected system account operations, recommended as `30060` with HTTP 403 and message equivalent to `系统保底管理员账号不允许执行该操作`.

#### Scenario: Auth error codes available

- **WHEN** a developer inspects `error_codes.py` and `docs/standards/error-codes.md`
- **THEN** MUST find codes including `AUTH_INVALID_REQUEST`, `AUTH_INVALID_CREDENTIALS`, and `AUTH_USER_DISABLED`
- **AND** API handlers MUST reference these codes rather than ad-hoc string literals

#### Scenario: Protected account error code registered

- **WHEN** a developer inspects `src/backend/app/core/error_codes.py` and `docs/standards/error-codes.md`
- **THEN** MUST find a stable error code for protected system account operations
- **AND** the documented HTTP status MUST be 403
- **AND** user-management and admin profile password handlers MUST reference this code rather than ad-hoc numbers

#### Scenario: Validation script checks error registry

- **WHEN** `python scripts/validate-api-standard.py` runs in CI or locally
- **THEN** it MUST pass when error code registry and governance docs are present and consistent

### Requirement: OpenAPI metadata

Public routes MUST declare OpenAPI metadata including `response_model`, `summary`, and `tags` so `openapi.json` is suitable for Orval client generation. User management response schemas MUST expose `is_protected` and `protected_reason`; protected account 403 branches SHOULD be documented in route descriptions or response metadata where supported.

#### Scenario: Route metadata present

- **WHEN** a developer opens `/docs` or exported OpenAPI for a public route
- **THEN** the operation MUST include a human-readable `summary`
- **AND** MUST be grouped under an appropriate `tags` entry
- **AND** MUST declare `response_model` for typed client generation

#### Scenario: User schemas expose protected fields

- **WHEN** OpenAPI is exported after this change
- **THEN** user list and detail response schemas MUST include `is_protected` and `protected_reason`
- **AND** Orval generation MUST produce corresponding TypeScript fields

#### Scenario: SDK generation documentation

- **WHEN** a developer reads `src/sdk/README.md`
- **THEN** MUST find instructions to regenerate clients via `./scripts/generate-openapi-client.sh` after API changes
