---
requirement_id: REQ-0028-admin-list-page-contract
title: AdminListPage 模板与管理端列表页契约验收标准
status: approved
created_at: 2026-07-05 10:18:38
updated_at: 2026-07-05 14:36:29
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001 `AdminListPage` 或等价模板 MUST 支持标题、说明、主操作、指标卡、筛选/搜索、表格列表、分页和 sticky action column 的标准组合。
- [ ] AC-002 模板默认模块顺序 MUST 为「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」。
- [ ] AC-003 模板输入类型 MUST 能描述标题、主操作、指标卡、筛选项、表格列、行数据、行操作、分页状态和空 / 加载 / 错误态。
- [ ] AC-004 业务页面 MAY 插入领域特有筛选项、列渲染和行操作，但 MUST NOT 破坏模块顺序、分页结构和操作列契约。
- [ ] AC-005 筛选/搜索模块 MUST 支持关键词、下拉、日期范围、状态 / 结果等常见筛选控件组合。
- [ ] AC-006 默认筛选区 MUST 保留统一「重置」按钮，并不得展示「查询」或「搜索」显式提交按钮，除非评审明确豁免。
- [ ] AC-007 筛选条件变化、点击重置、切换每页显示条数时 MUST 将当前页重置为第 1 页。
- [ ] AC-008 表格卡片上方 MUST NOT 出现与页面标题重复的列表标题、旧版 toolbar 或割裂 section heading。
- [ ] AC-009 表格最后一列存在行操作时，表头和表体 MUST 使用统一 sticky action column 契约。
- [ ] AC-010 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构。
- [ ] AC-011 分页页码按钮 MUST 使用 `page-buttons`、`page-btn`、`active` 或等价统一 class 契约。
- [ ] AC-012 分页最多展示 5 个可点击页码，不包含上一页 / 下一页按钮。
- [ ] AC-013 总页数为 1 时，分页 MUST 仍展示上一页 / 下一页禁用态和当前页 `1`。
- [ ] AC-014 `/design-system` MUST 增加 AdminListPage 验收样例或 Admin 管理端列表章节。
- [ ] AC-015 `/design-system` AdminListPage 样例 MUST 展示标题、指标卡、筛选区、表格、sticky 操作列和分页。
- [ ] AC-016 `/design-system` AdminListPage 样例 SHOULD 展示 loading、empty、error、单页分页、多页分页等边界态。
- [ ] AC-017 文档或样例 MUST 明确 BUG-0055 涉及页面矩阵：SKU、品牌、类目、规格、Banner、用户、日志、接口文档。
- [ ] AC-018 模板或等价组合 MUST 提供稳定 DOM 标识或 class 契约，便于 Vitest / Testing Library 定位。
- [ ] AC-019 后续实现 MUST 补充前端测试，覆盖模块顺序、筛选重置、分页窗口和 sticky action column。
- [ ] AC-020 本需求不应修改后端 API、数据库、MinIO、Docker Compose、店主 Web 展示端或微信小程序行为。

## UI AC

- [ ] AC-021 UI MUST 继承管理端暗色旗舰风与现有 Admin Shell，不得做营销式页面。
- [ ] AC-022 UI MUST 使用 Design System semantic token class，不得新增裸 Hex 色值。
- [ ] AC-023 UI MUST 使用 `cn()` 合并 className。
- [ ] AC-024 按钮、输入框、卡片、分页按钮的圆角、字号和间距 MUST 遵守 `rules/ui-design.md` 与既有管理端样式基线。
- [ ] AC-025 在 1366px、1440px、1920px 桌面宽度下，筛选区、表格、sticky 操作列和分页 MUST 不重叠、不裁切、不错位。
- [ ] AC-026 真实业务页迁移时 SHOULD 先选择 1 个代表页面做示范，再逐步推广。

## 安全与权限 AC

- [ ] AC-027 模板化 MUST 不改变管理端既有登录态、角色权限和路由守卫。
- [ ] AC-028 行操作的权限、禁用态、危险操作二次确认和业务规则 MUST 不回退。
- [ ] AC-029 样例数据 MUST 使用脱敏演示数据，不得包含真实客户、真实门店、真实账号、Token、Cookie、数据库连接串或 MinIO 凭据。

## 文档与追踪 AC

- [ ] AC-030 `trace.md` MUST 记录 `knowledge_base_refs` 与 `cross_cutting_tags`，供后续 `/req-opsx` design 引用。
- [ ] AC-031 后续 `/req-opsx` 生成 design.md 时 MUST 引用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`。
- [ ] AC-032 若实现阶段同步更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，MUST 保留其 Frontmatter 并刷新 `updated_at`。
- [ ] AC-033 若实现阶段调整 Design Token，MUST 同步 `src/shared/design-system/tokens/`、`globals.css` 或 `tokens.generated.css`。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003/004 管理端列表页一致性复发类缺陷

- [ ] AC-XCUT-001 新增或迁移的管理端列表页 MUST 与 `/admin/users` 基准保持分页 DOM 一致：左侧 `page-summary` 展示总数，右侧 `page-right` 承载页码与每页条数。
- [ ] AC-XCUT-002 摘要指标卡 DOM MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc` 或等价稳定结构，不得只复用外层 `.metric-card` 后用裸 `strong` / `span` 承载数值与说明。
- [ ] AC-XCUT-003 操作成功、失败、刷新或状态反馈 MUST 使用 fixed toast 或等价固定层，不得在 hero、筛选区、表格或分页之间插入文档流 notice 导致 layout shift。
- [ ] AC-XCUT-004 启停、冻结、上架 / 下架、删除、重置密码等状态变更或危险操作 MUST 使用 Design System confirm modal。
- [ ] AC-XCUT-005 管理端列表页 MUST NOT 使用 `window.confirm`、`window.alert` 或浏览器原生弹窗承载确认、成功、失败反馈。
- [ ] AC-XCUT-006 表格卡片内 MUST NOT 展示与 `page-head` / 标题模块重复的 section 标题。
- [ ] AC-XCUT-007 操作列中的启用、停用、上架、下架等条件和禁用态 SHOULD 对齐品牌管理页既有模式，避免同类操作语义漂移。
- [ ] AC-XCUT-008 新增管理端列表页 SHOULD 提供分页结构 smoke 或 snapshot 测试；若本期仅交付模板，则 MUST 覆盖模板分页结构测试。
