## ADDED Requirements

### Requirement: 用户主题偏好持久化

The database capability MUST persist account-level user theme preference for Web theme switching. SQLite and MySQL schemas MUST remain aligned, and new users MUST default to `system`.

#### Scenario: 用户表包含主题偏好字段

- **WHEN** the application schema is initialized or migrated
- **THEN** the `users` table SHALL include a theme preference field equivalent to `theme_mode`
- **AND** the field SHALL default to `system`
- **AND** supported stored values SHALL be `system`, `dark_flagship`, `comfort_dark`, and `light`.

#### Scenario: SQLite 与 MySQL 保持一致

- **WHEN** database documentation or schema checks compare SQLite and MySQL support
- **THEN** both backends SHALL document and support the same theme preference field semantics
- **AND** implementation notes SHALL record any type or constraint differences.

#### Scenario: 主题偏好不影响认证安全字段

- **WHEN** a user updates theme preference
- **THEN** the system SHALL NOT modify password hash, token version, role, status, or protected account semantics
- **AND** theme preference SHALL NOT be treated as sensitive credential data.
