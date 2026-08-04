## MODIFIED Requirements

### Requirement: 管理端列表基础组件展示

Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components and the `AdminListPage` page-level template contract. The preview SHALL cover `MetricCard`, `MetricCardGrid`, pagination-window examples, a complete admin list page sample, and admin filter dropdown consistency examples without introducing new color tokens. Design System SHALL also maintain an admin list field display adapter checklist for image, name, and fallback display rules across admin list pages.

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

#### Scenario: 建立管理端列表字段展示 adapter 检查表
- **WHEN** 团队为管理端列表新增、重构或回归展示字段
- **THEN** Design System SHALL provide an admin list field display adapter checklist
- **AND** 检查表 SHALL include `image adapter`、`name adapter`、`fallback adapter` 三个章节
- **AND** 每个章节 SHALL include 适用列表、检查项、期望表现、验证方式和强制/推荐/N/A 标记
- **AND** 首批覆盖列表 SHALL include 品牌列表、证书列表、SKU 列表和 Banner 列表

#### Scenario: 检查 image adapter 展示规则
- **WHEN** 管理端列表展示图片字段、缩略图、主图或文件预览
- **THEN** 检查表 SHALL require 缩略图优先、原图兜底、主图选择、无图态、加载失败态、容器尺寸和可访问性语义检查
- **AND** 多图对象 SHALL define 主图优先规则，例如优先 `is_main`，否则使用排序或第一张兜底
- **AND** 图片缺失或加载失败 SHALL NOT change 表格行高、列宽、操作列可用性或分页布局

#### Scenario: 检查 name adapter 展示规则
- **WHEN** 管理端列表展示主名称、辅助名称、编号或关联对象名称
- **THEN** 检查表 SHALL require 主名称来源、辅助名称来源、空名称兜底、长名称截断和重复字段去重检查
- **AND** 关联对象缺失 SHALL have 明确可读的兜底展示
- **AND** 长名称 SHALL NOT 撑开表格列宽或遮挡后续字段

#### Scenario: 检查 fallback adapter 展示规则
- **WHEN** 管理端列表遇到空字段、未设置、无数据、不适用、加载失败、未知枚举值或无权限字段
- **THEN** 检查表 SHALL distinguish these fallback semantics rather than using one ambiguous display for all cases
- **AND** 接口字段缺失或值不可解析 SHALL NOT crash the page
- **AND** 无权限字段 SHALL NOT leak sensitive information

#### Scenario: 保留管理端列表横切 gate
- **WHEN** 后续 Change 基于检查表修改管理端列表页面
- **THEN** 验收 SHALL include `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 的横切 gate
- **AND** 分页 DOM SHALL align with the user-management baseline when list DOM changes
- **AND** 操作成功或失败反馈 SHALL use fixed toast without layout shift when feedback behavior changes
- **AND** 状态变更、启停、上架/下架、删除等危险操作 SHALL use Design System confirm modal
- **AND** implementation SHALL NOT introduce `window.confirm`
