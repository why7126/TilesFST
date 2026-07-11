## MODIFIED Requirements

### Requirement: Change 测试

New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, or governance scripts MUST include focused regression tests for the modified behavior. Changes that modify management admin form validation error contracts MUST test backend validation envelope responses, frontend error parsing, OpenAPI/Orval contract generation, and business error compatibility.

#### Scenario: 治理文档声明测试要求

- **WHEN** a developer reads `docs/standards/testing-governance.md`
- **THEN** MUST find a rule that OpenSpec Change implementations MUST add matching tests
- **AND** MUST NOT allow implementation-only changes without test coverage for new Services or Routers

#### Scenario: 管理端 JSON body 校验 envelope 已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST submit invalid JSON body data to representative management admin form APIs
- **AND** tests MUST assert HTTP 422 by default
- **AND** tests MUST assert the response body includes `code`, `message`, and `data`
- **AND** tests MUST assert the response body is not only FastAPI/Pydantic default `detail`.

#### Scenario: 管理端路径查询枚举校验 envelope 已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST cover path, query, or enum parameter validation failure for at least one management admin API
- **AND** tests MUST assert the unified validation error envelope and a stable parameter error code.

#### Scenario: 管理端上传缺文件校验 envelope 已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST call at least one `POST /api/v1/admin/uploads/*` route without a required file or with an invalid file parameter shape
- **AND** tests MUST assert the unified validation error envelope
- **AND** tests MUST assert sensitive file paths, object keys, credentials, and raw file content are not exposed.

#### Scenario: 业务错误兼容已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST cover at least one existing business `AppError`, such as duplicate username, protected account, disallowed file type, or category max-depth validation
- **AND** tests MUST assert the original business error code, HTTP status, and message are preserved.

#### Scenario: Web 错误解析已测试

- **WHEN** frontend tests run for this change
- **THEN** tests MUST assert the admin error parser or equivalent form behavior reads envelope `message`
- **AND** tests SHOULD cover `data.errors[]` field mapping
- **AND** tests MUST cover safe fallback to global feedback when a field cannot be mapped.

#### Scenario: OpenAPI Orval 契约已测试

- **WHEN** this change modifies OpenAPI response schemas
- **THEN** the OpenAPI export and Orval generated client MUST be regenerated and reviewed
- **AND** generated client types MUST expose or tolerate the unified validation error envelope for management admin form APIs
- **AND** generated files MUST NOT be hand-edited.

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

### Requirement: Orval and OpenAPI regression

The testing capability SHALL include OpenAPI/Orval regression checks when the change adds or changes backend API contracts. Management admin form validation error contract changes SHALL include checks that exported OpenAPI and generated Orval output represent the unified validation error envelope and do not depend only on default `HTTPValidationError.detail`.

#### Scenario: Orval generated output updated

- **WHEN** API response contracts change
- **THEN** the OpenAPI export and Orval generated client SHALL be regenerated and reviewed.

#### Scenario: 管理端表单校验错误类型已检查

- **WHEN** API validation envelope governance is implemented
- **THEN** generated OpenAPI / Orval output SHALL expose or tolerate the unified validation error envelope for representative management admin form APIs
- **AND** review records SHALL confirm default `HTTPValidationError.detail` is not the only validation error type source.
