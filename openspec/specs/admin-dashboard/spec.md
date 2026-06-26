# admin-dashboard Specification

## Purpose
TBD - created by archiving change add-admin-home. Update Purpose after archive.
## Requirements
### Requirement: 管理端工作台 Shell 布局

Web 客户端 MUST 为已认证管理端用户提供 `/admin/dashboard` 工作台页面，采用固定 Sidebar + 右侧内容区布局，视觉 MUST 高保真对齐 `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.html` 的 CSS Port 策略。Sidebar 宽度 MUST 为 264px、高度 MUST 为 100vh（`position: sticky`），MUST NOT 随右侧内容高度拉伸或滚动；右侧内容区 MUST 为 100vh 且 `overflow: auto`，主内容最大宽度 MUST 为 1080px 居中。

#### Scenario: 桌面端 Shell 布局

- **WHEN** 已登录 `admin` 或 `employee` 用户在桌面端（>= 1024px）访问 `/admin/dashboard`
- **THEN** 页面 MUST 展示 `admin-shell` 网格布局（264px + 1fr）
- **AND** 左侧 Sidebar MUST 固定视口高度且不随右侧滚动
- **AND** 右侧内容区 MUST 独立纵向滚动

#### Scenario: 管理端 Shell CSS Port

- **WHEN** 开发者查看管理端首页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS（如 `features/admin/styles/admin-home.css`）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示品牌名 **TILESFST**（全大写），MUST NOT 出现 STONEX。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。当前路由为首页时，「首页」项 MUST 为 active 态；当前路由为 `/admin/brands` 时，「瓷砖品牌」项 MUST 为 active 态（品牌金弱强调与左侧指示条）。「瓷砖品牌」MUST 导航至 `/admin/brands`，MUST NOT 仅展示占位 toast。

#### Scenario: 品牌与分组展示

- **WHEN** 用户查看管理端 Sidebar
- **THEN** 顶部 MUST 展示 **TILESFST** Logo 文案
- **AND** MUST 展示 OPERATIONS 与 SYSTEM 两个分组及各自导航项
- **AND** MUST NOT 展示 STONEX 或旧品牌名

#### Scenario: 首页导航 active 态

- **WHEN** 用户位于 `/admin/dashboard`
- **THEN** 「首页」导航项 MUST 为 active 样式
- **AND** 其他导航项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌导航 active 态

- **WHEN** 用户位于 `/admin/brands`
- **THEN** 「瓷砖品牌」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌可导航

- **WHEN** 用户点击 Sidebar「瓷砖品牌」
- **THEN** 系统 MUST 导航至 `/admin/brands`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖品牌」「用户管理」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常

### Requirement: 管理端 Sidebar 用户菜单

Sidebar 底部 MUST 固定用户菜单（`margin-top: auto`），展示头像缩写、用户名、邮箱与展开箭头。用户菜单按钮下方 MUST NOT 直接展示「退出登录」按钮。点击用户菜单 MUST 在用户按钮上方展开下拉框，包含：个人资料、密码修改、0.5px 分隔线、退出登录（风险色弱强调）。

#### Scenario: 用户菜单展示

- **WHEN** 用户查看 Sidebar 底部（桌面端 >= 1024px）
- **THEN** MUST 展示用户触发按钮（头像缩写、用户名、邮箱、箭头）
- **AND** MUST NOT 在按钮下方直接展示「退出登录」按钮

#### Scenario: 用户菜单下拉内容

- **WHEN** 用户点击 Sidebar 底部用户菜单
- **THEN** MUST 在用户按钮上方展开下拉框
- **AND** 下拉框 MUST 包含「个人资料」「密码修改」、分隔线与「退出登录」
- **AND** 「退出登录」MUST 使用风险色弱强调

#### Scenario: 用户菜单可访问性

- **WHEN** 辅助技术访问用户菜单
- **THEN** 触发按钮 MUST 设置 `aria-expanded` 与 `aria-haspopup="menu"`
- **AND** 下拉框 MUST 使用 `role="menu"`，菜单项 MUST 使用 `role="menuitem"`

#### Scenario: 个人资料与密码修改占位

- **WHEN** 用户点击「个人资料」或「密码修改」
- **THEN** 系统 MAY 展示占位反馈
- **AND** MUST NOT 要求本期实现完整资料或改密流程

### Requirement: 管理端 Dashboard 数据概览

