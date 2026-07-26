## MODIFIED Requirements

### Requirement: 管理端列表基础组件展示

Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components and the `AdminListPage` page-level template contract. The preview SHALL cover `MetricCard`, `MetricCardGrid`, pagination-window examples, and a complete admin list page sample without introducing new color tokens.

#### Scenario: 展示指标卡基础状态
- **WHEN** 开发者或评审人员访问 `/design-system` 或等效管理端设计验收区
- **THEN** 页面 SHALL 展示 `MetricCard` / `MetricCardGrid` 的正常数值、空值或 loading 占位、danger 描述状态
- **AND** 示例 SHALL 覆盖 2、3、4 个指标卡布局

#### Scenario: 展示分页窗口边界
- **WHEN** 开发者或评审人员查看管理端列表基础组件示例
- **THEN** 页面 SHALL 展示分页窗口在首页附近、居中页和末页附近的最多 5 个页码示例
- **AND** 示例 SHALL 保留 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` DOM 契约

#### Scenario: 展示 AdminListPage 页面样例
- **WHEN** 开发者或评审人员访问 `/design-system` 的 AdminListPage 验收样例
- **THEN** 页面 SHALL 展示标题模块、指标卡模块、筛选/搜索模块、表格列表模块、sticky action column 与分页模块
- **AND** 模块顺序 SHALL 为「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」
- **AND** 示例 SHALL 标注 BUG-0055 涉及页面矩阵：`/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`

#### Scenario: 展示 AdminListPage 边界态
- **WHEN** 开发者或评审人员查看 AdminListPage 验收样例
- **THEN** 页面 SHALL 展示 loading、empty、error、单页分页和多页分页边界态
- **AND** 单页分页 SHALL 仍展示上一页/下一页禁用态和当前页 `1`

### Requirement: 管理端列表组件语义样式

Design System SHALL require admin list foundation components and the `AdminListPage` template to use semantic token classes, CSS variables, `cn()` class merging, or existing admin list classes, and SHALL NOT introduce raw Hex colors or one-off hardcoded color values in Web UI implementation.

#### Scenario: 新增指标卡组件样式
- **WHEN** 开发者实现或修改 `MetricCard`、`MetricCardGrid` 或 pagination-window presentation
- **THEN** implementation SHALL use semantic token classes or existing admin classes for color, border, radius, typography, and spacing
- **AND** TSX/CSS implementation SHALL NOT add raw Hex values or token-equivalent hardcoded `rgba(...)` colors

#### Scenario: 类名合并
- **WHEN** admin list foundation components accept custom `className`
- **THEN** implementation SHALL merge classes through `cn()` from `@/shared/lib/cn`

#### Scenario: AdminListPage 模板样式
- **WHEN** 开发者实现或修改 `AdminListPage`、`AdminListPageContent` 或等价模板组合
- **THEN** implementation SHALL use semantic token classes such as `bg-page`, `bg-surface`, `text-primary`, `text-secondary`, `border-border-default`, `rounded-card`, or existing admin list classes
- **AND** implementation SHALL merge configurable class names through `cn()`
- **AND** implementation SHALL NOT copy raw Hex values from the prototype into TSX/CSS

### Requirement: 管理端列表组件测试治理

Design System SHALL include test expectations for admin list foundation components and the `AdminListPage` template so DOM contracts remain stable across list pages.

#### Scenario: 指标卡渲染测试
- **WHEN** `MetricCard` is rendered in tests
- **THEN** tests SHALL assert label, value, description, and `.metric-card`, `.metric-label`, `.metric-value`, `.metric-desc` DOM classes

#### Scenario: 展示页结构测试
- **WHEN** the design-system or admin design acceptance example renders foundation components
- **THEN** tests SHOULD assert the example includes normal, empty/loading, danger, and multi-card states

#### Scenario: AdminListPage 模板结构测试
- **WHEN** `AdminListPage` or an equivalent template composition is rendered in tests
- **THEN** tests SHALL assert the module order is title, metrics, filters, list, and pagination
- **AND** tests SHALL assert pagination includes `page-summary`, `page-right`, `page-buttons`, and current `page-btn active` or equivalent roles/classes
- **AND** tests SHALL assert rows with actions expose a sticky action column contract
