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

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `tile-category-management-add.html` 弹窗策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区（**无**外层 section 标题）、左侧类目树（280px）与右侧类目列表（**无**外层「类目列表」section 标题）
- **AND** MUST NOT 展示导出按钮或批量操作入口

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击类目树节点
- **THEN** 右侧列表 MUST 刷新为该节点及其子级类目
- **AND** 表格工具栏 MUST 同步当前节点名称与记录数（`cat-table-toolbar`）

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态/层级并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页 MUST 支持每页显示数 10/20/50；切换 page_size MUST 重置页码为 1 并保留筛选条件
- **AND** 分页左侧 MUST 展示「共 {total} 个类目」（`total` 与 API 列表总数一致）
- **AND** 分页右侧 MUST 展示页码控件与「每页显示」条数选择（选项文案「10 条」「20 条」「50 条」）
- **AND** MUST NOT 展示「当前显示 x-y / N 条」「x-y / N」等 v1 分页文案

#### Scenario: 列表工具栏

- **WHEN** 用户查看列表工具栏
- **THEN** MUST 仅展示「调整排序」按钮（右侧）
- **AND** 左侧 MUST 展示树上下文标题与「共 {total} 条记录」
- **AND** MUST NOT 展示「导出」

#### Scenario: 列表行启停操作

- **WHEN** 列表行状态为 `ENABLED`
- **THEN** 操作列 MUST 展示「编辑」与「停用」
- **AND** MUST NOT 展示「删除」
- **WHEN** 列表行状态为 `DISABLED`
- **THEN** 操作列 MUST 展示「编辑」与「启用」（无论 `sku_count` 是否为 0）
- **WHEN** 用户点击「启用」或「停用」
- **THEN** MUST 先展示启停确认弹窗，MUST NOT 直接调用 API
- **WHEN** 用户在确认弹窗点击「确认启用」或「确认停用」
- **THEN** MUST 调用 `POST /api/v1/admin/tile-categories/{id}/enable` 或 `.../disable` 并刷新列表与树
- **WHEN** 用户取消或关闭确认弹窗
- **THEN** MUST NOT 改变类目状态

#### Scenario: 启停确认弹窗

- **WHEN** 用户触发启停确认
- **THEN** MUST 展示与「删除类目」确认框相同结构的 modal（`modal-backdrop` + `modal-card`）
- **AND** 停用标题 MUST 为「停用类目」；启用标题 MUST 为「启用类目」
- **AND** 正文 MUST 含类目 `{name}`；停用 MUST 含前台不可见说明
- **AND** 底部 MUST 含「取消」与「确认停用」/「确认启用」

#### Scenario: 删除入口规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** MUST 展示可点击「删除」（风险色），且 **同时** MUST 展示「启用」
- **WHEN** 列表行处于启用状态
- **THEN** MUST NOT 展示删除入口
- **WHEN** 列表行停用且 `sku_count > 0`
- **THEN** MAY 展示置灰「删除」并提示规则；MUST 仍展示可点击「启用」
- **AND** 删除 MUST 仍使用独立「删除类目」确认弹窗，MUST NOT 与启停确认合并

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
- **AND** 分页 SHOULD 复用与 `UserManagementPage` 一致的 DOM class（`.pagination`、`.page-summary`、`.page-right`）或等价样式

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-categories`
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 调整排序占位

- **WHEN** 用户点击「调整排序」且本期未实现 reorder
- **THEN** 系统 MAY 展示 Toast「排序调整功能即将上线」
- **AND** MUST NOT 抛出未捕获错误

### Requirement: 品牌管理 UI 一致性修复

Web 客户端 MUST 修复 `/admin/brands` 品牌管理页的 UI 一致性缺陷，使品牌列表分页与用户管理页分页保持一致，并使新增/编辑品牌弹窗的 Logo 选择文件控件与管理端表单和图片上传控件风格保持一致。修复 MUST NOT 修改品牌 API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: 品牌列表分页对齐用户管理页

- **WHEN** 管理员或运营人员分别访问 `/admin/brands` 与 `/admin/users`
- **THEN** 两个页面底部分页区域的布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 保持一致
- **AND** 品牌页 MUST NOT 使用与用户管理页割裂的 `page-left` / `brand-pagination-right` 主视觉结构

#### Scenario: 品牌分页功能不回退

- **WHEN** 用户在品牌列表页执行上一页、下一页或每页显示切换
- **THEN** 分页功能 MUST 继续可用
- **AND** 每页显示切换 MUST 将页码重置为 1

#### Scenario: 品牌跳页能力一致呈现

- **WHEN** 品牌列表保留跳页输入能力
- **THEN** 跳页输入 MUST 作为统一分页布局的可选扩展呈现
- **AND** MUST NOT 破坏与用户管理页分页的主视觉一致性

#### Scenario: 品牌 Logo 文件选择控件对齐管理端表单

- **WHEN** 用户打开新增或编辑品牌弹窗
- **THEN** 「品牌Logo」文件选择控件 MUST 与弹窗内输入框、按钮和用户管理弹窗头像上传控件保持一致的视觉层级
- **AND** 文件选择入口 MUST 使用明确按钮或可访问 label
- **AND** MUST NOT 展示浏览器默认 file input 皮相

#### Scenario: Logo 空态和预览态

- **WHEN** 品牌 Logo 尚未上传
- **THEN** 控件 MUST 展示统一空态说明和上传入口
- **WHEN** 品牌 Logo 已上传
- **THEN** 控件 MUST 展示 Logo 预览、文件更换入口和帮助文案
- **AND** MUST NOT 挤压弹窗布局或破坏头尾固定结构

#### Scenario: 品牌管理功能保持可用

- **WHEN** 用户执行查询、重置、分页、新增品牌、编辑品牌、上传 Logo 或保存品牌
- **THEN** 原有功能 MUST 保持可用
- **AND** 前端 MUST 继续使用既有品牌 API 与 Logo 上传 API

### Requirement: 品牌 Logo 展示与提示布局修复

Web 客户端 MUST 修复 `/admin/brands` 品牌 Logo 展示失败与状态提示导致页面上下波动的问题。品牌列表和品牌编辑弹窗 MUST 使用后端返回的可访问媒体 URL 正常展示/回显 Logo；品牌页自动消失状态提示 MUST NOT 通过插入普通文档流节点推挤页面主体。修复 MUST 保持品牌查询、分页、新增、编辑、启用、停用、删除等既有功能可用，并 MUST 遵守 Design System 语义样式约束。

#### Scenario: 品牌列表展示已上传 Logo

- **GIVEN** 品牌记录存在可访问 `logo_url` 或等价预览 URL
- **WHEN** `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 品牌列 MUST 展示已上传 Logo 图片
- **AND** 无 Logo 的品牌 MUST 保持首字/缩写占位
- **AND** 图片加载失败时 MUST 保持稳定单元格尺寸和空态，不得造成表格布局跳动

