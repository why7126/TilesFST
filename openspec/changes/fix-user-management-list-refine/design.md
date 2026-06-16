## Context

- **现状**：`UserManagementPage.tsx` 已实现 REQ-0005 v1 列表（6 列筛选含「搜索」、`section-head`、`table-toolbar`、用户列 email 回退、旧分页布局）；`user_repository.list_users` 的 keyword 匹配 username、display_name、email、phone。
- **父 change**：`add-user-management`（in-progress）；弹窗、行操作、API 路由不变。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.html`（v2）
  2. `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.png`（待重新导出）
  3. `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list-context.md`
  4. `issues/requirements/REQ-0005-user-management-list-refine/acceptance.md`
  5. `issues/requirements/REQ-0005-user-management-list-refine/requirement.md`
  6. `rules/ui-design.md`
  7. `openspec/changes/add-user-management/specs/user-management/spec.md`（基线 spec）
  8. Modal 仍引用 `REQ-0005-user-management/prototype/web/user-management-modal.*`（本 change 不修改）

## Conflict Resolution

| 检查项 | v2 HTML | v1 HTML/实现 | acceptance / add-user-management spec | 决议 |
|--------|---------|--------------|--------------------------------------|------|
| 「搜索」按钮 | 无 | 有 | v1 AC 要求点击搜索 | **MODIFIED** 以 v2 HTML 为准；自动查询 |
| 筛选网格列数 | 5 列 | 6 列 | v1 checklist「筛选 6 列」 | **MODIFIED** 5 列；更新 PNG gate |
| placeholder | 「搜索用户名/昵称」 | 「搜索用户名 / 昵称 / 邮箱」 | FR-002 无邮箱 | **MODIFIED** 以 v2 HTML 为准 |
| keyword 后端范围 | 仅 username、display_name | 含 email、phone | add-user-management API spec 含四字段 | **MODIFIED** 收窄至 username、display_name |
| section-head | 无 | 有 | v1 未强制标题行 | **MODIFIED** 删除 |
| table-toolbar | 无 | 有 | v1 含提示行 | **MODIFIED** 删除 |
| 用户列副标题 | 昵称两行；无邮箱 | display_name \|\| email | add spec「昵称/邮箱」 | **MODIFIED** 仅昵称；空则「未设置昵称」 |
| 用户列布局 | `.user-meta` column | 可能单行 | FR-005 两行 | **MODIFIED** flex column |
| 分页左侧 | 「共 N 个用户」 | 每页 + x-y/N | add spec「1-10 / N」 | **MODIFIED** 以 v2 HTML 为准 |
| 分页右侧 | 页码 +「每页显示」 | 页码在右、条数在左 | — | **MODIFIED** 以 v2 HTML 为准 |
| Modal / 行操作 | 不变 | 不变 | REQ-0005 modal | **冻结**，本 change 不触碰 |

## Goals / Non-Goals

**Goals:**

- `/admin/users` 列表区与 v2 `user-management-list.html` 在 1280×1024 并排验收 pass（≥15 项 checklist，见 `trace.md`）。
- 延续 **CSS Port**（`user-management.css`），增量 port v2 筛选网格、用户列、分页结构。
- keyword 前后端一致：仅 username、display_name。
- 弹窗、指标卡、行操作、权限边界零回归。

**Non-Goals:**

- 添加/编辑弹窗字段或校验变更。
- 4 指标卡内容与样式变更。
- 新 API 端点或角色/权限模型变更。
- 替换 Admin Shell 或 Sidebar 实现。

## Decisions

### D1：CSS Port 增量更新（延续 add-user-management D1）

- **决策**：在现有 `user-management.css` 上 port v2 HTML 差异（`filter-grid` 5 列、移除 section/toolbar 样式、`.user-meta` 纵向、`.pagination` 左右结构）。
- **理由**：v2 HTML 与 v1 同源 CSS Port；局部 diff 比 Tailwind 重装 fidelity 风险低。
- **备选**：Tailwind DS 拼装 — 已否决（与 add-user-management 策略不一致）。

### D2：筛选触发策略

- **决策**：移除「搜索」按钮；关键词 `onBlur` + Enter + **300ms debounce**（`useEffect` 或 `useDebouncedValue`）；角色/状态/登录情况下拉 `onChange` 立即请求；均 `setPage(1)`。
- **理由**：对齐 FR-001 与 v2 原型；减少无效点击。

### D3：后端 keyword 收窄

- **决策**：`user_repository._build_list_filters` 移除 `email`、`phone` LIKE 条件；保留 trim 与空 keyword 不附加条件。
- **理由**：与 O-02 及产品搜索能力一致；email/phone 仍可通过列表展示字段之外存在，只是不可被 keyword 命中。

### D4：Auth / Modal / API 冻结

- 不修改 login/me/logout、弹窗组件、`require_admin` 依赖、Orval 生成客户端方法签名（除文档注释可选）。

## 验收 Gate

- **视口**：1280×1024（或 1440 内容区 max-width 1080px 等比）。
- **Golden Reference**：`issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.png`（实现后须重新导出）。
- **Checklist**：见 `trace.md`（≥15 项：筛选 5 列、无搜索按钮、placeholder、无 section-head、无 toolbar、用户两行、分页文案等）。
- **回归**：modal PNG、`employee` 菜单隐藏、pytest/vitest/build 全绿。
