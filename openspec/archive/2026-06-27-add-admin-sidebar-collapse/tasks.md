## 1. 准备与定位

- [x] 1.1 阅读 `REQ-0011-admin-sidebar-expand-collapse` requirement、acceptance、prototype context
- [x] 1.2 对照 `AdminLayout.tsx`、`AdminSidebar.tsx`、`AdminUserMenu.tsx`、`admin-home.css`
- [x] 1.3 确认 REQ-0010 brand-head 现状；不涉及 API、数据库、Orval、店主端 Sidebar

## 2. Layout 状态与持久化

- [x] 2.1 `AdminLayout` 增加 `sidebarCollapsed` state + `localStorage`（`admin-sidebar-collapsed`）
- [x] 2.2 `.admin-shell` 设置 `data-sidebar-state` 与 `--admin-sidebar-width`（264/72）
- [x] 2.3 宽度过渡 ~220ms；`prefers-reduced-motion` 处理

## 3. Chevron 与头部

- [x] 3.1 `AdminSidebar` 头部 `.sidebar-head`：brand/REQ-0010 brand-head + 右上 chevron
- [x] 3.2 chevron `aria-expanded`、`aria-label`、键盘 Enter/Space
- [x] 3.3 expanded：`‹`；collapsed：`›`

## 4. Collapsed 裁剪 CSS

- [x] 4.1 collapsed 隐藏：`.nav-title`、nav 文案、用户姓名/邮箱、brand 文案/版本 pill
- [x] 4.2 collapsed 保留：nav 图标、active accent、avatar、logo 缩略
- [x] 4.3 nav 项 `aria-label`；`.nav-scroll` 无横向滚动

## 5. 用户菜单与 responsive

- [x] 5.1 collapsed 态 `AdminUserMenu` 仅 avatar；dropdown 行为不变
- [x] 5.2 ≤1023px：隐藏/禁用 chevron；不修改现有 @media grid/nav

## 6. 测试

- [x] 6.1 Vitest：chevron toggle、`aria-expanded`、localStorage
- [x] 6.2 Vitest：collapsed 态 active 项仍带 `active` class（SHOULD）
- [x] 6.3 `cd src/web && pnpm test` 与 `pnpm build`

## 7. 验收与追溯

- [x] 7.1 1280×1024 并排 `admin-sidebar-expanded.html` / `admin-sidebar-collapsed.html` checklist
- [x] 7.2 可选导出 PNG Golden（非阻塞 archive）
- [x] 7.3 更新 `REQ-0011` trace 与 `openspec/changes/add-admin-sidebar-collapse/trace.md` checklist
