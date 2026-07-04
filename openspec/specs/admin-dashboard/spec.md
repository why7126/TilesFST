# 管理端工作台规范

## Purpose
定义管理端 Admin Shell、Sidebar 品牌导航、Dashboard 数据概览、快捷操作、最近更新和视觉验收要求，确保管理端基础框架稳定一致。
## Requirements
### Requirement: 管理端工作台 Shell 布局

Web 客户端 MUST 为已认证管理端用户提供 `/admin/dashboard` 工作台页面，采用固定 Sidebar + 右侧内容区布局，视觉 MUST 高保真对齐管理端暗色旗舰风与当前 Design System，且 MUST 支持桌面端（>1023px）Sidebar **展开/收起**两种宽度态。Sidebar **展开**宽度 MUST 为 264px、**收起**宽度 MUST 为 72px，由 CSS 变量 `--admin-sidebar-width` 驱动 `.admin-shell` 网格第一列；高度 MUST 为 100vh（`position: sticky`），MUST NOT 随右侧内容高度拉伸或滚动；右侧内容区 MUST 为 100vh 且 `overflow: auto`。主内容 padding 在 desktop MUST 收敛到 `24px 24px 48px` 量级，`content-inner` MUST 使用统一宽度策略，MUST NOT 继续使用 1080px 硬上限；最终可采用 `max-width: min(1440px, 100%)` 或 `max-width: 100%`，但 MUST 在实现 trace 中记录。宽度切换 MUST 有约 200–250ms 过渡；`prefers-reduced-motion: reduce` 时 MAY 禁用或缩短动画。

#### Scenario: 桌面端 Shell 布局

- **WHEN** 已登录 `admin` 或 `employee` 用户在桌面端（>1023px）访问 `/admin/dashboard`
- **THEN** 页面 MUST 展示 `admin-shell` 网格布局（`var(--admin-sidebar-width)` + 1fr）
- **AND** 左侧 Sidebar MUST 固定视口高度且不随右侧滚动
- **AND** 右侧内容区 MUST 独立纵向滚动
- **AND** `.main-content` padding MUST 为 `24px 24px 48px` 或经评审确认的等价值
- **AND** `.content-inner` MUST NOT 使用 `max-width: 1080px`.

#### Scenario: 侧栏展开默认宽度

- **WHEN** 用户首次访问（无 `admin-sidebar-collapsed` localStorage）且视口 >1023px
- **THEN** `--admin-sidebar-width` MUST 为 264px
- **AND** Sidebar MUST 为 expanded 态

#### Scenario: 侧栏收起宽度

- **WHEN** 用户点击头部 chevron 收起侧栏且视口 >1023px
- **THEN** `--admin-sidebar-width` MUST 变为 72px
- **AND** 主内容区 MUST 自动扩展占据剩余列宽
- **AND** MUST NOT 出现多余页面级横向滚动条

#### Scenario: 管理端 Shell 响应式 padding

- **WHEN** 用户在 ≤1023px 视口访问管理端页面
- **THEN** `.main-content` padding SHOULD 为 `20px 16px 40px` 量级
- **AND** 侧栏 tablet 响应式结构 MUST 不回归
- **WHEN** 用户在 ≤639px 视口访问管理端页面
- **THEN** `.main-content` padding SHOULD 为 `16px 12px 32px` 量级
- **AND** 页面内容 MUST NOT 贴住视口边缘或产生 Shell 级横向滚动。

#### Scenario: 管理端 Shell CSS Port

- **WHEN** 开发者查看管理端首页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS（如 `features/admin/styles/admin-home.css`）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex
- **AND** 管理端 CSS MUST NOT 重新引入与全局 `content-inner` 策略冲突的页面级 1080px / 1120px 内容宽度上限。

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示菲尚特品牌区，展开态顶部 MUST 包含菲尚特 Logo、品牌主标题 **菲尚特FST**、产品版本 badge 与副标题 **家居建材资料库**。产品版本值 MUST 来自跨端单一常量 `PRODUCT_VERSION`（`src/shared/`），MUST NOT 来自 `package.json`、FastAPI OpenAPI version 或构建/Git 信息。版本 badge MUST 为小号 badge，使用 semantic token，MUST NOT 使用裸 Hex。Logo、品牌文字组与展开/收起按钮 MUST 处于同一品牌行且不得互相遮挡；Logo 区域 MUST NOT 增加独立卡片背景、边框、渐变底纹或阴影。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。**仅 `role=admin` 用户 MUST 看到「系统设置」项**；`employee` MUST NOT 看到该项。当前路由为首页时，「首页」项 MUST 为 active 态；当前路由为 `/admin/tile-skus` 时，「瓷砖SKU」项 MUST 为 active 态（品牌金弱强调与左侧指示条）；当前路由为 `/admin/brands` 时，「瓷砖品牌」项 MUST 为 active 态；当前路由匹配 `/admin/settings` 或其子路径时，「系统设置」项 MUST 为 active 态。「瓷砖SKU」MUST 导航至 `/admin/tile-skus`，MUST NOT 仅展示占位 toast。「瓷砖品牌」MUST 导航至 `/admin/brands`，MUST NOT 仅展示占位 toast。「系统设置」MUST 配置 `path: '/admin/settings'`（或等价），MUST NOT 无 path 或无效点击。

