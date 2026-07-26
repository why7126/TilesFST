## ADDED Requirements

### Requirement: 管理端 MetricCard 基础组件
Web 管理端 SHALL provide reusable `MetricCard` and `MetricCardGrid` or equivalent foundation components for admin list summary strips. The components MUST preserve the existing admin list DOM contract and MUST NOT change backend API behavior.

#### Scenario: 渲染指标卡 DOM 契约
- **WHEN** a Web admin list page renders a metric summary card through `MetricCard`
- **THEN** the rendered card SHALL include `.metric-card`, `.metric-label`, `.metric-value`, and `.metric-desc`
- **AND** it SHALL support `label`, `value`, and `description` content

#### Scenario: 指标卡状态展示
- **WHEN** metric data is empty, loading, or unavailable
- **THEN** `MetricCard` SHALL render a unified placeholder such as `—` or an equivalent loading/empty presentation
- **AND** danger or abnormal descriptions SHALL be visually distinguishable through semantic token or existing admin classes

#### Scenario: 指标卡容器布局
- **WHEN** an admin list page renders 2, 3, or 4 metric cards through `MetricCardGrid` or an equivalent container
- **THEN** the container SHALL preserve the `.summary-grid` contract
- **AND** it SHALL support an accessible label for the metric region

### Requirement: 管理端分页窗口工具
Web 管理端 SHALL provide a reusable pagination-window helper for admin list pages. The helper MUST default to at most 5 visible page numbers and MUST handle invalid input defensively.

#### Scenario: 总页数不超过窗口上限
- **WHEN** total pages are less than or equal to the visible window size
- **THEN** the helper SHALL return all page numbers from 1 through total pages

#### Scenario: 当前页靠近首页
- **WHEN** current page is near the beginning and total pages exceed the visible window size
- **THEN** the helper SHALL return a window starting at page 1 with at most 5 page numbers by default

#### Scenario: 当前页靠近末页
- **WHEN** current page is near the end and total pages exceed the visible window size
- **THEN** the helper SHALL return a window ending at the final page with at most 5 page numbers by default

#### Scenario: 当前页居中
- **WHEN** current page is away from both boundaries and total pages exceed the visible window size
- **THEN** the helper SHALL return a centered moving window around the current page with at most 5 page numbers by default

#### Scenario: 非法输入兜底
- **WHEN** current page, total pages, or max visible page count are outside valid ranges
- **THEN** the helper SHALL normalize inputs or return a safe single-page window without throwing during render

### Requirement: 管理端列表分页 DOM 契约
Web 管理端 list pages SHALL preserve the admin pagination structure used by the list-page consistency baseline.

#### Scenario: 渲染统一分页结构
- **WHEN** an applicable admin list page renders pagination
- **THEN** it SHALL include `.page-summary` for total or range copy
- **AND** it SHALL include `.page-right` containing `.page-buttons` and `.page-size-wrap`

#### Scenario: 不引入跳页输入框
- **WHEN** this change is implemented for admin list foundation components
- **THEN** it SHALL NOT introduce a jump-to-page input field
- **AND** it SHALL NOT introduce page-private pagination containers such as `brand-pagination-right`, `banner-pagination`, or `pagination-bar`

### Requirement: 管理端列表基础组件首批接入
Web 管理端 SHALL connect the foundation components to 2 to 3 baseline admin list pages while preserving each page's existing business behavior.

#### Scenario: 首批页面范围
- **WHEN** implementation selects baseline pages for this change
- **THEN** it SHALL choose 2 to 3 pages from `TileSkuManagementPage`, `LogAuditPage`, `ApiDocsPage`, and `BrandManagementPage`
- **AND** the selected set SHALL cover normal metrics, danger or abnormal metric descriptions, and pagination-window usage

#### Scenario: 页面业务行为不回归
- **WHEN** a selected baseline page migrates to the shared foundation components
- **THEN** its filtering, pagination state, empty state, permissions, and existing data behavior SHALL remain unchanged
- **AND** the change SHALL NOT modify backend pagination API, database schema, OpenAPI, or Orval generated clients

#### Scenario: 未接入页面追踪
- **WHEN** implementation completes the first batch
- **THEN** pages not included in the first batch SHALL be recorded as follow-up rollout items in trace or implementation notes
