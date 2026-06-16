## 1. CSS Port 与模块结构

- [x] 1.1 创建 `src/web/src/features/admin/styles/admin-home.css`，自 `admin-home.html` port CSS，颜色映射 `var(--color-*)`
- [x] 1.2 创建 `features/admin/data/dashboard-mock.ts`（指标 + 最近更新样例，对齐 HTML）
- [x] 1.3 创建 `features/admin/components/AdminSidebar.tsx`、`AdminUserMenu.tsx`（port CSS class 结构）
- [x] 1.4 创建 Dashboard 子组件：`DashboardMetrics`、`DashboardQuickActions`、`DashboardRecentUpdates`

## 2. 布局与页面重构

- [x] 2.1 重构 `AdminLayout.tsx` 为 `admin-shell` 网格（264px + 1fr），移除顶栏与外露退出按钮
- [x] 2.2 接入 `AdminSidebar` + `<Outlet />` 于 `main.main-content`
- [x] 2.3 重构 `DashboardPage.tsx` 为三模块工作台（概览 / 快捷操作 / 最近更新）
- [x] 2.4 实现 Sidebar 导航 active 态（首页 `/admin/dashboard`）与非首页占位反馈
- [x] 2.5 实现用户菜单下拉：个人资料/密码修改占位、退出调用 `useAuth().logout` 并跳转登录页
- [x] 2.6 实现用户展示 fallback（display_name、头像缩写、email fallback）

## 3. 响应式

- [x] 3.1 添加 `<1024px` 媒体查询：Sidebar 顶置、隐藏用户菜单（对齐 context）
- [x] 3.2 添加 `<640px` 媒体查询：网格单列、表格隐藏操作人列

## 4. Design System 预览

- [x] 4.1 在 `/design-system` 增加 Admin Shell / Dashboard 预览区块（可选片段）

## 5. 测试

- [x] 5.1 补充 AdminLayout / AdminUserMenu smoke 测试（渲染、下拉、logout 调用）
- [x] 5.2 补充 DashboardPage 测试（四指标、四快捷操作、表格列）
- [x] 5.3 运行 `cd src/web && npx vitest run src/features/admin src/pages/admin`

## 6. 构建与部署

- [x] 6.1 运行 `cd src/web && npm run build`
- [x] 6.2 运行 `./scripts/docker-up.sh` 或 `docker compose build web` 验证 `/admin/dashboard`

## 7. 视觉验收（PNG Golden Reference Gate）

- [x] 7.1 1280×1024 视口并排对比 `/admin/dashboard` 与 `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.png`
- [x] 7.2 填写 `openspec/changes/add-admin-home/trace.md` PNG checklist（≥18 项，全部 pass 或记录可接受偏差）
- [x] 7.3 确认页面无：欢迎区、待办、数据质量、风险提醒、热门材质、门店同步、材质库存、V4 已删快捷操作

## 8. 文档与追溯

- [x] 8.1 更新 `issues/requirements/REQ-0004-admin-home/trace.md`（change status: applied）
- [x] 8.2 更新 sprint acceptance-report（若已纳入 sprint-002）
- [x] 8.3 归档前确认 delta spec MODIFIED「退出登录」标题与 `openspec/specs/web-client/spec.md` 一致

## 9. 归档准备

- [ ] 9.1 本文件全部 `[x]` 后执行 `/opsx-archive add-admin-home`