`/admin/dashboard` MUST 展示「数据概览」区块，包含 4 个指标卡：SKU 总数、品牌数量、Banner 数量、用户数量。桌面端 MUST 为四列网格；关键数值 MUST 使用品牌金强调。本期 MUST 使用 mock 数据，数值 MAY 与 HTML 原型样例一致。

#### Scenario: 指标卡展示

- **WHEN** 用户访问 `/admin/dashboard`
- **THEN** MUST 展示 4 个指标卡，分别对应 SKU 总数、品牌数量、Banner 数量、用户数量
- **AND** 每个指标卡 MUST 包含标签、数值与辅助说明

#### Scenario: 指标卡桌面网格

- **WHEN** 视口宽度 >= 1024px
- **THEN** 指标卡 MUST 以四列网格排列

### Requirement: 管理端 Dashboard 快捷操作

`/admin/dashboard` MUST 展示「快捷操作」区块，采用四列宫格，且 MUST 仅包含：新增 SKU、新增品牌、新增类目、新增 Banner。MUST NOT 包含：导入 SKU、导入图片、价格管理、操作日志。「新增品牌」MUST 导航至 `/admin/brands`（MAY 通过 query 打开新增弹窗），MUST NOT 仅展示占位 toast。

#### Scenario: 快捷操作四项

- **WHEN** 用户查看快捷操作区块
- **THEN** MUST 展示且仅展示 4 个快捷操作卡片
- **AND** 标题 MUST 分别为「新增 SKU」「新增品牌」「新增类目」「新增 Banner」

#### Scenario: 新增品牌快捷操作

- **WHEN** 用户点击「新增品牌」快捷操作
- **THEN** 系统 MUST 导航至 `/admin/brands`
- **AND** MUST NOT 仅展示占位 toast

#### Scenario: 其他快捷操作占位

- **WHEN** 用户点击「新增 SKU」「新增类目」或「新增 Banner」
- **THEN** 系统 MUST 展示占位反馈
- **AND** MUST NOT 抛出未捕获错误

#### Scenario: 已删除快捷操作不得出现

- **WHEN** 用户查看 `/admin/dashboard` 全文
- **THEN** MUST NOT 出现「导入 SKU」「导入图片」「价格管理」「操作日志」入口

### Requirement: 管理端 Dashboard 最近更新

`/admin/dashboard` MUST 展示「最近更新」表格，列 MUST 包含：更新时间、类型、名称、操作人。类型列 MUST 使用 badge 样式（如 SKU / 品牌 / Banner / 类目 / 系统）。本期 MUST 使用 mock 数据，至少 5 行样例。

#### Scenario: 最近更新表格

- **WHEN** 用户访问 `/admin/dashboard`
- **THEN** MUST 展示最近更新表格及四列字段
- **AND** 类型列 MUST 使用 badge 样式

#### Scenario: 表格行交互

- **WHEN** 用户 hover 表格行
- **THEN** 行 MUST 展示弱背景反馈

### Requirement: 管理端 Dashboard 删除模块

管理端首页 MUST NOT 包含以下模块：顶部欢迎区域、今日待办、数据质量概览、风险提醒、热门材质、门店同步、材质库存分布。

#### Scenario: 无 V4 冗余模块

- **WHEN** 用户访问 `/admin/dashboard`
- **THEN** 页面 MUST NOT 渲染上述已删除模块

### Requirement: 管理端首页 PNG 视觉验收 Gate

管理端首页视觉对齐 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: 桌面 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/dashboard` 与 `admin-home.png`
- **THEN** diff checklist（Shell 264px、Sidebar 100vh、TILESFST Logo、导航分组、用户菜单与下拉、无顶栏退出、四指标卡、四快捷操作、最近更新表格、无欢迎区/待办等删除项、品牌金用法、分割线、圆角）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md` 与 sprint acceptance-report

#### Scenario: 构建验证

- **WHEN** 执行 `vite build` 与 `docker compose build web`
- **THEN** 构建 MUST 成功且 admin-home CSS 可访问

### Requirement: 管理端首页 refactor 不改变认证逻辑

管理端首页 UI 实现 MUST NOT 修改 auth store、login API、token 持久化、ProtectedRoute 与角色分流逻辑。

#### Scenario: Auth 逻辑冻结

- **WHEN** add-admin-home 实现完成
- **THEN** `features/auth/` 核心逻辑 MUST 无行为变更
- **AND** 未登录访问 `/admin/dashboard` MUST 仍跳转 `/admin/login`

