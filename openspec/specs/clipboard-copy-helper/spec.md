# clipboard-copy-helper Specification

## Purpose
TBD - created by archiving change add-clipboard-copy-helper-best-practice. Update Purpose after archive.
## Requirements
### Requirement: Clipboard 复制共享 helper

Web 管理端 SHALL provide a shared or equivalent Clipboard copy helper for reusable text-copy interactions. The helper SHALL normalize empty values, detect Clipboard API availability, preserve the correct `navigator.clipboard.writeText` call context, and return a structured result instead of directly controlling UI feedback.

#### Scenario: 自动复制成功

- **WHEN** a caller requests copying non-empty text and `navigator.clipboard.writeText` resolves
- **THEN** the helper SHALL return `success` or an equivalent structured result
- **AND** the helper SHALL expose the normalized copied text if the caller needs it
- **AND** the helper SHALL NOT directly show toast, mutate dialog state, or send usage events.

#### Scenario: 待复制文本为空

- **WHEN** a caller requests copying `null`, `undefined`, an empty string, or whitespace-only text
- **THEN** the helper SHALL return `empty` or an equivalent structured result
- **AND** it SHALL NOT call `navigator.clipboard.writeText`
- **AND** it SHALL NOT call the fallback selector.

#### Scenario: Clipboard API 不存在

- **WHEN** `navigator.clipboard` or `navigator.clipboard.writeText` is unavailable
- **THEN** the helper SHALL return `unavailable` or an equivalent structured result
- **AND** if the caller provides a fallback selector, the helper SHALL invoke it safely
- **AND** the caller SHALL be able to display manual-copy guidance.

#### Scenario: Clipboard 写入失败

- **WHEN** `navigator.clipboard.writeText` rejects or throws
- **THEN** the helper SHALL return `failed` or an equivalent structured result
- **AND** if the caller provides a fallback selector, the helper SHALL invoke it safely
- **AND** fallback selector errors SHALL NOT crash the caller render flow.

### Requirement: Clipboard 复制安全边界

The Clipboard copy helper SHALL NOT log copied text, passwords, tokens, Authorization values, cookies, object-storage keys, or other sensitive values. Business callers SHALL own user-facing copy, telemetry, and audit decisions.

#### Scenario: 敏感文本不进入日志或埋点

- **WHEN** a caller copies sensitive text such as a generated password
- **THEN** the helper SHALL NOT write the copied value to console logs, thrown error messages, usage event metadata, or persistent state outside the caller-provided UI
- **AND** tests SHALL avoid asserting by printing sensitive values into logs.

#### Scenario: 业务埋点由调用方决定

- **WHEN** a caller needs telemetry for a copy interaction
- **THEN** the caller SHALL decide whether and when to emit the event
- **AND** the shared helper SHALL NOT know business event names such as `copy_request_id`.

### Requirement: Clipboard 复制测试覆盖

The Web frontend test suite SHALL cover the shared Clipboard copy helper and representative admin callers.

#### Scenario: Helper 单元测试覆盖核心分支

- **WHEN** the helper tests run
- **THEN** they SHALL cover success, empty input, Clipboard API unavailable, `writeText` rejection, fallback invocation, and fallback throwing without crashing.

#### Scenario: 代表场景回归测试

- **WHEN** representative admin caller tests run
- **THEN** they SHALL cover request id copy behavior and generated-password copy behavior
- **AND** they SHALL verify user-visible messages and critical side effects do not regress.

