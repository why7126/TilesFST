## MODIFIED Requirements

### Requirement: 管理端列表基础组件展示

Design System SHALL provide a development preview or admin design acceptance area for reusable admin list foundation components and the `AdminListPage` page-level template contract. The preview SHALL cover `MetricCard`, `MetricCardGrid`, pagination-window examples, a complete admin list page sample, admin filter dropdown consistency examples, admin table column display rules, sticky action column behavior, and backend pagination contract examples without introducing new color tokens. Design System SHALL also maintain an admin list field display adapter checklist for image, name, and fallback display rules across admin list pages.

#### Scenario: 展示分页窗口边界
- **WHEN** 开发者或评审人员查看管理端列表基础组件示例
- **THEN** 页面 SHALL 展示分页窗口在首页附近、居中页和末页附近的最多 5 个页码示例

#### Scenario: 展示完整管理端列表样例
- **WHEN** 开发者或评审人员查看完整管理端列表样例
- **THEN** 页面 SHALL 展示标题模块、指标卡模块、筛选/搜索模块、列表模块
- **AND** 模块顺序 SHALL 为「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」
- **AND** 列表模块 SHALL include 表头 nowrap、普通字段单行截断、有效期双行例外、sticky action column、横向滚动和分页 DOM 示例

#### Scenario: 展示管理端列表边界态
- **WHEN** 开发者或评审人员查看管理端列表基础组件示例
- **THEN** 页面 SHALL 展示 loading、empty、error、单页分页和多页分页边界态
- **AND** 单页分页 SHALL 仍展示上一页/下一页禁用态和当前页 `1`
- **AND** 每个分页示例 SHALL 展示 `page-summary` 和 `page-right` 结构

#### Scenario: 建立管理端列表字段展示 adapter 检查表
- **WHEN** 团队为管理端列表新增、重构或回归展示字段
- **THEN** Design System SHALL provide an admin list field display adapter checklist
- **AND** the checklist SHALL cover image adapter, name adapter, and fallback adapter
- **AND** 每个章节 SHALL include 适用列表、检查项、期望表现、验证方式和强制/推荐/N/A 标记
- **AND** 首批覆盖列表 SHALL include 品牌列表、证书列表、SKU 列表和 Banner 列表

#### Scenario: 建立管理端列表列展示与分页契约
- **WHEN** 团队新增或修改 Banner、日志审计、用户管理或其它管理端列表
- **THEN** Design System SHALL provide an admin list column and pagination contract
- **AND** 表头和普通字段 SHALL default to nowrap / single-line display
- **AND** 长文本 SHALL use fixed width, max width, truncation, tooltip, title, or equivalent accessible strategy
- **AND** 有效期、投放周期或等价复合时间字段 MAY use two-line display only when the exception is documented
- **AND** 普通更新时间、创建时间、最后登录时间 SHALL remain single-line unless a documented exception exists
- **AND** sticky action column SHALL remain reachable during horizontal scrolling and SHALL NOT cover adjacent cells, filter overlays, dialogs, toasts, or pagination
- **AND** pagination DOM SHALL align with the user-management baseline using `page-summary` and `page-right`

#### Scenario: 建立真实分页契约
- **WHEN** 管理端列表声明支持分页
- **THEN** the list SHALL use backend pagination rather than fetching all rows and slicing on the client
- **AND** requests SHALL include page and page size parameters or project-equivalent names
- **AND** responses SHALL include current page rows and total count or project-equivalent fields
- **AND** filter, search, sort, page-size change, out-of-range page, empty result, and last-page deletion behavior SHALL be defined
- **AND** API contract changes SHALL update Pydantic Schema, OpenAPI, Orval, API docs, and tests

#### Scenario: 保留管理端列表横切 gate
- **WHEN** 后续 Change 基于检查表修改管理端列表页面
- **THEN** it SHALL reference `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- **AND** 分页 DOM SHALL align with the user-management baseline when list DOM changes
- **AND** 操作成功或失败反馈 SHALL use fixed toast without layout shift when feedback behavior changes
- **AND** 状态变更、启停、上架/下架、删除等危险操作 SHALL use Design System confirm modal
- **AND** implementation SHALL NOT introduce `window.confirm`

