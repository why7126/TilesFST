## MODIFIED Requirements

### Requirement: 管理端工作台 Shell 布局

Web 客户端 MUST 为已认证管理端用户提供 `/admin/dashboard` 工作台页面，采用固定 Sidebar + 右侧内容区布局，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0004-admin-home/prototype/web/admin-home.html` 的 CSS Port 策略，并 MUST 支持桌面端（>1023px）Sidebar **展开/收起**两种宽度态。Sidebar **展开**宽度 MUST 为 264px、**收起**宽度 MUST 为 72px，由 CSS 变量 `--admin-sidebar-width` 驱动 `.admin-shell` 网格第一列；高度 MUST 为 100vh（`position: sticky`），MUST NOT 随右侧内容高度拉伸或滚动；右侧内容区 MUST 为 100vh 且 `overflow: auto`，主内容最大宽度 MUST 为 1080px 居中。宽度切换 MUST 有约 200–250ms 过渡；`prefers-reduced-motion: reduce` 时 MAY 禁用或缩短动画。

#### Scenario: 桌面端 Shell 布局

- **WHEN** 已登录 `admin` 或 `employee` 用户在桌面端（>1023px）访问 `/admin/dashboard`
- **THEN** 页面 MUST 展示 `admin-shell` 网格布局（`var(--admin-sidebar-width)` + 1fr）
- **AND** 左侧 Sidebar MUST 固定视口高度且不随右侧滚动
- **AND** 右侧内容区 MUST 独立纵向滚动

#### Scenario: 侧栏展开默认宽度

- **WHEN** 用户首次访问（无 `admin-sidebar-collapsed` localStorage）且视口 >1023px
- **THEN** `--admin-sidebar-width` MUST 为 264px
- **AND** Sidebar MUST 为 expanded 态

#### Scenario: 侧栏收起宽度

- **WHEN** 用户点击头部 chevron 收起侧栏且视口 >1023px
- **THEN** `--admin-sidebar-width` MUST 变为 72px
- **AND** 主内容区 MUST 自动扩展占据剩余列宽
- **AND** MUST NOT 出现多余页面级横向滚动条

#### Scenario: 管理端 Shell CSS Port

- **WHEN** 开发者查看管理端首页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS（如 `features/admin/styles/admin-home.css`）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示品牌名 **TILESFST**（全大写），MUST NOT 出现 STONEX。Sidebar 头部右上角 MUST 提供折叠/展开 **chevron** 按钮：expanded 时指向左（收起语义），collapsed 时指向右（展开语义）；按钮 MUST 具备 `aria-expanded` 与可读 `aria-label`。若 REQ-0010 brand-head 已落地，expanded 态 MUST 同时展示产品版本 pill，chevron MUST NOT 遮挡产品名与 pill；collapsed 态 MUST 隐藏产品名、副标题、版本 pill 与分区标题 `.nav-title`，MUST 保留品牌缩略标识与 nav 图标。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。collapsed 态 MUST 隐藏 nav 文案但保留 `.nav-icon`；每项 MUST 提供 `aria-label` 或等价读屏名称。当前路由对应项 MUST 保持 active 样式（含 collapsed 态左侧 accent 或等价指示）。「瓷砖品牌」MUST 导航至 `/admin/brands`，MUST NOT 仅展示占位 toast。

#### Scenario: 品牌与分组展示（expanded）

- **WHEN** 用户在桌面端查看 expanded 管理端 Sidebar
- **THEN** 顶部 MUST 展示 **TILESFST** 与完整 nav 文案及 OPERATIONS/SYSTEM 分组
- **AND** 头部右上角 MUST 可见 chevron（收起语义）
- **AND** MUST NOT 展示 STONEX 或旧品牌名

#### Scenario: collapsed 导航裁剪

- **WHEN** 用户在桌面端查看 collapsed Sidebar
- **THEN** MUST NOT 展示 nav 文案与 `.nav-title`
- **AND** MUST 展示各 nav 图标
- **AND** 当前路由项 MUST 仍为 active 样式

#### Scenario: chevron 无障碍

- **WHEN** 用户使用键盘聚焦 chevron 并按 Enter 或 Space
- **THEN** MUST 切换 expanded/collapsed
- **AND** `aria-expanded` MUST 与当前态一致

#### Scenario: 首页导航 active 态

- **WHEN** 用户位于 `/admin/dashboard`
- **THEN** 「首页」导航项 MUST 为 active 样式
- **AND** 其他导航项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌可导航

- **WHEN** 用户点击 Sidebar「瓷砖品牌」（expanded 或 collapsed）
- **THEN** 系统 MUST 导航至 `/admin/brands`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖品牌」「用户管理」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常

### Requirement: 管理端 Sidebar 用户菜单

Sidebar 底部 MUST 固定用户菜单（`margin-top: auto`）。**expanded** 态 MUST 展示头像缩写、用户名、邮箱与展开箭头；**collapsed** 态（桌面 >1023px）MUST 仅展示头像缩写，点击 MUST 仍可展开下拉框（个人资料、密码修改、退出登录）。用户菜单按钮下方 MUST NOT 直接展示「退出登录」按钮。

#### Scenario: 用户菜单展示 expanded

- **WHEN** 用户查看 expanded Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 展示用户触发按钮（头像缩写、用户名、邮箱、箭头）
- **AND** MUST NOT 在按钮下方直接展示「退出登录」按钮

#### Scenario: 用户菜单展示 collapsed

- **WHEN** 用户查看 collapsed Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 仅展示头像缩写按钮
- **AND** 点击 MUST 打开与 expanded 相同的下拉菜单

#### Scenario: 用户菜单下拉内容

- **WHEN** 用户点击 Sidebar 底部用户菜单
- **THEN** MUST 在用户按钮上方展开下拉框
- **AND** 下拉框 MUST 包含「个人资料」「密码修改」、分隔线与「退出登录」
- **AND** 「退出登录」MUST 使用风险色弱强调

#### Scenario: 用户菜单可访问性

- **WHEN** 辅助技术访问用户菜单
- **THEN** 触发按钮 MUST 设置 `aria-expanded` 与 `aria-haspopup="menu"`
- **AND** 下拉框 MUST 使用 `role="menu"`，菜单项 MUST 使用 `role="menuitem"`
