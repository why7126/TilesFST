---
bug_id: BUG-0013-product-version-ui-inconsistency
status: pending_review
created_at: 2026-06-27 10:59:01
updated_at: 2026-06-27 10:59:01
related_requirement: REQ-0010-product-version-display
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0010 **AC-006**（Golden Reference 布局）、**AC-013**（semantic token 小号 badge）、**AC-015**（原型 HTML 并排），且 MUST NOT 回归 FR-001 版本常量、FR-002/FR-003 展示位置与 a11y。

## AC-001 版本 pill MUST 呈现可辨识的 badge 容器形态

**Given** 管理员已登录 Web 管理端  
**When** 查看 `AdminSidebar` 顶部 brand-head  
**Then** 版本号 MUST 以带边框、浅背景的小号 pill 呈现，而非裸文字  
**And** pill 与 `TILESFST` 品牌名垂直居中对齐、同一行 flex 排列（gap 约 8px）

## AC-002 pill 样式 MUST 对齐 REQ-0010 原型与 Design System

**Given** 修复完成  
**When** 检查 `ProductVersionBadge`（或 `Badge` variant）实现  
**Then** MUST 使用 semantic token（`text-muted`/`text-subtle`、`border-border-chip` 或 `border-border-default`、`bg-surface/30` 或 DS badge 背景 token）  
**And** MUST 含 `padding: 2px 7px` 等价、`font-weight: 500`、`tracking-badge`（或 prototype 约定的 0.04em）  
**And** TSX/CSS MUST NOT 含裸 Hex  
**And** SHOULD 复用或扩展 `src/web/src/shared/ui/badge.tsx`，避免与 DS §8 平行实现

## AC-003 1280×1024 并排验收 MUST 通过

**Given** 修复完成  
**When** 管理端与 `prototype/web/product-version-sidebar-admin.html`、Golden Reference PNG 并排对比  
**Then** 版本 pill 的高度（约 18px）、圆角、边框可见度、文字弱化层级 MUST 与原型语义一致  
**And** 店主端与 `prototype/web/product-version-sidebar-catalog.html` 并排对比 MUST 同样通过  
**And** Change `trace.md` MUST 记录并排验收结论

## AC-004 管理端 brand-head MUST 无布局回归

**Given** 管理员访问任意 `/admin/*` 页面  
**When** 查看侧边栏  
**Then** `TILESFST` 品牌名 MUST 保持 serif 金色、`letter-spacing: 0.16em`  
**And** 导航项、用户菜单、主内容区布局 MUST 无回归（REQ-0010 AC-008）

## AC-005 店主端 MUST 与管理端 pill 视觉一致

**Given** 访问店主端带侧栏页面（如 `LandingPage` / `ListPage`）  
**When** 查看 Sidebar 顶部 brand-head  
**Then** 版本 pill MUST 与管理端使用同一组件/variant，视觉一致  
**And** 版本值 MUST 仍为同一 `PRODUCT_VERSION` 常量（REQ-0010 AC-010）

## AC-006 a11y MUST 保持

**Given** 修复完成  
**When** 检查 brand-head 或 badge  
**Then** MUST 保留 `aria-label`（如「产品版本 v0.0.1」）与可见版本文案（REQ-0010 AC-014）

## AC-007 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite schema、Orval 生成物  
**And** MUST NOT 修改 `PRODUCT_VERSION` 维护策略（仍为人工常量）

## AC-008 测试 MUST 覆盖样式断言

**Given** 进入 `fix-product-version-ui-inconsistency`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** Vitest MUST 断言 `AdminSidebar` / `Sidebar` 渲染的版本元素含 pill 关键 class（边框、muted 文字等）  
**And** `cd src/web && pnpm test` 与 `pnpm build` MUST 通过

## AC-009 REQ-0010 视觉 AC MUST 闭环

**Given** BUG-0013 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0010-product-version-display/acceptance.md`  
**Then** AC-006、AC-013、AC-015 MUST 可由 REQ-0010 验收勾选通过
