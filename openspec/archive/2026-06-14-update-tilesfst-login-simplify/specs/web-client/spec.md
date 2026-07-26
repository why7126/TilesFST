## MODIFIED Requirements

### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html` 的布局与 CSS Port 策略（最高优先级视觉结构），并 MUST 满足 `issues/requirements/archive/REQ-0002-product-brand-login-simplify` 的品牌与简化要求。实现 MUST 采用 **CSS Port 策略**：自 `user-login.html` port 专用 stylesheet（`features/auth/styles/login-page.css`），React 负责 DOM 结构与 auth 交互。用户可见产品名称 MUST 为 **TilesFST**（取代 STONEX /「瓷砖信息管理平台」作为 Logo 与主标题文案）。颜色 MUST 引用 `globals.css` 的 `--color-*` token；TSX MUST NOT 含裸 Hex。

#### Scenario: 登录页布局

- **WHEN** 用户在桌面端（>= 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 展示左右 50% 分屏：左侧 `.brand-panel`、右侧 `.form-panel`
- **AND** 页面 MUST 加载登录专用 CSS（`features/auth/styles/login-page.css`）

#### Scenario: 移动端布局

- **WHEN** 用户在移动端（< 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 隐藏左侧品牌区（`display: none`）
- **AND** 登录表单 MUST 全屏居中，最大宽度 520px

#### Scenario: 登录表单元素

- **WHEN** 用户查看登录页
- **THEN** 页面 MUST 包含：`ADMIN PORTAL` 眉标、标题「登录管理端」、描述段落、账号 label + 输入框、密码 label + 输入框、记住登录状态复选框、忘记密码链接、登录按钮、语言切换、底部安全说明
- **AND** 页面 MUST NOT 包含企业微信登录入口或「或使用企业身份登录」第三方分割区
- **AND** 表单 MUST NOT 包含 notice 横幅或页脚版权（© STONEX…）
- **AND** 密码输入框 MUST NOT 包含显隐切换 icon（对齐 HTML 原型）

#### Scenario: 左侧品牌背景

- **WHEN** 用户在桌面端查看登录页左栏
- **THEN** MUST 展示 HTML 原型等价结构：**TilesFST** Logo、TILE DATA OPERATING SYSTEM 眉标、主标题 **TilesFST**、描述、三列统计卡、右下角 CSS 材质拼贴（`material-board` + 3 tiles）、底部 PRECISION · MATERIAL · INVENTORY
- **AND** MUST 叠加网格线与 radial glow 氛围层（对齐 `user-login.html`）
- **AND** MUST NOT 以 `/images/login-material-showcase.jpg` 全屏铺底替代材质拼贴

#### Scenario: 品牌 Logo 字体

- **WHEN** 用户查看登录页左栏 TilesFST Logo
- **THEN** Logo MUST 使用衬线品牌字体（`font-brand` / Cormorant Garamond）
- **AND** MUST 保持大写字距（`tracking-brand`）与品牌金色

#### Scenario: 登录页无页面级纵向滚动

- **WHEN** 用户在桌面视口（宽度 >= 1024px，高度 >= 720px）访问 `/admin/login`
- **THEN** `html` 与 `body` MUST NOT 产生页面级纵向滚动条
- **AND** `.login-shell` MUST 锁定于视口（如 `position: fixed; inset: 0; overflow: hidden`）

#### Scenario: 登录页组件结构

- **WHEN** 开发者查看登录页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS class（`login-shell`、`brand-panel`、`form-panel`、`login-card` 等）
- **AND** auth 业务逻辑 MUST 保留在 `LoginForm` / hooks / store，不与 presentation CSS 耦合

### Requirement: 登录页原型静态资源

Web 客户端 MUST 在 `src/web/public/` 提供登录页原型所需静态资源，并随生产构建与 Docker Web 镜像部署。

#### Scenario: 背景图存在

- **WHEN** 构建 Web 生产包
- **THEN** `public/images/login-material-showcase.jpg` MAY 存在且可在 `/images/login-material-showcase.jpg` 访问（左栏不强制 JPG 全屏铺底）

### Requirement: 登录页 PNG 视觉验收 Gate

登录页视觉对齐 MUST 通过 PNG golden reference 验收 gate；REQ-0002 变更项（TilesFST 品牌、无企微、无整页滚动）MUST 纳入 checklist。

#### Scenario: 桌面 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/login` 与 `user-login.png`
- **THEN** diff checklist（背景色、50/50 分屏、**TilesFST Logo**、材质拼贴、表单宽、输入高、focus 金边、按钮、间距、语言切换、无 notice 横幅、**无企微入口**、安全说明、**无页面级纵向滚动**）MUST 全部 pass
- **AND** 结果 MUST 记录在 change trace 与 sprint acceptance-report

