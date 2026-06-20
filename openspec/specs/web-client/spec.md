# web-client Specification

## Purpose
TBD - created by archiving change add-user-login. Update Purpose after archive.
## Requirements
### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html` 的布局与 CSS Port 策略（最高优先级视觉结构），并 MUST 满足 `issues/requirements/REQ-0002-product-brand-login-simplify` 与 `issues/requirements/REQ-0003-login-left-panel-refine` 的要求。实现 MUST 采用 **CSS Port 策略**：自 `user-login.html` port 专用 stylesheet（`features/auth/styles/login-page.css`），React 负责 DOM 结构与 auth 交互。左栏金色 Logo（`.logo`）MUST 为 **TilesFST**；左栏白色主标题（`.brand-title`）MUST 为 **「瓷砖信息管理后台」**。颜色 MUST 引用 `globals.css` 的 `--color-*` token；TSX MUST NOT 含裸 Hex。密码字段 MUST 按 `issues/requirements/REQ-0003-login-remember-autofill/prototype/web/login-form-enhancements-context.md` 提供显隐切换控件。

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
- **THEN** 页面 MUST 包含：`ADMIN PORTAL` 眉标、标题「登录管理端」、描述段落、账号 label + 输入框、密码 label + 输入框（含显隐切换按钮）、记住登录状态复选框、登录按钮、语言切换、底部安全说明
- **AND** 页面 MUST NOT 包含可见的「忘记密码？」入口（REQ-0003-login-left-panel-refine）
- **AND** 页面 MUST NOT 包含企业微信登录入口或「或使用企业身份登录」第三方分割区
- **AND** 表单 MUST NOT 包含 notice 横幅或页脚版权（© STONEX…）
- **AND** 密码输入框 MUST 在 `.password-wrap` 容器内提供显隐切换按钮（默认 `type="password"`）

#### Scenario: 左侧品牌背景

- **WHEN** 用户在桌面端查看登录页左栏
- **THEN** MUST 展示：**TilesFST** Logo（金色）、TILE DATA OPERATING SYSTEM 眉标、主标题 **「瓷砖信息管理后台」**（白色）、描述、三列统计卡、右下角 CSS 材质拼贴（`material-board` + 3 tiles）、底部 PRECISION · MATERIAL · INVENTORY
- **AND** MUST 叠加网格线与 radial glow 氛围层（对齐 `user-login.html`）

#### Scenario: 左栏主标题与 Logo 间距

- **WHEN** 用户在桌面端查看登录页左栏
- **THEN** Logo 与眉标/主标题之间垂直间距 MUST 紧凑（REQ-0003-login-left-panel-refine）

#### Scenario: 统计卡不被材质拼贴遮挡

- **WHEN** 用户在 1440×1024 桌面视口查看登录页左栏
- **THEN** 三列统计卡（含 126 / 门店同步）MUST 完整可读，不被 `.material-board` 覆盖

#### Scenario: Logo 品牌字体

- **WHEN** 用户查看登录页左栏 TilesFST Logo
- **THEN** Logo MUST 使用品牌字体样式（`font-brand` / Georgia 类）

#### Scenario: 登录页无页面级纵向滚动

- **WHEN** 用户在桌面端（>= 1024px）访问 `/admin/login`
- **THEN** 页面 MUST NOT 出现整页纵向滚动条（视口内完成布局）

#### Scenario: 登录页组件结构

- **WHEN** 开发者查看登录页源码
- **THEN** 页面 MUST 由 `features/auth` 模块组件组装（如 `LoginPage`、`LoginForm`、`BrandPanel`）

### Requirement: 登录页原型静态资源

Web 客户端 MUST 在 `src/web/public/` 提供登录页原型所需静态资源，并随生产构建与 Docker Web 镜像部署。

#### Scenario: 背景图存在

- **WHEN** 构建 Web 生产包
- **THEN** `public/images/login-material-showcase.jpg` MAY 存在且可在 `/images/login-material-showcase.jpg` 访问（左栏不强制 JPG 全屏铺底）

