# api-governance Specification

## Purpose
TBD - created by archiving change build-api-standard. Update Purpose after archive.
## Requirements
### Requirement: Unified response envelope

All public JSON APIs MUST return a unified envelope `{ code, message, data }` for success and error responses documented in `docs/api-governance.md`.

#### Scenario: Successful JSON response shape

- **WHEN** a public API returns HTTP 2xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and `data` fields
- **AND** `code` MUST be `0` or the documented success code for the endpoint family

#### Scenario: Error JSON response shape

- **WHEN** a public API returns HTTP 4xx or 5xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and MAY include `data` as null or error detail
- **AND** `code` MUST match a registered business or auth error code

### Requirement: Error code registry

Business and authentication errors MUST use stable codes documented in `docs/error-codes.md` and implemented in `src/backend/app/core/error_codes.py`.

#### Scenario: Auth error codes available

- **WHEN** a developer inspects `error_codes.py` and `docs/error-codes.md`
- **THEN** MUST find codes including `AUTH_INVALID_REQUEST`, `AUTH_INVALID_CREDENTIALS`, and `AUTH_USER_DISABLED`
- **AND** API handlers MUST reference these codes rather than ad-hoc string literals

#### Scenario: Validation script checks error registry

- **WHEN** `python scripts/validate-api-standard.py` runs in CI or locally
- **THEN** it MUST pass when error code registry and governance docs are present and consistent

### Requirement: OpenAPI metadata

Public routes MUST declare OpenAPI metadata including `response_model`, `summary`, and `tags` so `openapi.json` is suitable for Orval client generation.

#### Scenario: Route metadata present

- **WHEN** a developer opens `/docs` or exported OpenAPI for a public route
- **THEN** the operation MUST include a human-readable `summary`
- **AND** MUST be grouped under an appropriate `tags` entry
- **AND** MUST declare `response_model` for typed client generation

#### Scenario: SDK generation documentation

- **WHEN** a developer reads `src/sdk/README.md`
- **THEN** MUST find instructions to regenerate clients via `./scripts/generate-openapi-client.sh` after API changes

### Requirement: API governance validation script

The project MUST provide `scripts/validate-api-standard.py` to verify API governance artifacts exist and baseline conventions are met.

#### Scenario: Validation passes on baseline

- **WHEN** `python scripts/validate-api-standard.py` runs on the repository baseline
- **THEN** it MUST exit with code 0
- **AND** MUST report that API standard validation passed

### Requirement: API baseline integration tests

The repository MUST include integration tests that exercise at least one public API endpoint using the unified response envelope.

#### Scenario: Health or auth baseline test

- **WHEN** `./scripts/run-tests.sh` or `pytest tests/integration/api/` runs
- **THEN** at least one test MUST call a public endpoint and assert HTTP status and envelope fields

