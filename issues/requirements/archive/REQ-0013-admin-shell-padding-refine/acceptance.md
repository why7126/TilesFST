---
title: 需求验收标准
purpose: REQ-0013 管理端 Shell padding 与 content fluid 验收
content: 基于 requirement.md 与 prototype/web/admin-shell-padding-refine-*
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: done
created_at: 2026-06-28 09:20:59
updated_at: 2026-07-11 17:18:39
note: REQ-0013-admin-shell-padding-refine
---

# 验收标准

## 0. 归档验收结论

- [x] **AC-000** 本 REQ 已按当前实际由 `BUG-0054-admin-content-padding-too-large` / `fix-admin-content-padding-too-large` 闭环交付并归档。
- [x] **AC-000A** 原 REQ-0013 探索阶段目标 `32px 32px 72px`、`min(1400px, 100%)`、expanded sidebar `6px` 不再作为最终验收目标；当前事实源为 `BUG-0054` 采用的 `24px 24px 48px`、`min(1440px, 100%)` 方案。
- [x] **AC-000B** 关联 Change `fix-admin-content-padding-too-large` 已归档；无 API / DB / Orval / Docker 影响。

## 1. 主内容 padding（FR-001）

- [x] **AC-001** desktop（>1023px）`.main-content` padding 为当前落地值 **`24px 24px 48px`**（top / horizontal / bottom）。
- [x] **AC-002** bottom padding 已按 `BUG-0054` 修订为 **48px**；旧 72px 目标废止。
- [x] **AC-003** 主内容区仍 `overflow: auto`；shell 层无新增横向滚动条（表格内容超宽除外）。

## 2. 侧栏 padding — expanded（FR-002）

- [x] **AC-004** desktop expanded `.sidebar` padding 当前落地为 **`30px 10px 18px`**，已较原始 18px 水平 padding 收窄。
- [x] **AC-005** `.sidebar-head`、`.nav-title`、`.nav-item` 保持当前实现下的对齐与可读性。
- [x] **AC-006** 最长菜单项「Banner 管理」在 264px 列内无异常换行。
- [x] **AC-007** chevron 不遮挡 `TILESFST` 与 version badge（REQ-0010 / REQ-0011 回归）。
- [x] **AC-008** `--admin-sidebar-width` expanded 仍为 **264px**。

## 3. 侧栏 padding — collapsed（FR-003）

- [x] **AC-009** desktop collapsed `.sidebar` padding 当前落地为 **`16px 10px 18px`**。
- [x] **AC-010** collapsed 列宽仍为 **72px**；`.nav-scroll` 无横向滚动条回归。
- [x] **AC-011** 34px avatar、16px nav-icon、28px toggle 正常居中；`AdminUserMenu` dropdown 行为与 REQ-0011 一致。
- [x] **AC-012** collapsed 态按当前实现验收；历史 prototype 仅作背景参考。

## 4. Content-inner fluid — 策略 B（FR-004）

- [x] **AC-013** `.content-inner` 使用 **`max-width: min(1440px, 100%)`** 与 `margin: 0 auto`。
- [x] **AC-014** `tile-sku-management.css` 中 `:has(.sku-page-hero) .content-inner { max-width: 1120px }` **已删除**。
- [x] **AC-015** 其他页面 CSS 无 divergent content-inner / settings-content-inner 旧宽度 override。
- [x] **AC-016** **1920×1080** expanded：content-inner 受 1440px 软 cap 约束。
- [x] **AC-017** **1440×1024** expanded：content-inner 随可用宽度 fluid。

## 5. Gutter 阈值（FR-006，对照变更前）

- [x] **AC-018** **1920×1080** expanded：无 1080px 旧硬上限导致的明显死区。
- [x] **AC-019** **1920×1080** expanded：content-inner 右侧不再受 1080px / 1120px 旧策略限制。
- [x] **AC-020** **1440×1024** expanded：content-inner 随可用宽度 fluid。

## 6. 响应式（FR-005）

- [x] **AC-021** **≤1023px**：sidebar padding **非** desktop 紧凑 padding；当前为 **`22px 20px`**。
- [x] **AC-022** **≤1023px**：`.main-content` padding 为 **`20px 16px 40px`**。
- [x] **AC-023** **≤639px**：`.main-content` padding 为 **`16px 12px 32px`**。
- [x] **AC-024** ≤1023px 仍隐藏 sidebar-user、chevron；双列 nav 结构不变（REQ-0011 回归）。

## 7. 基准页验收（FR-006）

- [x] **AC-025** `/admin/tile-skus`：旧 1120px override 已清理；表格/筛选不再被旧上限限制。
- [x] **AC-026** `/admin/users`：用户列表、分页和操作列无布局回归。
- [x] **AC-027** `/admin/dashboard`：metric/quick grid 保持可读。
- [x] **AC-028** 其余 `/admin/*` smoke：无 shell 级布局错位或横向溢出记录。

## 8. 视觉与原型

- [x] **AC-029** desktop expanded 以当前实现和 `BUG-0054` 归档记录为准；历史 prototype 不再作为强约束。
- [x] **AC-030** 样式使用 admin semantic token；TSX/CSS **无**新增裸 Hex。
- [x] **AC-031** `prefers-reduced-motion: reduce` 下 padding/width transition 仍可用（不强制动画）。
- [x] **AC-032** PNG Golden 不再阻塞归档，保留为历史候选：
  - `prototype/web/images/admin-shell-padding-1440-expanded.png`
  - `prototype/web/images/admin-shell-padding-1920-expanded.png`
  - `prototype/web/images/admin-shell-padding-collapsed-sku.png`
  - `prototype/web/images/admin-shell-padding-tablet-1023.png`

## 9. 自动化与构建（FR-007）

- [x] **AC-033** vitest：`AdminSidebar.collapse.test.tsx` 已在 `BUG-0054` Change 验证中通过。
- [x] **AC-034** vitest：`AdminLayout.test.tsx` 已在 `BUG-0054` Change 验证中通过。
- [x] **AC-035** vitest / 静态断言：旧 content width 与 padding 策略不再出现。
- [x] **AC-036** `localStorage` 侧栏折叠偏好（REQ-0011）未被破坏。
- [x] **AC-037** `pnpm --dir src/web build` 已在 `BUG-0054` Change 验证中通过。

## 10. 范围与不回归

- [x] **AC-038** 无 API / OpenAPI / Orval / 数据库变更。
- [x] **AC-039** 店主端 / 小程序 **无** shell padding 变更。
- [x] **AC-040** BUG-0021 导航图标 **不在** 本 REQ 范围（可并行）。
- [x] **AC-041** 变更经 OpenSpec `fix-admin-content-padding-too-large` 开发并 archive。
