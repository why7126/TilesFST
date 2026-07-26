## MODIFIED Requirements

### Requirement: 管理端工作台 Shell 布局

Web 客户端 MUST 为已认证管理端用户提供 `/admin/dashboard` 工作台页面，采用固定 Sidebar + 右侧内容区布局，视觉 MUST 高保真对齐管理端暗色旗舰风与当前 Design System，且 MUST 支持桌面端（>1023px）Sidebar **展开/收起**两种宽度态。Sidebar **展开**宽度 MUST 为 264px、**收起**宽度 MUST 为 72px，由 CSS 变量 `--admin-sidebar-width` 驱动 `.admin-shell` 网格第一列；高度 MUST 为 100vh（`position: sticky`），MUST NOT 随右侧内容高度拉伸或滚动；右侧内容区 MUST 为 100vh 且 `overflow: auto`。主内容 padding 在 desktop MUST 收敛到 `24px 24px 48px` 量级，`content-inner` MUST 使用统一宽度策略，MUST NOT 继续使用 1080px 硬上限；最终可采用 `max-width: min(1440px, 100%)` 或 `max-width: 100%`，但 MUST 在实现 trace 中记录。宽度切换 MUST 有约 200–250ms 过渡；`prefers-reduced-motion: reduce` 时 MAY 禁用或缩短动画。在 `≤1023px` 窄屏和 `≤639px` 手机小屏视口下，Admin Shell MUST 进入基础可用布局：Sidebar 不得遮挡主内容，导航项必须可完整访问或滚动访问，折叠 chevron 不得与窄屏导航冲突，`.main-content` 与 `.content-inner` 不得引入 Shell 级或页面级不可控横向滚动。

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

#### Scenario: 窄屏 Sidebar 基础可用

- **WHEN** 已登录 `admin` 或 `employee` 用户在 `375x812`、`390x844` 或 `768x1024` 视口访问任意已实现 `/admin/*` 页面
- **THEN** Sidebar 或窄屏导航 MUST 不遮挡主内容
- **AND** 当前用户可访问的导航项 MUST 可完整访问或通过导航容器滚动访问
- **AND** 当前 active 路由状态 MUST 仍可识别
- **AND** 桌面 Sidebar 折叠 chevron MUST 隐藏、禁用或等价处理，且不得造成布局跳动或与窄屏导航控件重叠。

#### Scenario: 管理端 Shell CSS Port

- **WHEN** 开发者查看管理端首页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS（如 `features/admin/styles/admin-home.css`）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex
- **AND** 管理端 CSS MUST NOT 重新引入与全局 `content-inner` 策略冲突的页面级 1080px / 1120px 内容宽度上限。
