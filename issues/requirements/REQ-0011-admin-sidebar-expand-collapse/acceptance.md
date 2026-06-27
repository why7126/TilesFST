---
title: 需求验收标准
purpose: REQ-0011 管理端侧边栏展开/收起验收标准
content: 基于 requirement.md 与 prototype/web/admin-sidebar-collapse-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 10:25:49
updated_at: 2026-06-27 10:25:49
note: REQ-0011-admin-sidebar-expand-collapse
---

# 验收标准

## 1. 折叠状态与持久化（FR-001）

- [ ] **AC-001** 桌面端（> 1023px）侧栏支持 `expanded` 与 `collapsed` 两种状态；首次访问默认 **expanded**。
- [ ] **AC-002** 切换后写入 `localStorage`（key：`admin-sidebar-collapsed`）；刷新或跳转其他 `/admin/*` 页后状态恢复一致。
- [ ] **AC-003** 折叠 state 由 `AdminLayout`（或 Context）统一管理并传入 `AdminSidebar`，各业务页无重复实现。

## 2. 宽度与动画（FR-002）

- [ ] **AC-004** expanded 宽度 **264px**；collapsed 宽度 **72px**（通过 `--admin-sidebar-width` 或等价机制）。
- [ ] **AC-005** `.admin-shell` 第一列与 `.main-content` 随状态自适应；无内容被遮挡、无多余横向滚动条。
- [ ] **AC-006** 宽度过渡约 200–250ms；`prefers-reduced-motion: reduce` 下缩短或禁用动画。

## 3. Chevron 控件（FR-003）

- [ ] **AC-007** chevron 位于 `AdminSidebar` **头部右上角**，参照 SoulKing 参考图与 `prototype/web/admin-sidebar-expanded.html`。
- [ ] **AC-008** expanded 时 chevron 指向左（收起语义）；collapsed 时指向右（展开语义）。
- [ ] **AC-009** 按钮具备正确 `aria-expanded`、`aria-label`（收起/展开侧边栏）；键盘 Enter/Space 可切换。
- [ ] **AC-010** expanded 态 chevron 不遮挡产品名与版本 badge（REQ-0010 落地后并排验收）。

## 4. 展开态（FR-004）

- [ ] **AC-011** expanded 态展示完整：分区标题、nav 图标+文案、`AdminUserMenu` 全量（头像、姓名、邮箱）。
- [ ] **AC-012** REQ-0010 未落地时：至少保留现有 `.logo` + chevron；REQ-0010 落地后无需重做 chevron 位置。

## 5. 收起态（FR-005）

- [ ] **AC-013** collapsed 态隐藏：产品名、副标题、版本 badge、`.nav-title`、nav 文案、用户姓名/邮箱。
- [ ] **AC-014** collapsed 态保留：品牌/Logo 缩略区、各 nav `.nav-icon`、当前项 `active` 样式、用户 `.avatar`。
- [ ] **AC-015** collapsed 态 nav 按钮具备 `aria-label={label}` 或等价 tooltip。
- [ ] **AC-016** collapsed 态点击 avatar 仍可打开 dropdown（个人资料、密码修改、退出登录）。
- [ ] **AC-017** `.nav-scroll` 无横向滚动条。

## 6. 交互回归（FR-006）

- [ ] **AC-018** 折叠切换不改变 nav 路由与 placeholder 行为。
- [ ] **AC-019** 切换侧栏不卸载当前页、不丢失 `AdminLayout` notice 等局部状态。
- [ ] **AC-020** dropdown 点击外部关闭、选菜单项关闭行为与现网一致。

## 7. 响应式边界（FR-007）

- [ ] **AC-021** ≤ 1023px 沿用现有 responsive（顶栏双列 nav、隐藏 sidebar-user）；折叠 chevron 隐藏或禁用。
- [ ] **AC-022** 本 REQ 不修改 ≤ 1023px 下既有 grid/nav DOM 结构（回归对比 `admin-home.css` @media）。

## 8. 视觉与原型

- [ ] **AC-023** 1280×1024 桌面端与 `prototype/web/admin-sidebar-expanded.html`、`admin-sidebar-collapsed.html` 并排验收。
- [ ] **AC-024** 样式使用 admin semantic token / CSS variables；TSX/CSS 无新增裸 Hex。
- [ ] **AC-025** PNG Golden Reference：`prototype/web/images/admin-sidebar-expanded.png`、`admin-sidebar-collapsed.png`（**待导出**，非阻塞 req-opsx）。

## 9. 自动化与构建

- [ ] **AC-026** vitest：点击 chevron 切换 `data-sidebar-state` 或等价 class。
- [ ] **AC-027** vitest：`aria-expanded` 与状态一致；localStorage 读写。
- [ ] **AC-028** vitest（SHOULD）：collapsed 态 active 路由项仍带 `active` class。
- [ ] **AC-029** `cd src/web && pnpm test` 与 `pnpm build` 通过。

## 10. 范围与不回归

- [ ] **AC-030** 店主端 `Sidebar` 筛选栏 **无** 折叠 chevron（本期 Out）。
- [ ] **AC-031** 无 API / OpenAPI / Orval / 数据库变更。
- [ ] **AC-032** 变更经 OpenSpec `add-admin-sidebar-collapse`（或等价 change-id）开发并 archive。