### Requirement: 登录页语言切换占位

Web 客户端 MUST 在登录页右栏右上角展示语言切换占位，视觉对齐 `user-login.html` `.language` 样式。

#### Scenario: 语言切换展示

- **WHEN** 用户查看登录页右栏
- **THEN** MUST 展示「简体中文⌄」文案于 `.language` 边框按钮内
- **AND** 点击 MAY noop；MUST NOT 要求完整 i18n 实现

### Requirement: 登录页 PNG 视觉验收 Gate

登录页视觉对齐 MUST 通过 PNG golden reference 验收 gate；REQ-0002 与 REQ-0003 变更项 MUST 纳入 checklist。

#### Scenario: 桌面 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/login` 与 `user-login.png`
- **THEN** diff checklist（背景色、50/50 分屏、**TilesFST Logo**、**主标题「瓷砖信息管理后台」**、Logo-眉标间距、**统计卡三格可读（126 不遮挡）**、材质拼贴、表单宽、输入高、focus 金边、按钮、间距、语言切换、无 notice 横幅、**无企微入口**、**无忘记密码入口**、安全说明、**无页面级纵向滚动**）MUST 全部 pass
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
- **THEN** 输入框与主按钮 MUST 为原生 `<input>` / `button` 并应用 port CSS class
- **AND** MUST NOT 使用 shadcn `Input` / `Button` / `Checkbox` 作为登录页最终视觉层

#### Scenario: 语言切换占位不破坏布局

- **WHEN** 用户点击语言切换占位入口
- **THEN** 系统 MAY noop 或展示 inline/toast 弱提示
- **AND** MUST NOT 在表单区域上方插入 notice 横幅推挤布局

### Requirement: UI 设计规范登录页专章

项目 MUST 在 `rules/ui-design.md` 提供登录页设计专章，与 `user-login.html` 对齐，并说明 CSS Port 策略。

#### Scenario: 登录页规范存在

