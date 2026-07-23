## MODIFIED Requirements

### Requirement: Web 主题切换与偏好持久化

The Web client MUST provide theme switching for `system`, `dark_flagship`, `comfort_dark`, and `light` on management-side and supported store-owner Web surfaces. The active mode MUST persist locally and, for authenticated users, synchronize with the account-level theme preference API. Switching themes MUST apply immediately without losing current page state. Account preference synchronization failures MUST be communicated with recoverable admin feedback that automatically dismisses or provides an explicit close affordance; the feedback MUST NOT remain persistently visible without user control.

#### Scenario: 登录前主题偏好

- **WHEN** an unauthenticated user changes theme on the login page
- **THEN** the selected mode SHALL persist locally
- **AND** the login page SHALL update immediately without requiring reload
- **AND** the Web client SHALL NOT call the account-level theme preference API.

#### Scenario: 登录后账号偏好合并

- **WHEN** a user logs in successfully
- **THEN** the Web client SHALL load the account-level `theme_mode`
- **AND** the account-level value SHALL become authoritative when present
- **AND** the active local theme SHALL remain visually stable while synchronization completes.

#### Scenario: 主题切换失败可恢复

- **WHEN** an authenticated user changes theme and the backend persistence request fails
- **THEN** the Web client SHALL keep the local visual selection
- **AND** it SHALL show a recoverable error message using the existing toast or equivalent Design System feedback
- **AND** the error feedback SHALL automatically dismiss or provide an explicit close affordance
- **AND** the error feedback SHALL NOT persist indefinitely, stack repeatedly, or block the user from continuing management-side work.

#### Scenario: 主题切换重复失败不刷屏

- **WHEN** an authenticated user changes theme multiple times and multiple backend persistence attempts fail
- **THEN** the Web client SHALL avoid unbounded duplicate toast stacking
- **AND** the latest recoverable error feedback SHALL remain readable
- **AND** the management sidebar, routed page content, login/logout controls, and current page state SHALL remain usable.
