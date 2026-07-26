## MODIFIED Requirements

### Requirement: 当前用户主题偏好 API

The authentication capability MUST expose the current user's theme preference and allow authenticated users to update their own theme preference. Supported values are `system`, `dark_flagship`, `comfort_dark`, and `light`. Production and local deployments MUST keep this API route, persistence field, authentication behavior, and unified response envelope consistent so Web clients can distinguish successful account preference persistence from recoverable client-side fallback.

#### Scenario: 当前用户信息包含主题偏好

- **WHEN** an authenticated user calls `GET /api/v1/auth/me`
- **THEN** the response `data` SHALL include `theme_mode`
- **AND** `theme_mode` SHALL be one of `system`, `dark_flagship`, `comfort_dark`, or `light`.

#### Scenario: 当前用户更新主题偏好

- **WHEN** an authenticated user submits a valid theme mode to the current-user theme preference endpoint
- **THEN** the system SHALL persist the value for that user
- **AND** the response SHALL use the unified `ApiResponse` envelope
- **AND** the response `data.theme_mode` SHALL equal the persisted value
- **AND** a later `GET /api/v1/auth/me` SHALL return the updated `theme_mode`.

#### Scenario: 主题偏好生产链路可用

- **WHEN** a production or production-equivalent deployment serves the Web admin client and backend together
- **THEN** `PATCH /api/v1/auth/me/theme` SHALL be reachable through the configured `/api/` route
- **AND** authenticated requests with valid Bearer tokens SHALL preserve the Authorization context through reverse proxies
- **AND** the deployment database SHALL include the `users.theme_mode` persistence field with the supported values.

#### Scenario: 无效主题偏好被拒绝

- **WHEN** an authenticated user submits a theme mode outside the supported values
- **THEN** the system SHALL return HTTP 400 with the unified error envelope
- **AND** the stored preference SHALL NOT change.

#### Scenario: 未认证用户不能更新主题偏好

- **WHEN** a request without a valid Bearer token attempts to read or update account-level theme preference
- **THEN** the system SHALL return the existing authentication error behavior
- **AND** no user preference SHALL be changed.