#### Scenario: 品牌编辑弹窗回显 Logo

- **GIVEN** 品牌记录存在可访问 Logo URL
- **WHEN** 用户点击「编辑」打开品牌弹窗
- **THEN** 「品牌Logo」区域 MUST 展示当前 Logo 预览
- **AND** 更换 Logo 后预览 MUST 即时更新
- **AND** 保存后再次打开弹窗 MUST 回显最新 Logo

#### Scenario: 品牌状态变更提示不推挤页面

- **WHEN** 用户在 `/admin/brands` 执行启用或停用品牌
- **THEN** 系统 SHOULD 展示成功或失败提示
- **AND** 提示出现和消失 MUST NOT 改变 page-header、指标卡、筛选区、表格或分页区域的纵向位置
- **AND** 提示 MUST 使用固定 toast、稳定提示槽或等价不推挤主体内容的方式

#### Scenario: 品牌创建更新删除提示不推挤页面

- **WHEN** 用户创建、更新或删除品牌并触发提示
- **THEN** 提示出现和消失 MUST NOT 造成页面主体上下位移
- **AND** 弹窗内表单错误 MAY 使用 inline 错误文案
- **AND** inline 错误文案 MUST NOT 影响列表页主体稳定性

#### Scenario: 品牌管理功能不回退

- **WHEN** 用户执行查询、重置、分页、每页显示切换、新增、编辑、启用、停用或删除品牌
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌
- **AND** `store_owner` MUST NOT 访问管理端品牌维护能力

#### Scenario: Design System 约束

- **WHEN** 修复修改 Web UI 样式
- **THEN** 新增或修改样式 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式
- **AND** MUST NOT 新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式

### Requirement: 品牌列表启停二次确认

Web 客户端 MUST 在 `/admin/brands` 品牌列表页为行内「启用」与「停用」操作提供二次确认，以降低误触风险。启停确认 MUST 复用与同页「删除品牌」确认框相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「启用」或「停用」时 MUST NOT 直接调用 enable/disable API；MUST 先展示确认弹窗，仅在用户点击「确认启用」或「确认停用」后调用 API。删除操作 MUST 仍使用独立「删除品牌」确认弹窗，MUST NOT 与启停确认合并。本能力 MUST NOT 修改品牌 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 停用须先确认

- **WHEN** 用户在品牌列表行点击「停用」
- **THEN** MUST 展示停用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/disable`
- **AND** 弹窗标题 MUST 为「停用品牌」
- **AND** 正文 MUST 为「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」（`{name}` 为该行品牌名称）

#### Scenario: 启用须先确认

- **WHEN** 用户在品牌列表行点击「启用」
- **THEN** MUST 展示启用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/enable`
- **AND** 弹窗标题 MUST 为「启用品牌」
- **AND** 正文 MUST 为「确认启用品牌「{name}」？」

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 启停确认弹窗展示
- **THEN** 底部 MUST 含「取消」与「确认停用」或「确认启用」（主按钮）
- **WHEN** 用户点击「取消」、遮罩、× 或 ESC
- **THEN** MUST 关闭弹窗且 MUST NOT 改变品牌状态或调用 API

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在停用确认弹窗点击「确认停用」
- **THEN** MUST 调用 disable API 并展示 Toast「品牌已停用」，并刷新列表与指标卡 summary
- **WHEN** 用户在启用确认弹窗点击「确认启用」
- **THEN** MUST 调用 enable API 并展示 Toast「品牌已启用」，并刷新列表与指标卡 summary

#### Scenario: 删除确认独立

- **WHEN** 用户点击行内「删除」
- **THEN** MUST 仍使用独立「删除品牌」确认弹窗
- **AND** 启停确认 state MUST NOT 与删除确认 state 共用

#### Scenario: 无障碍与样式

- **WHEN** 启停确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 brand-management CSS Port

#### Scenario: 品牌管理其他能力不回退

- **WHEN** 用户执行查询、重置、分页、新增、编辑、删除品牌或上传 Logo
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌

### Requirement: 品牌 Logo 上传进度反馈

Web 客户端 MUST 修复 `/admin/brands` 编辑品牌弹窗 Logo 更换流程中的上传反馈缺陷。用户选择新 Logo 后，系统 MUST 立即触发上传，MUST 在弹窗内展示上传进度条、百分比或等价可感知反馈，并 MUST 在上传成功后更新 Logo 预览与待保存的 `logo_object_key`。上传失败时 MUST 提供明确错误和重试入口。该修复 MUST 保持品牌管理既有功能、权限边界和 Design System 约束。

#### Scenario: 选择 Logo 后触发上传

