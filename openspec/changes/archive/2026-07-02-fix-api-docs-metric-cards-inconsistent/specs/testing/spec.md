## ADDED Requirements

### Requirement: 管理端接口文档摘要指标卡回归测试
The testing capability SHALL include focused frontend regression tests for `/admin/api-docs` summary metric card structure.

#### Scenario: Summary metric class structure tested
- **WHEN** frontend tests render `ApiDocsPage`
- **THEN** they SHALL verify the summary metric section contains metric value and description elements using `metric-value` and `metric-desc`
- **AND** the test SHOULD fail if the implementation regresses to summary cards that only expose bare `strong` and `span` styling hooks.

#### Scenario: Existing API docs behavior tests retained
- **WHEN** frontend tests are updated for this fix
- **THEN** existing assertions for Orval method display, the "未生成" state, route filtering, and production Swagger read-only behavior SHALL continue to pass.

#### Scenario: No backend or Orval regression required
- **WHEN** this change is implemented without API contract changes
- **THEN** no backend aggregation endpoint tests or Orval regeneration SHALL be required for this fix.
