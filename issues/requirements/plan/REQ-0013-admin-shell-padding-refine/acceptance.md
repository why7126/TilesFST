---
title: 需求验收标准
purpose: REQ-0013 管理端 Shell padding 与 content fluid 验收
content: 基于 requirement.md 与 prototype/web/admin-shell-padding-refine-*
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 09:20:59
updated_at: 2026-06-28 09:20:59
note: REQ-0013-admin-shell-padding-refine
---

# 验收标准

## 1. 主内容 padding（FR-001）

- [ ] **AC-001** desktop（>1023px）`.main-content` padding 为 **`32px 32px 72px`**（top / horizontal / bottom）。
- [ ] **AC-002** bottom padding **MUST 保持 72px**；不得改为其他值。
- [ ] **AC-003** 主内容区仍 `overflow: auto`；shell 层无新增横向滚动条（表格内容超宽除外）。

## 2. 侧栏 padding — expanded（FR-002）

- [ ] **AC-004** desktop expanded `.sidebar` padding 为 **`30px 6px 18px`**。
- [ ] **AC-005** `.sidebar-head`、`.nav-title`、`.nav-item` 水平 padding 联动收紧；分区标题与 nav 项左缘视觉对齐（对照 `prototype/web/admin-shell-padding-refine-expanded.html`）。
- [ ] **AC-006** 最长菜单项「Banner 管理」在 264px 列内无异常换行。
- [ ] **AC-007** chevron 不遮挡 `TILESFST` 与 version badge（REQ-0010 / REQ-0011 回归）。
- [ ] **AC-008** `--admin-sidebar-width` expanded 仍为 **264px**。

## 3. 侧栏 padding — collapsed（FR-003）

- [ ] **AC-009** desktop collapsed `.sidebar` padding 为 **`12px 6px 14px`**（±2px 须同步更新 prototype）。
- [ ] **AC-010** collapsed 列宽仍为 **72px**；`.nav-scroll` 无横向滚动条。
- [ ] **AC-011** 34px avatar、16px nav-icon、28px toggle 正常居中；`AdminUserMenu` dropdown 行为与 REQ-0011 一致。
- [ ] **AC-012** collapsed 态与 `prototype/web/admin-shell-padding-refine-collapsed.html` 并排验收。

## 4. Content-inner fluid — 策略 B（FR-004）

- [ ] **AC-013** `.content-inner` 使用 **`max-width: min(1400px, 100%)`** 与 `margin: 0 auto`（或等价 CSS 变量 `--admin-content-max-width`）。
- [ ] **AC-014** `tile-sku-management.css` 中 `:has(.sku-page-hero) .content-inner { max-width: 1120px }` **已删除**。
- [ ] **AC-015** 其他页面 CSS **无** divergent content-inner max-width override。
- [ ] **AC-016** **1920×1080** expanded：content-inner 实测宽度 **1400px**。
- [ ] **AC-017** **1440×1024** expanded：content-inner 实测宽度 **≥1110px**（fluid 吃满可用宽，无 >48px 对称死区）。

## 5. Gutter 阈值（FR-006，对照变更前）

- [ ] **AC-018** **1920×1080** expanded：侧栏右缘至 content-inner 左缘 **≤128px**（变更前约 288px）。
- [ ] **AC-019** **1920×1080** expanded：content-inner 右缘至视口右缘 **≤128px**。
- [ ] **AC-020** **1440×1024** expanded：侧栏右缘至 content-inner 左缘 **≤32px**。

## 6. 响应式（FR-005）

- [ ] **AC-021** **≤1023px**：sidebar padding **非** desktop 6px；与 `admin-shell-padding-refine-tablet.html` 一致（约 **18px 16px**）。
- [ ] **AC-022** **≤1023px**：`.main-content` padding 约 **`24px 20px 56px`**。
- [ ] **AC-023** **≤639px**：`.main-content` padding 约 **`24px 16px 40px`**。
- [ ] **AC-024** ≤1023px 仍隐藏 sidebar-user、chevron；双列 nav 结构不变（REQ-0011 回归）。

## 7. 基准页验收（FR-006）

- [ ] **AC-025** `/admin/tile-skus`：1440 & 1920 expanded；1920 collapsed 另验；表格/筛选无错位。
- [ ] **AC-026** `/admin/users`：1440 & 1920；分页 DOM 仍对齐 `admin-list-page-consistency`。
- [ ] **AC-027** `/admin/dashboard`：1440 & 1920；metric/quick 四列 grid 可读、不过散。
- [ ] **AC-028** 其余 `/admin/*` smoke：无 shell 级布局错位或横向溢出。

## 8. 视觉与原型

- [ ] **AC-029** desktop expanded 与 `prototype/web/admin-shell-padding-refine-expanded.html` 并排验收。
- [ ] **AC-030** 样式使用 admin semantic token；TSX/CSS **无**新增裸 Hex。
- [ ] **AC-031** `prefers-reduced-motion: reduce` 下 padding/width transition 仍可用（不强制动画）。
- [ ] **AC-032** PNG Golden（**待导出**，非阻塞 req-opsx）：
  - `prototype/web/images/admin-shell-padding-1440-expanded.png`
  - `prototype/web/images/admin-shell-padding-1920-expanded.png`
  - `prototype/web/images/admin-shell-padding-collapsed-sku.png`
  - `prototype/web/images/admin-shell-padding-tablet-1023.png`

## 9. 自动化与构建（FR-007）

- [ ] **AC-033** vitest：`AdminSidebar.collapse.test.tsx` 全通过。
- [ ] **AC-034** vitest：`AdminLayout.test.tsx` 全通过。
- [ ] **AC-035** vitest（SHOULD）：collapsed 态 `.nav-scroll` 无横向溢出。
- [ ] **AC-036** `localStorage` 侧栏折叠偏好（REQ-0011）未被破坏。
- [ ] **AC-037** `cd src/web && pnpm test` 与 `pnpm build` 通过。

## 10. 范围与不回归

- [ ] **AC-038** 无 API / OpenAPI / Orval / 数据库变更。
- [ ] **AC-039** 店主端 / 小程序 **无** shell padding 变更。
- [ ] **AC-040** BUG-0021 导航图标 **不在** 本 REQ 范围（可并行）。
- [ ] **AC-041** 变更经 OpenSpec `fix-admin-shell-padding-refine` 开发并 archive。