- **GIVEN** `admin` 或 `employee` 已打开品牌编辑弹窗
- **WHEN** 用户点击「更换 Logo」并选择 JPG、PNG 或 WebP 图片
- **THEN** Web 客户端 MUST 立即触发品牌 Logo 上传流程
- **AND** 上传请求 MUST 使用既有后端授权上传接口
- **AND** MUST NOT 要求用户先保存品牌后才开始上传文件

#### Scenario: 上传过程中展示进度反馈

- **GIVEN** 用户已选择 Logo 图片
- **WHEN** 上传正在进行
- **THEN** 弹窗内 MUST 展示进度条、百分比或等价可感知上传反馈
- **AND** 进度反馈 MUST 位于 Logo 控件附近
- **AND** 上传过程中「更换 Logo」入口 SHOULD 展示上传中状态或被禁用，避免重复触发

#### Scenario: 上传成功后更新预览和保存对象 Key

- **GIVEN** 品牌 Logo 上传接口返回成功
- **WHEN** 响应包含新的 `object_key` 和可访问 URL
- **THEN** 弹窗中的 Logo 预览 MUST 更新为新图片
- **AND** 后续保存品牌时 MUST 使用新的 `logo_object_key`
- **AND** 保存后再次打开编辑弹窗 MUST 回显最新 Logo

#### Scenario: 上传失败可见且可重试

- **GIVEN** Logo 上传接口返回失败、网络异常或文件类型不合法
- **WHEN** 上传流程结束
- **THEN** 弹窗内 MUST 展示明确错误信息
- **AND** 用户 MUST 可以重新选择图片重试
- **AND** 失败时 MUST NOT 将旧 Logo 静默替换为无效预览或错误对象 Key

#### Scenario: 同一文件可重新选择

- **GIVEN** 用户已选择过某个 Logo 文件
- **WHEN** 用户再次选择同一个文件
- **THEN** Web 客户端 SHOULD 能再次触发上传或明确提示当前文件已选择
- **AND** 文件 input MUST NOT 因 value 未重置导致用户无法重试

#### Scenario: 品牌管理功能不回退

- **WHEN** 用户执行查询、重置、分页、每页显示切换、新增、编辑、启用、停用或删除品牌
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌
- **AND** `store_owner` MUST NOT 访问管理端品牌维护能力

#### Scenario: Design System 约束

- **WHEN** 修复修改品牌编辑弹窗 Logo 上传控件
- **THEN** 进度条、按钮、错误文案和预览态 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式
- **AND** MUST NOT 新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式

### Requirement: 管理端瓷砖品牌管理页

Web 客户端 MUST 提供瓷砖品牌管理页，路由为 `/admin/brands`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html` 与 `brand-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 品牌页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖品牌」、说明、「＋ 新增品牌」）
- **AND** MUST 展示 4 指标卡、筛选区、品牌表格与分页
- **AND** MUST NOT 展示导出按钮、批量操作、「品牌列表」「品牌检索」标题行

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页 MUST 支持跳页与每页显示数 20/50/100；切换 page_size MUST 重置页码为 1 并保留筛选条件

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** 「删除」MUST 可点击（风险色）
- **WHEN** 其他情况
- **THEN** 「删除」MUST 置灰且 hover 提示「仅允许删除未关联SKU且已停用的品牌」

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增品牌」或行内「编辑」
- **THEN** MUST 打开宽 720px 弹窗，`max-height: calc(100vh - 96px)`，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：名称+排序、简称+英文名、Logo、介绍（Logo 与介绍通栏同宽）
- **AND** MUST NOT 展示状态字段、创建默认状态提示、字段规则说明区块、国家/地区
- **AND** 品牌名称与排序 MUST 必填；排序 MUST 仅允许正整数

#### Scenario: 品牌管理 CSS Port

- **WHEN** 开发者查看品牌管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/brand-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/brands`
- **THEN** 前端 MUST 跳转至 `/admin/login`

### Requirement: SKU 弹窗内容溢出与滚动修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的内容溢出缺陷：当表单内容高度超过视口允许的最大弹窗高度时，弹窗 MUST 保持页眉与页脚固定可见，且主体内容区 MUST 提供垂直滚动以访问全部字段与操作按钮。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: 矮视口下弹窗主体可滚动

- **WHEN** 已登录 `admin` 或 `employee` 在视口高度 ≤900px 时打开「新增SKU」或「编辑SKU」弹窗
- **THEN** 弹窗 `.modal-body`（或等价内容 wrapper）MUST 支持垂直滚动
- **AND** 用户 MUST 能滚动至 SKU 图片、SKU 视频与备注说明字段

#### Scenario: 页眉页脚固定可见

- **WHEN** 弹窗内容超出可视高度且用户滚动主体区域
- **THEN** 标题、副标题与关闭按钮 MUST 保持可见
- **AND** 「取消 / 保存草稿 / 创建SKU（或保存）」footer MUST 保持可见且可点击

#### Scenario: 弹窗尺寸约束不变

- **WHEN** 用户打开 SKU 弹窗
- **THEN** 弹窗宽度 MUST 仍为 880px（`max-width: 100%` 响应式除外）
- **AND** 弹窗 `max-height` MUST NOT 超过视口（如 `calc(100vh - 64px)`）

#### Scenario: 关闭交互不回退

- **WHEN** 用户在弹窗内滚动
- **THEN** ESC、点击遮罩、点击 × MUST 仍可正常关闭弹窗
- **AND** MUST NOT 因滚动导致意外关闭

#### Scenario: SKU 表单功能保持可用

- **WHEN** 用户在修复后的弹窗中填写并保存
- **THEN** 保存草稿、创建 SKU、编辑更新、图片/视频上传 MUST 继续可用
- **AND** MUST NOT 变更 API 请求参数或响应结构

### Requirement: SKU 列表分页与表格结构 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 瓷砖 SKU 列表页的分页与表格卡片结构 UI 一致性缺陷：列表底部分页 MUST 与用户管理页分页保持相同的 DOM 结构与视觉语言；表格卡片内 MUST NOT 出现与页面级标题重复的二级标题行（如「SKU 列表」）。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: SKU 列表分页对齐用户管理页

- **WHEN** 已登录 `admin` 或 `employee` 分别访问「瓷砖 SKU」与「用户管理」列表页
- **THEN** 两个页面底部分页区域 MUST 使用相同 DOM 结构：`page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- **AND** 布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 视觉一致

