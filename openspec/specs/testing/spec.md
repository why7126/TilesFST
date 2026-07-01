# testing Specification

## Purpose
TBD - created by archiving change build-test-framework. Update Purpose after archive.
## Requirements
### Requirement: Pytest baseline

Backend tests MUST be runnable from repository root via `./scripts/run-tests.sh` with shared configuration in `pytest.ini` and `tests/conftest.py`.

#### Scenario: Run tests from repository root

- **WHEN** a developer runs `./scripts/run-tests.sh` from the repository root
- **THEN** pytest MUST execute backend unit and integration tests
- **AND** MUST exit with code 0 on the repository baseline

#### Scenario: Pytest configuration present

- **WHEN** a developer inspects repository test configuration
- **THEN** MUST find `pytest.ini` at repository root
- **AND** MUST find `tests/conftest.py` for shared fixtures

### Requirement: Test directory structure

The repository MUST maintain a test pyramid with dedicated directories for unit, integration, and end-to-end tests documented in `docs/standards/testing-governance.md`.

#### Scenario: Core test directories exist

- **WHEN** a developer lists `tests/`
- **THEN** MUST find `tests/unit/`, `tests/integration/`, and `tests/e2e/`
- **AND** `tests/unit/` and `tests/integration/` MUST contain at least one `test_*.py` file each

#### Scenario: Backend module tests retained

- **WHEN** a developer lists `src/backend/tests/`
- **THEN** MUST find at least one `test_*.py` for backend module-level tests

### Requirement: Test mapping

Each REQ-0000 infrastructure requirement MUST map to at least one automated test or validation script in `openspec/testing-mapping.md`.

#### Scenario: Sprint-000 mappings registered

- **WHEN** a developer reads `openspec/testing-mapping.md`
- **THEN** MUST find entries for `REQ-0000-build-design-system`, `REQ-0000-build-api-standard`, and `REQ-0000-build-test-standard`
- **AND** each entry MUST list at least one test path or validation script

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

### Requirement: Test framework validation script

The project MUST provide `scripts/validate-test-framework.py` to verify pytest configuration, governance documents, and baseline test directories exist.

#### Scenario: Validation passes on baseline

- **WHEN** `python scripts/validate-test-framework.py` runs on the repository baseline
- **THEN** it MUST exit with code 0
- **AND** MUST report that test framework validation passed

#### Scenario: Required governance docs checked

- **WHEN** the validation script runs
- **THEN** it MUST verify presence of `docs/standards/testing-governance.md`, `docs/standards/unit-test-standard.md`, `docs/standards/frontend-test-standard.md`, and `.coveragerc`

### Requirement: CI test workflow

The repository MUST include a GitHub Actions workflow that runs pytest and test framework validation on push and pull request.

#### Scenario: Backend tests in CI

- **WHEN** a pull request targets `main` or `master`
- **THEN** `.github/workflows/test.yml` MUST run backend pytest
- **AND** MUST run `python scripts/validate-test-framework.py`

### Requirement: 生产 MySQL 路径必须有集成验证

项目 MUST 提供至少一种 MySQL 集成验证路径，用于验证 MySQL schema 初始化、默认管理员 seed 和至少一条读写 API。该验证 MAY 作为 CI MySQL 8 service container job，也 MAY 作为 `@pytest.mark.mysql` optional pytest 与 documented manual smoke 组合。默认 SQLite pytest MUST 保持可从本地运行，不要求开发者本机安装 MySQL。

#### Scenario: MySQL 集成验证覆盖启动关键路径

- **WHEN** MySQL 集成验证运行
- **THEN** MUST 覆盖 MySQL schema 初始化
- **AND** MUST 覆盖默认管理员 seed
- **AND** MUST 覆盖至少一条 API 读写路径，如登录或 health + 简单 CRUD

#### Scenario: SQLite 默认 pytest 仍可运行

- **WHEN** 开发者在未安装 MySQL 的本地环境运行默认 pytest
- **THEN** 测试 MUST 使用 SQLite 默认路径
- **AND** MUST NOT 因缺少 MySQL 服务而失败

