## ADDED Requirements

### Requirement: 管理端重置密码结果复制兜底

Web 客户端 SHALL use the shared Clipboard copy helper or an equivalent normalized copy pattern when copying generated reset passwords from the user-management reset-password result dialog. The dialog SHALL preserve manual-copy fallback behavior when automatic Clipboard writing is unavailable or fails.

#### Scenario: 重置密码自动复制成功

- **WHEN** an admin copies a generated reset password and Clipboard writing succeeds
- **THEN** the dialog SHALL show a success status such as `密码已复制`
- **AND** it SHALL keep existing guidance that the password must be safely delivered and cannot be viewed again after closing.

#### Scenario: 重置密码自动复制失败

- **WHEN** Clipboard API is unavailable or Clipboard writing fails while copying a generated reset password
- **THEN** the dialog SHALL focus and select the generated password input or provide an equivalent manual-copy path
- **AND** the dialog SHALL show manual-copy guidance using `role="status"` or an equivalent accessible feedback pattern
- **AND** it SHALL NOT log or emit the generated password as telemetry.

#### Scenario: 重置密码弹窗布局不回归

- **WHEN** the reset-password result dialog displays copy success, failure, or manual fallback guidance
- **THEN** the modal width, body scroll, input visibility, and footer buttons SHALL remain stable and reachable
- **AND** the implementation SHALL NOT use `window.confirm` for this copy flow.

### Requirement: Web 管理端复制交互复用边界

Web 管理端 copy interactions SHALL prefer the shared Clipboard copy helper or an equivalent normalized pattern when adding or refactoring copy buttons for already-authorized visible text.

#### Scenario: 新增管理端复制入口

- **WHEN** developers add a new admin copy action for visible text
- **THEN** the implementation SHALL use the shared Clipboard helper or document why an equivalent platform-specific path is required
- **AND** it SHALL handle success, API unavailable, write failure, empty value, and manual-copy fallback where applicable.

#### Scenario: 店主 Web 与小程序边界

- **WHEN** this change is implemented
- **THEN** Web catalog and miniapp copy behavior SHALL remain unchanged
- **AND** miniapp Clipboard API adaptation SHALL require a separate requirement or change.