#### Scenario: 品牌与分组展示

- **WHEN** 用户查看管理端 Sidebar 展开态
- **THEN** 顶部品牌区 MUST 展示菲尚特 Logo、**菲尚特FST**、产品版本 badge 与 **家居建材资料库**
- **AND** 产品版本 badge 文案 MUST 等于 `PRODUCT_VERSION`
- **AND** MUST 展示 OPERATIONS 与 SYSTEM 两个分组及各自导航项
- **AND** MUST NOT 展示 STONEX、TILESFST 或旧品牌名
- **AND** MUST NOT 展示 API 或后端版本号

#### Scenario: 品牌区布局与 Logo 容器

- **WHEN** 用户查看管理端 Sidebar 顶部品牌区
- **THEN** Logo、品牌文字组与展开/收起按钮 MUST 位于同一品牌行
- **AND** Logo MUST 保持比例，不拉伸、不裁切关键内容
- **AND** Logo 区域 MUST NOT 出现独立卡片背景、边框、渐变底纹或投影
- **AND** 展开/收起按钮 hover 后边框 MUST 与 Sidebar 内右边界保留安全间距

#### Scenario: 产品版本可访问性

- **WHEN** 辅助技术访问 Sidebar 顶部品牌区
- **THEN** 版本信息 MUST 可通过可见 badge 文本或 `aria-label`（如「产品版本 v0.0.1」）感知
- **AND** Logo MUST 具备可理解的替代文本（如「菲尚特家居建材」）

#### Scenario: Sidebar 收起态品牌识别

- **WHEN** 用户将管理端 Sidebar 切换到 collapsed 态
- **THEN** Sidebar MUST 保留 Logo 作为主要品牌识别元素
- **AND** 品牌文案、导航图标与展开/收起按钮 MUST NOT 重叠
- **AND** 展开/收起按钮 MUST 仍可点击并保留可访问标签

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

- **WHEN** 用户点击 Sidebar「瓷砖 SKU」
- **THEN** 系统 MUST 导航至 `/admin/tile-skus`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 系统设置可导航

- **WHEN** `admin` 用户点击 Sidebar「系统设置」
- **THEN** 系统 MUST 导航至 `/admin/settings`（或 `/admin/settings/basic`）
- **AND** MUST NOT 展示「功能建设中」占位 toast

#### Scenario: 系统设置 active 态

- **WHEN** `admin` 位于 `/admin/settings/media`
- **THEN** 「系统设置」导航项 MUST 为 active 样式

#### Scenario: 运营不展示系统设置

- **WHEN** `employee` 查看 SYSTEM 分组
- **THEN** MUST 仅展示「用户管理」
- **AND** MUST NOT 展示「系统设置」

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖SKU」「瓷砖品牌」「用户管理」（若可见）、「系统设置」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常

### Requirement: 管理端 Sidebar 用户菜单

Sidebar 底部 MUST 固定用户菜单（`margin-top: auto`）。**expanded** 态 MUST 展示用户头像区（有 `avatar_url` 时 MUST 为头像图片，否则 MUST 为首字母缩写 fallback）、用户名、邮箱与展开箭头；**collapsed** 态（桌面 >1023px）MUST 仅展示用户头像区（同上规则），点击 MUST 仍可展开下拉框（个人资料、密码修改、退出登录）。用户菜单按钮下方 MUST NOT 直接展示「退出登录」按钮。头像区 MUST 为 34×34px，使用 semantic token（`--admin-gold-bg`、`--admin-avatar-border` 等），MUST NOT 硬编码裸 Hex。

#### Scenario: 用户菜单展示 expanded

- **WHEN** 用户查看 expanded Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 展示用户触发按钮（头像区、用户名、邮箱、箭头）
- **AND** MUST NOT 在按钮下方直接展示「退出登录」按钮

#### Scenario: 用户菜单展示 collapsed

- **WHEN** 用户查看 collapsed Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 仅展示头像区按钮
- **AND** 点击 MUST 打开与 expanded 相同的下拉菜单

#### Scenario: 侧栏头像图片展示

- **WHEN** `AdminLayout` 从 `GET /api/v1/profile/me` 获得非空 `avatar_url`
- **THEN** 侧栏 `.avatar` MUST 渲染 `<img src={avatar_url}>` 且图片可见
- **AND** 图片 MUST 填充 34×34px 容器（`object-fit: cover`）

#### Scenario: 侧栏头像 initials fallback

- **WHEN** `avatar_url` 为空、null 或图片加载失败（`onError`）
- **THEN** 侧栏 `.avatar` MUST 回退显示 `getUserInitials(display_name, username)` 文本占位
- **AND** MUST NOT 展示破损图片占满容器

#### Scenario: 用户菜单下拉内容

