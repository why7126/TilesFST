---
requirement_id: REQ-0029-admin-list-foundation-components
title: 管理端列表基础组件（MetricCard 与分页窗口工具）
terminal: web-admin
version: v1
status: approved
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0028-admin-list-page-contract
created_at: 2026-07-05 07:56:48
updated_at: 2026-07-05 14:35:48
---

# REQ-0029 管理端列表基础组件（MetricCard 与分页窗口工具）

## 1. 需求背景

Sprint 004 复盘指出，SKU、品牌、类目、规格、Banner、用户、日志、接口文档等管理端列表页在标题、指标卡、筛选、表格、分页和操作列上反复出现局部 DOM 漂移。`REQ-0028-admin-list-page-contract` 已记录 `AdminListPage` 模板与管理端列表页契约需求，本需求作为其子需求，聚焦两个高频基础能力：

1. `MetricCard` / summary strip：统一管理端列表页的指标卡 DOM、文案层级、状态变体与空值表现。
2. 分页窗口工具：统一管理端列表页最多 5 个页码的窗口算法与分页结构，避免各页面重复手写。

当前仓库已经存在 `src/web/src/features/admin/lib/pagination.ts` 的 `getPaginationWindow` 与测试，说明分页算法已形成事实基础；同时多个页面仍在本地手写 `article.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。本需求目标不是发明新的页面形态，而是把已被 BUG 与复盘反复验证的隐性标准提升为可复用、可测试、可验收的共享事实源。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部管理员 / 运营员工 | 在管理端列表页获得一致的指标摘要与分页体验，减少页面间认知切换 |
| 前端开发人员 | 通过共享组件和工具减少重复 DOM 与分页算法复制，降低后续列表页实现成本 |
| QA / 评审人员 | 通过稳定 DOM class、测试用例和 `/design-system` 示例快速识别列表页一致性回归 |
| 产品负责人 | 将 Sprint 004 复盘行动项 A-003 落为可追踪需求，防止同类列表页 UI BUG 反复出现 |

## 3. 范围

### 3.1 本期包含

- 抽象管理端 `MetricCard` 组件，稳定输出 `metric-card`、`metric-label`、`metric-value`、`metric-desc` 等既有 DOM class。
- 抽象 `MetricCardGrid` 或等价容器，用于承载管理端列表页 2–4 个指标卡。
- 抽象分页窗口工具，统一处理当前页、总页数、最大可见页码数、页码边界与非法输入兜底。
- 明确分页窗口工具与现有 `Pagination` 组件的关系：管理端列表页需要保留 `page-summary`、`page-right`、`page-buttons`、`page-size-wrap` 等 DOM 契约；通用店主端分页可继续使用独立 `Pagination`。
- 首批替换 SKU、日志审计、接口文档或品牌中的 2–3 个基准页面，后续页面在 `REQ-0028` 的列表页契约中逐步推广。
- 为 `MetricCard` 与分页窗口工具补充 Vitest / Testing Library 测试。
- 在 `/design-system` 增加基础组件展示或在管理端设计验收区增加示例，覆盖空值、danger 描述、loading/占位、分页边界。
- 更新管理端列表页一致性知识库或设计系统说明的引用关系，具体更新范围在 `/req-complete` 阶段确认。

### 3.2 本期不包含

- 不重做完整 `AdminListPage` 模板；页面级契约由 `REQ-0028-admin-list-page-contract` 承载。
- 不一次性重构全部管理端列表页；首期以高复用页面为基准，分阶段推广。
- 不改变后端分页 API、数据库表结构或 OpenAPI / Orval 生成逻辑。
- 不引入新的视觉主题、颜色 Token 或全局 CSS Token。
- 不处理 toast、confirm modal、sticky action column 等其它横切能力；这些由 `REQ-0028` 或后续独立需求承载。

## 4. 现状与依赖

```text
REQ-0028 AdminListPage 模板与管理端列表页契约
└── REQ-0029 管理端列表基础组件
    ├── MetricCard / MetricCardGrid
    ├── PaginationWindow 工具
    ├── 管理端分页 DOM 契约
    └── /design-system 示例与测试
```

相关现状：

- `src/web/src/features/admin/lib/pagination.ts` 已存在 `getPaginationWindow(currentPage, totalPages, maxVisible = 5)`。
- `src/web/src/features/admin/lib/pagination.test.ts` 已覆盖单页、总页数不超过窗口、总页数超过窗口等场景。
- `src/web/src/shared/ui/pagination.tsx` 已存在通用 `Pagination`，但其 ellipsis 模型与管理端列表页“最多 5 个页码 + page-summary + page-size-wrap”的 DOM 契约并不完全一致。
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 已把 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc` 作为管理端列表页基准。

## 5. 功能要求

### FR-001 MetricCard 组件

- MUST 提供管理端可复用的 `MetricCard` 或等价组件。
- MUST 稳定输出以下 DOM class：`metric-card`、`metric-label`、`metric-value`、`metric-desc`。
- MUST 支持基础字段：`label`、`value`、`description`。
- SHOULD 支持描述变体：默认、危险/异常（如日志审计 API 错误、慢请求）。
- MUST 对空值、加载中或未返回数据提供统一展示策略，例如 `—` 或骨架/占位，具体策略在 `/req-complete` 阶段定稿。
- MUST 使用 semantic token 或既有管理端 class，不得新增裸 Hex、页面私有颜色或一次性样式。

### FR-002 MetricCardGrid / summary strip

