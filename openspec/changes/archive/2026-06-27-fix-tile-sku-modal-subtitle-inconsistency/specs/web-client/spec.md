## ADDED Requirements

### Requirement: SKU 弹窗副标题 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）副标题与品牌新增弹窗的 UI 不一致问题：副标题 MUST 使用与管理端共享的 `.modal-desc` 样式（12px、`var(--admin-weak)`、上间距 8px）；弹窗头部 MUST 支持标题 + 副标题自适应高度。修复 MUST NOT 修改 SKU API、数据库、Orval 或 BUG-0011 弹窗滚动布局。

#### Scenario: SKU 弹窗使用共享 modal-desc

- **WHEN** 用户打开 SKU 新增或编辑弹窗
- **THEN** 标题下方副标题 MUST 使用 class `modal-desc`
- **AND** MUST NOT 使用未定义样式的 `modal-subtitle`

#### Scenario: 副标题 Typography 与品牌弹窗一致

- **WHEN** 并排对比 SKU 与品牌新增弹窗
- **THEN** 两弹窗副标题字号、颜色、行高与标题间距 MUST 视觉一致

#### Scenario: 弹窗头部自适应副标题

- **WHEN** 弹窗标题区包含副标题
- **THEN** `.modal-head` MUST 使用 `min-height: 64px` 与 `height: auto`
- **AND** 副标题 MUST 完整可见

#### Scenario: AC-023 副标题语义保留

- **WHEN** 用户阅读 SKU 新增弹窗副标题
- **THEN** 文案 MUST 说明弹窗内不提供状态选择

#### Scenario: 弹窗滚动与表单不回退

- **WHEN** 副标题修复合并后
- **THEN** BUG-0011 矮视口滚动与 BUG-0012 字段规则 MUST 保持可用
