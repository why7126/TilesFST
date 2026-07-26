## ADDED Requirements

### Requirement: 管理端列表页一致性回归测试

The testing capability SHALL include focused frontend regression coverage for BUG-0055 on Web admin list page layout order, filter/search behavior, sticky action columns, and pagination window behavior.

#### Scenario: Module order is covered

- **WHEN** frontend tests render affected Web admin list pages
- **THEN** they SHALL verify the DOM order is title module, metrics module, filter/search module, then list module
- **AND** they SHALL cover SKU, brand, category, spec, banner, user, log audit, and API docs pages where practical.

#### Scenario: Query buttons are removed

- **WHEN** frontend tests render affected filter/search modules
- **THEN** they SHALL verify no visible button named 「查询」 or 「搜索」 is rendered
- **AND** they SHALL verify a reset button remains available.

#### Scenario: Pagination window is covered

- **WHEN** frontend tests exercise pagination helpers or page components
- **THEN** they SHALL verify at most 5 clickable page number buttons are rendered
- **AND** they SHALL cover total page counts of 1, 5, and 6 or more
- **AND** they SHALL verify page size changes reset current page to 1.

#### Scenario: Filter reset behavior is covered

- **WHEN** frontend tests update filters or click reset
- **THEN** they SHALL verify current page returns to 1
- **AND** list result calculation or request parameters SHALL reflect the changed filters.

#### Scenario: Sticky action column contract is covered

- **WHEN** frontend tests render affected admin tables
- **THEN** they SHALL verify the last header and body cells use the sticky action column contract
- **AND** they SHALL verify existing action disabled states and confirmation flows remain test-covered where already present.
