## MODIFIED Requirements

### Requirement: OpenAPI 元数据

Public routes MUST declare OpenAPI metadata including `response_model`, `summary`, and `tags` so `openapi.json` is suitable for Orval client generation. User management response schemas MUST expose `is_protected` and `protected_reason`; protected account 403 branches SHOULD be documented in route descriptions or response metadata where supported. The final exported OpenAPI operation tags MUST use a single source of truth and MUST NOT contain duplicate, multi-source, or display-name/technical-name parallel tags.

#### Scenario: 路由元数据存在

- **WHEN** a developer opens `/docs` or exported OpenAPI for a public route
- **THEN** the operation MUST include a human-readable `summary`
- **AND** MUST be grouped under an appropriate `tags` entry
- **AND** MUST declare `response_model` for typed client generation

#### Scenario: OpenAPI operation tags 使用单一事实源

- **WHEN** OpenAPI is exported after API route metadata changes
- **THEN** each operation MUST expose exactly one tag
- **AND** the tag MUST be generated from the selected route tag source of truth
- **AND** the operation MUST NOT contain both router-level and decorator-level tag values.

#### Scenario: OpenAPI operation tags 命名统一

- **WHEN** OpenAPI is exported
- **THEN** each operation tag MUST use kebab-case technical naming such as `admin-brands` or `admin-tile-skus`
- **AND** the OpenAPI document MUST NOT expose display-name tags such as `Admin Brands` alongside technical tags
- **AND** an operation MUST NOT contain duplicate tag values.

#### Scenario: 用户 schema 暴露保护字段

- **WHEN** OpenAPI is exported after this change
- **THEN** user list and detail response schemas MUST include `is_protected` and `protected_reason`
- **AND** Orval generation MUST produce corresponding TypeScript fields

#### Scenario: SDK 生成文档

- **WHEN** a developer reads `src/sdk/README.md`
- **THEN** MUST find instructions to regenerate clients via `./scripts/generate-openapi-client.sh` after API changes

### Requirement: API 治理校验脚本

The project MUST provide `scripts/validate-api-standard.py` to verify API governance artifacts exist and baseline conventions are met. The validation MUST include checks against the final OpenAPI schema for operation tag count, duplicate tags, and kebab-case tag naming.

#### Scenario: 基线校验通过

- **WHEN** `python scripts/validate-api-standard.py` runs on the repository baseline
- **THEN** it MUST exit with code 0
- **AND** MUST report that API standard validation passed

#### Scenario: 最终 OpenAPI tags 漂移会失败

- **WHEN** the exported or generated OpenAPI schema contains an operation with more than one tag
- **OR** an operation contains duplicate tag values
- **OR** an operation contains a non-kebab-case tag
- **THEN** `python scripts/validate-api-standard.py` MUST exit with a non-zero code
- **AND** the failure output MUST identify the affected method/path or operationId.
