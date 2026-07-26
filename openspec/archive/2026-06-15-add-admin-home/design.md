## Context

- **现状**：`/admin/dashboard` 为占位卡片；`AdminLayout` 为顶栏 + 主内容，退出按钮外露于 header。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/archive/REQ-0004-admin-home/prototype/web/admin-home.html`
  2. `issues/requirements/archive/REQ-0004-admin-home/prototype/web/admin-home.png`（Golden Reference）
  3. `issues/requirements/archive/REQ-0004-admin-home/prototype/web/admin-home-context.md`
  4. `issues/requirements/archive/REQ-0004-admin-home/acceptance.md`
  5. `rules/ui-design.md`
  6. `openspec/specs/`（已归档能力）
- **登录页先例**：`fix-login-css-port` 已验证 CSS Port + token 映射路径；管理端首页 HTML 含完整 `<style>`，适合同策略。
- **约束**：auth store / hooks / API / 路由守卫冻结；TSX MUST NOT 裸 Hex；现有 `shared/ui/sidebar.tsx` 为店主端**筛选** Sidebar，不可复用为管理导航。

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 退出登录位置 | Sidebar 用户下拉框 | 同 HTML | AC-013 禁止底部直接退出；REQ-0001 曾验收顶栏退出 | **MODIFIED** `web-client`「退出登录」：入口改为 Sidebar 下拉；移除顶栏退出 |
| 品牌大小写 | `TILESFST` 全大写 | 同 HTML | AC-006 TILESFST | 以 HTML 为准；实现 `.logo` 全大写 |
| 颜色 Hex 描述 | CSS 变量含 hex | 同 HTML | AC-033 禁止 TSX 裸 Hex | PRD hex 为参考；实现通过 `admin-home.css` 映射 `var(--color-*)` |
| 用户邮箱 | `admin@tilesfst.com` 样例 | 同 HTML | AC-012 来自 auth/me 或 fallback | `auth/me` 无 email 字段时使用 `{username}@tilesfst.com` 或隐藏邮箱行 |
| 快捷操作数量 | 4 项 | 4 项 | AC-022/023 | 一致；V4 已删 4 项不得回归 |
| 店主端 Sidebar | — | — | AC-032 放 shared/ui | 新建 `AdminNavSidebar`（导航型），**不**改造 catalog `Sidebar` |

## Goals / Non-Goals

**Goals:**

- 1440×1024（验收视口 1280×1024）桌面端 `/admin/dashboard` 与 `admin-home.png` 并排判定为一致或可接受偏差。
- 自 `admin-home.html` port `admin-home.css`；React 负责 DOM、路由、auth 交互。
- Sidebar 264px / 100vh sticky；右侧 100vh 独立滚动；用户菜单固定底部。
- Dashboard 三模块 + mock 数据与 HTML 样例一致。
- ≥18 项 PNG diff checklist 写入 change `trace.md`。

**Non-Goals:**

- Dashboard 统计 / 最近更新真实 API。
- SKU、品牌、类目、Banner 列表与表单页。
- 个人资料、密码修改完整流程。
- 修改 auth API、store、ProtectedRoute 行为。
- 小程序管理端。

## Decisions

### D1：CSS Port 为主策略（路径 A）

- **决策**：新增 `src/web/src/features/admin/styles/admin-home.css`（或 `pages/admin/styles/`），从 `admin-home.html` port CSS；class 保留 HTML 语义（`admin-shell`、`sidebar`、`main-content`、`metric-card` 等）。
- **Token 映射**（与登录页一致）：

  | HTML 变量 | Token CSS 变量 |
  |-----------|----------------|
  | `--page` | `--color-page` |
  | `--deep` | `--color-deep` |
  | `--card` | `--color-surface` |
  | `--text` | `--color-text-primary` |
  | `--muted` | `--color-text-secondary` |
  | `--weak` | `--color-text-muted` |
  | `--gold` | `--color-brand-gold` |
  | `--line` | `--color-border-default` |
  | `--line-strong` | `--color-border-emphasis` |
  | `--danger` | `--color-danger` 或 ui-design 风险色 token |

- **理由**：HTML 含多层渐变、0.5px 边框、backdrop-filter；Tailwind 拼装难以还原。
- **备选 B**：Tailwind + semantic class — 适合无 HTML 的场景；本 REQ 有完整 HTML，fidelity 风险高。

### D2：组件结构（presentation / logic 分离）

```text
AdminLayout
  ├─ admin-shell (grid 264px 1fr)
  ├─ AdminSidebar (port CSS)
  │    ├─ logo TILESFST
  │    ├─ AdminNav (OPERATIONS + SYSTEM)
  │    └─ AdminUserMenu (trigger + dropdown)
  └─ main.main-content
       └─ <Outlet /> → DashboardPage
```

- 逻辑：`useAuth()` 提供 user / logout；导航 active 态由 `useLocation()` 驱动。
- 文件建议：
  - `src/web/src/features/admin/components/AdminSidebar.tsx`
  - `src/web/src/features/admin/components/AdminUserMenu.tsx`
  - `src/web/src/features/admin/components/DashboardMetrics.tsx` 等
  - `src/web/src/features/admin/data/dashboard-mock.ts`

### D3：Auth 冻结

- **决策**：不修改 `features/auth/store`、`useAuth`、`ProtectedRoute`、Orval 生成客户端。
- **退出**：`AdminUserMenu` 调用现有 `logout()` + `navigate('/admin/login')`。
- **用户展示**：`display_name` → 用户名；头像缩写取 display_name 或 username 前两字符大写；email fallback 见 Conflict Resolution。

### D4：Mock 数据与占位导航

- **决策**：指标与最近更新读取 `dashboard-mock.ts`；Sidebar 非首页项与快捷操作点击展示 toast「功能建设中」或跳转 `/admin/coming-soon`（可选轻量占位页）。
- **理由**：PRD 明确本期不接真实接口与子模块。

### D5：响应式

- 按 `admin-home-context.md`：`<1024px` Sidebar 顶置、隐藏用户菜单；`<640px` 网格单列、表格隐藏操作人列。
- 验收以桌面 1280×1024 为主 gate；响应式为 secondary checklist。

### D6：Design System 预览

- 在 `/design-system` 增加 Admin Shell 预览区块（AdminSidebar + Dashboard 片段），便于 token 与组件验收。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 专用 CSS 与 Tailwind 分叉 | 限定 scope 为 admin-home；颜色 MUST 走 `--color-*` |
| 误复用 catalog Sidebar | 新建 `AdminNavSidebar`，命名与路径区分 |
| REQ-0001 退出入口验收冲突 | delta spec MODIFIED「退出登录」；sprint acceptance 注明迁移 |
| auth/me 无 email | fallback 策略写入组件，AC-012 不阻塞 |
| 占位链接过多 | 统一 toast，避免空路由 404 |

## Migration Plan

1. 实现新 AdminLayout + Dashboard，删除旧顶栏退出 UI。
2. 登录成功跳转路径不变（`/admin/dashboard`）。
3. 无 DB/API 迁移；Web 镜像重建即可。
4. 回滚：恢复旧 `AdminLayout.tsx` / `DashboardPage.tsx`。

## Open Questions

- （无阻塞项）策略已选 CSS Port；若产品要求纯 Tailwind，需新建 fix-* change 并重新评估 fidelity。

## 验收 Gate

- **视口**：1280×1024 桌面并排 `admin-home.png`。
- **Checklist**：见 `openspec/changes/add-admin-home/trace.md`（≥18 项）。
- **命令**：`vitest` admin 相关测试 → `npm run build` → 可选 `docker compose build web`。
