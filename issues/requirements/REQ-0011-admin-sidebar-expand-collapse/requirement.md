---
requirement_id: REQ-0011-admin-sidebar-expand-collapse
title: 管理端侧边栏展开/收起（参照 SoulKing 交互）
terminal: web-admin
version: v1
status: approved
owner: product
source: issues/requirements/REQ-0011-admin-sidebar-expand-collapse/capture.md
priority: P1
parent_requirement: REQ-0010-product-version-display
---

# REQ-0011 管理端侧边栏展开/收起

## 1. 需求背景

管理端当前经 `AdminLayout` 渲染的导航侧栏（`AdminSidebar` + `admin-home.css`）为**固定 264px 宽度**，无展开/收起能力。竞品 SoulKing 管理端侧边栏在头部右上角提供 chevron 控件，可在完整导航与窄图标列之间切换，为主内容区释放横向空间。

`/req-explore` 已确认：本需求为 **REQ-0010**（侧边栏头部产品名 + 版本 badge）的后续能力；REQ-0010 PRD 已将折叠/展开 chevron 明确列为 Out of scope，由本 REQ 承接。

当前代码现状：

- `.admin-shell` 使用 `grid-template-columns: 264px 1fr` 写死侧栏宽度。
- `AdminSidebar` 头部为单一 `.logo` 文案，无 chevron、无折叠态。
- 导航项已有 `.nav-icon` 占位与 `.nav-item.active` 左侧 accent，可作为收起态识别基础。
- ≤1023px 时侧栏改为顶部双列导航布局（与用户菜单隐藏），与桌面「图标列折叠」为不同模型。

## 2. 目标用户

- **后台管理员 / 内部员工**：在 `/admin/*` 各页面通过侧边栏导航；需要按需收窄侧栏以扩大主内容阅读/表格区域。

## 3. 范围

### 3.1 本期包含

- 管理端 `AdminLayout` / `AdminSidebar` 支持 **expanded ↔ collapsed** 两种桌面侧栏宽度态
- 头部右上角 **chevron 切换按钮**（展开指向左，收起指向右），位置与交互参照 SoulKing 参考图
- 收起态：隐藏产品名、副标题、版本 badge（若 REQ-0010 已落地）、分区标题（OPERATIONS/SYSTEM）、导航文案；**保留** Logo/品牌标识区、导航图标、当前项 active 指示
- 展开态：与现有/REQ-0010 头部布局兼容，chevron 不遮挡产品名与版本 badge
- 侧栏宽度与主内容区 **平滑过渡动画**（约 200–250ms）
- 用户折叠偏好 **localStorage 持久化**，跨 `/admin/*` 路由保持
- Vitest 覆盖 toggle 行为、`aria-expanded` 与持久化读写
- 无障碍：chevron 可键盘操作；收起态导航项具备可读名称（`aria-label` 或等价 tooltip）

### 3.2 本期不包含

- 店主端 `Sidebar`（`src/web/src/shared/ui/sidebar.tsx` 筛选侧栏）
- ≤1023px / ≤639px **响应式布局变更**（维持 `admin-home.css` 现有 `@media` 行为；折叠 chevron 在该断点下不启用或不可见）
- 导航项替换为真实 SVG/Lucide 图标库（沿用现有 `.nav-icon` 占位即可，除非实现阶段发现不可验收）
- hover 临时 flyout 展开子菜单、键盘快捷键
- 后端 / API / 数据库变更
- 微信小程序

## 4. 功能要求

### FR-001 折叠状态与默认值

- 侧栏 MUST 支持两种状态：`expanded`（默认）与 `collapsed`。
- 用户**首次访问**（无持久化记录）MUST 默认为 **expanded**。
- 用户切换后，MUST 将偏好写入 `localStorage`（建议 key：`admin-sidebar-collapsed`，值为 boolean 或等价字符串）。
- 同一浏览器再次进入任意 `/admin/*`  authenticated 页面 MUST 恢复上次状态。
- 状态 SHOULD 由 `AdminLayout` 或等价 Context 持有，并传递给 `AdminSidebar`，避免各页重复实现。

### FR-002 侧栏宽度与壳层自适应

- **展开宽度** MUST 保持与现网一致：**264px**（与 `.admin-shell` 当前 grid 列宽一致）。
- **收起宽度** MUST 为 **72px**（实现时可 token 化为 CSS 变量，如 `--admin-sidebar-width`）。
- `.admin-shell` 网格 MUST 随状态更新第一列宽度；`.main-content` MUST 自动占据剩余空间，不得出现横向滚动条或内容被侧栏遮挡。
- 宽度过渡 MUST 使用 CSS `transition`（建议 200–250ms，`ease` 或 `ease-in-out`），包含 grid 列宽与侧栏内部 padding 的协调变化。

### FR-003 头部 chevron 控件

- MUST 在 `AdminSidebar` **头部区域右上角** 放置折叠/展开按钮，参照 SoulKing 参考图。
- **expanded** 时 chevron MUST 表示「向左收起」（如 `ChevronLeft` / `<`）。
- **collapsed** 时 chevron MUST 表示「向右展开」（如 `ChevronRight` / `>`）。
- 按钮 MUST 具备：
  - `aria-expanded` 对应当前是否 expanded
  - 可见 `aria-label`（如「收起侧边栏」/「展开侧边栏」）
  - 键盘可聚焦与激活（Enter / Space）
