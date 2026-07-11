## Context

REQ-0028 已完成评审并纳入 `sprint-005`，来源于 Sprint 004 复盘行动项 A-002 与 BUG-0055 的管理端列表页一致性经验。当前正式 spec 已在 `web-client` 中约束 8 个管理端列表页的模块顺序、筛选、sticky 操作列和分页，但缺少 Design System 层的 `AdminListPage` 页面模板契约与 `/design-system` 验收样例；现有 `src/web/src/shared/templates/admin-list-page.tsx` 与 `AdminListPageContent` 偏轻量，不能完整承载标题、指标卡、筛选、表格、分页、状态态和操作列。

## Goals / Non-Goals

**Goals:**

- 定义 `AdminListPage` 或等价模板组合的输入模型、模块顺序、DOM/class 契约和状态态。
- 在 `/design-system` 增加管理端列表页验收样例，覆盖标准列表、loading、empty、error、单页和多页分页边界。
- 将 `web-client` 既有管理端列表页横切一致性升级为模板复用门禁，避免新增页面绕过模板。
- 保持 REQ-0029 的边界：`MetricCard`、`MetricCardGrid` 和 pagination-window 工具可作为基础组件被组合，但本 Change 关注页面级模板契约。

**Non-Goals:**

- 不修改后端 API、数据库、MinIO、Docker Compose、店主 Web 展示端或微信小程序。
- 不一次性迁移全部 8 个管理端列表页；实现阶段可选择 1 个低风险代表页作为模板迁移示范。
- 不放宽管理端认证、角色权限、危险操作确认或安全边界。
- 不新增 Design Token；若实现发现 token 缺口，必须另行评审并同步 token 事实源。

## Decisions

### D1. UI 策略：Design System 组合优先，而非 HTML CSS Port

- **选择**：以 Design System 组合策略实现，优先复用 `src/web/src/shared/templates/`、`src/web/src/shared/ui/`、`src/web/src/components/ui/`、REQ-0029 基础组件和 semantic token。
- **原因**：REQ-0028 的 HTML prototype 是结构和视觉验收样例，不是生产页面 CSS Port 源；若直接 CSS Port，会继续扩大页面级 CSS 分叉，违背模板治理目标。
- **替代方案**：完整 CSS Port prototype。该方案视觉还原快，但会把一次性样例样式变成新事实源，后续难以复用和测试。

### D2. 模板输入模型覆盖页面骨架，不接管业务数据请求

- **选择**：扩展 `AdminListPageContent` 或建立等价类型，描述标题、说明、主操作、指标卡、筛选项、列定义、行操作、分页、loading/empty/error/permission 状态和少量扩展 slot。
- **原因**：模板应稳定页面结构和交互契约，但不应绑定具体 API、Repository 或业务加载函数。
- **替代方案**：为每个业务列表页提供专用模板 wrapper。该方案短期简单，但会让模板能力重新分叉。

### D3. `/design-system` 验收样例作为第一落点

- **选择**：先在 `/design-system` 增加 AdminListPage 样例与边界态，再选择代表页面迁移。
- **原因**：验收页可以先固化页面级契约，降低直接改业务页带来的 API/权限/数据状态干扰。
- **替代方案**：直接迁移 `/admin/users` 或 `/admin/tile-skus`。该方案能更快验证真实页面，但容易与业务缺陷、权限和数据加载耦合。

### D4. Conflict Resolution

优先级：`prototype/web/admin-list-page-contract.html` → `prototype/web/admin-list-page-contract-context.md` → `acceptance.md` → `rules/ui-design.md` → `openspec/specs/web-client/spec.md`。

- HTML prototype 明确了模块顺序、`.metric-*`、`.page-summary`、`.page-right`、`.page-buttons`、`.page-btn`、`.sticky-action` 与 fixed toast 视觉结构，作为 `/design-system` 样例最高结构参考。
- context.md 明确 prototype 不是生产实现，后续实现必须走 Design System 组合策略。
- acceptance.md 中“默认筛选区不展示查询/搜索按钮”“筛选/重置/page_size 重置到第 1 页”“操作反馈 fixed toast”优先于历史页面局部实现。
- `rules/ui-design.md` 约束 semantic token、`cn()` 与管理端暗色旗舰风；若 prototype 中存在裸 Hex，仅作为视觉参考，不得直接移入 TSX/CSS。
- `web-client` 现有横切一致性 requirement 保留 8 页面范围和非目标端不受影响边界，本 Change 只补强模板复用门禁。

## Risks / Trade-offs

- [风险] REQ-0028 与 REQ-0029 并行导致基础组件尚未全部可用 → [缓解] AdminListPage 先允许等价组合，基础组件完成后再替换内部实现。
- [风险] 一次性迁移 8 个页面超过 Sprint 容量 → [缓解] tasks 将真实页面迁移限定为 1 个代表页示范，其他页面后续推广。
- [风险] `/design-system` 样例与真实页面行为脱节 → [缓解] 补测试覆盖模块顺序、筛选重置、分页 DOM 和 sticky action column，并在代表页迁移中验证真实行为。
- [风险] prototype 裸 Hex 或静态 CSS 被误用 → [缓解] design 明确 DS 组合优先，验收必须通过 Design System 校验或等价裸 Hex 检查。

## Migration Plan

1. 扩展 AdminListPage 模板和类型，保持现有调用兼容或提供迁移适配层。
2. 增加 `/design-system` AdminListPage 样例与边界态。
3. 为模板和样例补充 Vitest / Testing Library 覆盖。
4. 选择 1 个低风险代表页接入模板或等价组合，确认不回退分页、筛选、sticky 操作列、toast 和权限行为。
5. 后续若推广到 8 个页面，以独立任务逐页替换，避免一次性大规模回归风险。
