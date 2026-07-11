## ADDED Requirements

### Requirement: 日志审计复制 helper 迁移边界

Product usage logging SHALL preserve the existing `/admin/logs` request id copy behavior when the Web client migrates that interaction to a shared Clipboard copy helper or equivalent normalized pattern.

#### Scenario: request_id 复制成功后埋点

- **WHEN** an admin copies a non-empty request id and Clipboard writing succeeds
- **THEN** the Web client SHALL continue to emit the `copy_request_id` usage event
- **AND** the event SHALL NOT include passwords, tokens, Authorization values, cookies, or unrelated sensitive metadata.

#### Scenario: request_id 复制失败不记录成功事件

- **WHEN** Clipboard API is unavailable, Clipboard writing fails, or the request id is empty
- **THEN** the Web client SHALL NOT emit a successful `copy_request_id` usage event
- **AND** it SHALL show fixed toast or equivalent manual-copy guidance without causing list layout shift.

#### Scenario: request_id 复制测试保持

- **WHEN** the logs page frontend tests run after helper migration
- **THEN** they SHALL cover request id copy success, Clipboard API unavailable fallback, Clipboard write failure fallback, and empty request id behavior
- **AND** they SHALL continue to cover list pagination structure.
