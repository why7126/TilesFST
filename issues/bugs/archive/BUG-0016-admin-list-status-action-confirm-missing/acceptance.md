---
bug_id: BUG-0016-admin-list-status-action-confirm-missing
status: pending_review
created_at: 2026-06-27 13:12:51
updated_at: 2026-06-27 13:12:51
related_requirement: REQ-0008-brand-status-confirm
suggested_fix_change: fix-admin-list-status-action-confirm
related_requirements:
  - REQ-0008-brand-status-confirm
  - REQ-0005-user-management
  - REQ-0006-tile-sku-management
  - REQ-0007-tile-category-management-refine
related_bugs:
  - BUG-0017-user-reset-password-confirm-ui-inconsistency
---

# 回归验收标准

> 修复本缺陷 MUST 对齐 REQ-0008 / REQ-0007 已归档启停确认模式（modal 结构、确认前不调 API、取消不生效）。**不在 scope**：品牌启停/删除（已满足）、类目启停/删除（参考）、重置密码 confirm UI（→ BUG-0017）。

## AC-001 用户冻结 MUST 二次确认后再调 API

**Given** `admin` 位于 `/admin/users`，目标用户 `status=active`  
**When** 点击行内「冻结」  
**Then** MUST NOT 立即调用 `PATCH .../status`  
**And** MUST 展示确认 modal（`role="dialog"`、`aria-modal="true"`）  
**And** 标题 MUST 含「冻结用户」或等价文案；正文 MUST 含用户名及冻结后果（如禁止登录）  
**And** 底部 MUST 含「取消」与主按钮「确认冻结」（或等价）  
**When** 点击「确认冻结」  
**Then** MUST 调用 API 将状态设为 `disabled`  
**And** Toast「用户已冻结」并刷新列表

## AC-002 用户解冻 MUST 二次确认后再调 API

**Given** 目标用户 `status=disabled`  
**When** 点击「解冻」  
**Then** MUST 先展示确认 modal，标题/正文/主按钮文案与解冻语义匹配  
**And** 确认前 MUST NOT 调用 API  
**When** 确认解冻  
**Then** Toast「用户已恢复正常」并刷新列表

## AC-003 用户冻结/解冻 modal MUST 可取消且无副作用

**Given** 冻结或解冻确认 modal 已打开  
**When** 点击「取消」、遮罩、× 或 ESC（若实现）  
**Then** modal MUST 关闭  
**And** MUST NOT 调用 status API  
**And** 用户状态 MUST 不变

## AC-004 用户删除 MUST 使用 DS modal，禁止 window.confirm

**Given** 从未登录用户（`last_login_at` 为空）且可删除  
**When** 点击「删除」  
**Then** MUST NOT 使用 `window.confirm`  
**And** MUST 展示与类目/品牌删除一致的 `modal-backdrop` + `modal-card` 结构  
**And** 正文 MUST 含用户名及不可恢复提示  
**When** 确认删除  
**Then** 软删除成功，Toast「用户已删除」

## AC-005 SKU 下架 MUST 二次确认后再调 API

**Given** `admin` 或 `employee` 位于 `/admin/tile-skus`，行 `status=PUBLISHED`  
**When** 点击「下架」  
**Then** MUST NOT 立即调用 `unpublish` API  
**And** MUST 展示确认 modal，正文含 SKU 名称  
**When** 确认下架  
**Then** Toast「SKU 已下架」并刷新列表

## AC-006 SKU 上架/恢复 MUST 二次确认后再调 API

**Given** 行 `status` 为 `DRAFT`、`NEEDS_COMPLETION` 或 `DISABLED`  
**When** 点击「上架」或「恢复」  
**Then** MUST NOT 立即调用 `publish` API  
**And** MUST 展示确认 modal  
**When** 确认  
**Then** Toast「SKU 已上架」（或等价）并刷新列表

## AC-007 SKU 上下架 modal MUST 可取消且无副作用

**Given** SKU 上下架/恢复确认 modal 已打开  
**When** 取消或关闭 modal  
**Then** MUST NOT 调用 publish/unpublish API  
**And** SKU 状态 MUST 不变

## AC-008 modal 视觉与结构 MUST 对齐 Golden Reference

**Given** 修复完成  
**When** 并排对比用户/SKU 确认 modal 与 `TileCategoryManagementPage` 启停确认  
**Then** MUST 使用相同 modal 类名（`modal-backdrop`、`modal-card`、`modal-head`、`modal-body`、`modal-footer`）  
**And** 按钮层级：次按钮「取消」、主按钮确认操作  
**And** TSX/CSS MUST NOT 新增裸 Hex；使用既有管理端 semantic token / CSS 变量

## AC-009 品牌/类目/SKU 删除 MUST NOT 回归

**Given** 本 BUG 修复已合并  
**When** 在 `/admin/brands`、`/admin/tile-categories`、`/admin/tile-skus` 执行已有 confirm 流程（品牌启停、类目启停、各页删除）  
**Then** 行为 MUST 与修复前一致  
**And** `BrandManagementPage.test.tsx` 启停确认用例 MUST 保持通过  
**And** `TileCategoryManagementPage.test.tsx` 启停确认用例 MUST 保持通过

## AC-010 重置密码 confirm 不在本 BUG scope

**Given** 用户列表「重置密码」  
**When** 点击操作  
**Then** MAY 仍使用 `window.confirm` 直至 **BUG-0017** 修复  
**And** 本 BUG 验收 MUST NOT 将重置密码 modal 统一作为通过条件

## AC-011 自动化 MUST 覆盖确认门禁

**Given** `fix-admin-list-status-action-confirm` 已 `/opsx-apply`  
**When** 运行 `UserManagementPage` / `TileSkuManagementPage` vitest  
**Then** MUST 含：点击冻结/解冻/删除（SKU：上架/下架/恢复）→ 先出现 dialog → 确认前 mock API **未被调用**  
**And** MUST 含：取消/关闭 dialog 后 mock API **未被调用**  
**And** MUST 含：确认后主按钮 → mock API **被调用**  
**And** 既有「冻结后立即调 API」类断言 MUST 更新为 confirm 流程

## AC-012 修复范围 MUST 为纯前端（默认）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 默认 MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 需要 Orval 重新生成

## AC-013 权限与角色 MUST NOT 回归

**Given** 修复完成  
**When** `employee` 访问 SKU 页、`admin` 访问用户页  
**Then** 权限边界与修复前一致  
**And** `employee` MUST NOT 访问 `/admin/users` 写操作

## AC-014 部署冒烟

**Given** Docker 或本地环境已启动  
**When** `admin` 在用户页执行冻结（后解冻）；在 SKU 页执行下架（后恢复/上架）  
**Then** 每步 MUST 先 modal 确认再生效  
**And** Toast 与列表状态 MUST 正确

## AC-015 文档与流程

**Given** 修复经 OpenSpec `fix-admin-list-status-action-confirm` 进入开发  
**When** `/opsx-archive` 完成  
**Then** 本 BUG `trace.md` MUST 更新为 `done`  
**And** Change `trace.md` MUST 记录 AC-001～AC-009 手工或自动化验收结论
