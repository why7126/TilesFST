---
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-28 16:14:20
updated_at: 2026-06-28 16:14:20
related_requirement: REQ-0009-tile-spec-management
suggested_fix_change: fix-tile-spec-status-confirm-ui
related_requirements:
  - REQ-0009-tile-spec-management
  - REQ-0005-tile-category-management
  - REQ-0008-brand-status-confirm
related_bug: null
---

# 回归验收标准

> 修复本缺陷 MUST 对齐 REQ-0009 **AC-013**（启停 confirm 对齐 `BrandManagementPage`）、**AC-018**（删除 confirm），并以 `TileCategoryManagementPage` 启停/删除 confirm 为 Golden Reference。**不在 scope**：分页（BUG-0027）、表单弹窗（BUG-0028）、列表刷新（BUG-0029）、启停/删除 API 与业务校验、后端错误码。

## AC-001 停用规格 MUST 二次确认后再调 API

**Given** `admin` 位于 `/admin/tile-specs`，目标规格 `status=ENABLED`  
**When** 点击行内「停用」  
**Then** MUST NOT 立即调用 `POST /api/v1/admin/tile-specs/{id}/disable`  
**And** MUST 展示确认 modal（`role="dialog"`、`aria-modal="true"`）  
**And** 标题 MUST 为「停用规格」  
**And** 正文 MUST 含 `确认停用规格「{display_name}」？停用后前台将不再展示该规格。`  
**And** 底部 MUST 含「取消」与主按钮「确认停用」  
**When** 点击「确认停用」  
**Then** MUST 调用 disable API  
**And** Toast「规格已停用」（或等价）且列表刷新

## AC-002 启用规格 confirm MUST 对齐类目页模式

**Given** `admin` 位于 `/admin/tile-specs`，目标规格 `status=DISABLED`  
**When** 点击行内「启用」  
**Then** MUST 展示 confirm modal，标题「启用规格」  
**And** 正文 MUST 含 `确认启用规格「{display_name}」？`  
**And** 主按钮 MUST 为「确认启用」  
**And** 确认前 MUST NOT 调用 enable API

## AC-003 删除规格 confirm MUST 对齐类目页模式

**Given** `admin` 位于 `/admin/tile-specs`，目标规格满足 `sku_count=0` 且 `status=DISABLED`  
**When** 点击行内「删除」  
**Then** MUST 展示 confirm modal，标题「删除规格」  
**And** 正文 MUST 含 `确认删除规格「{display_name}」？此操作不可恢复。` 且使用 `page-desc`  
**And** 主按钮 MUST 为「删除规格」且使用 `btn primary`（MUST NOT 使用 `danger` 变体）  
**And** 确认前 MUST NOT 调用 DELETE API

## AC-004 confirm modal MUST 可取消且无副作用

**Given** 任一启停/删除 confirm modal 已打开  
**When** 点击「取消」、遮罩或标题区 ×  
**Then** modal MUST 关闭  
**And** MUST NOT 调用 enable/disable/delete API  
**And** 列表数据 MUST 不变

## AC-005 modal 视觉与结构 MUST 对齐 Golden Reference

**Given** 修复完成  
**When** 并排对比规格页 confirm modal 与 `TileCategoryManagementPage` 同类 confirm  
**Then** MUST 使用相同 modal 类名（`modal-backdrop`、`modal-card`、`modal-head`、`modal-body`、`modal-footer`）  
**And** MUST NOT 使用 `confirm-card` class  
**And** 标题区 MUST 含 `modal-close`（×）与 `aria-labelledby`  
**And** 正文 MUST 使用 `page-desc`  
**And** TSX/CSS MUST NOT 新增裸 Hex

## AC-006 BUG-0027/28/29 已交付项 MUST NOT 回归

**Given** 本 BUG 修复已合并  
**When** 在 `/admin/tile-specs` 验证分页、表单弹窗、保存后列表刷新  
**Then** 行为 MUST 与 `fix-tile-spec-admin-ui` 验收结论一致  
**And** `TileSpecManagementPage.test.tsx` 既有用例 MUST 保持通过

## AC-007 类目/品牌 confirm MUST NOT 回归

**Given** 本 BUG 修复已合并  
**When** 在 `/admin/tile-categories`、`/admin/brands` 执行启停/删除 confirm  
**Then** 行为 MUST 与修复前一致  
**And** `TileCategoryManagementPage.test.tsx`、`BrandManagementPage.test.tsx` confirm 用例 MUST 保持通过

## AC-008 自动化 MUST 覆盖停用 confirm 门禁

**Given** `fix-tile-spec-status-confirm-ui` 已 `/opsx-apply`  
**When** 运行 `TileSpecManagementPage` vitest  
**Then** MUST 含：点击「停用」→ 先出现 dialog → 确认前 `disableTileSpec` mock **未被调用**  
**And** MUST 含：dialog 内文案含「停用后前台将不再展示该规格。」  
**And** MUST 含：点击「确认停用」→ mock **被调用**

## AC-009 修复范围 MUST 为纯前端（默认）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 默认 MUST 仅涉及 `src/web/` 与测试  
**And** MUST NOT 修改后端 API、SQLite schema、Orval 生成接口

## AC-010 REQ-0009 AC-013 / AC-018 对齐确认

**Given** BUG-0037 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0009-tile-spec-management/acceptance.md`  
**Then** AC-013（启停 confirm 对齐品牌页）与 AC-018（删除 confirm）MUST 标记为通过

## AC-011 PNG 并排验收（可选增强）

**Given** 修复完成  
**When** 1440×1024 下并排对比规格停用 confirm 与类目停用 confirm 截图  
**Then** 标题区、正文 Typography、按钮区 MUST 视觉一致（记录于 Change `trace.md`）
