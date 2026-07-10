---
req_id: REQ-0029-admin-list-foundation-components
status: captured
created_at: 2026-07-04 15:22:32
updated_at: 2026-07-04 15:22:32
recorded_by: product
source: Sprint 004 复盘行动项 / 用户输入
priority_hint: P1
parent_requirement: REQ-0028-admin-list-page-contract
---

# 一句话

抽象管理端列表基础组件与工具，包括 `MetricCard` 和分页窗口工具，减少 SKU、品牌、类目、规格、Banner、用户、日志、接口文档等页面的局部 DOM 漂移。

# 原始描述

管理端列表基础组件，抽象 MetricCard 与分页窗口工具，减少页面局部 DOM 漂移。

补充上下文：

- Sprint 004 复盘行动项 A-003：抽象 `MetricCard` 与分页窗口工具，减少页面局部 DOM 漂移；建议下一步为 `/req-capture` 管理端列表基础组件。
- Sprint 004 复盘指出 `MetricCard` / summary strip 在 SKU、接口文档、日志审计等页面重复出现，`.metric-value` / `.metric-desc` 等局部 DOM 容易持续分叉。
- BUG-0055 已形成管理端列表分页窗口的测试基础，后续宜提升为共享工具与页面契约的一部分，而不是在每个页面内继续手写。
- 本需求作为 `REQ-0028-admin-list-page-contract` 的子需求，聚焦基础组件与分页算法；`REQ-0028` 继续承载 `AdminListPage` 模板、列表页契约和验收页范围。

# 待澄清

- [ ] `MetricCard` 首版应支持哪些字段与状态：标题、数值、描述、趋势、图标、loading、空值、错误态是否全部纳入。
- [ ] 分页窗口工具是否仅返回页码窗口，还是同时封装上一页、下一页、省略号、禁用态与总页数边界。
- [ ] 首批替换页面是否覆盖 SKU、接口文档、日志审计，并逐步推广至品牌、类目、规格、Banner、用户列表。
- [ ] 新组件应归属 `src/web/src/shared/ui/`，还是作为 `AdminListPage` 模板内部组合能力暴露。
- [ ] `/design-system` 验收页是否需要单独展示 `MetricCard` 组合与分页窗口边界样例。

# 探索结论

（/req-explore 后人工确认写入）
