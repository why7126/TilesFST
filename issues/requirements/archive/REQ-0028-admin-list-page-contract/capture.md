---
req_id: REQ-0028-admin-list-page-contract
status: captured
created_at: 2026-07-04 15:17:26
updated_at: 2026-07-04 15:17:26
recorded_by: product
source: Sprint 004 复盘行动项 / 用户输入
priority_hint: P1
parent_requirement: REQ-0000-build-design-system
---

# 一句话

落地 `AdminListPage` 模板、管理端列表页契约与设计验收页示例，将 BUG-0055 的跨页面一致性经验沉淀为后续管理端列表页面的可复用事实源。

# 原始描述

AdminListPage 模板与验收页，落地 AdminListPage / 管理端列表页契约，吸收 BUG-0055 经验。

补充上下文：

- Sprint 004 复盘行动项 A-002：落地 `AdminListPage` / 管理端列表页契约，吸收 BUG-0055 经验；建议下一步为 `/req-capture` AdminListPage 模板与验收页。
- BUG-0055 指出管理端列表页缺少统一结构和横切验收，导致 SKU、品牌、类目、规格、Banner、用户、日志、接口文档等页面在模块顺序、筛选/搜索、sticky action column 与分页窗口上持续分叉。
- 当前仓库已有 `src/web/src/shared/templates/admin-list-page.tsx` 初始模板，但尚未形成覆盖管理端列表页的完整契约、页面矩阵、验收页示例和后续新增页面的强制复用门禁。

# 待澄清

- [ ] `AdminListPage` 契约首批强制覆盖哪些页面：SKU、品牌、类目、规格、Banner、用户、日志、接口文档是否全部纳入。
- [ ] 契约是否同时包含 `MetricCard`、`PaginationWindow`、sticky action column 等基础组件，或将这些拆为后续独立 REQ。
- [ ] `/design-system` 验收页应展示静态模板样例，还是接入真实管理端列表页面的可视矩阵。
- [ ] 后续实现是增强现有 `src/web/src/shared/templates/admin-list-page.tsx`，还是新增更细粒度的 `shared/ui` 组件组合。
- [ ] 是否需要同步更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 `src/shared/design-system/spec.md`。

# 探索结论

（/req-explore 后人工确认写入）
