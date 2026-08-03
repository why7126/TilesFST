## MODIFIED Requirements

### Requirement: 管理端列表基础组件展示

Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components and the `AdminListPage` page-level template contract. The preview SHALL cover `MetricCard`, `MetricCardGrid`, pagination-window examples, a complete admin list page sample, and admin filter dropdown consistency examples without introducing new color tokens.

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

#### Scenario: 展示管理端筛选下拉一致性样例
- **WHEN** 开发者或评审人员访问 `/design-system` 或等效管理端设计验收区
- **THEN** 页面 SHALL 展示管理端筛选下拉基准样例，覆盖普通下拉、可搜索下拉、空态、加载态、禁用态和已选中态
- **AND** 样例 SHALL 以瓷砖类目页筛选下拉的触发位置、控件尺寸、弹层对齐、宽度策略和状态样式作为管理端筛选区基准
- **AND** 样例 SHALL 标注 BUG-0098 覆盖页面矩阵：`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/brand-certificates`、`/admin/banners`、`/admin/users`、`/admin/settings`、`/admin/logs`、`/admin/api-docs` 与界面主题入口

### Requirement: 管理端列表组件语义样式

Design System SHALL require admin list foundation components, admin filter dropdowns, and the `AdminListPage` template to use semantic token classes, CSS variables, `cn()` class merging, or existing admin list classes, and SHALL NOT introduce raw Hex colors or one-off hardcoded color values in Web UI implementation.

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

#### Scenario: 管理端筛选下拉样式一致
- **WHEN** 开发者实现或修改管理端筛选区内的 Select、Dropdown、Popover、Combobox、date picker 或等价筛选下拉控件
- **THEN** implementation SHALL use the shared admin filter dropdown pattern, shared UI component, or an equivalent wrapper aligned with the tile category page baseline
- **AND** implementation SHALL use semantic token classes, CSS variables, `cn()` class merging, or existing admin list classes for control background, border, focus, text, icon, option, hover, selected, disabled, empty, loading, shadow, and overlay styling
- **AND** implementation SHALL NOT add raw Hex colors, token-equivalent hardcoded colors, or page-local dropdown styles that diverge from the shared admin filter baseline

#### Scenario: 管理端筛选下拉弹层不裁切
- **WHEN** a filter dropdown opens on an admin page
- **THEN** the overlay SHALL align to the trigger according to the tile category page baseline
- **AND** the overlay SHALL not be clipped by tables, page containers, scroll regions, dialogs, or sticky action columns
- **AND** desktop and narrow admin viewports SHALL not show text overflow, incoherent overlap, unreachable options, or layout shift caused by the dropdown

### Requirement: 管理端列表组件测试治理

Design System SHALL include test expectations for admin list foundation components, admin filter dropdowns, and the `AdminListPage` template so DOM contracts remain stable across list pages.

#### Scenario: 指标卡渲染测试
- **WHEN** `MetricCard` is rendered in tests
- **THEN** tests SHALL assert label, value, description, and `.metric-card`, `.metric-label`, `.metric-value`, `.metric-desc` DOM classes

#### Scenario: 展示页结构测试
- **WHEN** the design-system or admin design acceptance example renders foundation components
- **THEN** tests SHOULD assert the example includes normal, empty/loading, danger, and multi-card states

#### Scenario: 管理端筛选下拉交互测试
- **WHEN** admin filter dropdown components or equivalent wrappers are changed
- **THEN** tests SHALL cover open, select, clear, reset, disabled, empty, loading, and selected states
- **AND** tests SHALL verify existing filter query parameter names and result semantics are not changed by the UI refactor

#### Scenario: 管理端筛选下拉视觉 smoke
- **WHEN** BUG-0098 is implemented
- **THEN** Web visual smoke or Playwright checks SHALL cover desktop and narrow admin viewports for at least tile categories plus representative pages from brand, tile spec, brand certificate, Banner, user, logs, API docs, settings, or theme surfaces
- **AND** checks SHALL confirm dropdown overlays are visible, aligned, not clipped, and do not introduce layout shift