#### Scenario: SKU 分页 MUST NOT 使用废弃 brand 局部结构

- **WHEN** 用户查看 SKU 列表底部分页
- **THEN** MUST NOT 出现 `page-left` 或 `brand-pagination-right` 类名/结构
- **AND** 总数摘要 MUST 独立于翻页按钮组（`page-summary`）

#### Scenario: 表格卡片内无重复标题行

- **WHEN** 用户访问 SKU 列表页
- **THEN** `table-card` 内 MUST NOT 渲染 `table-head`、`table-title`「SKU 列表」或等价卡片内二级标题
- **AND** 表格 MUST 直接以 `<table>` 表头开始（与用户管理页一致）

#### Scenario: SKU 列表分页功能不回退

- **WHEN** 用户在 SKU 列表页切换页码或修改每页条数（10 / 20 / 50 / 100）
- **THEN** 列表 MUST 正确刷新，`total` 与当前筛选结果一致
- **AND** 切换每页条数后 page=1，筛选条件 MUST 保留

#### Scenario: SKU 列表 CRUD 与筛选保持可用

- **WHEN** 用户执行查询、重置、新增 SKU、编辑、上下架或删除
- **THEN** 原有功能 MUST 继续可用
- **AND** MUST NOT 变更 API 请求参数或响应结构

### Requirement: 管理端 Sidebar 展开/收起

Web 客户端 MUST 在管理端 `AdminLayout` 包裹的全部 `/admin/*`  authenticated 页面支持 Sidebar **expanded** 与 **collapsed** 两种状态。状态 MUST 由 `AdminLayout`（或等价 Context）统一管理并传入 `AdminSidebar`；首次访问 MUST 默认为 **expanded**。用户切换后 MUST 将偏好写入 `localStorage`（key：`admin-sidebar-collapsed`）；刷新或路由切换后 MUST 恢复一致。折叠交互 MUST 仅在视口宽度 **>1023px** 生效；≤1023px MUST 沿用现有 responsive 布局且 MUST NOT 展示或 MUST 禁用折叠 chevron。MUST NOT 变更店主端 `Sidebar` 筛选栏。切换 Sidebar 状态 MUST NOT 改变 nav 路由行为、卸载当前页面或丢失 `AdminLayout` 内 notice 等局部 UI 状态。

#### Scenario: 状态持久化

- **WHEN** 用户在桌面端收起 Sidebar 并刷新页面或导航至其他 `/admin/*` 路由
- **THEN** Sidebar MUST 保持 collapsed
- **AND** `localStorage['admin-sidebar-collapsed']` MUST 反映该偏好

#### Scenario: 默认 expanded

- **WHEN** 用户首次访问且无 localStorage 记录
- **THEN** Sidebar MUST 为 expanded（264px）

#### Scenario: 移动端不启用折叠

- **WHEN** 视口宽度 ≤1023px
- **THEN** MUST NOT 与桌面 collapsed 72px 模型冲突
- **AND** 折叠 chevron MUST 隐藏或禁用

#### Scenario: 导航行为无回归

- **WHEN** 用户在 collapsed 态点击 nav 项
- **THEN** MUST 与 expanded 态相同执行 `navigate` 或 placeholder 逻辑

#### Scenario: 自动化测试

- **WHEN** 运行 vitest 覆盖 AdminLayout 或 AdminSidebar
- **THEN** MUST 断言 chevron 切换 `data-sidebar-state` 或等价 class
- **AND** MUST 断言 `aria-expanded` 与 localStorage 读写

### Requirement: 产品版本常量与 Web 端展示

Web 客户端 MUST 在 `src/shared/` 维护单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端 MUST 引用同一导出。产品版本 MUST 由发版时人工更新该常量；MUST NOT 从 `package.json`、`pyproject.toml`、FastAPI `version` 或 CI/Git 构建信息读取。Web 客户端 MUST NOT 在登录页、页脚或关于页展示产品版本（本期 Out）。Web 客户端 MUST NOT 展示 API / OpenAPI / 后端版本号作为产品版本。

#### Scenario: 单一事实源

- **WHEN** 开发者查看产品版本定义
- **THEN** MUST 存在且仅存在一处 `src/shared/` 产品版本常量导出
- **AND** 管理端 `AdminSidebar` 与店主端 `Sidebar` MUST import 同一常量

#### Scenario: 禁止自动版本源

- **WHEN** 实现读取展示用版本号
- **THEN** MUST NOT 使用 npm package version、FastAPI app version 或 git sha 作为 `PRODUCT_VERSION` 展示值

### Requirement: 店主端侧边栏产品版本展示

店主端使用筛选侧栏的页面（如经 `LandingPage`、`ListPage` 与 `CatalogBody` 渲染的模板）MUST 在 `Sidebar` **最上方**（第一个筛选 section 之上）展示品牌名与产品版本 pill。布局语义 MUST 与管理端一致：品牌名左、版本 pill 紧邻右侧；版本值 MUST 等于 `PRODUCT_VERSION`。版本 MUST 在侧栏内展示；MUST NOT 仅在顶栏 `SiteNav` 展示而侧栏缺失。

#### Scenario: 店主端侧栏顶部版本

- **WHEN** 用户访问店主端带侧栏页面（如首页或目录列表）
- **THEN** 侧栏最上方 MUST 可见品牌名（默认 STONEX 或 DS 等价）与版本 pill
- **AND** pill 文案 MUST 等于 `PRODUCT_VERSION`

#### Scenario: 筛选区无回归

