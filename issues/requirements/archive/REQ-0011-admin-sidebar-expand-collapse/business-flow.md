---
title: 业务流程
purpose: 描述管理端侧边栏展开/收起交互流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 10:25:49
updated_at: 2026-06-27 10:25:49
note: REQ-0011-admin-sidebar-expand-collapse
---

# 业务流程

## 1. 与父需求 REQ-0010 的差异

| 维度 | REQ-0010（产品版本展示） | REQ-0011（本需求） |
|---|---|---|
| 交互 | 无；版本 badge 常驻 | chevron 切换 expanded / collapsed |
| 头部 | 产品名 + 版本 pill | 在 REQ-0010 头部上增加 chevron；collapsed 隐藏文案与 badge |
| 侧栏宽度 | 固定 264px | 264px ↔ 72px |
| 持久化 | 无 | localStorage 记住折叠偏好 |

```text
REQ-0010 Out scope                    REQ-0011 In scope
────────────────────────────────────────────────────────────
「折叠 chevron 后续迭代」      →      头部右上 chevron + 宽度动画
固定 grid 264px              →      --admin-sidebar-width 驱动
```

## 2. 与 REQ-0004 管理端壳层的差异

```text
变更前                                    变更后
──────────────────────────────────────────────────────────────────
AdminLayout: 无折叠 state                 AdminLayout 持有 collapsed state
AdminSidebar: .logo 静态                  .sidebar-head: brand + chevron
.admin-shell: 264px 1fr 写死              grid: var(--admin-sidebar-width) 1fr
无 localStorage                           读写 admin-sidebar-collapsed
```

## 3. 页面加载与状态恢复

```text
用户进入 /admin/*（视口 > 1023px）
  ↓
AdminLayout mount
  ↓
读取 localStorage['admin-sidebar-collapsed']
  ├─ null / false → expanded（264px）
  └─ true         → collapsed（72px）
  ↓
.admin-shell 应用 data-sidebar-state 或等价 class
  ↓
AdminSidebar 渲染对应头部 / nav / user 裁剪
  ↓
主内容区占据剩余列宽
```

## 4. 用户切换折叠（桌面）

```text
用户点击头部 chevron
  ↓
toggle collapsed state
  ↓
  ├─ 更新 CSS 变量 --admin-sidebar-width（264 ↔ 72）
  ├─ 写入 localStorage
  ├─ 更新 aria-expanded / aria-label
  └─ 触发 width transition（200–250ms）
  ↓
expanded: 显示 nav 文案、分区标题、用户全信息、版本 badge（若有）
collapsed: 仅 logo 块、nav 图标、avatar；active 项仍高亮
  ↓
MUST NOT 卸载 Outlet / 丢失 notice 等 Layout 状态
```

## 5. 导航与用户菜单（两态一致）

```text
点击 nav-item
  ↓
  ├─ 有 path → navigate(path)
  └─ 无 path → onPlaceholder()（功能建设中 toast）
  ↓
collapsed / expanded 行为相同

点击 avatar（collapsed 或 expanded）
  ↓
打开 AdminUserMenu dropdown
  ↓
个人资料 / 密码修改 / 退出登录（逻辑不变）
```

## 6. 响应式边界（不改动现有 mobile 流）

```text
视口 ≤ 1023px
  ↓
沿用 admin-home.css 现有规则：
  - 侧栏置顶、双列 nav
  - sidebar-user 隐藏
  - 折叠 chevron 隐藏或禁用
  ↓
本 REQ 不定义 mobile 折叠行为
```

## 7. 组件结构（目标）

```text
AdminLayout
  ├─ state: sidebarCollapsed + setSidebarCollapsed
  ├─ effect: localStorage 读写
  └─ .admin-shell[data-sidebar-state=expanded|collapsed]
        ├─ AdminSidebar
        │     ├─ .sidebar-head
        │     │     ├─ brand / logo（collapsed 缩略）
        │     │     ├─ product + version badge（expanded only，REQ-0010）
        │     │     └─ button.sidebar-toggle（chevron）
        │     ├─ .nav-scroll
        │     └─ AdminUserMenu（collapsed: avatar only）
        └─ main.main-content
```

## 8. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0010-product-version-display | 头部 DOM；建议同 Sprint 先行或并行 |
| REQ-0004-admin-home | `AdminLayout`、`AdminSidebar` |
| `admin-home.css` | 网格、侧栏、nav、transition |
| `rules/ui-design.md` | semantic token、无裸 Hex |
