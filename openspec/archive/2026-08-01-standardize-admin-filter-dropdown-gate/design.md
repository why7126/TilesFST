## Context

管理端列表页已经存在 `AdminFilterSelect`、`SearchableSelect`、统一 `admin-filter-dropdown-*` 类名、类目页基准测试，以及 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 的筛选下拉 gate。`openspec/specs/design-system/spec.md` 也已要求下拉基准样例、语义样式和测试覆盖，但 `/opsx-apply` 的横切 gate 仍以宽泛 `admin-list` 标签为主，容易在新增或修改筛选控件时遗漏“先读最佳实践、再检查共享组件、最后补测试”的专门步骤。

本变更把筛选下拉 gate 作为设计系统契约和 apply checklist 契约，而不是新增业务功能。目标用户是后续实现管理端列表、设置页筛选、日志筛选、API 文档筛选和主题入口筛选的开发者与评审者。

## Goals / Non-Goals

**Goals:**

- 让涉及管理端筛选下拉的 Change 在 `/opsx-apply` 前显式命中最佳实践回读。
- 要求实现优先复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper。
- 将状态覆盖、页面矩阵、窄屏和弹层裁切检查写入 apply checklist。
- 保持 API 查询参数、筛选语义、分页重置和现有权限边界不因 UI 统一改动而漂移。

**Non-Goals:**

- 不重写当前管理端筛选组件实现。
- 不新增 Design Token、主题、API、数据库或环境变量。
- 不要求所有历史页面在 propose 阶段立即返工；具体页面整改仍由后续 apply tasks 按范围执行。
- 不用文档 gate 替代 Vitest、Testing Library 或 Playwright/视觉 smoke。

## Decisions

1. 将筛选下拉 gate 纳入 `design-system` delta spec。
   - 原因：下拉视觉、状态、弹层和 shared UI 复用属于 Design System 约束。
   - 备选：只改最佳实践文档。放弃原因是文档缺少 OpenSpec 归档后的规范约束。

2. 将 apply checklist 纳入 `agent-workflow-tooling` delta spec。
   - 原因：用户明确要求“进入 apply checklist”，而 `/opsx-apply` 的 Cross-cutting Apply Gate 是当前实现前门禁入口。
   - 备选：只在每个具体页面 Change 的 tasks 里手写检查项。放弃原因是容易遗漏，且不能复用到后续 Change。

3. 使用现有共享组件和类名作为默认实现路径。
   - 原因：`AdminFilterSelect`、`SearchableSelect` 和 `admin-filter-dropdown-*` 已覆盖普通/可搜索下拉、空态、加载态、选中态和测试基准。
   - 备选：引入新的 Select 抽象。放弃原因是会增加迁移面，并可能再次制造页面级样式分叉。

4. 将门禁输出设为 `pass|warn|n/a`，但新增或修改管理端筛选下拉时不得跳过。
   - 原因：纯后端、非管理端 UI 或无筛选控件的 Change 不应被误阻断；但命中筛选控件的 Change 必须有明确证据。

## Risks / Trade-offs

- [Risk] apply gate 过宽导致无关管理端页面也被要求读取筛选文档 → Mitigation：触发条件限定为管理端筛选区内 Select、Dropdown、Popover、Combobox、date picker 或等价下拉控件。
- [Risk] 只检查类名会掩盖查询参数或筛选语义回归 → Mitigation：checklist 要求测试覆盖 query params、筛选结果语义和分页重置。
- [Risk] 页面级 CSS 仍可能覆盖共享弹层 → Mitigation：视觉 smoke 和窄屏检查必须确认弹层不被表格、滚动容器、弹窗或 sticky action column 裁切。
- [Risk] 文档和技能 checklist 漂移 → Mitigation：实现任务同时更新最佳实践、`opsx-apply` gate 和相关测试。