- **WHEN** 用户查看店主端侧栏筛选 checkbox 区
- **THEN** 筛选 section 标题与选项 MUST 正常展示
- **AND** brand-head MUST NOT 挤压或遮挡筛选交互

#### Scenario: 店主端版本 pill 样式

- **WHEN** 开发者查看店主端版本 pill 实现
- **THEN** MUST 复用与管理端相同的 badge 组件或等价 semantic token 类
- **AND** TSX MUST NOT 包含裸 Hex

### Requirement: 产品版本 pill 视觉一致性修复（Web 客户端）

Web 客户端 MUST 修复跨端产品版本 pill 的视觉一致性缺陷（BUG-0013）：管理端与店主端 MUST 共用同一 badge 组件或 variant，pill 样式 MUST 对齐 REQ-0010 原型与 `rules/ui-design.md` §8。pill MUST 含 `padding: 2px 7px` 等价、`font-weight: 500`、`tracking-badge`（或 prototype 0.04em）；MUST 使用 semantic token，MUST NOT 含裸 Hex。Vitest MUST 断言渲染的版本元素含 pill 关键 class（如边框与 muted 文字），不仅断言版本字符串。修复 MUST NOT 变更 `PRODUCT_VERSION` 单一事实源、登录页/页脚版本展示策略或 API。

#### Scenario: 跨端 badge 组件复用

- **WHEN** 开发者查看管理端 `AdminSidebar` 与店主端 `Sidebar` brand-head 实现
- **THEN** 两端 MUST 使用同一 `ProductVersionBadge`（或 `Badge` version variant）实现
- **AND** MUST NOT 在两端分别维护 divergent ad-hoc pill 样式

#### Scenario: 店主端 pill 与管理端视觉一致

- **WHEN** 用户访问店主端带侧栏页面（如 `LandingPage` / `ListPage`）
- **THEN** 侧栏顶部版本 pill MUST 与管理端 pill 视觉一致
- **AND** 版本值 MUST 仍等于 `PRODUCT_VERSION`

#### Scenario: 店主端原型并排验收

- **WHEN** 开发者在 1280×1024 下将店主端与 `product-version-sidebar-catalog.html` 并排对比
- **THEN** brand-head 内版本 pill MUST 与原型语义一致
- **AND** 筛选 section MUST 无回归

#### Scenario: Vitest 样式断言

- **WHEN** 运行 `cd src/web && pnpm test` 中与版本 badge 相关用例
- **THEN** 测试 MUST 断言 pill 元素含边框与 muted 文字等关键 class
- **AND** MUST 继续 import `PRODUCT_VERSION` 断言文案，MUST NOT duplicate 硬编码版本字符串

### Requirement: SKU 弹窗副标题 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）副标题与品牌新增弹窗的 UI 不一致问题：副标题 MUST 使用与管理端共享的 `.modal-desc` 样式（12px、`var(--admin-weak)`、上间距 8px）；弹窗头部 MUST 支持标题 + 副标题自适应高度。修复 MUST NOT 修改 SKU API、数据库、Orval 或 BUG-0011 弹窗滚动布局。

#### Scenario: SKU 弹窗使用共享 modal-desc

- **WHEN** 用户打开 SKU 新增或编辑弹窗
- **THEN** 标题下方副标题 MUST 使用 class `modal-desc`
- **AND** MUST NOT 使用未定义样式的 `modal-subtitle`

#### Scenario: 副标题 Typography 与品牌弹窗一致

- **WHEN** 并排对比 SKU 与品牌新增弹窗
- **THEN** 两弹窗副标题字号、颜色、行高与标题间距 MUST 视觉一致

#### Scenario: 弹窗头部自适应副标题

- **WHEN** 弹窗标题区包含副标题
- **THEN** `.modal-head` MUST 使用 `min-height: 64px` 与 `height: auto`
- **AND** 副标题 MUST 完整可见

#### Scenario: AC-023 副标题语义保留

- **WHEN** 用户阅读 SKU 新增弹窗副标题
- **THEN** 文案 MUST 说明弹窗内不提供状态选择

#### Scenario: 弹窗滚动与表单不回退

- **WHEN** 副标题修复合并后
- **THEN** BUG-0011 矮视口滚动与 BUG-0012 字段规则 MUST 保持可用

### Requirement: SKU 弹窗表单字段规则修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的表单字段规则，对齐 UAT 产品决策（[BUG-0012](issues/bugs/BUG-0012-tile-sku-modal-form-field-rules/)）：**表面工艺非必填**、**参考价格（元）必填且新建默认 0**。修复 MUST 同步前后端校验，且 MUST NOT 回退 BUG-0011 弹窗滚动布局或 BUG-0009 列表 UI。

#### Scenario: 表面工艺非必填

- **WHEN** 用户打开新增或编辑 SKU 弹窗
- **THEN** 「表面工艺」Label MUST NOT 显示必填星号
- **AND** 留空表面工艺、填齐其它必填项后点击「创建 SKU」或「保存」 MUST 成功提交

#### Scenario: 参考价格必填且新建默认零

- **WHEN** 用户打开「新增 SKU」弹窗
- **THEN** 「参考价格（元）」输入框 MUST 默认值为 `0`
- **AND** Label MUST 显示必填星号
- **AND** Label 文案 MUST 仍为「参考价格（元）」

#### Scenario: 参考价格空值被拦截

- **WHEN** 用户清空参考价格并尝试创建或保存
- **THEN** 前端 MUST 展示校验错误且不关闭弹窗
- **AND** MUST NOT 向 API 发送 `reference_price: null`

#### Scenario: 参考价格零元列表展示

- **WHEN** SKU 保存后 `reference_price` 为 `0`
- **THEN** 列表「参考价格」列 MUST 显示 `¥ 0.00`
- **AND** MUST NOT 显示「—」

#### Scenario: 弹窗布局与滚动不回退

