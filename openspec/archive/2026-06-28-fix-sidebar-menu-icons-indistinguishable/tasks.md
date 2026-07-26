## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0021-sidebar-menu-icons-indistinguishable` 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 REQ-0011 collapsed/expanded 原型 HTML 与 `AdminSidebar.tsx`、`admin-nav.ts`、`admin-home.css`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO、Docker compose 变更

## 2. 导航数据与渲染

- [x] 2.1 `AdminNavItem` 增加 `icon: LucideIcon`；为 7 个 id 配置语义 icon（见 design.md D1 映射表）
- [x] 2.2 `AdminSidebar` 渲染 `<item.icon className="nav-icon" size={16} strokeWidth={1.5} aria-hidden />`；移除空 `<span className="nav-icon" />`
- [x] 2.3 确认 employee 角色过滤 `users` 后其余 icon 仍可区分

## 3. 样式

- [x] 3.1 `admin-home.css`：`.nav-icon` 改为 SVG 容器（inline-flex、16px、currentColor）；移除 CSS 方块 border/::after
- [x] 3.2 确认 expanded/collapsed active、hover 样式无回归；TSX/CSS 无裸 Hex

## 4. 测试

- [x] 4.1 新增或扩展 Vitest：collapsed 态下至少 2 个 nav id 渲染不同 icon
- [x] 4.2 运行 `AdminSidebar.collapse.test.tsx`、`AdminSidebar.user-mgmt.test.tsx` 无回归
- [x] 4.3 运行 `cd src/web && pnpm test && pnpm build`

## 5. 验收与追溯

- [x] 5.1 1280×1024 expanded / collapsed 人工验收；记录于本 change `trace.md`
- [x] 5.2 对照 BUG-0021 acceptance AC-001～AC-010 勾选
- [x] 5.3 更新 `BUG-0021-sidebar-menu-icons-indistinguishable/trace.md` 中 `openspec_changes` 状态
- [x] 5.4 更新 `iterations/change/sprint-003/acceptance-report.md` BUG-0021 项（apply 完成后）
- [x] 5.5 评估 `docs/knowledge-base/incidents/`（本缺陷为 UI UX，通常不需要）

## 6. 归档准备

- [x] 6.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-sidebar-menu-icons-indistinguishable`
