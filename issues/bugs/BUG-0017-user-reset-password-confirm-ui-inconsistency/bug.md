---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
title: 用户重置密码二次确认弹窗与类目启用停用确认弹窗 UI 不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 12:03:34
environment: local|docker
related_requirement: REQ-0005-user-management
related_change: null
related_bug: BUG-0016-admin-list-status-action-confirm-missing
suggested_fix_change: fix-user-reset-password-confirm-ui
related_requirements:
  - REQ-0005-user-management
  - REQ-0007-tile-category-management-refine
  - REQ-0008-brand-status-confirm
---

# 缺陷说明

Web 管理端「用户管理」列表页（`/admin/users`）行内「重置密码」在调用 API 前虽已有二次确认，但使用的是浏览器原生 `window.confirm`，与同页「冻结」「解冻」「删除」以及「瓷砖类目」「瓷砖品牌」列表页已对齐的 Design System confirm modal（`modal-backdrop` + `modal-card` + head/body/footer）在布局、按钮层级、标题区 Typography、遮罩与 semantic token 等方面明显不一致，破坏管理端确认 Dialog 统一性。

经 `/bug-explore` 核对源码：`UserManagementPage.tsx` 中 `handleResetPassword` 使用 `window.confirm`；同页 `statusConfirmTarget` / `deleteTarget` 已 modal 化（BUG-0016 / `fix-admin-list-status-action-confirm` 交付）。**重置密码成功后的随机密码展示弹窗**（`ResetPasswordDialog`）已是 DS modal，**不在本缺陷范围**；本缺陷仅针对**重置 API 调用前**的确认步骤。

**不在本缺陷范围**：

- 用户冻结/解冻、删除 confirm modal（BUG-0016，已交付或并行）
- SKU、品牌、类目启停/删除 confirm（参考实现，修复时 MUST NOT 回归）
- 后端 `POST .../reset-password` API、密码生成规则、权限边界
- `ResetPasswordDialog` 结果弹窗内容与复制交互（REQ-0005 AC-022 已覆盖）

# 复现步骤

1. 以 `admin` 登录 Web 管理端（local 或 Docker）。
2. 进入「用户管理」（`/admin/users`），对某非 `deleted` 用户点击「重置密码」。
3. 观察确认 UI：为浏览器原生对话框（非页面内 modal），文案为「确认为用户 {username} 重置密码？」。
4. 进入「瓷砖类目」（`/admin/tile-categories`），对停用类目点击「启用」（或对启用类目点击「停用」）。
5. 观察确认 UI：为 DS modal（`role="dialog"`、`modal-title`、取消 + 主按钮等）。
6. 并排对比两确认框的视觉与交互形态。

| 页面 | 路由 | 操作 | 当前确认方式 | 参考实现 |
|---|---|---|---|---|
| 用户管理 | `/admin/users` | 重置密码 | `window.confirm` | 类目启停 modal |
| 用户管理 | `/admin/users` | 冻结/解冻/删除 | DS modal | 已对齐 |
| 瓷砖类目 | `/admin/tile-categories` | 启用/停用 | DS modal | Golden Reference |

复现稳定性：**100%**（由 `handleResetPassword` 内 `window.confirm` 决定）。

# 期望结果

- 点击「重置密码」时 MUST NOT 使用 `window.confirm`。
- MUST 在调用 `POST /api/v1/admin/users/{id}/reset-password` 前展示 DS confirm modal，结构 MUST 与同页冻结确认及 `TileCategoryManagementPage` 启停确认一致：
  - `modal-backdrop` + `modal-card` + `modal-head` / `modal-body` / `modal-footer`
  - `role="dialog"`、`aria-modal="true"`、标题 `aria-labelledby`
  - 正文使用 `page-desc`（或等价 semantic class），含用户名及操作后果说明
  - 底部「取消」+ 主按钮「确认重置」（或等价文案）