- **WHEN** 修复完成后在矮视口打开 SKU 弹窗
- **THEN** 880px 宽度、主体可滚动、头尾固定 MUST 仍满足 BUG-0011 验收

#### Scenario: Orval 类型同步

- **WHEN** 后端 OpenAPI 更新 reference_price 必填语义
- **THEN** 团队 MUST 运行 `./scripts/generate-openapi-client.sh` 并提交生成客户端

### Requirement: 管理端瓷砖 SKU 管理页

Web 客户端 MUST 提供瓷砖 SKU 管理页，路由为 `/admin/tile-skus`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `tile-sku-create-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1120px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: SKU 页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-skus`
- **THEN** 页面 MUST 展示 page-head（eyebrow「OPERATIONS / SKU」、标题「瓷砖SKU」、说明、「＋ 新增SKU」）
- **AND** MUST 展示 4 指标卡（SKU总数/已上架/待完善/草稿）、五维筛选区、SKU 表格与分页

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择筛选项并点击查询或回车
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」
- **AND** 分页 MUST 支持页码与每页 10/20/50/100 条；默认 20；切换 page_size MUST 重置页码为 1

#### Scenario: 列表列与价格格式

- **WHEN** 用户查看 SKU 表格
- **THEN** 列 MUST 包含：SKU信息、品牌/类目、规格/工艺、参考价格、素材、状态、更新时间、操作
- **AND** 参考价格 MUST 格式化为 `¥ 268.00` 样式（两位小数）

#### Scenario: 列表行上下架操作

- **WHEN** 列表行 `status` 为 `PUBLISHED`
- **THEN** 操作列 MUST 展示「编辑」与「下架」
- **AND** 「删除」MUST 展示但置灰，并提示已上架不可删
- **WHEN** 列表行 `status` 为 `DISABLED`（已下架）
- **THEN** 操作列 MUST 展示「编辑」与「恢复」（或等价「上架」文案）
- **AND** 点击 MUST 调用 `POST /api/v1/admin/tile-skus/{id}/publish` 并刷新列表
- **WHEN** 列表行 `status` 为 `DRAFT` 或 `NEEDS_COMPLETION`
- **THEN** 操作列 MUST 展示「编辑」与「上架」
- **AND** publish 按钮 MUST NOT 因 `canDeleteTileSku` 或 delete 按钮状态而被隐藏

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增SKU」或行内「编辑」
- **THEN** MUST 打开宽 880px 弹窗，遮罩半透明，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：SKU名称、SKU编码、所属品牌、所属类目、规格尺寸、表面工艺、主色系、参考价格（元）、SKU图片、SKU视频、备注说明
- **AND** MUST NOT 展示状态字段
- **AND** 标题 MUST 含「创建后默认草稿」提示
- **AND** 底部 MUST 为：取消、保存草稿、创建SKU

#### Scenario: 多图主图与多视频

- **WHEN** 用户在弹窗管理素材
- **THEN** MUST 支持多张图片缩略图网格、主图标签与「设为主图」
- **AND** MUST 支持多个视频文件卡片（名称、大小、删除、继续添加）
- **AND** 视频 MUST NOT 为必填

#### Scenario: 保存草稿与创建 SKU

- **WHEN** 用户点击「保存草稿」
- **THEN** MUST 以宽松校验提交（至少 SKU 名称）
- **WHEN** 用户点击「创建SKU」
- **THEN** MUST 校验全部必填项；成功 Toast「SKU创建成功，已保存为草稿」

#### Scenario: SKU 管理 CSS Port

