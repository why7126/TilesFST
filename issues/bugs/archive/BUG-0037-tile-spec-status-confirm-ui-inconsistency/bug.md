---
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
title: 瓷砖规格页启用/停用/删除确认弹窗与类目页 UI/UE 不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 16:06:42
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_change: null
related_bug: null
suggested_fix_change: fix-tile-spec-status-confirm-ui
related_requirements:
  - REQ-0009-tile-spec-management
  - REQ-0005-tile-category-management
  - REQ-0008-brand-status-confirm
---

# 缺陷说明

Web 管理端「瓷砖规格」列表页（`/admin/tile-specs`）行内「启用」「停用」「删除」在调用 API 前虽已有二次确认，但使用的是与「瓷砖类目」「瓷砖品牌」「用户管理」等页面不一致的简化 confirm 模板，在 DOM 结构、标题区关闭按钮、描述 Typography、主按钮文案、停用后果说明等方面与 Design System confirm modal（`modal-backdrop` + `modal-card` + head/body/footer）明显分裂，破坏管理端确认 Dialog 统一性。

经 `/bug-explore` 核对源码：`TileSpecManagementPage.tsx` 内联启停/删除 confirm 使用 `<section className="modal-card confirm-card">`、无 `modal-close`、主按钮泛化「确认」、停用描述无前台影响说明；`confirm-card` 在全仓库 CSS 中**无定义**。同域 `TileCategoryManagementPage.tsx`、`BrandManagementPage.tsx` 已采用标准 modal 结构。

**不在本缺陷范围**：

- 规格列表分页、尺寸名称字号（BUG-0027，已归档 `fix-tile-spec-admin-ui`）
- 规格编辑弹窗字段布局（BUG-0028，已归档）
- 新增/编辑保存后列表刷新（BUG-0029，已归档）
- 启停/删除 API、权限、业务校验逻辑
- 后端 `POST .../enable|disable|DELETE` 契约与错误码

# 复现步骤

1. 以 `admin` 登录 Web 管理端（local 或 Docker）。
2. 进入「瓷砖规格」（`/admin/tile-specs`），对某启用规格点击「停用」。
3. 观察确认 UI：标题「停用规格」、正文「确认停用规格「…」？」、主按钮「确认」、**无**标题区 × 关闭按钮。
4. 进入「瓷砖类目」（`/admin/tile-categories`），对某启用类目点击「停用」。
5. 观察确认 UI：标题「停用类目」、正文含「停用后前台将不再展示该类目。」、主按钮「确认停用」、含 × 关闭按钮。
6. 分别在规格页触发「启用」「删除」确认弹窗，与类目/品牌页同类弹窗并排对比。

| 页面 | 路由 | 操作 | 当前 confirm 特征 | 参考实现 |
|---|---|---|---|---|
| 瓷砖规格 | `/admin/tile-specs` | 启用/停用 | 简化 `confirm-card`、主按钮「确认」 | 类目启停 modal |
| 瓷砖规格 | `/admin/tile-specs` | 删除 | `btn primary danger` +「删除」 | 类目「删除类目」 |
| 瓷砖类目 | `/admin/tile-categories` | 启用/停用/删除 | DS modal | Golden Reference |
| 瓷砖品牌 | `/admin/brands` | 启用/停用/删除 | DS modal | 同等参考 |

复现稳定性：**100%**（由 `TileSpecManagementPage.tsx` 内联 markup 决定）。

# 期望结果

- 规格页启用/停用/删除 confirm MUST 与 `TileCategoryManagementPage`（或 `BrandManagementPage`）同类弹窗结构一致：
  - `modal-backdrop` + `modal-card` + `modal-head` / `modal-body` / `modal-footer`
  - `role="dialog"`、`aria-modal="true"`、标题 `aria-labelledby`
  - 标题区含 `modal-close`（×），点击关闭 MUST NOT 调用 API
  - 正文使用 `page-desc`，停用 MUST 含「停用后前台将不再展示该规格。」
  - 主按钮语义化：「确认启用」「确认停用」「删除规格」
  - 删除主按钮 MUST 使用 `btn primary`（与类目/品牌一致），MUST NOT 单独引入 `danger` 变体
