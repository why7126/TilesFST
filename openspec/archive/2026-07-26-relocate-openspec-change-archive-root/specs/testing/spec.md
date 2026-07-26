## MODIFIED Requirements

### Requirement: Change 测试
New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, governance scripts, form validation contracts, workflow snapshot contracts, archive path contracts, or generated backend-owned fields MUST include focused regression tests for the modified behavior. Shared test fixtures and helpers MUST be updated in the same change when request payloads, validation rules, generated fields, archive path roots, or snapshot schemas change.

#### Scenario: 测试夹具跟随契约变更
- **WHEN** an API, form validation, generated-field, workflow snapshot, archive path, or release-governance contract changes
- **THEN** shared pytest/Vitest fixtures and helper payloads MUST be updated to use the current minimum valid contract
- **AND** tests MUST NOT keep submitting deprecated client-writable fields that are now backend-generated
- **AND** tests MUST cover the new fixture, path, or snapshot fields required by validators.

#### Scenario: OpenSpec Change 文件读取兼容归档路径
- **WHEN** automated tests need to read implementation evidence or task files from an OpenSpec Change
- **THEN** tests MUST resolve the file from `openspec/changes/<change-id>/...`, `openspec/archive/*-<change-id>/...`, or legacy `openspec/changes/archive/*-<change-id>/...`
- **AND** tests SHOULD prefer active path first, canonical archive path second, and legacy archive path only as compatibility fallback
- **AND** tests SHOULD reuse a shared resolver helper rather than hard-coding only the active Change path.

#### Scenario: 测试阻止 legacy archive 新写入
- **WHEN** workflow scripts, archive commands, release generation, Fact Sheet, AI usage, or readiness reports create or update Change archive facts
- **THEN** focused regression tests MUST assert generated paths use `openspec/archive/`
- **AND** tests MUST fail if newly generated facts use `openspec/changes/archive/` as the canonical archive path.
