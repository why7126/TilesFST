## ADDED Requirements

### Requirement: 管理端内容区域布局回归测试

The testing capability SHALL include focused frontend regression coverage for BUG-0054 on the Web admin shell content padding and width strategy.

#### Scenario: Admin shell legacy padding is covered
- **WHEN** frontend tests or static style assertions inspect `admin-home.css`
- **THEN** they SHALL verify `.main-content` no longer uses the legacy `48px 56px 72px` desktop padding.

#### Scenario: Content-inner max width is covered
- **WHEN** frontend tests or static style assertions inspect admin shell styles
- **THEN** they SHALL verify `.content-inner` no longer uses `max-width: 1080px`
- **AND** they SHALL verify the chosen global strategy is `max-width: 100%` or `max-width: min(1440px, 100%)`.

#### Scenario: Page-level divergent width is covered
- **WHEN** frontend tests or static style assertions inspect admin page CSS
- **THEN** they SHALL verify SKU management does not keep a `1120px` `content-inner` override
- **AND** they SHALL verify system settings does not lock the full page content wrapper to `1080px`.

#### Scenario: Sidebar collapse behavior remains covered
- **WHEN** BUG-0054 tests are added or updated
- **THEN** existing `AdminSidebar.collapse.test.tsx` and `AdminLayout.test.tsx` assertions SHALL continue to pass
- **AND** sidebar width, collapsed state, and localStorage behavior SHALL not regress.

#### Scenario: Visual baseline pages are listed for manual validation
- **WHEN** implementation records validation results
- **THEN** it SHALL include `/admin/logs`, `/admin/tile-skus`, `/admin/users`, `/admin/dashboard`, and `/admin/settings`
- **AND** it SHOULD include 1440px, 1920px, collapsed, tablet, and mobile-smoke viewports.