- 确认前 MUST NOT 调用 enable/disable/delete API；取消、遮罩、× 关闭 MUST 无副作用。
- 用户确认后 MUST 调用现有 API 并 Toast「规格已启用/停用/删除」（现有行为保持）。
- TSX MUST NOT 引入裸 Hex；样式 MUST 复用既有 `user-management.css` / `brand-management.css` modal 类。
- 满足 REQ-0009 **AC-013**（启停 confirm 对齐 `BrandManagementPage`）与 **AC-018**（删除 confirm）。

# 实际结果

- 启停 confirm 使用 `<section>` + 无效 `confirm-card` class，无 × 关闭、无 `page-desc`、主按钮为泛化「确认」。
- 停用 confirm 缺少「停用后前台将不再展示该规格。」后果说明。
- 删除 confirm 主按钮为「删除」+ `btn primary danger`，与类目「删除类目」+ `btn primary` 不一致。
- `TileSpecManagementPage.test.tsx` 无 confirm dialog 用例；`TileCategoryManagementPage.test.tsx` 已有启停 confirm 测试可作模板。

涉及源码：

| 文件 | 说明 |
|---|---|
| `src/web/src/pages/admin/TileSpecManagementPage.tsx` | 启停/删除 confirm 内联实现（约 L329–382） |
| `src/web/src/pages/admin/TileCategoryManagementPage.tsx` | 启停/删除 confirm 参考（约 L423–505） |
| `src/web/src/pages/admin/BrandManagementPage.tsx` | 同等参考（约 L355–437） |

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖规格 | 确认 Dialog UX 不统一；启停/删除功能可用，无阻断 |
| 角色 | 管理端已登录用户（规格管理权限） |
| 后端 / API / 数据库 | 无变更需求 |
| Orval | 不需要 |
| 店主端 / 小程序 | 无 |
| 关联需求 | REQ-0009（AC-013、AC-018）；REQ-0008（品牌 confirm 先例）；REQ-0005 类目页（视觉基准） |
| 关联 Change | `add-tile-spec-management`（初始实现遗留简化 confirm）；`fix-tile-spec-admin-ui`（BUG-0027/28/29，**未覆盖** confirm 弹窗，已 archived） |
| 关联缺陷 | BUG-0017（同类 confirm UI 不一致，用户页已修）；BUG-0016（管理端 confirm 规范先例） |

# 严重等级说明

严重程度为 **medium**。

理由：

- 问题可 100% 稳定复现，属于管理端 Confirm Dialog 规范未横向对齐，非功能缺陷或安全漏洞。
- 启停/删除仍有二次确认门槛，误触风险低于「无确认直接调 API」类缺陷。
- **非近期回归**：`add-tile-spec-management` 上线即采用简化模板；`fix-tile-spec-admin-ui`  scope 不含 confirm，非 apply 回退。
- REQ-0009 AC-013 验收项**未满足**，属需求交付缺口。
- 无 API 契约、权限绕过或数据损坏风险，不属于 hotfix 或 blocker。
- 修复面小（单页 JSX + Vitest），建议独立 `fix-tile-spec-status-confirm-ui` change。

# 修复建议（供 bug-complete / bug-opsx）

1. 将 `TileSpecManagementPage.tsx` 启停/删除两处 confirm markup 对齐 `TileCategoryManagementPage`（复制结构，替换「类目」→「规格」、`name` → `display_name`）。
2. 停用正文：`确认停用规格「{display_name}」？停用后前台将不再展示该规格。`
3. 删除主按钮改为「删除规格」，移除 `danger` class。
4. 移除无效 `confirm-card` class；补 `aria-labelledby` 与 `modal-close`。
5. 新增 Vitest：参照类目页 `opens disable confirm dialog before calling disableCategory`，覆盖停用 confirm 文案与 API 调用时序。
6. OpenSpec delta：扩展 `web-client` 或 `tile-spec-management` spec，明确规格页 confirm MUST 复用品牌/类目 modal 结构。

# 备注

- 截图：`screenshots/tile-spec-disable-confirm-dialog.png`
- 与 BUG-0027/28/29 可同 Sprint 编排，fix change 职责 MUST 独立（勿回改已 archived `fix-tile-spec-admin-ui`）。
- 可选后续：抽取共享 `AdminConfirmDialog`（非本 BUG 阻塞项，见 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`）。