#### Scenario: 构建与部署验证

- **WHEN** 执行 `vite build` 与 `docker compose build web`
- **THEN** 构建 MUST 成功且登录页 CSS、字体可访问

### Requirement: 登录页控件原型形态

登录页表单控件 MUST 对齐 `user-login.html` 与 PNG 视觉；样式 MUST 来自 port CSS，MUST NOT 沿用 shadcn 默认态。

#### Scenario: 输入框默认与 focus 态

- **WHEN** 用户查看或 focus 账号/密码输入框
- **THEN** 默认边框 MUST 为 `1px solid` 且颜色等价 `--color-border-emphasis`（0.1 白）
- **AND** focus 时边框 MUST 变为纯品牌金（`--color-brand-gold`），背景 MAY 为极弱 white overlay
- **AND** MUST NOT 展示 ring-offset 或大偏移 focus ring

#### Scenario: 主按钮形态

- **WHEN** 用户查看登录按钮
- **THEN** 按钮 MUST 为 56px 高、全宽、金色实底、深色文字、2px 圆角（`.primary`）

#### Scenario: 表单控件为原生元素

- **WHEN** 开发者查看 `LoginForm` markup
- **THEN** 输入框与主按钮 MUST 为原生 `<input>` / `<button>` 并应用 port CSS class
- **AND** MUST NOT 使用 shadcn `Input` / `Button` / `Checkbox` 作为登录页最终视觉层

#### Scenario: 占位交互不破坏布局

- **WHEN** 用户点击语言切换或忘记密码占位入口
- **THEN** 系统 MAY noop 或展示 inline/toast 弱提示
- **AND** MUST NOT 在表单区域上方插入 notice 横幅推挤布局

### Requirement: 占位功能

登录页中的非本期功能 MUST 以占位方式呈现，不阻塞主登录流程。

#### Scenario: 忘记密码占位

- **WHEN** 用户点击「忘记密码？」
- **THEN** 系统 MUST 展示「功能建设中」提示或 noop
- **AND** MUST NOT 跳转至完整找回密码流程

### Requirement: 可访问性

登录页 MUST 满足基础可访问性要求。

#### Scenario: 键盘导航

- **WHEN** 用户使用 Tab 键导航
- **THEN** Tab 顺序 MUST 为：语言切换 → 用户名 → 密码 → 记住我 → 忘记密码 → 登录

#### Scenario: 表单标签

- **WHEN** 屏幕阅读器访问表单
- **THEN** 输入框 MUST 具备可访问 label（可视觉隐藏）
- **AND** 错误提示 MUST 通过 `aria-describedby` 关联对应字段

### Requirement: 管理端登录页 Design System 实现

Web 客户端管理端登录页（`/admin/login`）MUST 通过 port CSS 引用 Design Token（`--color-*`），MUST 对齐 `user-login.html` 布局与视觉；登录页 presentation MUST NOT 依赖 shadcn 表单 primitive 的默认皮相。

#### Scenario: Token 引用

- **WHEN** 开发者查看 `login-page.css`
- **THEN** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX 组件 MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex

#### Scenario: 桌面分屏与右栏背景

- **WHEN** 视口宽度 >= 1024px
- **THEN** 页面 MUST 展示左右 50% 分屏
- **AND** 右栏背景 MUST 为 `--color-page` 加 radial glow（对齐 HTML `.form-panel`）

#### Scenario: 精确间距

- **WHEN** 视口为桌面端
- **THEN** 表单 max-width MUST 为 420px
- **AND** 输入框高度 MUST 为 64px（<640px 为 52px）
- **AND** 表单项间距 MUST 为 28px；标题到表单 MUST 为 48px

#### Scenario: 登录按钮 loading

- **WHEN** 登录请求进行中
- **THEN** 按钮 MUST 展示 loading 文案或状态且 `disabled`
- **AND** MUST 设置 `aria-busy="true"`

#### Scenario: 占位功能行为不变

- **WHEN** 用户点击「忘记密码？」
- **THEN** MAY noop 或展示弱提示
- **AND** MUST NOT 发起 OAuth 或跳转外部流程

## REMOVED Requirements

### Requirement: 企业微信图标视觉

**Reason**: REQ-0002 明确登录页仅保留账号密码路径，不再展示企业微信登录入口。

**Migration**: 删除 `ThirdPartyLoginSection`、`WeComLoginButton` 及 port CSS（`.third-party`、`.divider`、`.wecom`）；`public/icons/wecom.svg` 可保留供未来 change 复用，但登录页 MUST NOT 引用。
