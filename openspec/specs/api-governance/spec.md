# API 治理规范

## Purpose
定义统一响应结构、错误码登记、OpenAPI 元数据、API 标准校验脚本和基线集成测试要求，确保后端接口与前端 Orval 客户端长期保持一致。
## Requirements
### Requirement: 统一响应信封

All public JSON APIs MUST return a unified envelope `{ code, message, data }` for success and error responses documented in `docs/standards/api-governance.md`. Management admin form APIs MUST also return this envelope for FastAPI/Pydantic request validation failures, including JSON body, path parameter, query parameter, enum, and `multipart/form-data` parameter validation errors. The validation error response SHOULD keep HTTP 422 by default, and MUST NOT expose raw framework-default `detail` as the only user-facing or frontend-contract response structure.

#### Scenario: 成功 JSON 响应结构

- **WHEN** a public API returns HTTP 2xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and `data` fields
- **AND** `code` MUST be `0` or the documented success code for the endpoint family

#### Scenario: 错误 JSON 响应结构

- **WHEN** a public API returns HTTP 4xx or 5xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and MAY include `data` as null or error detail
- **AND** `code` MUST match a registered business or auth error code

#### Scenario: 请求校验错误响应结构

- **WHEN** a Web client submits an invalid JSON request body to a public API
- **THEN** the response body MUST include `code`, `message`, and `data`
- **AND** `message` MUST be suitable for display or mapping by the Web client
- **AND** the response body MUST NOT only expose FastAPI/Pydantic default `detail` as the user-facing error contract

#### Scenario: 管理端表单校验错误 envelope

- **WHEN** a management admin form API fails FastAPI/Pydantic validation before entering business logic
- **THEN** the response SHOULD use HTTP 422
- **AND** the response body MUST include `code`, `message`, and `data`
- **AND** `code` MUST be `40001` / `INVALID_PARAMETER` or an equivalent registered parameter validation error code
- **AND** `message` MUST be a Chinese user-facing parameter error message such as `请求参数无效`
- **AND** the response body MUST NOT only expose FastAPI/Pydantic default `detail`.

#### Scenario: 管理端字段级错误结构

- **WHEN** the validation error can be represented as field-level details
- **THEN** `data.errors[]` SHOULD include `field`, `message`, `type`, and `location`
- **AND** `field` SHOULD be suitable for Web form mapping, such as `username`, `body.name`, `query.status`, or `file`
- **AND** `location` SHOULD preserve the normalized validation location for debugging and tests.

#### Scenario: 管理端 multipart 缺文件校验错误

- **WHEN** an admin upload API under `POST /api/v1/admin/uploads/*` receives a request missing the required file field or with an invalid file parameter shape
- **THEN** the response MUST follow the unified validation error envelope
- **AND** the response MUST NOT only expose framework-default `detail`.

#### Scenario: 业务错误不被通用校验 handler 覆盖

- **WHEN** an existing business `AppError` occurs, such as duplicate username, protected account operation, disallowed file type, or category max-depth validation
- **THEN** the response MUST keep the existing business error code, HTTP status, and message
- **AND** the generic parameter validation handler MUST NOT replace it with `INVALID_PARAMETER`.

#### Scenario: 错误详情不泄露敏感信息

- **WHEN** `data.errors[]` is generated from invalid request input
- **THEN** the response MUST NOT include plaintext passwords, tokens, Authorization headers, MinIO credentials, database connection strings, real filesystem paths, complete uploaded object keys, or raw file content
- **AND** the response SHOULD include only field path, normalized message, error type, and location.

#### Scenario: 创建用户的用户名校验响应

- **WHEN** `POST /api/v1/admin/users` receives `username="abc"`
- **THEN** the response MUST follow the unified envelope
- **AND** the response message MUST identify the username length problem

#### Scenario: 首批管理端表单接口覆盖

- **WHEN** framework validation fails for user, brand, tile category, tile SKU, tile spec, banner, system settings, profile, password, or admin upload form APIs
- **THEN** the response MUST follow the unified validation error envelope
- **AND** the covered routes MUST include the representative create, update, status, reset, profile, password, and upload endpoints listed by REQ-0031.

### Requirement: 错误码登记表

Business and authentication errors MUST use stable codes documented in `docs/standards/error-codes.md` and implemented in `src/backend/app/core/error_codes.py`. This registry MUST include a stable business error for protected system account operations, recommended as `30060` with HTTP 403 and message equivalent to `系统保底管理员账号不允许执行该操作`.

#### Scenario: 认证错误码可用

- **WHEN** a developer inspects `error_codes.py` and `docs/standards/error-codes.md`
- **THEN** MUST find codes including `AUTH_INVALID_REQUEST`, `AUTH_INVALID_CREDENTIALS`, and `AUTH_USER_DISABLED`
- **AND** API handlers MUST reference these codes rather than ad-hoc string literals

