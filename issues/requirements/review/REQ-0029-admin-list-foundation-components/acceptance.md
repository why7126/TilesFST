---
title: 验收标准
purpose: REQ-0029 管理端列表基础组件验收清单
content: 组件、分页工具、页面接入、设计验收、测试与知识库横切 AC
source: AI 根据 requirement.md、user-stories.md、business-flow.md 与 best-practices 生成
update_method: PRD、原型、OpenSpec 或 Sprint 评审变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 14:14:26
updated_at: 2026-07-05 14:14:26
note: REQ-0029-admin-list-foundation-components
---

# 验收标准

## 1. MetricCard

- [ ] AC-001 MUST 提供 `MetricCard` 或等价组件，用于管理端列表页指标摘要。
- [ ] AC-002 `MetricCard` MUST 稳定输出 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。
- [ ] AC-003 `MetricCard` MUST 支持 `label`、`value`、`description` 基础字段。
- [ ] AC-004 `MetricCard` MUST 对空值、加载中或未返回数据提供统一展示策略。
- [ ] AC-005 `MetricCard` SHOULD 支持 danger / 异常描述变体，并用于日志审计等异常指标。
- [ ] AC-006 `MetricCard` MUST 使用 semantic token 或既有管理端 class，不得新增裸 Hex 或页面私有颜色。

## 2. MetricCardGrid

- [ ] AC-007 MUST 提供 `MetricCardGrid` 或等价容器，减少页面重复书写 `summary-grid`。
- [ ] AC-008 `MetricCardGrid` MUST 支持 2、3、4 个指标卡布局。
- [ ] AC-009 `MetricCardGrid` MUST 支持 `aria-label` 标识指标区域。
- [ ] AC-010 指标卡容器替换后 MUST 不造成 hero、filter、table 的纵向位移。
- [ ] AC-011 指标卡容器 MUST 与现有管理端列表页 spacing、边框、圆角和字号保持一致。

## 3. 分页窗口工具

- [ ] AC-012 MUST 将分页窗口算法沉淀到共享工具或管理端共享层，禁止新页面继续从页面局部复制算法。
- [ ] AC-013 分页窗口工具默认 MUST 最多展示 5 个页码。
- [ ] AC-014 当总页数小于等于 5 时，分页窗口工具 MUST 展示全部页码。
- [ ] AC-015 分页窗口工具 MUST 对 `currentPage < 1`、`currentPage > totalPages`、`totalPages < 1`、`maxVisible < 1` 做兜底。
- [ ] AC-016 分页窗口工具测试 MUST 覆盖单页、首页附近、末页附近、当前页居中和非法输入。
- [ ] AC-017 迁移现有 `getPaginationWindow` 时 MUST 保留或补齐既有测试覆盖。

## 4. 管理端分页 DOM 契约

- [ ] AC-018 管理端列表页分页 MUST 保留 `.page-summary`。
- [ ] AC-019 管理端列表页分页 MUST 保留 `.page-right`。
- [ ] AC-020 管理端列表页分页 MUST 保留 `.page-buttons`。
- [ ] AC-021 管理端列表页分页 MUST 保留 `.page-size-wrap`。
- [ ] AC-022 本需求 MUST NOT 引入跳页输入框。
- [ ] AC-023 本需求 MUST NOT 新增页面私有分页容器，例如 `brand-pagination-right`、`banner-pagination`、`pagination-bar`。

## 5. 首批页面接入

- [ ] AC-024 首批接入页面 MUST 从 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`、`BrandManagementPage` 中选择 2–3 个。
- [ ] AC-025 首批接入 MUST 同时覆盖普通指标卡、danger / 异常描述和分页窗口。
- [ ] AC-026 首批页面替换后 MUST 保持原有筛选、分页状态、空态、权限逻辑不变。
- [ ] AC-027 未纳入首批的页面 MUST 在 trace 或实现任务中列为后续推广项，不得默认为已完成。

## 6. 设计系统与原型

- [ ] AC-028 `/design-system` 或管理端设计验收区 MUST 展示 `MetricCard` / `MetricCardGrid` 基础样例。
- [ ] AC-029 设计验收样例 SHOULD 展示正常数值、空值 / 加载中、danger 描述、2/3/4 卡布局。
- [ ] AC-030 设计验收样例 SHOULD 展示分页窗口边界，例如第 1 页、第 3 页、第 6 页、末页。
- [ ] AC-031 原型 context MUST 明确组件归属、页面接入策略、空态、loading、danger 描述和分页边界。
- [ ] AC-032 PNG Golden Reference 可在后续设计验收时导出；若无 PNG，本需求仍可进入评审但 readiness 标记为 Partially Ready。

## 7. 测试

- [ ] AC-033 MUST 为 `MetricCard` 增加渲染测试，检查 label、value、description 与关键 DOM class。
- [ ] AC-034 MUST 为分页窗口工具增加或迁移单元测试。
- [ ] AC-035 SHOULD 为首批接入页面保留结构测试，检查 `summary-grid`、`metric-card`、`page-summary`、`page-right`、`page-buttons`、`page-size-wrap`。
- [ ] AC-036 SHOULD 在实现完成后运行相关 Vitest 测试，并记录结果。

## 8. 非目标与影响边界

- [ ] AC-037 本需求 MUST NOT 修改后端分页 API。
- [ ] AC-038 本需求 MUST NOT 修改数据库表结构。
- [ ] AC-039 本需求 MUST NOT 修改 OpenAPI 或触发 Orval。
- [ ] AC-040 本需求 MUST NOT 引入新的颜色 Token 或全局主题变化；若需要 Token 变更，必须另走 Design System 变更流程。
- [ ] AC-041 本需求 MUST NOT 实现 toast、confirm modal、sticky action column 等其它横切能力；相关范围归属 `REQ-0028` 或后续独立需求。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 首批接入页面的分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 首批接入页面的指标摘要 DOM MUST 使用 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`。
- [ ] AC-XCUT-003 N/A — 本需求不新增操作成功 / 失败 toast；若首批页面接入过程中触碰查询、复制、加载失败反馈，反馈 MUST 使用 fixed toast 或等价固定层，不得造成 hero / 表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求不新增启停、冻结、上架 / 下架、删除、重置密码等状态变更操作；若首批页面接入触碰危险操作，MUST 使用 DS confirm modal，禁止 `window.confirm`。
- [ ] AC-XCUT-005 Vitest SHOULD 覆盖首批页面分页结构 smoke / snapshot，并检查指标卡 DOM 未从 `.metric-label` / `.metric-value` / `.metric-desc` 漂移。