- **WHEN** 开发者查看 SKU 管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-sku-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-skus`
- **THEN** 前端 MUST 跳转至 `/admin/login`

### Requirement: 管理端列表页操作反馈 Toast 布局统一

Web 客户端 MUST 在管理端以下四个列表页对「操作成功/失败且约 3.2 秒后自动消失」的全局反馈使用固定位置 toast（`.admin-toast-region` + `.admin-toast` 或等价共享组件），MUST NOT 在 `page-hero` 或主体内容上方插入文档流 `.admin-notice` 占位节点。toast 样式 MUST 来自管理端共享样式（如 `admin-home.css`），四页视觉与行为 MUST 一致。弹窗内 inline 表单错误 MAY 继续使用 inline 错误文案；`AdminLayout` 侧栏占位 notice 不在本 requirement 范围。修复 MUST NOT 回归品牌 Logo 展示、上传进度及四页 CRUD、筛选、分页、权限边界。

涵盖路由：

- `/admin/brands`（瓷砖品牌）
- `/admin/users`（用户管理）
- `/admin/tile-categories`（瓷砖类目）
- `/admin/tile-skus`（瓷砖 SKU）

#### Scenario: 用户管理列表操作反馈不推挤页面

- **WHEN** `admin` 在 `/admin/users` 执行冻结、解冻、删除、重置密码、新建/编辑用户成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 改变 page-hero、指标卡、筛选区、表格或分页的纵向位置
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖类目列表操作反馈不推挤页面

- **WHEN** `admin` 或 `employee` 在 `/admin/tile-categories` 执行启用、停用、删除、保存类目成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 推挤 page-hero、筛选区、表格或分页
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖 SKU 列表操作反馈不推挤页面

- **WHEN** `admin` 或 `employee` 在 `/admin/tile-skus` 执行上架、下架、删除、保存 SKU 成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 推挤 page-hero、指标卡、筛选区、表格或分页
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖品牌列表 toast 共享实现且不回归

- **WHEN** `admin` 或 `employee` 在 `/admin/brands` 执行启用、停用、删除、保存品牌或加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 继续使用 fixed toast，行为与 BUG-0003 / `fix-brand-image-display-layout-shift` 验收一致
- **AND** toast 样式 MUST 来自管理端共享样式，MUST NOT 仅私有于 `brand-management.css`
- **AND** 品牌 Logo 展示、上传进度、启停确认弹窗 MUST NOT 回归

#### Scenario: 四页 toast 视觉与行为一致

- **WHEN** 对比四页成功 toast（如「品牌已启用」「用户已冻结」「类目已启用」「SKU 已上架」）
- **THEN** 位置、圆角、边框、背景、字号、阴影 MUST 一致
- **AND** 自动消失时长 MUST 为 3200ms
- **AND** MUST 保留 `aria-live="polite"` 与 `role="status"` 可访问性语义

#### Scenario: Design System 约束

- **WHEN** 修复修改 Web UI 样式
- **THEN** MUST 使用既有管理端 CSS 变量与 semantic token
- **AND** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的提示样式

### Requirement: 用户列表状态变更二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「冻结」「解冻」与「删除」操作提供二次确认，以降低误触风险。冻结/解冻确认 MUST 复用与同项目类目/品牌启停确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。删除确认 MUST 使用与同页/类目/品牌删除一致的 modal 结构，MUST NOT 使用 `window.confirm`。用户点击「冻结」「解冻」或「删除」时 MUST NOT 直接调用 status API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。重置密码 confirm 见「用户重置密码二次确认」requirement。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 冻结须先确认

- **WHEN** `admin` 在用户列表行点击「冻结」
- **THEN** MUST 展示冻结确认弹窗，MUST NOT 直接调用 `PATCH /api/v1/admin/users/{id}/status`
- **AND** 弹窗标题 MUST 为「冻结用户」或等价文案
- **AND** 正文 MUST 含用户名及冻结后果（如禁止登录）

#### Scenario: 解冻须先确认

- **WHEN** `admin` 在用户列表行点击「解冻」
- **THEN** MUST 展示解冻确认弹窗，MUST NOT 直接调用 status API
- **AND** 正文 MUST 含用户名

#### Scenario: 删除须使用 DS modal

- **WHEN** `admin` 对可删除用户点击「删除」
- **THEN** MUST 展示删除确认 modal，MUST NOT 使用 `window.confirm`
- **AND** 正文 MUST 含用户名及不可恢复提示

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 用户状态变更确认弹窗展示
- **THEN** 底部 MUST 含「取消」与确认主按钮（如「确认冻结」「确认解冻」「删除用户」）
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 API 或改变用户状态

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在冻结确认弹窗点击确认
- **THEN** MUST 调用 status API 将用户设为 `disabled` 并 Toast「用户已冻结」，刷新列表
- **WHEN** 用户在解冻确认弹窗点击确认
- **THEN** MUST 调用 status API 将用户设为 `active` 并 Toast「用户已恢复正常」，刷新列表
- **WHEN** 用户在删除确认弹窗点击确认
- **THEN** MUST 软删除用户并 Toast「用户已删除」，刷新列表

#### Scenario: 无障碍与样式

- **WHEN** 用户状态变更确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 user-management CSS

#### Scenario: 用户管理其他能力不回退

- **WHEN** `admin` 执行查询、分页、新建/编辑用户或重置密码
- **THEN** 既有功能 MUST 保持可用
- **AND** 仅 `admin` MUST 可访问用户管理写操作

### Requirement: SKU 列表上下架二次确认

Web 客户端 MUST 在 `/admin/tile-skus` 瓷砖 SKU 列表页为行内「上架」「下架」与「恢复」（或等价上架文案）操作提供二次确认。确认 MUST 复用与同页「删除 SKU」确认框相同的 modal 结构。用户点击上述操作时 MUST NOT 直接调用 publish/unpublish API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。本能力 MUST NOT 修改 SKU API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 下架须先确认

- **WHEN** `admin` 或 `employee` 在已上架 SKU 行点击「下架」
- **THEN** MUST 展示下架确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/tile-skus/{id}/unpublish`
- **AND** 正文 MUST 含 SKU 名称

#### Scenario: 上架或恢复须先确认

- **WHEN** 用户在草稿/待完善/已停用 SKU 行点击「上架」或「恢复」
- **THEN** MUST 展示上架确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/tile-skus/{id}/publish`
- **AND** 正文 MUST 含 SKU 名称

#### Scenario: SKU 上下架确认弹窗按钮与取消

- **WHEN** SKU 上下架确认弹窗展示
- **THEN** 底部 MUST 含「取消」与确认主按钮
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 publish/unpublish API

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在下架确认弹窗点击确认
- **THEN** MUST 调用 unpublish API 并 Toast「SKU 已下架」，刷新列表
- **WHEN** 用户在上架/恢复确认弹窗点击确认
- **THEN** MUST 调用 publish API 并 Toast「SKU 已上架」（或等价），刷新列表

#### Scenario: SKU 删除确认独立

- **WHEN** 用户点击行内「删除」
- **THEN** MUST 仍使用独立「删除 SKU」确认弹窗
- **AND** 上下架 confirm state MUST NOT 与删除 confirm state 共用

#### Scenario: SKU 管理其他能力不回退

- **WHEN** 用户执行查询、分页、新增/编辑 SKU 或删除 SKU
- **THEN** 既有功能 MUST 保持可用
- **AND** BUG-0011 弹窗滚动、BUG-0014 恢复按钮可见性 MUST NOT 回归

### Requirement: 用户重置密码二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「重置密码」操作提供二次确认。确认 MUST 复用与同项目类目/品牌启停及同页冻结确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「重置密码」时 MUST NOT 使用 `window.confirm`；MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。确认成功后 MUST 继续打开既有结果弹窗展示一次性随机密码（REQ-0005 AC-022）。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 重置密码须先确认

- **WHEN** `admin` 在用户列表行点击「重置密码」
- **THEN** MUST 展示重置密码确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`
- **AND** MUST NOT 调用 `window.confirm`
- **AND** 弹窗标题 MUST 为「重置密码」或等价文案
- **AND** 正文 MUST 含用户名及重置后果（如将生成新随机密码）

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 重置密码确认弹窗展示
- **THEN** 底部 MUST 含「取消」与主按钮「确认重置」（或等价）
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 reset-password API
- **AND** MUST NOT 打开结果密码展示弹窗

