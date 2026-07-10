## ADDED Requirements

### Requirement: 管理端列表基础组件展示
Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components, covering `MetricCard`, `MetricCardGrid`, and pagination-window examples without introducing new color tokens.

#### Scenario: 展示指标卡基础状态
- **WHEN** 开发者或评审人员访问 `/design-system` 或等效管理端设计验收区
- **THEN** 页面 SHALL 展示 `MetricCard` / `MetricCardGrid` 的正常数值、空值或 loading 占位、danger 描述状态
- **AND** 示例 SHALL 覆盖 2、3、4 个指标卡布局

#### Scenario: 展示分页窗口边界
- **WHEN** 开发者或评审人员查看管理端列表基础组件示例
- **THEN** 页面 SHALL 展示分页窗口在首页附近、居中页和末页附近的最多 5 个页码示例
- **AND** 示例 SHALL 保留 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` DOM 契约

### Requirement: 管理端列表组件语义样式
Design System SHALL require admin list foundation components to use semantic token classes, CSS variables, or existing admin list classes, and SHALL NOT introduce raw Hex colors or one-off hardcoded color values in Web UI implementation.

#### Scenario: 新增指标卡组件样式
- **WHEN** 开发者实现或修改 `MetricCard`、`MetricCardGrid` 或 pagination-window presentation
- **THEN** implementation SHALL use semantic token classes or existing admin classes for color, border, radius, typography, and spacing
- **AND** TSX/CSS implementation SHALL NOT add raw Hex values or token-equivalent hardcoded `rgba(...)` colors

#### Scenario: 类名合并
- **WHEN** admin list foundation components accept custom `className`
- **THEN** implementation SHALL merge classes through `cn()` from `@/shared/lib/cn`

### Requirement: 管理端列表组件测试治理
Design System SHALL include test expectations for admin list foundation components so DOM contracts remain stable across list pages.

#### Scenario: 指标卡渲染测试
- **WHEN** `MetricCard` is rendered in tests
- **THEN** tests SHALL assert label, value, description, and `.metric-card`, `.metric-label`, `.metric-value`, `.metric-desc` DOM classes

#### Scenario: 展示页结构测试
- **WHEN** the design-system or admin design acceptance example renders foundation components
- **THEN** tests SHOULD assert the example includes normal, empty/loading, danger, and multi-card states
