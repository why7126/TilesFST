## MODIFIED Requirements

### Requirement: 当前用户主题偏好 API

The authentication capability MUST expose the current user's theme preference and allow authenticated users to update their own theme preference. Supported persisted API values for the current product surface are `system` and `dark_flagship`. Production and local deployments MUST keep this API route, persistence field, authentication behavior, unified response envelope, OpenAPI schema, and generated Web client types consistent so Web clients can distinguish successful account preference persistence from recoverable client-side fallback. Historical stored values `light` and `comfort_dark` MUST be normalized on read or migration to avoid unknown theme state.

#### Scenario: 当前用户信息包含主题偏好

- **WHEN** an authenticated user calls `GET /api/v1/auth/me`
- **THEN** the response `data` SHALL include `theme_mode`
- **AND** `theme_mode` SHALL be one of `system` or `dark_flagship`
- **AND** historical stored `light` SHALL be returned as `system`
- **AND** historical stored `comfort_dark` SHALL be returned as `dark_flagship`.

#### Scenario: 当前用户更新主题偏好

- **WHEN** an authenticated user submits `system` or `dark_flagship` to the current-user theme preference endpoint
- **THEN** the system SHALL persist the normalized value for that user
- **AND** the response SHALL use the unified `ApiResponse` envelope
- **AND** the response `data.theme_mode` SHALL equal the persisted normalized value
- **AND** a later `GET /api/v1/auth/me` SHALL return the updated `theme_mode`.

#### Scenario: 主题偏好生产链路可用

- **WHEN** a production or production-equivalent deployment serves the Web admin client and backend together
- **THEN** `PATCH /api/v1/auth/me/theme` SHALL be reachable through the configured `/api/` route
- **AND** authenticated requests with valid Bearer tokens SHALL preserve the Authorization context through reverse proxies
- **AND** the deployment database SHALL include the `users.theme_mode` persistence field with values that can be normalized to the supported modes.

#### Scenario: 无效主题偏好被拒绝

- **WHEN** an authenticated user submits a theme mode outside `system`, `dark_flagship`, `light`, or `comfort_dark`
- **THEN** the system SHALL return HTTP 400 with the unified error envelope
- **AND** the stored preference SHALL NOT change.

#### Scenario: 历史主题偏好写入兼容

- **WHEN** an authenticated user or historical client submits `light`
- **THEN** the system MAY accept it as a backward-compatible input and normalize it to `system`
- **AND** the response `data.theme_mode` SHALL be `system`.

- **WHEN** an authenticated user or historical client submits `comfort_dark`
- **THEN** the system MAY accept it as a backward-compatible input and normalize it to `dark_flagship`
- **AND** the response `data.theme_mode` SHALL be `dark_flagship`.

#### Scenario: 未认证用户不能更新主题偏好

- **WHEN** a request without a valid Bearer token attempts to read or update account-level theme preference
- **THEN** the system SHALL return the existing authentication error behavior
- **AND** no user preference SHALL be changed.

