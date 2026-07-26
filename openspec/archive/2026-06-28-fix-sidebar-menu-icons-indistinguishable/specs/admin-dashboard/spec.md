## MODIFIED Requirements

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示品牌名 **TILESFST**（全大写），MUST NOT 出现 STONEX。品牌名右侧 MUST 紧邻展示产品版本 pill（如 `v0.0.1`），版本值 MUST 来自跨端单一常量 `PRODUCT_VERSION`（`src/shared/`），MUST NOT 来自 `package.json`、FastAPI OpenAPI version 或构建/Git 信息。版本 pill MUST 为小号圆角 badge，使用 semantic token，MUST NOT 使用裸 Hex。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。**每个导航项 MUST 配置语义明确且彼此可区分的图标**（Lucide outline 或 DS 等价 SVG；见 BUG-0021 acceptance AC-001 映射表）。**collapsed** 态（72px icon-only）下用户 MUST 可仅凭图标形状识别各菜单；任意两菜单 MUST NOT 渲染相同 SVG path 或相同 icon 组件。**expanded** 态下图标与文案 MUST 并排显示。当前路由为首页时，「首页」项 MUST 为 active 态；当前路由为 `/admin/tile-skus` 时，「瓷砖SKU」项 MUST 为 active 态（品牌金弱强调与左侧指示条）；当前路由为 `/admin/brands` 时，「瓷砖品牌」项 MUST 为 active 态。「瓷砖SKU」MUST 导航至 `/admin/tile-skus`，MUST NOT 仅展示占位 toast。「瓷砖品牌」MUST 导航至 `/admin/brands`，MUST NOT 仅展示占位 toast。图标颜色 MUST 继承 nav-item 的 currentColor；TSX/CSS MUST NOT 新增裸 Hex；MUST NOT 使用纯 CSS 伪元素方块作为唯一 nav 图标实现。

#### Scenario: 品牌与分组展示

- **WHEN** 用户查看管理端 Sidebar
- **THEN** 顶部 MUST 展示 **TILESFST** Logo 文案
- **AND** TILESFST 右侧同一行 MUST 展示产品版本 pill，文案 MUST 等于 `PRODUCT_VERSION`
- **AND** MUST 展示 OPERATIONS 与 SYSTEM 两个分组及各自导航项
- **AND** MUST NOT 展示 STONEX 或旧品牌名
- **AND** MUST NOT 展示 API 或后端版本号

#### Scenario: 各菜单语义图标可区分

- **WHEN** 用户查看 Sidebar nav 区域（expanded 或 collapsed）
- **THEN** 首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner、用户管理、系统设置 MUST 各自渲染不同语义的 icon
- **AND** 任意两可见菜单项的 icon MUST NOT 相同

#### Scenario: collapsed 态 icon-only 可识别

- **WHEN** 侧栏处于 collapsed 态（`.nav-label` 隐藏）
- **THEN** 各菜单前方 icon MUST 在形状上彼此可区分
- **AND** 点击任一 icon MUST 与 expanded 态相同执行 navigate 或 placeholder 逻辑

#### Scenario: 产品版本可访问性

- **WHEN** 辅助技术访问 Sidebar 顶部品牌区
- **THEN** 版本信息 MUST 可通过可见 pill 文本或 `aria-label`（如「产品版本 v0.0.1」）感知

#### Scenario: 首页导航 active 态

- **WHEN** 用户位于 `/admin/dashboard`
- **THEN** 「首页」导航项 MUST 为 active 样式
- **AND** 其他导航项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌导航 active 态

- **WHEN** 用户位于 `/admin/brands`
- **THEN** 「瓷砖品牌」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: 瓷砖 SKU 导航 active 态

- **WHEN** 用户位于 `/admin/tile-skus`
- **THEN** 「瓷砖SKU」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌可导航

- **WHEN** 用户点击 Sidebar「瓷砖品牌」
- **THEN** 系统 MUST 导航至 `/admin/brands`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 瓷砖 SKU 可导航

- **WHEN** 用户点击 Sidebar「瓷砖SKU」
- **THEN** 系统 MUST 导航至 `/admin/tile-skus`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖SKU」「瓷砖品牌」「用户管理」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常

#### Scenario: 非 admin 角色用户管理隐藏后图标仍可区分

- **WHEN** 以 `employee` 角色登录并查看 Sidebar
- **THEN** 「用户管理」菜单 MUST 不可见
- **AND** 其余可见菜单 icon MUST 仍可区分