#### Scenario: 受保护账号错误码已登记

- **WHEN** a developer inspects `src/backend/app/core/error_codes.py` and `docs/standards/error-codes.md`
- **THEN** MUST find a stable error code for protected system account operations
- **AND** the documented HTTP status MUST be 403
- **AND** user-management and admin profile password handlers MUST reference this code rather than ad-hoc numbers

#### Scenario: 校验脚本检查错误码登记表

- **WHEN** `python scripts/validate-api-standard.py` runs in CI or locally
- **THEN** it MUST pass when error code registry and governance docs are present and consistent

### Requirement: OpenAPI 元数据

Public routes MUST declare OpenAPI metadata including `response_model`, `summary`, and `tags` so `openapi.json` is suitable for Orval client generation. User management response schemas MUST expose `is_protected` and `protected_reason`; protected account 403 branches SHOULD be documented in route descriptions or response metadata where supported. The final exported OpenAPI operation tags MUST use a single source of truth and MUST NOT contain duplicate, multi-source, or display-name/technical-name parallel tags. Management admin form APIs SHOULD document the unified validation error envelope for HTTP 422 responses so generated Web clients do not treat default `HTTPValidationError.detail` as the only validation error contract.

#### Scenario: 路由元数据存在

- **WHEN** a developer opens `/docs` or exported OpenAPI for a public route
- **THEN** the operation MUST include a human-readable `summary`
- **AND** MUST be grouped under an appropriate `tags` entry
- **AND** MUST declare `response_model` for typed client generation

#### Scenario: 管理端表单 422 OpenAPI 契约

- **WHEN** OpenAPI is exported after this change
- **THEN** representative management admin form APIs MUST expose a 422 response schema compatible with the unified envelope
- **AND** generated Orval types MUST NOT make `HTTPValidationError.detail` the only available validation error response shape for those APIs.

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

### Requirement: API 基线集成测试

The repository MUST include integration tests that exercise at least one public API endpoint using the unified response envelope.

#### Scenario: 健康检查或认证基线测试

- **WHEN** `./scripts/run-tests.sh` or `pytest tests/integration/api/` runs
- **THEN** at least one test MUST call a public endpoint and assert HTTP status and envelope fields

### Requirement: 管理端 API 文档聚合
The API governance capability SHALL support an admin-only route inventory source for the `/admin/api-docs` page when OpenAPI alone cannot represent all system routes.

#### Scenario: Admin aggregation endpoint
- **WHEN** the implementation adds a route inventory endpoint
- **THEN** the endpoint SHALL be under `/api/v1/admin`
- **AND** it SHALL require admin-only authorization.

#### Scenario: Employee forbidden for aggregation endpoint
- **WHEN** an authenticated `employee` calls the route inventory endpoint
- **THEN** the API SHALL return 403 using the unified error response structure.

#### Scenario: Route metadata schema
- **WHEN** the route inventory endpoint returns route entries
- **THEN** each entry SHALL include method, path, tag or module, summary or description, auth requirement, OpenAPI inclusion status, operation id, Orval method name, and source when known.

### Requirement: 非 /api/v1 路由文档化
The API documentation governance SHALL include non-`/api/v1` system routes in the admin-facing route inventory.

#### Scenario: Health route documented
- **WHEN** route inventory is generated
- **THEN** `GET /health` SHALL be present and marked as a health-check route.

#### Scenario: Media passthrough route documented
- **WHEN** route inventory is generated
- **THEN** `/media/{object_key:path}` SHALL be present and marked as a media passthrough route.

#### Scenario: OpenAPI inclusion is explicit
- **WHEN** a route is not included in the OpenAPI schema
- **THEN** the route inventory SHALL mark `included_in_openapi=false` or an equivalent state.

### Requirement: Orval 方法名治理
The API governance capability SHALL keep admin-displayed Orval method names aligned with the generated Web client.

#### Scenario: Generated client is source of truth
- **WHEN** API changes affect generated frontend methods
- **THEN** the implementation SHALL run the Orval generation script and commit updated generated output.

#### Scenario: Method mapping visible
- **WHEN** a route has an Orval generated method
- **THEN** route inventory or the Web client SHALL expose that method name for display on `/admin/api-docs`.

#### Scenario: Missing mapping is explicit
- **WHEN** a route has no generated Orval method
- **THEN** route inventory or the Web client SHALL expose an explicit missing state instead of an empty or misleading method value.

### Requirement: 管理端接口文档索引同步
The long-term API index SHALL document the admin API docs page and production Swagger debugging policy.

#### Scenario: API index updated
- **WHEN** the `/admin/api-docs` capability is implemented
- **THEN** `docs/03-api-index.md` SHALL mention the admin API docs page, route inventory scope, OpenAPI/Swagger/Orval relationship, and production `Try It Out` policy.

