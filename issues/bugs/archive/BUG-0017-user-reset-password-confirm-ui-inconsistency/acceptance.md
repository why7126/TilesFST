---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-27 13:29:34
updated_at: 2026-06-27 13:29:34
related_requirement: REQ-0005-user-management
suggested_fix_change: fix-user-reset-password-confirm-ui
related_requirements:
  - REQ-0005-user-management
  - REQ-0007-tile-category-management-refine
  - REQ-0008-brand-status-confirm
related_bug: BUG-0016-admin-list-status-action-confirm-missing
---

# 回归验收标准

> 修复本缺陷 MUST 对齐 REQ-0007 / 同页冻结确认已交付的启停 confirm modal 模式（modal 结构、确认前不调 API、取消不生效）。**不在 scope**：冻结/解冻/删除 confirm（BUG-0016）、`ResetPasswordDialog` 结果弹窗内容与复制交互（REQ-0005 AC-022）、后端 API、品牌/类目/SKU 其他 confirm。

## AC-001 重置密码 MUST 二次确认后再调 API

**Given** `admin` 位于 `/admin/users`，目标用户非 `deleted`  
**When** 点击行内「重置密码」  
**Then** MUST NOT 立即调用 `POST /api/v1/admin/users/{id}/reset-password`  
**And** MUST 展示确认 modal（`role="dialog"`、`aria-modal="true"`）  
**And** 标题 MUST 含「重置密码」或等价文案  
**And** 正文 MUST 含用户名及重置后果（如将生成新随机密码）  
**And** 底部 MUST 含「取消」与主按钮「确认重置」（或等价）  
**When** 点击「确认重置」  
**Then** MUST 调用 reset-password API  
**And** Toast「密码已重置」（或等价）并打开结果弹窗展示一次性密码

## AC-002 重置密码 confirm MUST 禁止 window.confirm

**Given** `admin` 位于 `/admin/users`  
**When** 点击「重置密码」  
**Then** MUST NOT 调用 `window.confirm`  
**And** MUST 使用页面内 DS modal，与同页冻结确认及类目启停确认形态一致

## AC-003 重置密码 confirm modal MUST 可取消且无副作用

**Given** 重置密码确认 modal 已打开  
**When** 点击「取消」、遮罩、× 或 ESC（若实现）  
**Then** modal MUST 关闭  
**And** MUST NOT 调用 reset-password API  
**And** MUST NOT 打开 `ResetPasswordDialog`  
**And** 用户密码 MUST 不变

## AC-004 modal 视觉与结构 MUST 对齐 Golden Reference

**Given** 修复完成  
**When** 并排对比重置密码 confirm modal 与 `TileCategoryManagementPage` 启停确认（或同页 `statusConfirmTarget` modal）  
**Then** MUST 使用相同 modal 类名（`modal-backdrop`、`modal-card`、`modal-head`、`modal-body`、`modal-footer`）  
**And** 正文 MUST 使用 `page-desc`（或等价 semantic class）  
**And** 按钮层级：次按钮「取消」、主按钮「确认重置」  
**And** TSX/CSS MUST NOT 新增裸 Hex；使用既有管理端 semantic token / CSS 变量

## AC-005 重置成功后结果弹窗 MUST NOT 回归

**Given** 用户在 confirm modal 中确认重置且 API 成功  
**When** 结果弹窗展示  
**Then** MUST 继续打开既有 `ResetPasswordDialog`（或等价）  
**And** MUST 展示一次性随机密码与复制按钮  
**And** 关闭后 MUST NOT 再次展示同一密码（REQ-0005 AC-022 / AC-023）

## AC-006 同页其他 confirm MUST NOT 回归

**Given** 本 BUG 修复已合并  
**When** 在 `/admin/users` 执行冻结/解冻/删除 confirm 流程  
**Then** 行为 MUST 与修复前一致  
**And** `UserManagementPage.test.tsx` 冻结/删除 confirm 用例 MUST 保持通过

## AC-007 品牌/类目启停 confirm MUST NOT 回归

**Given** 本 BUG 修复已合并  
**When** 在 `/admin/brands`、`/admin/tile-categories` 执行启停 confirm  
**Then** 行为 MUST 与修复前一致  
**And** `BrandManagementPage.test.tsx`、`TileCategoryManagementPage.test.tsx` 启停 confirm 用例 MUST 保持通过

## AC-008 自动化 MUST 覆盖重置密码 confirm 门禁

**Given** `fix-user-reset-password-confirm-ui` 已 `/opsx-apply`  
**When** 运行 `UserManagementPage` vitest  
**Then** MUST 含：点击「重置密码」→ 先出现 dialog → 确认前 `resetUserPassword` mock **未被调用**  
**And** MUST 含：取消/关闭 dialog 后 mock **未被调用**  
**And** MUST 含：`window.confirm` **未被调用**（spy 断言）  
**And** MUST 含：确认「确认重置」→ mock **被调用** 且结果弹窗 state 更新（或等价断言）

## AC-009 修复范围 MUST 为纯前端（默认）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 默认 MUST 仅涉及 `src/web/` 与测试  
**And** MUST NOT 修改后端 API、SQLite schema、Orval 生成接口  
**And** MUST NOT 修改 `ResetPasswordDialog` 结果弹窗业务逻辑（除非仅为配合 confirm 流程的最小接线）

## AC-010 已删除用户 MUST NOT 可重置

**Given** 目标用户 `status=deleted`  
**When** 查看操作列  
**Then** 「重置密码」按钮 MUST 置灰或不可用（与修复前行为一致，本 BUG MUST NOT 回归）