- **WHEN** 用户点击 Sidebar 底部用户菜单
- **THEN** MUST 在用户按钮上方展开下拉框
- **AND** 下拉框 MUST 包含「个人资料」「密码修改」、分隔线与「退出登录」
- **AND** 「退出登录」MUST 使用风险色弱强调

#### Scenario: 用户菜单可访问性

- **WHEN** 辅助技术访问用户菜单
- **THEN** 触发按钮 MUST 设置 `aria-expanded` 与 `aria-haspopup="menu"`
- **AND** 下拉框 MUST 使用 `role="menu"`，菜单项 MUST 使用 `role="menuitem"`

#### Scenario: 密码修改打开弹窗

- **WHEN** 用户点击「密码修改」
- **THEN** 系统 MUST 打开 `ChangePasswordModal`
- **AND** MUST NOT 展示「功能建设中」占位 toast

#### Scenario: 个人资料入口（至 REQ-0014 apply 前）

- **WHEN** `add-admin-profile-page` 尚未 apply
- **THEN** 「个人资料」MAY 仍为 placeholder
- **WHEN** `add-admin-profile-page` 已 apply
- **THEN** 「个人资料」MUST 导航至 `/admin/profile`

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

`/admin/dashboard` MUST 展示「快捷操作」区块，采用四列宫格，且 MUST 仅包含：新增 SKU、新增品牌、新增类目、新增 Banner。MUST NOT 包含：导入 SKU、导入图片、价格管理、操作日志。「新增 SKU」MUST 导航至 `/admin/tile-skus`（MAY 通过 query 打开新增弹窗），MUST NOT 仅展示占位 toast。「新增品牌」MUST 导航至 `/admin/brands`（MAY 通过 query 打开新增弹窗），MUST NOT 仅展示占位 toast。「新增 Banner」MUST 导航至 `/admin/banners`（MAY 通过 `?action=create` 打开新增弹窗），MUST NOT 仅展示占位 toast。

#### Scenario: 快捷操作四项

- **WHEN** 用户查看快捷操作区块
- **THEN** MUST 展示且仅展示 4 个快捷操作卡片
- **AND** 标题 MUST 分别为「新增 SKU」「新增品牌」「新增类目」「新增 Banner」

#### Scenario: 新增 Banner 快捷操作

- **WHEN** 用户点击「新增 Banner」快捷操作
- **THEN** 系统 MUST 导航至 `/admin/banners`
- **AND** MAY 通过 query 自动打开新增 Banner 弹窗
- **AND** MUST NOT 仅展示占位 toast

#### Scenario: 新增类目快捷操作占位

- **WHEN** 用户点击「新增类目」
- **THEN** 系统 MUST 展示占位反馈或导航至类目页（若已实现）
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

### Requirement: 产品版本 pill 视觉一致性修复（管理端）

Web 客户端 MUST 修复管理端 Sidebar brand-head 内产品版本 pill 的视觉一致性缺陷（BUG-0013）：版本 pill MUST 呈现可辨识的小号 badge 容器（可见边框、浅背景、弱化文字色），MUST NOT 退化为与主文字同色级的裸 sans-serif 文案。样式 MUST 对齐 `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html` 与 Golden Reference PNG 的布局语义；MUST 使用 semantic token（`text-muted`/`text-subtle`、`border-border-chip` 或 `border-border-default`、浅背景 token），TSX/CSS MUST NOT 含裸 Hex。实现 SHOULD 扩展 `src/web/src/shared/ui/badge.tsx` 而非平行 ad-hoc 组件。修复 MUST NOT 变更 `PRODUCT_VERSION` 常量来源、Sidebar 导航项或 API。

#### Scenario: 管理端版本 pill 可辨识

- **WHEN** 已登录 `admin` 或 `employee` 查看管理端 Sidebar 顶部 brand-head
- **THEN** `TILESFST` 右侧版本 pill MUST 展示可见边框与浅背景
- **AND** 版本文字 MUST 使用弱化色（`text-muted` 或等价 semantic token）
- **AND** pill MUST 与产品名垂直居中对齐、同一行 flex 排列（gap 约 8px）

#### Scenario: 管理端 pill 对齐 REQ-0010 原型

- **WHEN** 开发者在 1280×1024 下将实现与 `product-version-sidebar-admin.html`、Golden Reference PNG 并排对比
- **THEN** pill 高度（约 18px）、圆角（2px 工业圆角）、边框可见度与文字弱化层级 MUST 与原型语义一致
- **AND** change `trace.md` MUST 记录并排验收结论

#### Scenario: 管理端 brand-head 无布局回归

- **WHEN** 用户访问任意 `/admin/*` 经 `AdminLayout` 页面
- **THEN** `TILESFST` 品牌名 MUST 保持 serif 金色与既有 letter-spacing
- **AND** 导航项、用户菜单、主内容区 MUST 无回归

#### Scenario: 管理端 a11y 保持

- **WHEN** 辅助技术访问 brand-head 版本区
- **THEN** MUST 保留可见 pill 文案与 `aria-label`（如「产品版本 v0.0.1」）