- chevron MUST NOT 遮挡 REQ-0010 产品名与版本 badge 的可读区域；expanded 态下与头部同一行或同一头部容器内右对齐。

### FR-004 展开态展示（与 REQ-0010 兼容）

- expanded 态 MUST 展示完整导航：分区标题、导航图标 + 文案、底部 `AdminUserMenu` 全量信息（头像、姓名、邮箱）。
- 若 REQ-0010 已落地：头部 MUST 同时展示产品名、版本 badge、可选副标题；本 REQ 不改变 REQ-0010 文案与 badge 规范，仅在其布局上增加 chevron。
- 若 REQ-0010 尚未落地：MUST 至少保留现有 `.logo` / 品牌区，且 chevron 位置仍满足 FR-003；REQ-0010 落地后 MUST 无需重做 chevron 位置逻辑。

### FR-005 收起态展示

- collapsed 态 MUST **隐藏**：
  - 产品名称、副标题、版本 badge（REQ-0010）
  - 分区标题 `.nav-title`
  - 导航项文字 label
  - 用户菜单中的姓名、邮箱、chevron 文案区
- collapsed 态 MUST **保留并可见**：
  - 品牌/Logo 区域（可收窄为图标或缩略品牌块，仍须可识别为 TILESFST 管理端）
  - 各导航项 `.nav-icon`
  - 当前路由对应项的 **active** 样式（金色文字/背景 + 左侧 2px accent，可居中适配窄宽）
  - 用户头像（`.avatar`），点击 MUST 仍可打开现有 dropdown（个人资料、密码修改、退出登录）
- 收起态导航按钮 MUST 提供可访问名称（`aria-label={item.label}` 或 title），避免仅图标无读屏信息。

### FR-006 导航与交互回归

- 收起/展开 MUST NOT 改变导航路由行为；点击 nav item 仍调用既有 `navigate(path)` / placeholder 逻辑。
- 切换状态 MUST NOT 卸载当前页面或丢失 `AdminLayout` 内 notice 等局部 UI 状态。
- `AdminUserMenu` 下拉在 collapsed 态 MUST 正常定位与关闭（点击外部、选择菜单项）。
- MUST NOT 在 collapsed 态引入横向滚动条于 `.nav-scroll`。

### FR-007 响应式边界

- 视口宽度 **> 1023px**（桌面）：FR-001–FR-006 全部生效。
- 视口宽度 **≤ 1023px**：MUST 沿用现有 `admin-home.css` 响应式（侧栏置顶、双列 nav、隐藏 sidebar-user）；折叠 chevron MAY 隐藏或禁用，且 MUST NOT 与现有 mobile 布局冲突。
- 本 REQ MUST NOT 修改 ≤1023px 下既有 grid/nav 结构，除非后续独立需求明确。

### FR-008 测试与回归

- MUST 新增或扩展 Vitest（`AdminSidebar` 或 `AdminLayout`）：
  - 点击 chevron 切换 `expanded` / `collapsed` 对应 class 或 `data-state`
  - `aria-expanded` 与状态一致
  - localStorage 写入与初始读取
- SHOULD 覆盖 active 项在 collapsed 态仍带 `active` class。
- 全量 `/admin/*`  smoke：折叠后主内容区可见、导航仍可跳转。

## 5. UI / UE 约束

- 视觉参照 SoulKing 管理端侧边栏参考图（`/req-capture` 附件）：头部右上 chevron、收起后图标列、active 项 accent。
- MUST 使用 `admin-home.css` semantic/admin token（`--admin-gold`、`--admin-line` 等）；**禁止**新增裸 Hex / rgba。
- chevron 图标 SHOULD 使用 shadcn/lucide 或 DS 一致图标，颜色 `text-muted` / `text-secondary`，hover 可见反馈。
- 动画 SHOULD 克制，避免影响可访问性（尊重 `prefers-reduced-motion` 时可缩短或关闭 transition）。
- 实现 SHOULD 通过 CSS 变量驱动 `--admin-sidebar-width`，避免 TS 硬编码多处 magic number。

## 6. 依赖与实施顺序

| 依赖 | 说明 |
|------|------|
| **REQ-0010**（建议同 Sprint 且优先或并行） | 头部 DOM 结构（产品名 + 版本 badge）；本 REQ chevron 依附该头部 |
| **REQ-0004-admin-home** | `AdminLayout`、`AdminSidebar` 壳层 |
| `rules/ui-design.md` | Token、管理端视觉 |
| `src/web/src/features/admin/styles/admin-home.css` | 网格、侧栏、nav、user menu 样式主文件 |

**建议 OpenSpec change 命名**：`add-admin-sidebar-collapse` 或 `update-admin-sidebar-interaction`。

## 7. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0010-product-version-display | 父需求；头部内容与版本 badge；折叠交互由其 PRD Out  scope 移交本 REQ |
| REQ-0004-admin-home | 管理端布局与侧栏挂载点 |
| 店主端 `Sidebar` | 无直接关系；本 REQ 不涉及 |

## 8. 状态

```yaml
requirement_id: REQ-0011-admin-sidebar-expand-collapse
priority: P1
status: approved
iteration: null
owner: product
parent_requirement: REQ-0010-product-version-display
openspec_change: null  # 建议 add-admin-sidebar-collapse
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
```
