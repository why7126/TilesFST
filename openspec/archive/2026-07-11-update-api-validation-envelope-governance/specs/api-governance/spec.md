## MODIFIED Requirements

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
