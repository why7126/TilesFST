---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
status: captured
created_at: 2026-06-27 21:33:13
updated_at: 2026-06-27 21:33:13
severity_hint: medium
environment: local|docker
related_requirement:
related_bug:
captured_via: capture
classification_rationale: 管理端侧边栏收起后菜单项仅靠图标区分，当前各菜单图标完全相同，属于可用性/UI 缺陷而非新功能需求。
---

# 现象

Web 管理端侧边栏各菜单项前方的图标样式完全一致（均为 CSS 绘制的通用占位方块），侧边栏展开时可依赖文字标签区分，但**收起侧边栏后仅显示图标**，用户无法快速识别当前菜单对应的功能模块。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入任意管理页（如 `/admin/dashboard`）。
3. 点击侧边栏顶部的收起按钮，使侧边栏进入 collapsed 状态。
4. 观察 OPERATIONS / SYSTEM 分组下各菜单项（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理、用户管理、系统设置）前方的图标。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 每个菜单项应有语义明确且彼此可区分的图标；收起侧边栏后用户可仅凭图标识别并切换目标菜单。 |
| **实际** | 所有菜单项使用相同的 `<span class="nav-icon">` 占位样式（`AdminSidebar.tsx`），视觉上无差异，收起后无法区分。 |

# 初步线索

- `src/web/src/features/admin/components/AdminSidebar.tsx` 第 83 行：各 `nav-item` 均渲染相同的 `<span className="nav-icon" aria-hidden="true" />`。
- `src/web/src/features/admin/data/admin-nav.ts` 的 `AdminNavItem` 未定义 `icon` 字段。
- `admin-home.css` 中 `.nav-icon` 为通用 CSS 方块，非独立 SVG/图标组件。

# 附件

- 暂无截图