- MUST 提供 `MetricCardGrid` 或等价容器，减少页面重复书写 `summary-grid`。
- MUST 支持 2–4 个指标卡的常规布局，并在移动宽度下保持可读。
- MUST 保持与现有管理端列表页视觉一致，避免因容器替换造成 hero、filter、table 的纵向位移。
- SHOULD 支持通过 `aria-label` 标识指标区域，例如 `SKU 统计`、`日志摘要`。

### FR-003 分页窗口工具

- MUST 将分页窗口算法沉淀为共享工具，避免继续在各页面复制或从 feature 私有目录导入。
- MUST 默认最多展示 5 个页码；当总页数小于等于 5 时展示全部页码。
- MUST 对 `currentPage < 1`、`currentPage > totalPages`、`totalPages < 1`、`maxVisible < 1` 等异常输入进行兜底。
- MUST 覆盖以下基础场景：
  - 单页返回 `[1]`。
  - 总页数等于窗口上限时返回完整页码。
  - 当前页靠近首页时从 1 开始。
  - 当前页靠近末页时以末页结束。
  - 当前页居中时窗口随当前页移动。
- SHOULD 保留现有 `getPaginationWindow` 的可理解 API，除非 `/req-complete` 明确需要更名或返回更丰富结构。

### FR-004 管理端分页 DOM 契约

- MUST 明确管理端列表页分页结构与通用 `Pagination` 组件的边界。
- 管理端列表页分页 SHOULD 保持：
  - 左侧 `page-summary` 展示 `共 N 条/个/...` 或范围文案。
  - 右侧 `page-right` 承载页码按钮与每页条数选择。
  - 页码按钮区域使用 `page-buttons`。
  - 每页条数区域使用 `page-size-wrap`。
- MUST NOT 在本需求中引入跳页输入框。
- MUST 避免重新出现页面私有分页容器，如 `brand-pagination-right`、`banner-pagination`、`pagination-bar` 等已被历史 BUG 标记的问题结构。

### FR-005 首批页面接入

- 首批接入页面 SHOULD 从以下页面中选择 2–3 个：
  - `TileSkuManagementPage`
  - `LogAuditPage`
  - `ApiDocsPage`
  - `BrandManagementPage`
- 首批页面 MUST 同时覆盖普通指标卡、异常/危险描述、管理端分页窗口。
- 首批页面替换后 MUST 保持原有业务行为、筛选条件、分页状态、空态和权限逻辑不变。
- 其它管理端列表页的批量推广 SHOULD 跟随 `REQ-0028` 的 `AdminListPage` 契约进行，不在本需求强行扩大范围。

### FR-006 设计系统展示

- MUST 在 `/design-system` 或管理端设计验收区展示 `MetricCard` / `MetricCardGrid` 的基础样例。
- SHOULD 展示以下状态：
  - 正常数值。
  - 空值或加载中占位。
  - danger/异常描述。
  - 2、3、4 卡片布局。
- SHOULD 展示分页窗口边界样例，便于评审最多 5 页码与边界移动规则。

### FR-007 测试要求

- MUST 保留或迁移现有分页窗口测试，确保路径迁移不丢覆盖。
- MUST 为 `MetricCard` 增加渲染测试，检查 label、value、description 与关键 DOM class。
- SHOULD 为首批接入页面保留列表页结构测试，确保 `summary-grid`、`metric-card`、`page-summary`、`page-right`、`page-buttons`、`page-size-wrap` 未回归。
- UI 视觉变化完成后 SHOULD 在 `REQ-0028` 或本需求后续验收中记录 `/design-system` 或页面截图验收结果。

## 6. UI 约束

- MUST 遵守 `rules/ui-design.md` 的工业石材 · 暗色旗舰风。
- MUST 优先使用 `src/web/src/shared/ui/`、`src/web/src/shared/templates/` 与 shadcn 基础组件，不在业务页面内重复实现通用组件。
- MUST 使用 `cn()` 合并 `className`。
- MUST 使用 semantic token class 或既有管理端 class，禁止新增裸 Hex、硬编码 rgba 颜色或一次性全局 CSS 覆盖。
- 卡片圆角、边框、字号和间距 MUST 与现有管理端列表页视觉一致；若需要 Token 变更，必须另走 Design System 变更流程。
- 新组件 SHOULD 保持既有 DOM class 兼容，以降低从页面手写 DOM 迁移到共享组件的回归风险。

## 7. 关联需求与缺陷

| 类型 | ID | 关系 |
|---|---|---|
| 父需求 | REQ-0028-admin-list-page-contract | 管理端列表页模板、页面矩阵与横切契约 |
| 上级治理 | REQ-0000-build-design-system | Design System 与组件治理来源 |
| 关联缺陷 | BUG-0055-admin-list-layout-unification | 管理端列表页横切不一致复盘来源 |
| 相关知识库 | docs/knowledge-base/best-practices/admin-list-page-consistency.md | 管理端列表页 DOM 与验收基准 |

## 8. 状态块

| 字段 | 值 |
|---|---|
| 当前状态 | approved |
| 生命周期阶段 | plan |
| 是否可进入 `/req-complete` | 是 |
| 是否可进入 `/req-opsx` | 是 |
| 是否已纳入 Sprint | 否 |
| 是否影响接口 | 否 |
| 是否影响数据库 | 否 |
| 是否需要 Orval | 否 |
| 是否需要 Docker Compose 验证 | 否 |
| 是否影响 Web 管理端 | 是 |
| 是否影响店主 Web / 小程序 | 否 |
