---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
status: pending_review
created_at: 2026-06-27 21:40:26
updated_at: 2026-06-27 21:40:26
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 所有菜单项渲染同一空占位元素

`AdminSidebar.tsx` 对每个 `nav-item` 均渲染无内容的 `<span className="nav-icon" aria-hidden="true" />`，未读取 per-item 图标配置：

```tsx
<span className="nav-icon" aria-hidden="true" />
<span className="nav-label">{item.label}</span>
```

### 1.2 导航数据模型缺少 `icon` 字段

`admin-nav.ts` 中 `AdminNavItem` 仅含 `id`、`label`、`path`，7 个菜单项（首页、瓷砖 SKU、品牌、类目、Banner、用户管理、系统设置）均无图标映射。

### 1.3 `.nav-icon` 为纯 CSS 通用方块，非语义 SVG

`admin-home.css` 通过边框 + `::after` 伪元素绘制 16×16 占位方块，所有 item 共享同一套样式规则，视觉上无法区分。

### 1.4 collapsed 态隐藏文案后问题显性化

REQ-0011 交付的 `[data-sidebar-state='collapsed']` 规则隐藏 `.nav-label`、`.nav-title`，侧栏收窄为 72px 图标列。展开态用户可依赖文字标签，collapsed 态仅剩同质方块，导航识别完全依赖记忆或试错。

## 2. 根本原因

### 2.1 REQ-0011 原型与验收未要求差异化图标

`admin-sidebar-collapsed.html` 原型同样使用相同 `.nav-icon` 占位；AC-014 仅要求「保留各 nav `.nav-icon`」，未要求语义可区分。`add-admin-sidebar-collapse` 按原型交付折叠布局，**占位图标未升级为 per-menu 语义 icon**。

### 2.2 Admin Shell 早期采用 CSS Port 占位策略

管理端侧栏自 REQ-0004 / 品牌管理 HTML port 起即使用 CSS 方块作为 nav 图标占位，功能迭代（折叠、版本 badge）未同步补齐图标资产，导致折叠能力上线后 UX 缺口暴露。

### 2.3 组件/数据层未引入图标库映射

项目其他模块（`SearchBar`、`Pagination`、登录页）已使用 `lucide-react`，但 `AdminSidebar` 未沿用；导航配置与渲染层均未建立 `id → LucideIcon` 映射。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin（或 employee）登录 Web 管理端（local 或 Docker，`> 1023px` 视口）。
2. 访问任意 `/admin/*` 页面。
3. 点击侧栏 chevron，使 `data-sidebar-state="collapsed"`。
4. 观察 nav 区域：各菜单前方图标形状完全一致。

展开态下问题存在但影响较小（有 `.nav-label` 文案）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（图标始终相同；REQ-0011 折叠使问题可见） |
| 主要修复面 | `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css`、vitest |
| 关联需求 | REQ-0011 AC-014（保留 icon）— 本 fix 为其体验补全 |
| 建议 Change | `fix-sidebar-menu-icons-indistinguishable` |

## 5. 后续修复建议

1. 在 `AdminNavItem` 增加 `icon: LucideIcon`（或等价类型），为 7 个 `id` 配置语义图标（如 `LayoutDashboard`、`Package`、`Building2`、`FolderTree`、`Image`、`Users`、`Settings`）。
2. `AdminSidebar` 渲染 `<item.icon className="nav-icon" size={16} strokeWidth={1.5} />`，移除 CSS 伪元素方块样式。
3. 保持 `aria-label={item.label}`；图标 `aria-hidden="true"`。
4. expanded / collapsed 两态并排验收；vitest 断言各 nav id 对应不同 icon（`data-nav-id` 或 role + 子 SVG 差异）。
5. 可选：同步更新 REQ-0011 原型 HTML（非阻塞，fix acceptance 为准）。
