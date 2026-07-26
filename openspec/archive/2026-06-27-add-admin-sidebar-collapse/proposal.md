## Why

REQ-0011-admin-sidebar-expand-collapse 要求管理端导航侧栏支持桌面端展开（264px）与收起（72px icon 列），头部右上角 chevron 切换，并持久化用户偏好。当前 `AdminLayout` / `admin-home.css` 固定 264px，无法为主内容区释放横向空间。REQ-0010 已将折叠 chevron 列为 Out of scope，由本 change 承接。

## What Changes

- `AdminLayout` 持有 `sidebarCollapsed` state，读写 `localStorage`（`admin-sidebar-collapsed`）；默认 expanded。
- `AdminSidebar` 头部右上角 chevron（expanded `‹` / collapsed `›`）；`data-sidebar-state` 或等价 class。
- `.admin-shell` 网格第一列由 CSS 变量 `--admin-sidebar-width`（264px / 72px）驱动；200–250ms transition。
- collapsed 态：隐藏产品名/副标题/版本 pill（若 REQ-0010 brand-head 已落地）、分区标题、nav 文案、用户姓名/邮箱；保留 logo 缩略、nav 图标、active accent、avatar 菜单。
- Vitest：toggle、`aria-expanded`、localStorage；HTML 原型并排验收。
- **不** 变更后端 API、数据库、Orval、店主端 `Sidebar`、≤1023px responsive 布局。

## Capabilities

### New Capabilities

（无新 capability 目录；交互归入 `admin-dashboard` 与 `web-client` delta。）

### Modified Capabilities

- `admin-dashboard`：MODIFIED「管理端工作台 Shell 布局」— 可变侧栏宽度 grid；MODIFIED「管理端 Sidebar 品牌与导航」— chevron 与 collapsed 裁剪；MODIFIED「管理端 Sidebar 用户菜单」— collapsed 仅 avatar。
- `web-client`：ADDED「管理端 Sidebar 展开/收起」— localStorage、无障碍、桌面端边界。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无 |
| 前端 Web 管理端 | `AdminLayout.tsx`、`AdminSidebar.tsx`、`AdminUserMenu.tsx`、`admin-home.css` |
| 店主端 | 无 |
| `src/shared/` | 无（可选 localStorage key 常量） |
| 数据库 | 无 |
| API / Orval | 无 |
| 依赖 REQ | REQ-0010 brand-head（若已 apply，chevron 依附同一头部；未 apply 时保留 `.logo` + chevron） |
| 测试 | vitest AdminLayout/AdminSidebar；1280×1024 HTML 原型并排 |
| Docker | 可选 `pnpm build`；无 compose 变更 |

## 风险

- REQ-0010 头部 DOM 未就绪时 chevron 位置需兼容 `.logo`；REQ-0010 apply 后不得重做 toggle 逻辑。
- 桌面折叠与 ≤1023px 顶栏导航模型分离：mobile MUST NOT 启用 chevron。