#### Scenario: 确认后调用 API 并展示结果

- **WHEN** 用户在重置密码确认弹窗点击「确认重置」
- **THEN** MUST 调用 reset-password API
- **AND** MUST Toast「密码已重置」（或等价）
- **AND** MUST 打开结果弹窗展示一次性密码与复制按钮
- **AND** 关闭结果弹窗后 MUST NOT 再次展示同一密码

#### Scenario: 无障碍与样式

- **WHEN** 重置密码确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** 正文 MUST 使用 `page-desc`（或等价 semantic class）
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 user-management CSS

#### Scenario: 用户管理其他 confirm 不回退

- **WHEN** 本修复已合并
- **THEN** 同页冻结/解冻/删除 confirm MUST 保持 BUG-0016 行为
- **AND** 品牌/类目启停 confirm MUST NOT 回归

### Requirement: Docker Web 反代必须允许大文件上传

Docker Compose 部署的 Web 容器（Nginx 反代 `/api/` 至 backend）MUST 配置 `client_max_body_size` 不小于 `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`。当运营或部署人员调大 `.env` 中图片或视频上传上限时，MUST 同步提高 Nginx `client_max_body_size` 并重建 Web 镜像，否则大文件上传 MAY 在代理层失败并返回 413。

#### Scenario: Nginx body 限制与 env 对齐

- **GIVEN** 根目录 `.env` 中 `MAX_VIDEO_SIZE_MB=500` 且 `MAX_IMAGE_SIZE_MB=20`
- **WHEN** 检查 `src/web/nginx.conf` 随本 change 部署后的配置
- **THEN** `client_max_body_size` MUST ≥ 500MB（或项目文档声明的等价值）
- **AND** `docs/standards/file-upload.md` MUST 说明该对齐关系

#### Scenario: 重建 Web 镜像后大文件上传可用

- **GIVEN** 已修改 `nginx.conf` 并完成 Web 镜像重建与容器重启
- **WHEN** 用户经 `localhost:3000` 上传大于 1MB 的合法 MP4
- **THEN** 请求 MUST 到达后端 FastAPI
- **AND** 成功时 MUST 返回 JSON 统一响应结构（非 Nginx 默认 HTML 413 页）

### Requirement: SKU 弹窗商品视频上传状态与即时回显修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）「商品视频」区块的上传反馈缺陷。用户选择 MP4 后，系统 MUST 立即触发授权上传，MUST 在视频区内展示 `idle → uploading → uploaded / failed` 状态与可感知进度或等价文案，MUST 在上传成功后 **同一弹窗会话内** 立即追加文件卡片（`.sku-video-card` 或等价）展示文件名与大小，MUST 在上传失败时在视频区内展示明确错误。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略；MUST NOT 回归 BUG-0011 弹窗主体滚动能力。

#### Scenario: 选择 MP4 后立即触发上传

- **GIVEN** `admin` 或 `employee` 已打开 SKU 新增或编辑弹窗并位于「商品视频」区块
- **WHEN** 用户点击「上传视频」并选择合法 MP4
- **THEN** Web 客户端 MUST 立即触发 `POST /api/v1/admin/uploads/tile-videos`
- **AND** MUST NOT 要求用户先保存 SKU 后才开始上传

#### Scenario: 上传过程中展示可感知状态

- **GIVEN** 用户已选择 MP4 文件
- **WHEN** 上传正在进行
- **THEN** 「商品视频」区块 MUST 展示上传中状态（进度条、百分比或等价文案）
- **AND** 状态 MUST 经过 `idle → uploading → uploaded / failed`
- **AND** 上传中 SHOULD 禁用「上传视频」重复触发
- **AND** 上传中 MUST 禁止提交保存（对齐 `BrandFormModal` Logo 行为）

#### Scenario: 上传成功后即时回显视频预览

- **GIVEN** 视频上传接口返回 200 且含有效 `object_key` 与可访问 `url`
- **WHEN** 上传完成且用户未关闭弹窗
- **THEN** 「商品视频」区块 MUST 立即出现视频卡片，含 **16:9 视频预览/播放器**（`<video>`，`preload="metadata"`，`controls`）
- **AND** 卡片 MUST 展示文件名与大小（或占位「—」）
- **AND** 卡片 MUST 提供「移除」入口
- **AND** 区域 SHOULD 展示简短成功提示（如「视频已添加」）

#### Scenario: 上传失败在视频区内可见且可重试

- **GIVEN** 上传失败、网络异常或非 MP4 文件
- **WHEN** 上传流程结束
- **THEN** 「商品视频」区块 MUST 进入 `failed` 状态并展示明确错误信息
- **AND** MUST NOT 仅依赖弹窗顶部 notice 作为唯一反馈
- **AND** 用户 MUST 可重新选择文件重试

#### Scenario: 支持继续添加多个视频

- **GIVEN** 已有一个视频文件卡片
- **WHEN** 用户再次上传另一个 MP4 并成功
- **THEN** 新卡片 MUST 追加到列表
- **AND** 先前卡片 MUST 保留

#### Scenario: SKU 弹窗滚动与图片能力不回退

- **WHEN** 用户在使用修复后的 SKU 弹窗
- **THEN** `.modal-body` 垂直滚动 MUST 仍可用（BUG-0011）
- **AND** SKU 图片上传与主图逻辑 MUST 无回归
- **AND** MUST NOT 变更 API 请求参数或响应结构

#### Scenario: Design System 约束

- **WHEN** 修复修改 SKU 弹窗视频上传控件
- **THEN** 进度条、按钮禁用态、错误与成功文案 MUST 使用 semantic token 或既有管理端样式
- **AND** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部色值

