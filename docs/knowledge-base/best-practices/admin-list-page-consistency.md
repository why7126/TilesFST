---
title: 管理端列表页一致性最佳实践
purpose: 预防管理端多列表页分页、反馈、操作列重复不一致类 BUG
content: 提炼自 Sprint 002 BUG-0002、0009、0015、0016 等
source: /sprint-exps sprint-002
update_method: 新模式或新页面时更新
owner: 前端负责人
status: draft
created_at: 2026-06-27 16:15:00
updated_at: 2026-08-12 14:56:00
note: Sprint 015 补充 BUG-0098 管理端筛选下拉统一 gate；Sprint 023 补充 REQ-0112 列展示与分页契约
---

# 管理端列表页一致性最佳实践

## 背景

Sprint 002 中用户、品牌、类目、SKU 四个列表页分别 port CSS，导致：

- 分页 DOM 与用户管理基准不一致（`BUG-0009`）
- 文档流 `.admin-notice` 推挤布局（`BUG-0015`，与 `BUG-0003` 同类）
- 状态操作缺少二次确认（`BUG-0016`）
- 停用行操作列逻辑与品牌页不一致（`BUG-0001`、`BUG-0014`）

**Sprint 003 复发**（`best-practices` 未在 apply 前强制）：

- 瓷砖规格、Banner 列表分页 DOM 与用户管理不一致（`BUG-0027`、`BUG-0030`）
- Banner 列表第一列结构未按 Golden 拆分「展示位置」列（`BUG-0039`）

## 必须对齐的基准

**视觉与 DOM 基准页**：`/admin/users`（`UserManagementPage` + `user-management.css`）