- **WHEN** 开发者查阅 `rules/ui-design.md`
- **THEN** MUST 找到登录页专章，涵盖 CSS Port 策略、色彩、字体、间距、组件态
- **AND** MUST 指向 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html` 作为最高优先级视觉源

### Requirement: 登录表单校验

前端 MUST 在提交前校验表单必填字段，不通过时不发起 API 请求。

#### Scenario: 用户名为空

- **WHEN** 用户未填写用户名并点击登录
- **THEN** 系统 MUST 展示「请输入用户名」提示
- **AND** MUST NOT 调用登录 API

#### Scenario: 密码为空

- **WHEN** 用户未填写密码并点击登录
- **THEN** 系统 MUST 展示「请输入密码」提示
- **AND** MUST NOT 调用登录 API

#### Scenario: Enter 键提交

- **WHEN** 用户在用户名或密码输入框内按下 Enter 键
- **THEN** 系统 MUST 触发登录提交（若校验通过）

### Requirement: 登录提交与状态

前端 MUST 在登录过程中展示 loading 状态，防止重复提交。

#### Scenario: 登录 loading

- **WHEN** 用户点击登录且校验通过
- **THEN** 登录按钮 MUST 进入 loading/disabled 状态
- **AND** 请求完成前 MUST NOT 允许重复提交

#### Scenario: 登录成功跳转

- **WHEN** 登录 API 返回成功且用户 role 为 `admin` 或 `employee`
- **THEN** 前端 MUST 保存 token 与用户信息
- **AND** MUST 跳转至 `/admin/dashboard`

#### Scenario: 登录失败提示

- **WHEN** 登录 API 返回 401
- **THEN** 前端 MUST 展示「账号或密码错误」
- **AND** MUST NOT 清空用户名输入

#### Scenario: 账号被禁用

- **WHEN** 登录 API 返回 403 且错误码为 `AUTH_USER_DISABLED`
- **THEN** 前端 MUST 展示「账号已停用，请联系管理员」

#### Scenario: 网络异常

- **WHEN** 登录 API 请求因网络错误失败
- **THEN** 前端 MUST 展示「网络异常，请稍后重试」

### Requirement: 登录态保持

前端 MUST 支持登录态持久化，刷新页面后可恢复已登录状态。前端 MUST 在用户勾选「记住登录状态」且登录成功时，将上次成功登录使用的用户名与密码保存至 `localStorage`（key：`stonex_login_credentials`），并在下次进入 `/admin/login` 时自动填充表单。

#### Scenario: 刷新后恢复登录

- **WHEN** 用户已登录且 token 仍有效，刷新页面
- **THEN** 前端 MUST 从本地存储读取 token 并调用 `/auth/me` 恢复用户信息
- **AND** 用户 MUST 保持已登录状态

#### Scenario: remember_me 持久化

- **WHEN** 用户勾选「记住我」并登录成功
- **THEN** 前端 MUST 将 token 持久化至 localStorage

#### Scenario: 未勾选 remember_me

- **WHEN** 用户未勾选「记住我」并登录成功
- **THEN** 前端 MUST 将 token 存储至 sessionStorage

#### Scenario: 记住登录状态保存凭证

- **WHEN** 用户勾选「记住登录状态」且登录 API 返回成功
- **THEN** 前端 MUST 将 trim 后的 `username` 与 `password` 及 `remember: true` 写入 `localStorage`（`stonex_login_credentials`）
- **AND** MUST NOT 将密码写入服务端或日志

#### Scenario: 未勾选记住登录状态清除凭证

- **WHEN** 用户未勾选「记住登录状态」且登录 API 返回成功
- **THEN** 前端 MUST 清除 `stonex_login_credentials`（若存在）

#### Scenario: 再次进入登录页自动填充

- **WHEN** 用户未持有有效登录态并访问 `/admin/login`，且 `stonex_login_credentials` 存在且 `remember` 为 true
- **THEN** 前端 MUST 自动填充用户名与密码输入框
- **AND** MUST 将「记住登录状态」复选框设为勾选

#### Scenario: 登录失败不更新凭证

- **WHEN** 登录 API 返回失败（如 401）
- **THEN** 前端 MUST NOT 更新 `stonex_login_credentials`

### Requirement: 管理端路由守卫

Web 客户端 MUST 对管理端路由实施鉴权，除 `/admin/login` 外均为受保护路由。

#### Scenario: 未登录访问受保护路由

- **WHEN** 未登录用户访问 `/admin/*`（非 login）
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 已登录访问登录页

- **WHEN** 已登录用户访问 `/admin/login`
- **THEN** 前端 MUST 自动跳转至 `/admin/dashboard`

#### Scenario: Token 过期

- **WHEN** 已登录用户访问受保护路由但 token 已过期（API 返回 401）
- **THEN** 前端 MUST 清除本地登录态
- **AND** MUST 跳转至 `/admin/login` 并提示「登录已过期，请重新登录」

### Requirement: 角色权限前端拦截

前端 MUST 根据用户角色限制管理端访问。用户管理路由 `/admin/users` 与 SYSTEM 分组「用户管理」菜单 MUST 仅对 `role=admin` 可见且可访问；`employee` MUST 可访问其他管理端页面（如 `/admin/dashboard`）但 MUST NOT 访问用户管理。

#### Scenario: 店主角色拒绝管理端

- **WHEN** 角色为 `store_owner` 的用户登录成功
- **THEN** 前端 MUST NOT 进入管理端受保护页面
- **AND** MUST 展示无权限提示或跳转无权限页

#### Scenario: 运营人员不可访问用户管理

- **WHEN** 角色为 `employee` 的用户已登录
- **THEN** Sidebar MUST NOT 展示「用户管理」菜单项
- **AND** 直接访问 `/admin/users` MUST 展示无权限提示或重定向至 `/admin/dashboard`

#### Scenario: 管理员可访问用户管理

- **WHEN** 角色为 `admin` 的用户已登录
- **THEN** Sidebar MUST 展示「用户管理」且可导航至 `/admin/users`
- **AND** 页面 MUST 正常加载用户列表

#### Scenario: 非管理员访问管理员专属页面（通用）

- **WHEN** 角色为 `employee` 的用户访问其他管理员专属页面（若存在）
- **THEN** 前端 MUST 展示无权限提示

### Requirement: 退出登录

Web 客户端 MUST 提供退出登录能力。退出入口 MUST 位于管理端 Sidebar 底部用户菜单的下拉框内，MUST NOT 在 Sidebar 用户按钮下方或管理端顶栏直接展示独立的「退出登录」按钮。退出时 MUST 清除本地登录凭证（`stonex_login_credentials`）。

#### Scenario: 退出操作

- **WHEN** 用户在管理端 Sidebar 用户菜单下拉框中点击「退出登录」
- **THEN** 前端 MUST 调用 logout API（可选）、清除本地 token 与用户态
- **AND** MUST 清除 `stonex_login_credentials`
- **AND** MUST 跳转至 `/admin/login`

#### Scenario: 退出后再访问

- **WHEN** 用户退出后访问管理端受保护页面
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 无顶栏退出按钮

- **WHEN** 用户查看管理端 Shell（`/admin/dashboard` 及后续 AdminLayout 包裹页）
- **THEN** 页面 MUST NOT 在顶栏 header 展示独立「退出登录」按钮
- **AND** MUST NOT 在用户菜单触发按钮正下方直接展示「退出登录」

### Requirement: 占位功能

登录页中非本期能力 MUST NOT 以可见入口干扰主登录流程；忘记密码本期 MUST 隐藏。

#### Scenario: 忘记密码隐藏

- **WHEN** 用户查看登录页右栏表单
- **THEN** MUST NOT 渲染可见的「忘记密码？」入口
- **AND** MUST NOT 跳转至找回密码流程

#### Scenario: 语言切换占位

- **WHEN** 用户点击语言切换
- **THEN** 系统 MAY noop
- **AND** MUST NOT 要求完整 i18n 实现

### Requirement: Auth Feature 模块封装

前端登录逻辑 MUST 封装在独立 `src/web/src/features/auth/` 模块中，不散落在页面组件内。

#### Scenario: 模块边界

- **WHEN** 实现登录相关功能
- **THEN** API 调用、状态管理、token 工具 MUST 位于 `features/auth/` 目录
- **AND** 页面组件 MUST 通过 hooks 或 store 消费 auth 能力

### Requirement: Orval 客户端集成

前端 MUST 通过 Orval 生成的 API 客户端调用认证接口，不得手写 `/api/generated/` 目录代码。

#### Scenario: API 客户端来源

- **WHEN** 前端调用 auth 相关 API
- **THEN** MUST 使用 Orval 生成的类型化客户端
- **AND** auth API 变更后 MUST 运行 `./scripts/generate-openapi-client.sh`

### Requirement: 可访问性

登录页 MUST 满足基础可访问性要求。

#### Scenario: 键盘导航

- **WHEN** 用户使用 Tab 键导航
- **THEN** Tab 顺序 MUST 为：语言切换 → 用户名 → 密码 → 密码显隐切换 → 记住我 → 登录
- **AND** MUST NOT 包含「忘记密码？」可聚焦项（REQ-0003-login-left-panel-refine）

#### Scenario: 表单标签

- **WHEN** 屏幕阅读器访问表单
- **THEN** 输入框 MUST 具备可访问 label（可视觉隐藏）
- **AND** 错误提示 MUST 通过 `aria-describedby` 关联对应字段

#### Scenario: 密码显隐可访问性

- **WHEN** 用户聚焦密码显隐切换按钮
- **THEN** 按钮 MUST 具备 `aria-label`（如「显示密码」/「隐藏密码」）或等效 `aria-pressed` 状态

### Requirement: 管理端登录页 Design System 实现

Web 客户端管理端登录页（`/admin/login`）MUST 通过 port CSS 引用 Design Token（`--color-*`），MUST 对齐 `user-login.html` 布局与视觉；登录页 presentation MUST NOT 依赖 shadcn 表单 primitive 的默认皮相；左栏布局 MUST 满足 REQ-0003 间距与统计卡可读性要求。

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

#### Scenario: 左栏 Logo 与统计区间距

- **WHEN** 开发者查看 `login-page.css` 左栏规则
- **THEN** `.brand-top` 与 `.brand-content` 间距 MUST 已收紧（REQ-0003）
- **AND** `.stats-card` 与 `.material-board` 定位 MUST 保证三格统计可读

#### Scenario: 登录按钮 loading

- **WHEN** 登录请求进行中
- **THEN** 按钮 MUST 展示 loading 文案或状态且 `disabled`
- **AND** MUST 设置 `aria-busy="true"`

#### Scenario: 忘记密码不可见

- **WHEN** 用户查看登录表单
- **THEN** MUST NOT 存在 `.login-link` 忘记密码入口
- **AND** `.form-options` 布局 MUST NOT 因隐藏入口产生明显错位

### Requirement: 登录页 refactor 不改变认证逻辑

登录页 UI 重构 MUST NOT 修改 auth store、login API 调用、token 持久化策略、路由守卫与角色分流逻辑。

#### Scenario: Auth 逻辑冻结

- **WHEN** refactor-login-ui 实现完成
- **THEN** `src/web/src/features/auth/store/`、`hooks/useAuth.ts`、`api/auth-api.ts` MUST 无行为变更
- **AND** 现有登录成功/失败/记住我行为 MUST 与 refactor 前一致

### Requirement: 管理端瓷砖类目管理页

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 与 `tile-category-management-add.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区、左侧类目树（280px）与右侧类目列表
- **AND** MUST NOT 展示导出按钮或批量操作入口

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击类目树节点
- **THEN** 右侧列表 MUST 刷新为该节点及其子级类目
- **AND** 工具栏标题 MUST 同步当前节点名称与记录数

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态/层级并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页 MUST 支持每页显示数 10/20/50；切换 page_size MUST 重置页码为 1 并保留筛选条件

#### Scenario: 列表工具栏

- **WHEN** 用户查看列表工具栏
- **THEN** MUST 仅展示「调整排序」按钮
- **AND** MUST NOT 展示「导出」

#### Scenario: 列表行启停操作

- **WHEN** 列表行状态为 `ENABLED`
- **THEN** 操作列 MUST 展示「编辑」与「停用」
- **AND** MUST NOT 展示「删除」
- **WHEN** 列表行状态为 `DISABLED`
- **THEN** 操作列 MUST 展示「编辑」与「启用」（无论 `sku_count` 是否为 0）
- **AND** 点击「启用」MUST 调用 `POST /api/v1/admin/tile-categories/{id}/enable` 并刷新列表与树

#### Scenario: 删除入口规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** MUST 展示可点击「删除」（风险色），且 **同时** MUST 展示「启用」
- **WHEN** 列表行处于启用状态
- **THEN** MUST NOT 展示删除入口
- **WHEN** 列表行停用且 `sku_count > 0`
- **THEN** MAY 展示置灰「删除」并提示规则；MUST 仍展示可点击「启用」

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增类目」或行内「编辑」
- **THEN** MUST 打开宽 560px 居中弹窗，暗色遮罩 + blur
- **AND** 字段 MUST 一行一个：上级类目、类目名称、类目编码、排序权重、类目描述、状态（Switch）
- **AND** 类目名称、编码、排序 MUST 必填；排序 MUST 仅允许正整数
- **AND** 选择三级类目作为上级时 MUST 禁止保存子级

#### Scenario: 类目管理 CSS Port

- **WHEN** 开发者查看类目管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-category-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-categories`
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 调整排序占位

- **WHEN** 用户点击「调整排序」且本期未实现 reorder
- **THEN** 系统 MAY 展示 Toast「排序调整功能即将上线」
- **AND** MUST NOT 抛出未捕获错误

