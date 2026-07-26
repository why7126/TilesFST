## Why

[BUG-0015-admin-list-status-tips-layout-shift](issues/bugs/archive/BUG-0015-admin-list-status-tips-layout-shift/) 已评审通过（REV-BUG-0015-001）。Web 管理端瓷砖品牌、用户管理、瓷砖类目、瓷砖 SKU 四个列表页在执行状态变更、CRUD 成功或 API 错误反馈时，用户/类目/SKU 三页仍使用文档流 `.admin-notice`，Tips 约 3.2s 后自动消失会推挤 hero、指标卡、筛选区与表格。品牌页在 [BUG-0003](issues/bugs/archive/BUG-0003-brand-image-display-layout-shift/) / `fix-brand-image-display-layout-shift` 中已改为 fixed toast，但样式耦合在 `brand-management.css` 且未推广至其他列表页。

根因见 `issues/bugs/archive/BUG-0015-admin-list-status-tips-layout-shift/root-cause.md`：自动消失反馈误用占位文档流节点；管理端缺少统一 toast 组件契约。本 change 以 `fix-*` 承载四页统一修复，禁止绕过 OpenSpec 直接改 `src/`。

## What Changes

- 将 `.admin-toast-region` / `.admin-toast` 提升至管理端共享样式（如 `admin-home.css`），或抽取共享 `AdminToast` 组件。
- 用户管理、瓷砖类目、瓷砖 SKU 三页：列表级操作成功/失败反馈 MUST 改为 fixed toast，MUST NOT 在 `page-hero` 前插入文档流 `.admin-notice`。
- 瓷砖品牌页：迁移至共享 toast 实现，保留 BUG-0003 既有 fixed 行为与单测，MUST NOT 回归 Logo 展示/上传进度。
- 四页 toast 视觉、位置、3200ms 自动消失、`aria-live` 行为 MUST 一致。
- 补充 Vitest：品牌页保留现有断言；用户/类目/SKU 各至少 1 条「toast 存在、无文档流 notice」用例。
- 弹窗内 inline 错误（`.form-error` 等）MAY 保持现状；`AdminLayout` 侧栏占位 notice 不在本 change scope。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：ADDED「管理端列表页操作反馈 Toast 布局统一」— 四列表页自动消失操作反馈 MUST 使用 fixed toast，MUST NOT 推挤主体布局；共享样式/组件约束。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/brands`、`/admin/users`、`/admin/tile-categories`、`/admin/tile-skus` 列表页 notice/toast 渲染 |
| 样式 | `admin-home.css`（新增/迁移 toast）；`brand-management.css`（移除或 re-export toast）；可选 `shared/ui/AdminToast` |
| REQ | REQ-0005-brand-management、REQ-0005-user-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management（交互体验对齐） |
| API / 数据库 / Orval | 不变 |
| 测试 | Vitest（四页或三页新增 + 品牌回归） |
| Docker | web 镜像重建（CSS/TSX） |
| 关联 | `fix-brand-image-display-layout-shift`（品牌 toast 先例）；BUG-0016/BUG-0017 职责独立 |

## Rollback Plan

若修复引起管理端提示不可见或布局异常，可按以下顺序回滚：

1. 回滚四页 TSX 中 toast 渲染改动，恢复修复前 `.admin-notice` 文档流模式（接受布局抖动回归）。
2. 回滚共享样式/组件新增，恢复 `brand-management.css` 内 toast 定义（品牌页）。
3. 移除新增 Vitest。

回滚不涉及 API、数据库或 Orval。回滚后保留 BUG 与 OpenSpec 记录，重新评估共享组件方案。