| 区域 | 要求 |
|------|------|
| 摘要指标卡 | 使用 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`，禁止只复用外层 `metric-card` 后用裸 `strong` / `span` 承载数值与说明 |
| 分页 | 左侧 `page-summary`「共 N 条/个」；右侧 `page-right` 页码 + 每页条数 |
| 表格卡片 | `table-card` 内 **无** 与 `page-head` 重复的 section 标题 |
| 筛选下拉 | 使用统一筛选下拉组件或 shared admin filter select；触发框、弹层宽度、边界对齐、选项状态、重置态、空态、加载态和窄屏行为必须与瓷砖类目页基准一致 |
| 操作反馈 | **fixed toast**（`fix-admin-list-status-toast-layout`），禁止 hero 前文档流 notice |
| 危险操作 | 启停、冻结、上架/下架、删除、重置密码 **MUST** DS confirm modal |
| 操作列 | 启用/停用/上架条件 **对齐品牌管理** 模式（对照 `BrandManagementPage`） |
| 列展示 | 表头与普通字段默认 nowrap；长文本使用固定宽度、ellipsis、tooltip/title 或等价策略 |
| 有效期例外 | 仅有效期、投放周期等复合时间字段允许双行；普通更新时间、创建时间、最后登录保持单行 |
| 真实分页 | 列表页必须使用后端真实分页与真实 total；禁止全量拉取后前端切片伪分页 |

## 实现优先级

```text
1. src/web/src/shared/templates/AdminListPage（或等价模板）
2. 共享 FixedAdminToast + AdminConfirmModal
3. 共享列展示契约 class：`admin-list-cell-nowrap`、`admin-list-cell-truncate`、`admin-list-cell-multiline-exception`
4. 单页 port CSS 仅覆盖页面特有列、有效期例外与筛选，不重写分页/notice
```

## Apply 前必读 Gate

凡 OpenSpec Change 新增或修改管理端筛选区内的 Select、Dropdown、Popover、Combobox、date picker、可搜索下拉或等价筛选下拉控件，`/opsx-apply` MUST 在编辑 `src/` 前命中 `admin-filter-dropdown` 横切标签并回读本文档。

门禁结论必须记录：

- `best-practice read`：已回读本文档或继任最佳实践。
- `shared component reuse`：优先使用 `AdminFilterSelect`、`SearchableSelect` 或与瓷砖类目页基准对齐的 shared wrapper；若使用等价 wrapper，必须说明原因。
- `page-local overlay CSS`：不得新增页面级一次性弹层、裸 Hex、token 等价硬编码颜色或偏离共享基准的 native control。
- `state coverage`：覆盖普通下拉、可搜索下拉（如适用）、禁用态、已选中态、空态、加载态、清空/重置态、focus/hover 与窄屏行为。
- `overlay clipping`：弹层必须与触发框对齐，且不被表格、滚动容器、弹窗、sticky action column 或页面容器裁切。
- `query semantics`：筛选 query 参数名、结果语义、分页重置、权限边界、错误态和空态恢复不得因 UI 统一漂移。
- `regression test plan`：至少覆盖共享组件或一个代表页面的 DOM class、open/select/clear/reset 和相关状态。

## 列展示与分页契约 Gate

来源：`REQ-0112-admin-list-column-pagination-consistency-contract` / sprint-022 T-002。

凡新增或修改管理端列表页、共享表格模板、分页组件、列数量、sticky 操作列或列表数据加载方式，`/opsx-apply` MUST 记录以下结论：

- `column nowrap`：表头与普通字段默认单行；长文本使用截断、tooltip/title 或等价可访问策略。
- `multi-line exception`：仅有效期、投放周期等复合时间字段可双行；新增例外必须写明理由。
- `sticky action column`：横向滚动、窄屏、hover/focus、disabled/loading 下操作入口可达，不遮挡筛选弹层、弹窗、toast 或分页。
- `pagination DOM`：继续使用 `page-summary` + `page-right`，展示后端真实 total、页码和每页条数。
- `backend pagination`：列表请求带 page/page_size 或等价参数；响应使用后端 total，不以全量数据前端切片作为验收证据。
- `test coverage`：至少覆盖分页 DOM、筛选/搜索/每页条数变化后的页码重置、nowrap/sticky 关键 class 或行为；API 变更时同步后端测试、OpenAPI 与 Orval。

## 验收 gate（新增列表页 MUST）

- [ ] 1440×1024 与用户管理分页 DOM 并排 diff pass
- [ ] 摘要指标卡 DOM 使用 `.metric-label` / `.metric-value` / `.metric-desc`，与 SKU/用户管理基准一致
- [ ] 筛选下拉命中 `admin-filter-dropdown` apply gate，复用 `AdminFilterSelect`、`SearchableSelect` 或有等价 shared wrapper 理由
- [ ] 筛选下拉不使用页面级一次性弹层样式；弹层不被表格、滚动容器、弹窗或 sticky action column 裁切
- [ ] 筛选下拉测试覆盖 open/select/clear/reset、禁用态、已选中态、空态、加载态和筛选 query 语义不变
- [ ] 操作成功/失败 toast 不引起 hero/表格纵向位移
- [ ] 状态变更类操作均有 confirm；无 `window.confirm`
- [ ] 表头与普通字段默认 nowrap；长文本不撑宽整表，不挤压操作列
- [ ] 有效期/投放周期双行例外已明确，普通时间字段保持单行
- [ ] sticky 操作列在横向滚动和窄屏下可达，不遮挡筛选弹层、弹窗、toast 或分页
- [ ] 后端真实分页参数与 total 展示已验证；无前端全量切片伪分页
- [ ] Vitest：分页结构、列展示契约、sticky 操作列和状态操作 smoke 或 snapshot

## 关联 BUG（个案）

- `issues/bugs/archive/BUG-0002-brand-ui-inconsistency/`
- `issues/bugs/archive/BUG-0009-tile-sku-list-ui-inconsistency/`
- `issues/bugs/archive/BUG-0015-admin-list-status-tips-layout-shift/`
- `issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/`
- `issues/bugs/archive/BUG-0027-tile-spec-list-ui-inconsistency/`（Sprint 003）
- `issues/bugs/archive/BUG-0030-banner-list-ui-inconsistency/`（Sprint 003）
- `issues/bugs/archive/BUG-0039-banner-list-display-position-column/`（Sprint 003）
- `issues/bugs/archive/BUG-0052-api-docs-metric-cards-inconsistent/`（Sprint 004）
- `issues/bugs/archive/BUG-0098-admin-filter-dropdown-ui-consistency/`（Sprint 015）
- `issues/requirements/archive/REQ-0112-admin-list-column-pagination-consistency-contract/`（Sprint 023）

## 参考

- `rules/ui-design.md` 管理端列表章节
- `iterations/archive/sprint-002/retrospectives` → `sprint-002-retrospective.md` §4
