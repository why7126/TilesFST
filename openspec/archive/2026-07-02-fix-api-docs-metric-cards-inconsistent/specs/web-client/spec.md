## ADDED Requirements

### Requirement: 管理端接口文档摘要指标卡一致性
The Web admin client SHALL render `/admin/api-docs` summary metric cards using the existing admin metric card structure and Design System styling baseline.

#### Scenario: Summary metric card DOM matches baseline
- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** each summary metric card SHALL use the existing `metric-card` pattern
- **AND** each card SHALL include `metric-label`, `metric-value`, and `metric-desc` elements
- **AND** the summary metric values SHALL NOT rely on bare `strong` elements as the only styling hook
- **AND** the summary descriptions SHALL NOT rely on bare `span` elements as the only styling hook.

#### Scenario: Summary metric visual hierarchy matches tile SKU page
- **WHEN** the `/admin/api-docs` summary metrics are compared with `/admin/tile-skus` summary metrics
- **THEN** the cards SHALL preserve the same border, background, radius, padding, value emphasis, and description hierarchy provided by the shared admin metric styles.

#### Scenario: Semantic styling retained
- **WHEN** implementing the summary metric fix
- **THEN** the Web client SHALL reuse existing semantic classes such as `summary-grid`, `metric-card`, `metric-label`, `metric-value`, and `metric-desc`
- **AND** TSX/CSS changes SHALL NOT introduce hard-coded design color hex values.

#### Scenario: API docs behavior does not regress
- **WHEN** the summary metric DOM is fixed
- **THEN** `/admin/api-docs` SHALL still display total routes, protected routes, Orval mapped routes, and non-`/api/v1` route counts
- **AND** route filtering, OpenAPI JSON access, Swagger UI/read-only policy, Orval method display, and missing method states SHALL continue to work.

#### Scenario: Permissions do not regress
- **WHEN** the summary metric DOM is fixed
- **THEN** `admin` users SHALL still access `/admin/api-docs`
- **AND** `employee` users SHALL still be denied direct access and SHALL NOT see the sidebar menu item
- **AND** shop-owner Web and WeChat miniapp clients SHALL NOT expose an API docs entry.
