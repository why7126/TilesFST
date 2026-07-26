## Context

`REQ-0029-admin-list-foundation-components` 是 `REQ-0028-admin-list-page-contract` 的子需求，来源于 Sprint 004 复盘行动项与 `BUG-0055-admin-list-layout-unification`。当前管理端列表页已形成事实基线：指标卡使用 `article.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`，分页使用 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`，且 `src/web/src/features/admin/lib/pagination.ts` 已存在 `getPaginationWindow` 与测试。

本 change 只创建 OpenSpec 事实源，不修改 `src/`。后续实现由 `/opsx-apply add-admin-list-foundation-components` 执行。

## Goals / Non-Goals

**Goals:**

- 将 `MetricCard`、`MetricCardGrid` 与分页窗口工具沉淀为 Web 管理端可复用能力。
- 保留既有 DOM class，避免首批页面迁移后破坏历史测试、知识库和验收基准。
- 在 `/design-system` 或管理端设计验收区提供可视示例，覆盖正常、空值/loading、danger 描述、2/3/4 卡布局与分页边界。
- 首批接入 2–3 个页面，建议优先 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`；容量不足时先做 `TileSkuManagementPage` + `LogAuditPage`。

**Non-Goals:**

- 不修改后端分页 API、数据库结构、OpenAPI、Orval 或 MinIO 链路。
- 不一次性重构全部管理端列表页。
- 不新增颜色 token、不改变工业石材暗色旗舰风。
- 不实现 toast、confirm modal、sticky action column、跳页输入框等其它列表页横切能力。

## Decisions

### D1. UI 策略：Design System 组件抽象

采用 DS / Tailwind semantic token 策略，而非 CSS Port 或静态 Asset 策略。

- 原因：本需求目标是共享组件与工具，不是复制单页原型。实现 MUST 复用 `src/web/src/shared/ui/`、`src/web/src/shared/templates/`、`src/web/src/components/ui/` 等既有层级。
- 约束：TSX/CSS 新增样式 MUST 使用 semantic token、CSS variable 或既有管理端 class；不得新增裸 Hex 或硬编码 `rgba(...)`。
- 原型冲突处理：`prototype/web/admin-list-foundation-components.html` 是独立验收原型，内部 `--danger: #e07050` 等 CSS 值只作为视觉表达；实际实现必须映射到 DS 语义 token 或既有管理端 danger class。

### D2. DOM 兼容优先于重命名

`MetricCard` MUST 稳定输出 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`，`MetricCardGrid` 或等价容器 MUST 保留 `.summary-grid`。

- 原因：知识库、验收标准、历史页面测试均以这些 DOM class 识别管理端列表页一致性。
- 替代方案：使用全新 BEM 命名或 shadcn 默认 card class。拒绝原因是会增加迁移成本并削弱横切回归测试价值。

### D3. 分页窗口工具从 feature 私有层迁移到共享层

保留 `getPaginationWindow(currentPage, totalPages, maxVisible = 5)` 的可理解 API，迁移到共享工具或管理端共享层；旧路径可保留兼容导出，直到首批页面迁移完成。

- 原因：现有工具已有事实基础和测试，迁移重点是归属治理和边界兜底，不重新设计分页模型。
- 约束：管理端列表分页继续使用 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`，通用店主端 `Pagination` 可保持独立。

### D4. 首批页面作为推广样板

首批页面选择 MUST 覆盖普通指标卡、danger / 异常描述和分页窗口。建议优先：

1. `TileSkuManagementPage`：普通指标卡与 SKU 主列表分页。
2. `LogAuditPage`：danger / 异常描述指标卡。
3. `ApiDocsPage`：接口文档页摘要指标卡与历史分页一致性风险。

未纳入首批的页面 MUST 在 trace 或实现任务中列为后续推广项，不得标记为已完成。

## Conflict Resolution

| 来源 | 结论 |
|---|---|
| HTML 原型 | 最高优先级，确认 `.metric-*`、`.summary-grid`、`.page-*` DOM 和最多 5 页码窗口。 |
| PNG Golden Reference | 当前未提供；不阻塞 req-opsx，后续设计验收可补充。 |
| prototype context | 明确本 change 只表达基础组件和分页工具，页面级契约继续归属 `REQ-0028`。 |
| acceptance.md | 采纳 AC-001 至 AC-041 与 AC-XCUT；实现任务按组件、工具、页面接入、展示、测试拆分。 |
| rules/ui-design.md | 实现必须使用 semantic token、`cn()`、DS 组件复用，禁止裸 Hex。 |
| openspec/specs | `web-client` 已有管理端列表横切一致性，本 change 只补充基础组件与工具层事实源，不移除既有要求。 |

## Risks / Trade-offs

- [Risk] 共享组件替换导致页面纵向间距或 DOM 层级轻微变化 → Mitigation：首批页面增加结构 smoke，并对 `summary-grid`、`metric-card`、分页结构做断言。
- [Risk] 迁移分页工具路径导致旧页面导入断裂 → Mitigation：保留兼容导出或分阶段替换，测试覆盖旧路径与新路径的窗口输出一致性。
- [Risk] `/design-system` 示例与生产页面样式分叉 → Mitigation：示例直接使用同一组件，不复制一份演示专用 DOM。
- [Risk] 首批页面范围扩大影响 Sprint 容量 → Mitigation：任务允许 2 页最低闭环，第三页作为容量充足时接入。

## Migration Plan

1. 新建共享 `MetricCard` / `MetricCardGrid` 与分页窗口工具归属层。
2. 迁移或保留现有 `getPaginationWindow` 测试，补齐非法输入兜底场景。
3. 在 `/design-system` 或管理端设计验收区展示组件和分页窗口边界。
4. 首批替换 2–3 个管理端列表页，保持筛选、分页状态、空态、权限逻辑不变。
5. 运行相关 Vitest / Testing Library，记录未接入页面的后续推广清单。

## Open Questions

- 最终组件路径由实现阶段根据现有目录选择：`src/web/src/shared/ui/` 或管理端专属共享层。
- `MetricCard` 是否支持图标、趋势值、tooltip；本 change 仅把它们列为后续增强，不纳入 v1 必须范围。