- 确认前 MUST NOT 调用 reset-password API；取消、遮罩、× 关闭 MUST NOT 调用 API 且无副作用。
- 用户确认后 MUST 调用现有 API；成功后 MUST 继续打开既有 `ResetPasswordDialog` 展示一次性密码，并 Toast「密码已重置」（或等价）。
- TSX MUST NOT 引入裸 Hex；样式 MUST 复用既有 `user-management.css` / `brand-management.css` modal 类。

# 实际结果

- `handleResetPassword` 首行执行 `window.confirm`，确认框为浏览器原生 UI，与类目启停 modal 视觉分裂。
- 同页其他危险操作已 modal 化，用户在同一操作列内体验到两套确认形态。
- `UserManagementPage.test.tsx` 覆盖冻结/删除 modal，**无**重置密码 confirm 用例；删除用例显式断言 `window.confirm` 未被调用，但重置密码路径仍会触发原生 confirm。

涉及源码：

| 文件 | 说明 |
|---|---|
| `src/web/src/pages/admin/UserManagementPage.tsx` | `handleResetPassword` 使用 `window.confirm`（约 L134–143） |
| `src/web/src/pages/admin/TileCategoryManagementPage.tsx` | 启停 confirm modal 参考（约 L423–466） |
| `src/web/src/features/admin/components/ResetPasswordDialog.tsx` | 结果弹窗（已 DS modal，非本 BUG） |

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 用户管理 | 确认 Dialog UX 不统一；功能可用，无阻断 |
| 角色 | 仅 `admin` 可重置密码 |
| 后端 / API / 数据库 | 无变更需求 |
| Orval | 不需要 |
| 店主端 / 小程序 | 无 |
| 关联需求 | REQ-0005（AC-021 重置前确认、AC-022 结果弹窗）；REQ-0007（类目 modal 参考）；REQ-0008（品牌 modal 先例） |
| 关联 Change | `fix-admin-list-status-action-confirm`（已归档，显式排除本项 → BUG-0017）；`add-user-management`（初始实现遗留 `window.confirm`） |
| 关联缺陷 | BUG-0016（同页相邻；职责独立，可同 Sprint 编排） |

# 严重等级说明

严重程度为 **medium**。

理由：

- 问题可 100% 稳定复现，属于管理端 Confirm Dialog 规范未横向对齐，非功能缺陷或安全漏洞。
- 重置密码仍有二次确认门槛（原生 confirm），误触风险低于「无确认直接调 API」类缺陷。
- **非近期回归**：`fix-admin-list-status-action-confirm` 有意保留 `window.confirm` 直至本 BUG 修复；`openspec/specs/web-client/spec.md` 将重置密码 confirm UI 单独标注为 BUG-0017。
- 无 API 契约、权限绕过或数据损坏风险，不属于 hotfix 或 blocker。
- 修复面小（单页 + Vitest），建议独立 `fix-user-reset-password-confirm-ui` change，MUST NOT 与 BUG-0016 change 混 scope。

# 修复建议（供 bug-complete / bug-opsx）

1. 增加 `resetPasswordConfirmTarget` 状态；点击「重置密码」→ 打开 confirm modal，确认后再调用 `resetUserPassword`。
2. Modal 文案建议：标题「重置密码」；正文「确认为用户「{username}」重置密码？重置后将生成新随机密码。」；按钮「取消」/「确认重置」。
3. 新增 Vitest：确认前 API mock MUST NOT 被调用；取消后不调用；确认后调用 API 并打开结果弹窗逻辑（可 mock `ResetPasswordDialog`）。
4. OpenSpec delta：扩展 `web-client` 或 `user-management` 中重置密码确认 requirement，明确 MUST NOT 使用 `window.confirm` 且 MUST 复用类目启停 modal 结构。
5. 可选后续：抽取共享 `AdminConfirmDialog`（非本 BUG 阻塞项）。

# 备注

- REQ-0005 `business-flow.md` §6 已描述「点击重置密码 → 确认对话框 → API → 二次弹窗展示密码」，但未限定 confirm 须为 DS modal；修复以四页已交付 modal 模式为准。
- 与 BUG-0015（toast 布局）、BUG-0016（冻结/删除 confirm）可同 Sprint 编排，fix change 职责 MUST 独立。
