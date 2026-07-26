## MODIFIED Requirements

### Requirement: Change 测试
New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, governance scripts, form validation contracts, workflow snapshot contracts, or generated backend-owned fields MUST include focused regression tests for the modified behavior. Shared test fixtures and helpers MUST be updated in the same change when request payloads, validation rules, generated fields, or snapshot schemas change.

#### Scenario: 测试夹具跟随契约变更
- **WHEN** an API, form validation, generated-field, workflow snapshot, or release-governance contract changes
- **THEN** shared pytest/Vitest fixtures and helper payloads MUST be updated to use the current minimum valid contract
- **AND** tests MUST NOT keep submitting deprecated client-writable fields that are now backend-generated
- **AND** tests MUST cover the new fixture or snapshot fields required by validators.

#### Scenario: OpenSpec Change 文件读取兼容归档路径
- **WHEN** automated tests need to read implementation evidence or task files from an OpenSpec Change
- **THEN** tests MUST resolve the file from either `openspec/changes/<change-id>/...` or `openspec/changes/archive/*-<change-id>/...`
- **AND** tests SHOULD reuse a shared resolver helper rather than hard-coding only the active Change path.
