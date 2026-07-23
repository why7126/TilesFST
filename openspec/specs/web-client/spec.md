# Web 客户端规范

## Purpose
定义 Web 管理端与店主端的登录、路由守卫、管理端页面、列表弹窗交互、上传体验、品牌展示和 Docker Web 反代等客户端能力要求。
## Requirements
### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html` 的布局与 CSS Port 策略（最高优先级视觉结构），并 MUST 满足 `issues/requirements/archive/REQ-0002-product-brand-login-simplify` 与 `issues/requirements/archive/REQ-0003-login-left-panel-refine` 的要求。实现 MUST 采用 **CSS Port 策略**：自 `user-login.html` port 专用 stylesheet（`features/auth/styles/login-page.css`），React 负责 DOM 结构与 auth 交互。左栏金色 Logo（`.logo`）MUST 为 **TilesFST**；左栏白色主标题（`.brand-title`）MUST 为 **「瓷砖信息管理后台」**。颜色 MUST 引用 `globals.css` 的 `--color-*` token；TSX MUST NOT 含裸 Hex。密码字段 MUST 按 `issues/requirements/archive/REQ-0003-login-remember-autofill/prototype/web/login-form-enhancements-context.md` 提供显隐切换控件。登录页辅助工具区 MUST 统一承载主题选择模块与语言选择模块，两个模块 MUST 在桌面和窄屏视口下保持清晰对齐且不得遮挡登录内容。

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

#### Scenario: 登录页辅助工具区对齐

- **WHEN** 用户查看 Web 管理端登录页
- **THEN** 主题选择模块与语言选择模块 MUST 使用统一的登录页工具区布局或等价对齐规则
- **AND** 两个模块的垂直对齐、控件高度、视觉重心和交互热区 MUST 保持一致
- **AND** 桌面视口下两个模块之间的水平间距 MUST 稳定，右上角工具区 MUST NOT 重叠、裁切或异常换行
- **AND** 窄屏视口下两个模块 MUST 保持可见且布局稳定，MUST NOT 遮挡登录标题、表单字段或安全提示。

#### Scenario: 登录页辅助工具区行为不回退

- **WHEN** 修复登录页辅助工具区对齐后
- **THEN** 主题选择控件 MUST 仍可切换现有主题模式
- **AND** 语言选择按钮 MUST 保持文案「简体中文⌄」与可访问名称 `切换语言`
- **AND** 登录表单提交、记住登录状态、登录成功跳转和认证错误提示 MUST 保持不变
- **AND** 修复 MUST NOT 要求新增完整 i18n 能力、主题模式、认证 API 字段或数据库结构。

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
- **AND** MUST 指向 `issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html` 作为最高优先级视觉源

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

前端 MUST 根据用户角色限制管理端访问。用户管理路由 `/admin/users` 与 SYSTEM 分组「用户管理」菜单 MUST 仅对 `role=admin` 可见且可访问。系统设置路由 `/admin/settings` 及其子路径与 SYSTEM 分组「系统设置」菜单 MUST 仅对 `role=admin` 可见且可访问。`employee` MUST 可访问其他管理端页面（如 `/admin/dashboard`）但 MUST NOT 访问用户管理与系统设置。

#### Scenario: 店主角色拒绝管理端

- **WHEN** 角色为 `store_owner` 的用户登录成功
- **THEN** 前端 MUST NOT 进入管理端受保护页面
- **AND** MUST 展示无权限提示或跳转无权限页

#### Scenario: 运营人员不可访问用户管理

- **WHEN** 角色为 `employee` 的用户已登录
- **THEN** Sidebar MUST NOT 展示「用户管理」菜单项
- **AND** 直接访问 `/admin/users` MUST 展示无权限提示或重定向至 `/admin/dashboard`

#### Scenario: 运营人员不可访问系统设置

- **WHEN** 角色为 `employee` 的用户已登录
- **THEN** Sidebar MUST NOT 展示「系统设置」菜单项
- **AND** 直接访问 `/admin/settings/basic` MUST 展示无权限提示或重定向 forbidden

#### Scenario: 管理员可访问用户管理

- **WHEN** 角色为 `admin` 的用户已登录
- **THEN** Sidebar MUST 展示「用户管理」且可导航至 `/admin/users`
- **AND** 页面 MUST 正常加载用户列表

#### Scenario: 管理员可访问系统设置

- **WHEN** 角色为 `admin` 的用户已登录
- **THEN** Sidebar MUST 展示「系统设置」且可导航至 `/admin/settings`
- **AND** 页面 MUST 正常加载系统设置 Shell

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

Web 客户端 MUST 提供瓷砖类目管理页，路由为 `/admin/tile-categories`，视觉 MUST 高保真对齐 **`REQ-0007-tile-category-management-refine`** 目录下 v2 context（相对 `REQ-0005-tile-category-management/prototype/web/tile-category-management.html` 的 CSS Port diff）与 `REQ-0067` 类目新增 / 编辑弹窗字段策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 类目页布局

- **WHEN** 用户访问 `/admin/tile-categories`
- **THEN** 页面 MUST 展示 page-header（eyebrow「CATEGORY MANAGEMENT」、标题「瓷砖类目管理」、说明、「＋ 新增类目」）
- **AND** MUST 展示 4 指标卡、类目检索区（**无**外层 section 标题）、左侧类目树（280px）与右侧类目列表（**无**外层「类目列表」section 标题）

#### Scenario: 类目树与列表联动

- **WHEN** 用户点击左侧类目树节点
- **THEN** 右侧类目列表 MUST 按节点及其子孙范围刷新

#### Scenario: 类目列表名称列第二行仅展示编码

- **WHEN** 管理端类目列表展示类目名称列
- **THEN** 名称列第一行 MUST 展示类目名称
- **AND** 名称列第二行 MUST 仅展示系统类目编码
- **AND** 名称列第二行 MUST NOT 展示层级路径，例如 `父级类目 / 二级类目`

#### Scenario: 新增类目弹窗字段

- **WHEN** 用户点击「新增类目」
- **THEN** 系统 MUST 打开新增类目弹窗
- **AND** 弹窗 MUST 展示带必填标识的「上级类目」「类目名称」「排序权重」
- **AND** 弹窗 MUST NOT 展示可填写的「类目编码」输入项
- **AND** 弹窗 MUST 提示类目编码由系统自动生成或等价弱提示

#### Scenario: 编辑类目弹窗字段

- **WHEN** 用户点击类目行「编辑」
- **THEN** 系统 MUST 打开编辑类目弹窗
- **AND** 弹窗 MUST NOT 提供可编辑的「类目编码」输入项
- **AND** 本期 MUST NOT 允许通过编辑弹窗修改上级类目

#### Scenario: 上级类目选择

- **WHEN** 用户在新增类目弹窗选择上级类目
- **THEN** 下拉项 MUST 包含「无上级，创建一级类目」或等价顶级选项
- **AND** 下拉项 MUST 仅包含可作为上级的一级类目
- **AND** 二级类目 MUST NOT 出现在上级类目可选项中

#### Scenario: 类目名称本地校验

- **WHEN** 用户提交空名称、超过 10 个用户可见字符的名称，或包含中文/英文/数字之外字符的名称
- **THEN** 前端 MUST 阻止保存
- **AND** 错误提示 MUST 展示在类目名称字段或字段组下方

#### Scenario: 排序权重本地校验

- **WHEN** 用户提交空值、0、负数、小数或非数字排序权重
- **THEN** 前端 MUST 阻止保存
- **AND** 错误提示 MUST 展示在排序权重字段或字段组下方

#### Scenario: 创建请求不包含编码

- **WHEN** 用户提交新增类目弹窗
- **THEN** 前端调用创建 API 的 payload MUST NOT 包含用户填写的 `code`
- **AND** 前端 MUST 使用 Orval 生成类型或等价生成客户端契约

#### Scenario: 服务端错误展示

- **WHEN** 创建或更新 API 返回统一错误 envelope
- **THEN** 前端 MUST 优先展示 `message`
- **AND** 字段级错误 SHOULD 映射到对应字段
- **AND** 无法映射字段的错误 MUST 展示在弹窗固定错误区域或等价表单错误区

#### Scenario: 保存成功刷新

- **WHEN** 类目创建或更新成功
- **THEN** 弹窗 MUST 关闭
- **AND** 类目树、类目列表和页面统计 MUST 刷新

#### Scenario: 类目弹窗横切质量

- **WHEN** 开发者实现或回归类目新增 / 编辑弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与专属类
- **AND** 1440px 视口下 computed width MUST 为 560px 或 design/tasks 中批准的宽度
- **AND** 矮视口下弹窗 body MUST 可滚动且 footer 操作按钮始终可达
- **AND** 实现 MUST 使用 Design System semantic token 或既有管理端样式，MUST NOT 新增裸 Hex

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

Web 客户端 MUST 提供瓷砖品牌管理页，路由为 `/admin/brands`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0005-brand-management/prototype/web/brand-management.html` 与 `brand-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: 品牌页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖品牌」、说明、「＋ 新增品牌」）
- **AND** MUST 展示 4 指标卡、筛选区、品牌表格与分页
- **AND** MUST NOT 展示导出按钮、批量操作、「品牌列表」「品牌检索」标题行
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过页面级 `.content-inner` max-width 退回 1080px。

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

Web 客户端 MUST 在 `src/shared/` 维护单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端 MUST 引用同一导出。产品版本 MUST 由发版时人工更新该常量；MUST NOT 从 `package.json`、`pyproject.toml`、FastAPI `version`、OpenAPI 版本、CI/Git 构建信息或其他自动版本源读取。Web 客户端 MUST NOT 在登录页、页脚或关于页展示产品版本（本期 Out）。Web 客户端 MUST NOT 展示 API / OpenAPI / 后端版本号作为产品版本。产品发布流程 MUST 校验 `src/shared/product-version.ts` 中的 `PRODUCT_VERSION` 与产品版本发布对象和公开发布公告版本一致；若一次发布不改变 `PRODUCT_VERSION`，发布材料 MUST 记录原因。

#### Scenario: 单一事实源

- **WHEN** 开发者查看产品版本定义
- **THEN** MUST 存在且仅存在一处 `src/shared/` 产品版本常量导出
- **AND** 管理端 `AdminSidebar` 与店主端 `Sidebar` MUST import 同一常量

#### Scenario: 禁止自动版本源

- **WHEN** 实现读取展示用版本号
- **THEN** MUST NOT 使用 npm package version、FastAPI app version、OpenAPI version、git sha 或 CI build number 作为 `PRODUCT_VERSION` 展示值

#### Scenario: 发布版本一致性校验

- **WHEN** 产品发布流程准备或确认公开发布公告
- **THEN** MUST compare the release version against `src/shared/product-version.ts` `PRODUCT_VERSION`
- **AND** MUST block release confirmation or record an explicit no-version-change rationale when the values do not match

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

### Requirement: SKU 弹窗规格未匹配提示 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 编辑 SKU 弹窗（`TileSkuFormModal`）中，当 SKU 无 `spec_id`（迁移失败）时在「瓷砖规格」下拉下方展示的辅助提示样式问题：提示 MUST 使用与管理端共享的 `.form-help` 样式（11px、`var(--admin-weak)`、`margin-top: 7px`），与用户管理、品牌弹窗字段辅助文案一致。修复 MUST NOT 修改 SKU API、数据库、Orval、提示文案语义或显隐条件逻辑。

#### Scenario: 规格未匹配提示使用 form-help

- **WHEN** 用户编辑一条 `spec_id` 为 NULL 的历史 SKU 且规格下拉未选择
- **THEN** MUST 展示提示「历史 SKU 未匹配规格，请手动选择后保存」
- **AND** 提示元素 MUST 使用 class `form-help`
- **AND** MUST NOT 使用 `form-hint` 或未定义样式类名

#### Scenario: 提示 Typography 对齐管理端字段辅助文案

- **WHEN** AC-001 场景
- **THEN** 提示 MUST 呈现 11px、`var(--admin-weak)` 次要文字色
- **AND** 视觉层级 MUST 低于字段标签（12px `--admin-muted`）

#### Scenario: 提示显隐逻辑不变

- **WHEN** 用户从规格下拉选择有效规格
- **THEN** 提示 MUST 消失
- **WHEN** 新增 SKU 或编辑已有有效 `spec_id` 的 SKU
- **THEN** MUST NOT 展示该提示

#### Scenario: 同弹窗既有修复不回退

- **WHEN** 本修复合并后
- **THEN** BUG-0010（modal-desc）、BUG-0011（弹窗滚动）、BUG-0012（字段规则）相关行为 MUST 保持

### Requirement: SKU 弹窗表单字段规则修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的表单字段规则，对齐 UAT 产品决策（[BUG-0012](issues/bugs/archive/BUG-0012-tile-sku-modal-form-field-rules/)）：**表面工艺非必填**、**参考价格（元）必填且新建默认 0**。修复 MUST 同步前后端校验，且 MUST NOT 回退 BUG-0011 弹窗滚动布局或 BUG-0009 列表 UI。

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

Web 客户端 MUST 提供瓷砖 SKU 管理页，路由为 `/admin/tile-skus`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` 与 `tile-sku-create-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 保留 1120px 页面级 `content-inner` override）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。

#### Scenario: SKU 页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-skus`
- **THEN** 页面 MUST 展示 page-head（eyebrow「OPERATIONS / SKU」、标题「瓷砖SKU」、说明、「＋ 新增SKU」）
- **AND** MUST 展示 4 指标卡（SKU总数/已上架/待完善/草稿）、五维筛选区、SKU 表格与分页
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过 `:has(.sku-page-hero) .content-inner` 或等价规则退回 1120px。

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择筛选项并点击查询或回车
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」
- **AND** 分页 MUST 支持页码与每页 10/20/50/100 条；默认 20；切换 page_size MUST 重置页码为 1。

### Requirement: 管理端列表页操作反馈 Toast 布局统一

Web 客户端 MUST 在管理端以下四个列表页对「操作成功/失败且约 3.2 秒后自动消失」的全局反馈使用固定位置 toast（`.admin-toast-region` + `.admin-toast` 或等价共享组件），MUST NOT 在 `page-hero` 或主体内容上方插入文档流 `.admin-notice` 占位节点。toast 样式 MUST 来自管理端共享样式（如 `admin-home.css`），四页视觉与行为 MUST 一致。弹窗内 inline 表单错误 MAY 继续使用 inline 错误文案；`AdminLayout` 侧栏占位 notice 不在本 requirement 范围。修复 MUST NOT 回归品牌 Logo 展示、上传进度及四页 CRUD、筛选、分页、权限边界。受保护账号操作提示或失败反馈也 MUST 使用 fixed toast、title、tooltip 或等价不改变文档流布局的方式，MUST NOT 推挤用户管理页布局。

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

#### Scenario: 受保护账号提示不推挤页面

- **WHEN** 用户管理列表展示受保护账号禁用原因
- **THEN** 提示 MUST 使用 `title`、tooltip、fixed toast 或等价方式
- **AND** MUST NOT 插入文档流 notice 推挤 page-hero、筛选区、表格或分页

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

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「冻结」「解冻」与「删除」操作提供二次确认，以降低误触风险。冻结/解冻确认 MUST 复用与同项目类目/品牌启停确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。删除确认 MUST 使用与同页/类目/品牌删除一致的 modal 结构，MUST NOT 使用 `window.confirm`。用户点击「冻结」「解冻」或「删除」时 MUST NOT 直接调用 status API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。重置密码 confirm 见「用户重置密码二次确认」requirement。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。当目标用户 `is_protected=true` 时，冻结/解冻/删除按钮 MUST 置灰并展示 `protected_reason`，MUST NOT 打开确认弹窗或调用 status API。

#### Scenario: 受保护账号状态按钮置灰

- **GIVEN** 用户列表行 `is_protected=true`
- **WHEN** 管理员查看冻结、解冻或删除操作
- **THEN** 对应按钮 MUST 置灰但仍可见
- **AND** 禁用原因 MUST 来自 `protected_reason`
- **AND** 点击这些按钮 MUST NOT 展示 confirm modal
- **AND** MUST NOT 调用 `PATCH /api/v1/admin/users/{id}/status`

#### Scenario: 冻结须先确认

- **WHEN** `admin` 在普通用户列表行点击「冻结」
- **THEN** MUST 展示冻结确认弹窗，MUST NOT 直接调用 `PATCH /api/v1/admin/users/{id}/status`
- **AND** 弹窗标题 MUST 为「冻结用户」或等价文案
- **AND** 正文 MUST 含用户名及冻结后果（如禁止登录）

#### Scenario: 删除须使用 DS modal

- **WHEN** `admin` 对可删除普通用户点击「删除」
- **THEN** MUST 展示删除确认 modal，MUST NOT 使用 `window.confirm`
- **AND** 正文 MUST 含用户名及不可恢复提示

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

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「重置密码」操作提供二次确认。确认 MUST 复用与同项目类目/品牌启停及同页冻结确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「重置密码」时 MUST NOT 使用 `window.confirm`；MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。确认成功后 MUST 继续打开既有结果弹窗展示一次性随机密码（REQ-0005 AC-022）。当目标用户 `is_protected=true` 时，重置密码按钮 MUST 置灰并展示 `protected_reason`，MUST NOT 打开确认弹窗或调用 reset-password API。本能力 MUST NOT 修改数据库或权限边界；本 change 会通过 API schema 扩展 `is_protected` / `protected_reason` 并要求 Orval 同步。

#### Scenario: 受保护账号重置密码按钮置灰

- **GIVEN** 用户列表行 `is_protected=true`
- **WHEN** 管理员查看「重置密码」操作
- **THEN** 按钮 MUST 置灰但仍可见
- **AND** 禁用原因 MUST 来自 `protected_reason`
- **AND** 点击按钮 MUST NOT 展示重置密码确认弹窗
- **AND** MUST NOT 调用 `POST /api/v1/admin/users/{id}/reset-password`

#### Scenario: 重置密码须先确认

- **WHEN** `admin` 在普通用户列表行点击「重置密码」
- **THEN** MUST 展示重置密码确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`
- **AND** MUST NOT 调用 `window.confirm`
- **AND** 弹窗标题 MUST 为「重置密码」或等价文案
- **AND** 正文 MUST 含用户名及重置后果（如将生成新随机密码）

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

### Requirement: 管理端 Sidebar 菜单语义图标修复

Web 客户端 MUST 修复管理端 Sidebar 各菜单图标无法区分的缺陷（BUG-0021）：`AdminNavItem` MUST 配置 per-item Lucide（或 DS 等价）语义 icon；`AdminSidebar` MUST 渲染 SVG icon 而非纯 CSS 占位方块。**collapsed** 态下用户 MUST 可仅凭图标识别目标菜单；**expanded** 态 MUST 图标与文案并存且无布局回归。修复 MUST NOT 变更 REQ-0011 折叠/展开、localStorage（`admin-sidebar-collapsed`）、chevron、active 路由高亮、≤1023px 响应式或店主端 `Sidebar`。修复 MUST NOT 变更 API、SQLite、Orval 或 Docker 部署。

#### Scenario: nav 配置含 icon 字段

- **WHEN** 开发者查看 `admin-nav.ts`
- **THEN** 每个 `AdminNavItem` MUST 含 `icon` 属性（LucideIcon 或等价）
- **AND** home/sku/brand/category/banner/users/settings MUST 映射至可区分的 icon

#### Scenario: AdminSidebar 渲染 Lucide icon

- **WHEN** 用户查看任意 `/admin/*` 页面 Sidebar
- **THEN** 各 nav 按钮 MUST 渲染对应 Lucide SVG（约 16px，`strokeWidth` 约 1.5）
- **AND** 装饰性 icon MUST `aria-hidden="true"`
- **AND** nav 按钮 MUST 保留 `aria-label={item.label}`

#### Scenario: collapsed 态 Vitest 覆盖

- **WHEN** 运行 vitest 覆盖 AdminSidebar icon 修复
- **THEN** MUST 断言 collapsed（或等价）渲染下至少 2 个不同 nav id 对应不同 icon
- **AND** 现有 `AdminSidebar.collapse.test.tsx` 用例 MUST 仍通过

#### Scenario: REQ-0011 折叠能力无回归

- **WHEN** 用户切换 chevron 或刷新页面
- **THEN** 264px ↔ 72px 过渡、localStorage 持久化、`data-sidebar-state` MUST 正常
- **AND** ≤1023px MUST 无折叠 chevron 回归

#### Scenario: 纯前端修复范围

- **WHEN** 本 change 合并
- **THEN** MUST NOT 修改后端路由、数据库 migration 或 Orval 生成物
- **AND** `cd src/web && pnpm test` 与 `pnpm build` MUST 通过

### Requirement: 管理端个人资料路由

Web 客户端 MUST 注册 `/admin/profile` 路由，受管理端路由守卫保护。`admin` 与 `employee` MUST 可访问；`store_owner` MUST 跳转 forbidden。`AdminLayout` MUST 通过 `GET /api/v1/profile/me` 预取当前用户 profile 摘要，并将 `email` 与 `avatar_url`（非空时）传递给侧栏 `AdminUserMenu`；MUST NOT 依赖 auth login `/me` 的 `UserProfile` 获取头像 URL。

#### Scenario: 路由注册与守卫

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 渲染 `ProfilePage`
- **AND** MUST NOT 要求 `requireAdmin`

#### Scenario: 店主拒绝

- **WHEN** `store_owner` 访问 `/admin/profile`
- **THEN** MUST 跳转 `/admin/forbidden`

#### Scenario: 侧栏邮箱展示

- **WHEN** 用户 profile 含 email
- **THEN** Sidebar 用户区 MUST 展示该 email
- **WHEN** email 为空
- **THEN** MAY fallback `{username}@tilesfst.com`

#### Scenario: 侧栏头像数据 plumbing

- **WHEN** `AdminLayout` 挂载且用户为 `admin` 或 `employee`
- **THEN** MUST 调用 `GET /api/v1/profile/me`（或等价 `fetchProfileMe`）
- **AND** 响应中的 `avatar_url` MUST 传递给 `AdminUserMenu`
- **AND** MUST NOT 扩展 auth `UserProfile` schema 作为唯一数据源

#### Scenario: Profile 上传后侧栏刷新

- **WHEN** 用户在 `/admin/profile` 成功上传并持久化新头像
- **THEN** 导航至其他 `/admin/*` 页时侧栏 MUST 展示新头像图片
- **AND** MUST NOT 要求整页硬刷新浏览器

### Requirement: 管理端修改密码弹窗组件

Web 客户端 MUST 在管理端修改密码弹窗中展示当前 effective 密码策略，并在新密码策略失败时展示具体失败原因。客户端 MUST NOT 仅依赖静态旧规则或泛化错误文案。若后端返回结构化策略失败详情，客户端 MUST 将详情映射为用户可理解的中文提示。

#### Scenario: 默认策略规则展示

- **GIVEN** effective 密码策略为最小 12 位、要求大写、小写、数字、特殊字符
- **WHEN** 用户打开修改密码弹窗
- **THEN** 页面 MUST 展示上述规则
- **AND** 页面 MUST NOT 只展示“8-32 位字符、至少包含字母和数字”

#### Scenario: API 策略失败详情映射

- **WHEN** 修改密码 API 返回策略失败详情，例如缺少特殊字符或缺少大写字母
- **THEN** 客户端 MUST 展示对应中文提示
- **AND** 提示 MUST 位于新密码字段或规则区
- **AND** 原密码字段 MUST NOT 误显示新密码策略失败

#### Scenario: 既有错误映射无回归

- **WHEN** API 返回原密码错误、弱密码、同原密码、限流或受保护账号不可改密
- **THEN** 客户端 MUST 继续展示对应明确文案
- **AND** MUST NOT 统一降级为“新密码不符合安全策略”

### Requirement: 管理端瓷砖规格管理页

Web 客户端 MUST 提供瓷砖规格管理页，路由为 `/admin/tile-specs`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html` 与 `tile-size-management-modal.html` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。列表底部分页 MUST 复用与用户管理页一致的标准 DOM 与样式（`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`），MUST NOT 使用项目内未定义的 `pagination-bar` / `page-indicator` 结构。表单弹窗保存成功后 MUST 自动重新加载列表与 summary（Toast + 列表 refresh），行为 MUST 与品牌管理页一致。行内「启用」「停用」「删除」二次确认 MUST 复用与 `TileCategoryManagementPage` / `BrandManagementPage` 相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）；MUST NOT 使用简化 `confirm-card` 模板或泛化「确认」主按钮。

#### Scenario: 规格页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/tile-specs`
- **THEN** 页面 MUST 展示 page-header（eyebrow「MASTER DATA」、标题「瓷砖规格」、说明、「＋ 新增瓷砖规格」）
- **AND** MUST 展示 4 指标卡（规格总数/启用规格/停用规格/未关联 SKU）、关键词+状态筛选、规格表格与分页
- **AND** MUST NOT 展示导出、批量操作、列表 section 标题行

#### Scenario: 筛选与分页

- **WHEN** 用户输入关键词或选择状态并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 条」（`page-summary`）
- **AND** 分页 MUST 使用与用户管理页一致的 `page-buttons`（含当前页 `.page-btn.active`）与 `page-size-wrap`（「每页显示」+ 20/50/100 条选项）
- **AND** MUST NOT 使用 `{page} / {totalPages}` 文本指示器替代激活页码按钮

#### Scenario: 列表主列字号

- **WHEN** 用户查看规格表格「尺寸名称」列
- **THEN** 字号与字色 MUST 与同表标准数据列视觉 rhythm 协调
- **AND** MUST NOT 明显大于相邻宽度/长度/厚度列而造成表格层级失衡

#### Scenario: 启停二次确认

- **WHEN** 用户点击行内「启用」或「停用」
- **THEN** MUST NOT 直接调用 enable/disable API
- **AND** MUST 展示确认 modal（`role="dialog"`、`aria-modal="true"`），结构 MUST 对齐 `BrandManagementPage` / `TileCategoryManagementPage`
- **AND** 标题区 MUST 含 `modal-close`（×）与 `aria-labelledby`
- **AND** 正文 MUST 使用 `page-desc`
- **WHEN** 用户点击「停用」
- **THEN** 标题 MUST 为「停用规格」
- **AND** 正文 MUST 含 `确认停用规格「{display_name}」？停用后前台将不再展示该规格。`
- **AND** 主按钮 MUST 为「确认停用」
- **WHEN** 用户点击「启用」
- **THEN** 标题 MUST 为「启用规格」
- **AND** 正文 MUST 含 `确认启用规格「{display_name}」？`
- **AND** 主按钮 MUST 为「确认启用」
- **WHEN** 用户在 confirm modal 点击确认主按钮
- **THEN** MUST 调用 enable/disable API 并刷新列表
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭 modal 且 MUST NOT 调用 API

#### Scenario: 删除二次确认

- **WHEN** 用户点击可删除行的「删除」
- **THEN** MUST NOT 直接调用 DELETE API
- **AND** MUST 展示删除确认 modal，结构 MUST 对齐类目/品牌删除 confirm
- **AND** 标题 MUST 为「删除规格」
- **AND** 正文 MUST 含 `确认删除规格「{display_name}」？此操作不可恢复。` 且使用 `page-desc`
- **AND** 底部 MUST 含「取消」与主按钮「删除规格」（`btn primary`）
- **AND** MUST NOT 使用 `confirm-card` class 或 `btn primary danger` 删除按钮变体
- **WHEN** 用户点击「删除规格」
- **THEN** MUST 调用 DELETE API 并刷新列表
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭 modal 且 MUST NOT 调用 API

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `sku_count` 为 0 且状态为停用
- **THEN** 「删除」MUST 可点击（风险色）
- **WHEN** 其他情况
- **THEN** 「删除」MUST 置灰且 hover 提示「仅允许删除未关联SKU且已停用的规格」

#### Scenario: 新增编辑弹窗

- **WHEN** 用户点击「新增瓷砖规格」或行内「编辑」
- **THEN** MUST 打开宽 720px 弹窗，头尾固定、主体可滚动
- **AND** 字段顺序 MUST 为：宽*、长*、只读尺寸名称（跨列）、厚度、排序*、备注（跨列）
- **AND** MUST NOT 展示状态、规格类型、单位选择、可编辑尺寸名称
- **AND** 宽长变化 MUST 实时生成 `{w}×{l}mm`；重复时 MUST 展示错误并禁止提交（服务端校验仍生效）
- **AND** 备注 `textarea` MUST 在跨列容器内占满整行宽度，固定高度，`resize: none`

#### Scenario: 保存后刷新列表

- **WHEN** 用户通过弹窗成功创建或更新规格
- **THEN** MUST 展示成功 Toast 并关闭弹窗
- **AND** MUST 无需整页刷新即更新列表行与「共 {total} 条」及 4 指标卡 summary
- **AND** MUST 调用与启停/删除相同的列表加载函数（如 `loadSpecs()`）

#### Scenario: 规格管理 CSS Port

- **WHEN** 开发者查看规格管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/tile-spec-management.css`（或等价 port CSS）
- **AND** 颜色 MUST 通过 semantic token 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/tile-specs`
- **THEN** 前端 MUST 跳转至 `/admin/login`

### Requirement: 管理端 Banner 管理页

Web 客户端 MUST 提供 Banner 管理页，路由为 `/admin/banners`，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html` 与 `banner-management-list.png` 的 CSS Port 策略（**展示位置独立列**与第一列仅标题为 BUG-0039 策略 delta，MUST 以本 requirement 为准）。页面 MUST 复用 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容最大宽度 1080px）。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。列表表格 MUST NOT 展示与 page-hero 重复的「Banner 列表」section 标题或「当前显示 X-Y / N」toolbar 统计行。列表底部分页 MUST 复用与用户管理页一致的标准 DOM 与样式（`pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`），MUST NOT 使用 `banner-pagination` / `table-toolbar` 范围行结构。展示端筛选、表格和弹窗文案 MUST 仅表达“小程序”；展示位置 MUST 仅表达“首页轮播”和“品牌列表页轮播”。

#### Scenario: Banner 列表页布局

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/banners`
- **THEN** 页面 MUST 展示 page-hero（眉标 `OPERATIONS / BANNER MANAGEMENT`、标题「Banner 管理」、说明、「＋ 新增 Banner」）
- **AND** MUST 展示 4 指标卡（Banner 总数/当前筛选/已上线/待生效）
- **AND** MUST 展示关键词、展示端、展示位置、状态、时间状态筛选与 Banner 表格、分页
- **AND** 展示端控件 MUST 仅显示“小程序”或等价只读表达
- **AND** 展示位置控件 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 表格 MUST 含 Banner 缩略图（86×38）与标题、**展示位置**、展示端、跳转类型、状态、有效期、排序、更新时间、操作
- **AND** 第一列 MUST 仅展示缩略图与 Banner 标题，MUST NOT 在同一单元格叠放展示位置副文案
- **AND** MUST NOT 展示导出、批量操作
- **AND** MUST NOT 展示「Banner 列表」section 标题或「当前显示 … / …」toolbar 行。

#### Scenario: 展示位置独立列

- **WHEN** 管理员查看 Banner 列表表格
- **THEN** MUST 存在表头「展示位置」
- **AND** 单元格 MUST 展示 `position` 对应中文文案「首页轮播」或「品牌列表页轮播」
- **AND** 「展示位置」列 MUST 与「展示端」列语义区分，MUST NOT 重复展示同一信息。

#### Scenario: 筛选与分页

- **WHEN** 用户输入筛选条件并点击查询
- **THEN** 系统 MUST 重置页码为 1 并重新加载列表
- **AND** 分页左侧 MUST 显示「共 {total} 个 Banner」（`page-summary`）
- **AND** 分页 MUST 使用与用户管理页一致的 `page-buttons`（含当前页 `.page-btn.active`）与 `page-size-wrap`（「每页显示」+ 10/20/50 条选项）
- **AND** MUST NOT 使用连续多页码条替代单页 active 按钮模式
- **AND** `total` MUST 仅统计小程序两个轮播位置范围内的 Banner。

#### Scenario: 上线与下线二次确认

- **WHEN** 用户点击行内「上线」或「下线」
- **THEN** MUST 弹出二次确认（对齐 `BrandManagementPage` / REQ-0008）
- **AND** 确认后 MUST 调用 online/offline API 并刷新列表。

#### Scenario: 删除按钮规则

- **WHEN** 列表行 `status=ONLINE`
- **THEN** 「删除」MUST 不可点；提示「已上线 Banner 需先下线后删除」
- **WHEN** `status` 为 `DRAFT`、`OFFLINE` 或 `EXPIRED`
- **THEN** 「删除」MUST 可点击且二次确认。

#### Scenario: Banner 管理 CSS Port

- **WHEN** 开发者查看 Banner 管理页源码
- **THEN** 视觉样式 MUST 主要来自 `features/admin/styles/banner-management.css`
- **AND** 颜色 MUST 通过 semantic token 引用 `globals.css`
- **AND** TSX MUST NOT 包含裸 Hex。

#### Scenario: 未登录访问

- **WHEN** 未登录用户访问 `/admin/banners`
- **THEN** 前端 MUST 跳转至 `/admin/login`。

#### Scenario: 管理端列表横切质量

- **WHEN** 开发者实现 Banner 管理范围收敛
- **THEN** 分页 DOM MUST 对齐用户管理基准
- **AND** 指标卡 MUST 使用 `.metric-label`、`.metric-value`、`.metric-desc` 或共享 `MetricCard`
- **AND** 保存、删除、上线、下线反馈 MUST 使用 fixed toast 或等价固定反馈
- **AND** 状态/危险操作 MUST 使用 DS confirm modal
- **AND** MUST NOT 使用 `window.confirm` 或会造成 layout shift 的文档流 notice。

### Requirement: Banner 新增编辑弹窗

Web 客户端 MUST 提供 `BannerFormModal`，宽 **880px**（与瓷砖 SKU 弹窗 `.sku-modal-card` 一致，`max-width: 100%` 响应式保留）、最大高度 92vh、内容区可滚动（头尾固定）。弹窗 MUST 按 `jump_type` 展示条件字段：`SKU_DETAIL`（关联 SKU + 图库选图）、`BRAND_DETAIL`（关联品牌 + 品牌 Logo 取图）、`EXTERNAL_LINK`（HTTPS 外链）、`TOPIC_PAGE`（关联专题）、`NO_JUMP`（无跳转目标）。弹窗 MUST NOT 展示状态编辑或状态策略说明块。Banner 图片模块 MUST NOT 展示冗余来源首行标题（如「自定义上传 / SKU 主图」）；自定义上传按钮 MUST 使用「选择/更换/上传中」文案并对齐 `BrandFormModal` 的 `hidden` file input 模式。展示端 MUST 默认为“小程序”且不得保存为其他端；展示位置 MUST 仅允许“首页轮播”和“品牌列表页轮播”。关联 SKU、关联品牌与关联专题 MUST 为单一可搜索选择控件（Combobox），MUST NOT 分离为独立搜索框与下拉框。运营备注 `textarea` MUST 占满整行且 placeholder 字号与同弹窗 input 一致。有效期 MUST 为单字段区间「{开始} 至 {结束}」，格式 `YYYY-MM-DD HH:mm`（分钟精度），MUST NOT 使用原生 `<input type="datetime-local">` 作为最终方案。视觉 MUST 对齐管理端大表单弹窗基准（宽度与 SKU 弹窗一致）。

#### Scenario: 公共字段

- **WHEN** 用户打开新增或编辑 Banner 弹窗
- **THEN** MUST 展示 Banner 标题、展示端、展示位置、Banner 图片、跳转类型、排序、有效期、运营备注
- **AND** 展示端 MUST 显示为“小程序”且不得出现 Web 首页、专题页等旧选项
- **AND** 展示位置 MUST 仅提供“首页轮播”和“品牌列表页轮播”
- **AND** 新增 Banner 默认展示位置 SHOULD 为“首页轮播”
- **AND** 主按钮 MUST 为「保存 Banner」品牌金样式
- **AND** 弹窗主体超出视口时 MUST 可纵向滚动且 footer 操作按钮始终可达。

#### Scenario: jump_type 切换

- **WHEN** 用户切换跳转类型
- **THEN** MUST 清空不兼容的跳转目标字段
- **AND** MUST 展示对应该类型的条件块。

#### Scenario: Banner 弹窗横切质量

- **WHEN** 开发者实现或回归 Banner 弹窗
- **THEN** TSX MUST NOT 同时挂载通用 `modal-card` 与 `banner-modal-card`
- **AND** 1440px 视口下 Computed width MUST 符合 Banner/SKU 大弹窗基准
- **AND** 矮视口下 body 必须可滚动，footer 主操作按钮始终可达。

#### Scenario: Banner 图片上传回归

- **WHEN** 用户在 Banner 弹窗选择图片
- **THEN** 上传控件 MUST 呈现 `idle -> uploading -> done/failed` 状态机
- **AND** 成功后 MUST 在同一会话即时回显缩略图或文件卡片
- **AND** 失败信息 MUST 显示在上传控件附近
- **AND** Docker Web `:3000` 边界下小文件上传必须成功，超限文件必须返回业务错误而非 Nginx 413。

### Requirement: Banner 管理 PNG 视觉验收 Gate

Banner 管理视觉对齐 MUST 通过 PNG golden reference 与跨页弹窗一致性验收 gate。

#### Scenario: 列表 PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/banners` 与 `banner-management-list.png`
- **THEN** diff checklist（Shell、筛选四列、四指标卡、跳转类型列、分页、无弹窗遮罩）MUST 全部 pass
- **AND** 第一列仅标题 + 独立「展示位置」列 MUST pass（允许与 PNG 第一列叠放结构不一致，以 BUG-0039 acceptance 为准）

#### Scenario: 弹窗宽度并排验收

- **WHEN** 团队在视口 ≥ 880px 并排对比 Banner 弹窗与瓷砖 SKU 弹窗
- **THEN** 两弹窗宽度 MUST 视觉一致（880px）
- **AND** 四套 `jump_type` 条件字段显隐、无状态块、modal-body 可滚动 MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`（不以 640px modal PNG 为宽度 pass 条件）

### Requirement: 用户创建校验错误提示修复

Web 客户端 MUST 修复 `/admin/users` 添加用户弹窗的校验失败提示缺陷。创建用户失败时，弹窗或等价错误区域 MUST 优先展示后端统一错误响应中的 `message`，并 MUST 让管理员能够判断需要修改「用户名」字段。该修复 MUST 保持用户管理弹窗既有 CSS Port、Design System Token、头像上传、成功 Toast、一次性密码弹窗和列表刷新行为不回归。

#### Scenario: 用户名长度不足展示明确错误

- **WHEN** 管理员打开 `/admin/users` 添加用户弹窗
- **AND** 输入 `username="abc"` 与合法 role 后提交
- **THEN** 页面 MUST 展示来自 API 或等价映射的明确中文错误
- **AND** 错误文案 MUST 指向用户名长度不足
- **AND** 页面 MUST NOT 仅展示无法定位字段的泛化兜底失败文案

#### Scenario: 其他用户名格式错误展示明确错误

- **WHEN** 管理员分别提交 `username="1abc"`、`username="ab__cd"` 或保留字
- **THEN** 页面 MUST 展示对应用户名规则错误
- **AND** 管理员 MUST 能判断应修改用户名字段

#### Scenario: 错误修正后可成功创建

- **GIVEN** 添加用户弹窗已展示用户名校验错误
- **WHEN** 管理员将用户名改为合法且未重复的值并重新提交
- **THEN** 系统 MUST 创建用户成功
- **AND** MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password`，一次性密码弹窗 MUST 正常展示

#### Scenario: 弹窗布局不回归

- **WHEN** 添加用户弹窗展示校验错误
- **THEN** 弹窗宽度、字段顺序、按钮区、头像上传区域和遮罩布局 MUST 保持用户管理弹窗既有视觉约束
- **AND** 新增或变更样式 MUST 使用 semantic token 或既有 CSS 变量，MUST NOT 新增裸 Hex

### Requirement: 管理端接口文档 Swagger 入口

The Web admin API docs page SHALL open backend Swagger documentation through a same-origin Web route instead of sending users to the Web app homepage. The page SHALL also provide row-level Swagger detail links for OpenAPI routes that can be mapped to a concrete operationId, while keeping non-OpenAPI routes visible but unavailable for Swagger detail navigation. Future changes touching this page, its Swagger entry, or its proxy assumptions MUST document and verify the Swagger Web proxy and production `Try It Out` checklist.

#### Scenario: Swagger UI link uses same-origin docs path

- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** the Swagger action SHALL point to `/docs` or an equivalent same-origin Web route
- **AND** the action SHALL NOT hardcode the backend host, container service name, or port.

#### Scenario: 生产 Swagger 操作保持只读

- **WHEN** the Web client is configured for production
- **THEN** the Swagger action MAY be labeled as read-only
- **AND** it SHALL still use the same-origin Web docs route
- **AND** the frontend SHALL NOT enable production Try It Out.

#### Scenario: 未知 Web 路由 fallback 不用于 Swagger

- **WHEN** an admin opens the Swagger action from `/admin/api-docs`
- **THEN** the user SHALL see FastAPI Swagger UI or an equivalent backend docs response
- **AND** the Web SPA fallback SHALL NOT serve the Web homepage for that docs route.

#### Scenario: 行级 Swagger operationId 深链

- **WHEN** an authenticated `admin` user views a `/admin/api-docs` route row with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** the row-level Swagger view action SHALL be enabled
- **AND** the action SHALL link to a same-origin Swagger UI deep link for that specific operationId, such as `/docs#/{tag}/{operationId}` after URL-safe encoding.
- **AND** the PATH cell MAY provide the same safe Swagger UI deep link as an additional row-level view affordance.

#### Scenario: 行级 Swagger 链接安全打开新上下文

- **WHEN** an admin activates an enabled row-level Swagger view action
- **THEN** the link SHALL open in a safe new browsing context or an equivalently safe navigation mode
- **AND** it SHALL use attributes such as `rel="noreferrer"` when opening a new tab.

#### Scenario: 非 OpenAPI 路由不可跳转

- **WHEN** an admin views a route row with `included_in_openapi=false`
- **THEN** the row-level Swagger view action SHALL be disabled or equivalently unavailable
- **AND** it SHALL NOT navigate to `/docs` or an incorrect operationId
- **AND** the PATH cell SHALL NOT include a clickable Swagger detail href
- **AND** the page SHALL communicate that the route is not included in OpenAPI or has no Swagger detail.

#### Scenario: 缺少 operationId 的 OpenAPI 路由不可跳转

- **WHEN** an admin views a route row with `included_in_openapi=true` but no usable `operation_id`
- **THEN** the row-level Swagger view action SHALL be disabled or equivalently unavailable
- **AND** it SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.
- **AND** the PATH cell SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.

#### Scenario: 行级 Swagger 链接不泄露认证上下文

- **WHEN** row-level Swagger view actions are rendered
- **THEN** the generated URL SHALL NOT include bearer tokens, session data, database DSNs, MinIO credentials, JWT secrets, or real environment variable values in the path, query string, hash fragment, or persisted browser storage
- **AND** the Web client SHALL NOT add a new Swagger token auto-injection mechanism for this feature.

#### Scenario: API docs refine records Swagger proxy checklist

- **WHEN** a future Web client change modifies `/admin/api-docs`, Swagger actions, row-level Swagger links, or docs route proxy assumptions
- **THEN** its design, acceptance, or trace records MUST include the Swagger Web proxy and production `Try It Out` checklist
- **AND** the checklist MUST state whether `docs/03-api-index.md` and `docs/standards/api-governance.md` need updates
- **AND** if either document is not updated, the trace MUST record the reason.

### Requirement: 管理端品牌 favicon

Web 客户端 MUST 为管理端入口声明菲尚特品牌 favicon 与 apple-touch-icon。图标 MUST 使用用户提供的菲尚特 Logo 或由该 Logo 派生的 Web 优化图标，MUST NOT 继续使用 Vite、React 或浏览器默认图标。本能力 MUST 使用前端静态资源实现，MUST NOT 新增后端 API、数据库字段、MinIO 上传流程、Orval 客户端或小程序能力。favicon 变更 MUST NOT 影响管理端路由守卫、权限、现有页面主体、`/api/`、`/media/` 或 `/openapi.json` 代理行为。

#### Scenario: 浏览器标签展示菲尚特图标

- **WHEN** 已登录或未登录用户通过 Web 入口打开管理端任意页面
- **THEN** 浏览器标签 favicon MUST 指向菲尚特 Logo 或其派生图标
- **AND** MUST NOT 展示 Vite、React 或浏览器默认图标

#### Scenario: Apple touch icon 声明

- **WHEN** 浏览器或设备读取 Web 入口 HTML 的 touch icon 声明
- **THEN** `apple-touch-icon` MUST 指向菲尚特 Logo 或其派生图标

#### Scenario: 静态图标不影响运行时能力

- **WHEN** favicon / apple-touch-icon 更新完成
- **THEN** 管理端登录、路由守卫、Sidebar 导航、`/api/`、`/media/` 与 `/openapi.json` 行为 MUST 保持不变
- **AND** 后端 API、数据库、MinIO、Orval 与小程序 MUST 无契约变更

### Requirement: 管理端接口文档摘要指标卡一致性

Web 管理端 SHALL 使用既有管理端指标卡结构和 Design System 样式基线渲染 `/admin/api-docs` 摘要指标卡。

#### Scenario: 摘要指标卡 DOM 匹配基线

- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** each summary metric card SHALL use the existing `metric-card` pattern
- **AND** each card SHALL include `metric-label`, `metric-value`, and `metric-desc` elements
- **AND** the summary metric values SHALL NOT rely on bare `strong` elements as the only styling hook
- **AND** the summary descriptions SHALL NOT rely on bare `span` elements as the only styling hook.

#### Scenario: 摘要指标视觉层级匹配瓷砖 SKU 页面

- **WHEN** the `/admin/api-docs` summary metrics are compared with `/admin/tile-skus` summary metrics
- **THEN** the cards SHALL preserve the same border, background, radius, padding, value emphasis, and description hierarchy provided by the shared admin metric styles.

#### Scenario: 保留语义化样式

- **WHEN** implementing the summary metric fix
- **THEN** the Web client SHALL reuse existing semantic classes such as `summary-grid`, `metric-card`, `metric-label`, `metric-value`, and `metric-desc`
- **AND** TSX/CSS changes SHALL NOT introduce hard-coded design color hex values.

#### Scenario: API docs 行为不回归

- **WHEN** the summary metric DOM is fixed
- **THEN** `/admin/api-docs` SHALL still display total routes, protected routes, Orval mapped routes, and non-`/api/v1` route counts
- **AND** route filtering, OpenAPI JSON access, Swagger UI/read-only policy, Orval method display, and missing method states SHALL continue to work.

#### Scenario: 权限行为不回归

- **WHEN** the summary metric DOM is fixed
- **THEN** `admin` users SHALL still access `/admin/api-docs`
- **AND** `employee` users SHALL still be denied direct access and SHALL NOT see the sidebar menu item
- **AND** shop-owner Web and WeChat miniapp clients SHALL NOT expose an API docs entry.

### Requirement: 管理端接口文档列表标题与分页一致性
Web 管理端 SHALL 修复 `/admin/api-docs` 路由目录列表布局，移除冗余的 `系统接口` 分区标题，并使用既有管理端列表分页交互与 DOM 基线。

#### Scenario: 冗余列表标题已移除
- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** the route directory list area SHALL NOT render the redundant `系统接口` title
- **AND** the implementation SHALL NOT keep the title by renaming it
- **AND** the implementation SHALL NOT treat `系统接口` as a real API route data row to filter out.

#### Scenario: 路由目录对筛选结果分页
- **WHEN** the route directory has more routes than the selected page size
- **THEN** the table SHALL render only the routes for the current page
- **AND** the pagination total SHALL be calculated from the currently filtered route count.

#### Scenario: 分页控件匹配管理端列表基线
- **WHEN** an admin views the route directory pagination
- **THEN** the pagination SHALL include previous-page, current-page, and next-page controls
- **AND** the pagination DOM SHALL use the existing admin list structure with `page-summary` on the left and `page-right` on the right
- **AND** page buttons SHALL use the existing `page-buttons`, `page-btn`, and `active` class pattern.

#### Scenario: 每页条数选择器匹配瓷砖 SKU 页面
- **WHEN** an admin changes the route directory page size
- **THEN** the selector SHALL offer 10, 20, 50, and 100 rows per page
- **AND** the default page size SHOULD be 20
- **AND** the selector SHALL use the existing `page-size-wrap` and `page-size` class pattern.

#### Scenario: 筛选重置分页
- **WHEN** an admin changes Method, Tag, Auth, or keyword filters
- **THEN** the route directory SHALL reset the current page to page 1
- **AND** the page count SHALL be recalculated from the filtered results.

#### Scenario: 空状态与单页状态保持有效
- **WHEN** route filters match no routes
- **THEN** the page SHALL show an explicit empty state
- **AND** pagination SHALL NOT show invalid page numbers
- **AND** previous-page and next-page actions SHALL be disabled or equivalently unavailable.

#### Scenario: API docs 行为不回归
- **WHEN** the list pagination fix is implemented
- **THEN** `/admin/api-docs` SHALL still show route metadata, OpenAPI inclusion status, Orval method status, and missing-method reasons
- **AND** OpenAPI JSON access, Swagger UI/read-only policy, route filtering, and admin-only access SHALL continue to work
- **AND** shop-owner Web and WeChat miniapp clients SHALL NOT expose an API docs entry.

#### Scenario: 无后端契约变更
- **WHEN** implementing the list pagination fix
- **THEN** the Web client SHALL NOT require backend API request, response, or error-code changes
- **AND** it SHALL NOT require database schema changes, MinIO changes, Orval generation, or Docker Compose changes.

### Requirement: 管理端接口文档路由
The Web admin client SHALL register `/admin/api-docs` as an admin-only route that renders inside the existing Admin Shell.

#### Scenario: Admin route renders
- **WHEN** an authenticated `admin` user navigates to `/admin/api-docs`
- **THEN** the Web client SHALL render the API docs page
- **AND** the page SHALL use the existing Admin Shell layout.

#### Scenario: Forbidden direct navigation
- **WHEN** an authenticated `employee` user navigates directly to `/admin/api-docs`
- **THEN** the Web client SHALL render a 403 page or equivalent forbidden state.

### Requirement: 管理端 Sidebar 接口文档菜单
The Web admin client SHALL add an "接口文档" item to the SYSTEM sidebar group immediately below "系统设置".

#### Scenario: Admin sees API docs menu
- **WHEN** an authenticated `admin` user views the sidebar
- **THEN** the SYSTEM group SHALL include "接口文档" immediately below "系统设置".

#### Scenario: Employee menu hidden
- **WHEN** an authenticated `employee` user views the sidebar
- **THEN** the SYSTEM group SHALL NOT include "接口文档".

#### Scenario: Collapsed sidebar remains accessible
- **WHEN** the sidebar is collapsed
- **THEN** the API docs menu item SHALL retain an accessible name or tooltip for "接口文档".

### Requirement: 管理端接口文档页面 UI
The Web admin client SHALL render the API docs page according to the REQ-0022 prototype and Design System constraints.

#### Scenario: Prototype-led layout
- **WHEN** an admin opens `/admin/api-docs`
- **THEN** the page SHALL include a page hero, environment policy, summary metrics, filters, route table, and Swagger panel or link.

#### Scenario: Semantic token styling
- **WHEN** implementing the API docs page
- **THEN** new TSX/CSS SHALL use semantic token classes rather than hard-coded design color hex values.

#### Scenario: Admin list consistency
- **WHEN** the route table includes pagination
- **THEN** pagination DOM SHALL align with the `/admin/users` baseline using left `page-summary` and right `page-right` controls.

#### Scenario: Layout-stable feedback
- **WHEN** the API docs page shows loading, refresh, or error feedback
- **THEN** the feedback SHALL NOT insert a document-flow notice between hero and table that causes vertical layout shift.

#### Scenario: No native dialogs
- **WHEN** the API docs page needs a confirmation interaction
- **THEN** it SHALL use the Design System modal pattern
- **AND** it SHALL NOT use `window.confirm` or `window.alert`.

### Requirement: 管理端列表页横切一致性

Web 客户端 MUST 统一管理端列表型页面的模块顺序、筛选/搜索交互、表格最后一列固定浮动和分页页码呈现。适用页面 MUST 包含 `/admin/tile-skus`、`/admin/brands`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/banners`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。上述页面 MUST 按「标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块」顺序展示；筛选/搜索模块 MUST 以瓷砖 SKU 页为交互和样式基线但 MUST NOT 展示【查询】或【搜索】显式提交按钮；重置按钮 MUST 保持统一尺寸和样式；列表最后一列 MUST 使用以接口文档页为基线的固定浮动操作列；分页 MUST 最多展示 5 个可点击页码。新增或迁移管理端列表页 MUST 优先复用 `AdminListPage` 或等价 Design System 模板组合，不得在业务页面内重复实现已有列表页骨架、分页 DOM、sticky action column 或 fixed toast 契约。

#### Scenario: 列表页模块顺序统一

- **WHEN** 已登录管理端用户访问任一适用页面
- **THEN** 页面 MUST 先展示标题模块
- **AND** 标题模块之后 MUST 展示指标卡模块
- **AND** 指标卡模块之后 MUST 展示筛选/搜索模块
- **AND** 筛选/搜索模块之后 MUST 展示列表模块
- **AND** 列表模块上方 MUST NOT 展示重复的列表标题、旧版 table toolbar 或割裂的 section heading。

#### Scenario: 筛选区无查询按钮

- **WHEN** 用户查看任一适用页面的筛选/搜索模块
- **THEN** 页面 MUST NOT 展示文案为「查询」或「搜索」的显式提交按钮
- **AND** 页面 MUST 展示统一形态的「重置」按钮
- **AND** 筛选控件变化 MUST 将当前页重置为 1 并刷新或重新计算列表结果。

#### Scenario: 日志审计状态结果筛选使用下拉

- **WHEN** 用户查看 `/admin/logs` 的状态 / 结果筛选项
- **THEN** 页面 MUST 使用下拉选择交互，而不是自由输入框
- **AND** 下拉 MUST 同时支持 `result=success`、`result=failed` 与常见 HTTP status code 精确筛选
- **AND** 常见 HTTP status code MUST 至少包含 200、201、204、301、302、304、400、401、403、404、409、422、429、500、502、503、504
- **AND** 若当前列表数据出现上述静态集合未覆盖的状态码，页面 SHOULD 将该状态码补充为可选项。

#### Scenario: 重置按钮统一

- **WHEN** 用户对比任一适用页面的筛选/搜索模块
- **THEN** 重置按钮 MUST 使用统一高度、padding、圆角、字号、边框和图标策略
- **AND** 点击重置 MUST 清空或恢复默认筛选条件
- **AND** 点击重置 MUST 将当前页重置为 1。

#### Scenario: 最后一列固定浮动

- **WHEN** 任一适用页面的列表存在操作列
- **THEN** 最后一列表头和单元格 MUST 在横向滚动时保持可见
- **AND** 固定列 MUST 使用与接口文档页一致的右侧背景、左侧分割线和阴影层次
- **AND** 行 hover 时固定列背景 MUST 与当前行 hover 状态协调
- **AND** 固定列内的编辑、启停、删除、查看、重置密码等操作权限、禁用态和确认流程 MUST 不回退。

#### Scenario: 分页最多五个可点击页码

- **WHEN** 任一适用页面展示分页
- **THEN** 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构
- **AND** 页码按钮 MUST 使用 `page-buttons`、`page-btn`、`active` 或等价统一 class
- **AND** 可点击页码数量 MUST 不超过 5 个，不包含上一页/下一页按钮
- **AND** 总页数为 1 时 MUST 仍展示统一分页结构，上一页/下一页为禁用态，页码 `1` 为当前态
- **AND** 切换每页显示条数 MUST 将页码重置为 1。

#### Scenario: 新增管理端列表页复用模板

- **WHEN** 开发者新增或重构管理端列表型页面
- **THEN** 页面 MUST 优先使用 `AdminListPage` 或等价模板组合承载标题、指标卡、筛选/搜索、列表和分页模块
- **AND** 页面 MUST NOT 在业务页面内重复实现已有分页 DOM、sticky action column、固定 toast 或列表骨架
- **AND** 业务页面 MAY 通过列定义、筛选项、行操作、状态态文案或受控 slot 插入领域内容，但 MUST NOT 破坏模块顺序、分页结构或操作列契约。

#### Scenario: 非目标端不受影响

- **WHEN** 本修复完成
- **THEN** 店主 Web 展示端和微信小程序 MUST 不受此列表页一致性修复影响
- **AND** 后端 API、数据库、MinIO、媒体上传和 Docker Compose MUST 不因本修复发生契约变化。

### Requirement: 管理端 MetricCard 基础组件
Web 管理端 SHALL provide reusable `MetricCard` and `MetricCardGrid` or equivalent foundation components for admin list summary strips. The components MUST preserve the existing admin list DOM contract and MUST NOT change backend API behavior.

#### Scenario: 渲染指标卡 DOM 契约
- **WHEN** a Web admin list page renders a metric summary card through `MetricCard`
- **THEN** the rendered card SHALL include `.metric-card`, `.metric-label`, `.metric-value`, and `.metric-desc`
- **AND** it SHALL support `label`, `value`, and `description` content

#### Scenario: 指标卡状态展示
- **WHEN** metric data is empty, loading, or unavailable
- **THEN** `MetricCard` SHALL render a unified placeholder such as `—` or an equivalent loading/empty presentation
- **AND** danger or abnormal descriptions SHALL be visually distinguishable through semantic token or existing admin classes

#### Scenario: 指标卡容器布局
- **WHEN** an admin list page renders 2, 3, or 4 metric cards through `MetricCardGrid` or an equivalent container
- **THEN** the container SHALL preserve the `.summary-grid` contract
- **AND** it SHALL support an accessible label for the metric region

### Requirement: 管理端分页窗口工具
Web 管理端 SHALL provide a reusable pagination-window helper for admin list pages. The helper MUST default to at most 5 visible page numbers and MUST handle invalid input defensively.

#### Scenario: 总页数不超过窗口上限
- **WHEN** total pages are less than or equal to the visible window size
- **THEN** the helper SHALL return all page numbers from 1 through total pages

#### Scenario: 当前页靠近首页
- **WHEN** current page is near the beginning and total pages exceed the visible window size
- **THEN** the helper SHALL return a window starting at page 1 with at most 5 page numbers by default

#### Scenario: 当前页靠近末页
- **WHEN** current page is near the end and total pages exceed the visible window size
- **THEN** the helper SHALL return a window ending at the final page with at most 5 page numbers by default

#### Scenario: 当前页居中
- **WHEN** current page is away from both boundaries and total pages exceed the visible window size
- **THEN** the helper SHALL return a centered moving window around the current page with at most 5 page numbers by default

#### Scenario: 非法输入兜底
- **WHEN** current page, total pages, or max visible page count are outside valid ranges
- **THEN** the helper SHALL normalize inputs or return a safe single-page window without throwing during render

### Requirement: 管理端列表分页 DOM 契约
Web 管理端 list pages SHALL preserve the admin pagination structure used by the list-page consistency baseline.

#### Scenario: 渲染统一分页结构
- **WHEN** an applicable admin list page renders pagination
- **THEN** it SHALL include `.page-summary` for total or range copy
- **AND** it SHALL include `.page-right` containing `.page-buttons` and `.page-size-wrap`

#### Scenario: 不引入跳页输入框
- **WHEN** this change is implemented for admin list foundation components
- **THEN** it SHALL NOT introduce a jump-to-page input field
- **AND** it SHALL NOT introduce page-private pagination containers such as `brand-pagination-right`, `banner-pagination`, or `pagination-bar`

### Requirement: 管理端列表基础组件首批接入
Web 管理端 SHALL connect the foundation components to 2 to 3 baseline admin list pages while preserving each page's existing business behavior.

#### Scenario: 首批页面范围
- **WHEN** implementation selects baseline pages for this change
- **THEN** it SHALL choose 2 to 3 pages from `TileSkuManagementPage`, `LogAuditPage`, `ApiDocsPage`, and `BrandManagementPage`
- **AND** the selected set SHALL cover normal metrics, danger or abnormal metric descriptions, and pagination-window usage

#### Scenario: 页面业务行为不回归
- **WHEN** a selected baseline page migrates to the shared foundation components
- **THEN** its filtering, pagination state, empty state, permissions, and existing data behavior SHALL remain unchanged
- **AND** the change SHALL NOT modify backend pagination API, database schema, OpenAPI, or Orval generated clients

#### Scenario: 未接入页面追踪
- **WHEN** implementation completes the first batch
- **THEN** pages not included in the first batch SHALL be recorded as follow-up rollout items in trace or implementation notes

### Requirement: 管理端表单校验错误解析

Web 管理端 MUST provide a shared or equivalent error parsing strategy for management admin form, modal, and upload API failures. The parser MUST prioritize the unified envelope `message`, SHOULD map `data.errors[]` to field-level errors when possible, and MUST safely fall back to a global toast, modal fixed error area, or upload control error state when field mapping is unavailable. Web admin code MUST NOT rely on raw `detail[0].msg` as the only validation error source.

#### Scenario: Envelope message becomes global feedback

- **WHEN** a management admin form API returns `{ code, message, data }` for a validation failure
- **THEN** the Web admin client MUST use `message` as the preferred global error feedback
- **AND** existing business error messages for users, brands, categories, SKUs, specs, banners, system settings, profile, password, and uploads MUST remain compatible.

#### Scenario: Field errors map when possible

- **WHEN** a validation error response includes `data.errors[]`
- **AND** an error item can be mapped to a visible form field
- **THEN** the Web admin client SHOULD display or expose the field-level message for that field
- **AND** unmapped field errors MUST safely degrade to global feedback.

#### Scenario: Raw detail is not the only source

- **WHEN** a management admin form request fails validation
- **THEN** Web admin code MUST NOT depend on raw `detail[0].msg` as the only path for user-facing errors
- **AND** any legacy `detail` compatibility branch MUST be secondary to the unified envelope.

#### Scenario: Error display uses existing Design System

- **WHEN** validation errors are displayed in admin pages, modals, or upload controls
- **THEN** the display MUST use existing admin fixed toast, inline field text, modal fixed error area, or upload fixed error area patterns
- **AND** it MUST NOT add naked Hex colors, independent light error cards, `window.alert`, or `window.confirm`
- **AND** it MUST NOT visibly push modal footer buttons, resize modal width, or break upload `idle → uploading → done/failed` state.

#### Scenario: Upload validation failure keeps preview state stable

- **WHEN** an admin upload API returns a validation envelope for missing `file` or invalid file parameter
- **THEN** the upload control MUST show a stable failure state or toast
- **AND** a successful preview from the same session MUST NOT be cleared unless the user explicitly replaces or removes it.

### Requirement: 管理端主题选择器侧边栏位置

Web admin clients SHALL render the global theme selector inside the AdminLayout sidebar, positioned directly above the bottom user avatar/account block. The selector SHALL NOT render in the page top-right content or header area on AdminLayout pages.

#### Scenario: 主题选择器位于侧边栏用户区上方

- **WHEN** an authenticated admin user opens any AdminLayout page
- **THEN** the sidebar SHALL render the 「界面主题」 selector
- **AND** the selector SHALL be positioned above the bottom user avatar/account block
- **AND** the selector SHALL not overlap the avatar, username, email, user menu trigger, navigation items, or sidebar collapse control.

#### Scenario: 顶部区域不再渲染主题选择器

- **WHEN** an authenticated admin user opens pages such as `/admin/dashboard`, `/admin/users`, `/admin/settings`, or `/admin/api-docs`
- **THEN** the page top-right content/header area SHALL NOT render the 「界面主题」 selector
- **AND** page-level top actions SHALL remain reserved for page-specific commands or filters.

#### Scenario: 主题切换行为保持不变

- **WHEN** the user changes the active theme from the sidebar selector
- **THEN** the selected theme SHALL apply immediately according to existing theme switching behavior
- **AND** existing local and account-level persistence behavior SHALL remain unchanged
- **AND** current page state such as filters, pagination, forms, open dialogs, and upload state SHALL not be reset by moving the selector.

#### Scenario: 侧边栏收起与窄屏不重叠

- **WHEN** the AdminLayout sidebar is collapsed or rendered in a narrow viewport
- **THEN** the theme selector SHALL remain accessible through a compact or equivalent sidebar treatment
- **AND** text, icons, select trigger, user avatar, and menu controls SHALL not overlap or become unreadable.

#### Scenario: Design System 约束

- **WHEN** implementing or styling the sidebar theme selector
- **THEN** Web UI changes SHALL use existing semantic token classes, CSS variables, or established admin/sidebar classes
- **AND** TSX/CSS SHALL NOT introduce raw Hex color values for this placement fix.

### Requirement: Web 主题切换与偏好持久化

The Web client MUST provide theme switching for `system`, `dark_flagship`, `comfort_dark`, and `light` on management-side and supported store-owner Web surfaces. The active mode MUST persist locally and, for authenticated users, synchronize with the account-level theme preference API. Switching themes MUST apply immediately without losing current page state. Account preference synchronization failures MUST be communicated with recoverable admin feedback that automatically dismisses or provides an explicit close affordance; the feedback MUST NOT remain persistently visible without user control.

#### Scenario: 登录前主题偏好

- **WHEN** an unauthenticated user changes theme on the login page
- **THEN** the selected mode SHALL persist locally
- **AND** the login page SHALL update immediately without requiring reload
- **AND** the Web client SHALL NOT call the account-level theme preference API.

#### Scenario: 登录后账号偏好合并

- **WHEN** a user logs in successfully
- **THEN** the Web client SHALL load the account-level `theme_mode`
- **AND** the account-level value SHALL become authoritative when present
- **AND** the active local theme SHALL remain visually stable while synchronization completes.

#### Scenario: 主题切换失败可恢复

- **WHEN** an authenticated user changes theme and the backend persistence request fails
- **THEN** the Web client SHALL keep the local visual selection
- **AND** it SHALL show a recoverable error message using the existing toast or equivalent Design System feedback
- **AND** the error feedback SHALL automatically dismiss or provide an explicit close affordance
- **AND** the error feedback SHALL NOT persist indefinitely, stack repeatedly, or block the user from continuing management-side work.

#### Scenario: 主题切换重复失败不刷屏

- **WHEN** an authenticated user changes theme multiple times and multiple backend persistence attempts fail
- **THEN** the Web client SHALL avoid unbounded duplicate toast stacking
- **AND** the latest recoverable error feedback SHALL remain readable
- **AND** the management sidebar, routed page content, login/logout controls, and current page state SHALL remain usable.

### Requirement: 管理端主题舒适度首批验收矩阵

The Web admin implementation MUST validate theme comfort across login, one list page, one form page/state, one modal, and `/design-system`, with tile SKU management as the representative business workflow.

#### Scenario: 登录页主题验收

- **WHEN** a user opens the admin login page in any supported theme mode
- **THEN** background, material composition, form controls, validation/error state, language controls, and theme switcher SHALL remain readable and visually comfortable
- **AND** the existing login page brand composition SHALL not regress.

#### Scenario: 瓷砖 SKU 列表主题验收

- **WHEN** a user opens `/admin/tile-skus` in any supported theme mode
- **THEN** page hero, metrics, filters, table, sticky action column, pagination, and fixed toast SHALL remain readable, aligned, and free of layout shift
- **AND** the page SHALL continue to reuse the established admin list template or equivalent Design System composition.

#### Scenario: 瓷砖 SKU 表单与弹窗主题验收

- **WHEN** a user opens a tile SKU create/edit form or modal in any supported theme mode
- **THEN** labels, inputs, validation errors, dirty state, modal width, modal scroll behavior, modal footer actions, and confirmation dialogs SHALL remain readable and usable
- **AND** the SKU media upload area SHALL show `idle`, `uploading`, `uploaded`, and `failed` states clearly.

### Requirement: 店主 Web 舒适主题边界

Store-owner Web pages outside brand display pages MUST support comfortable theme modes. Brand display pages MAY remain in `dark_flagship` when preserving the flagship brand expression is a product decision.

#### Scenario: 品牌展示页可保持暗色旗舰

- **WHEN** a store-owner Web brand display page is opened
- **THEN** the page MAY remain in `dark_flagship`
- **AND** this exception SHALL be documented in the page or route-level theme strategy.

#### Scenario: 非品牌展示页支持舒适主题

- **WHEN** a store-owner Web catalog, detail, or inquiry page is opened
- **THEN** it SHALL support the active comfortable theme mode
- **AND** it SHALL continue to use semantic tokens rather than page-local raw Hex values.

### Requirement: 管理端重置密码结果复制兜底

Web 客户端 SHALL use the shared Clipboard copy helper or an equivalent normalized copy pattern when copying generated reset passwords from the user-management reset-password result dialog. The dialog SHALL preserve manual-copy fallback behavior when automatic Clipboard writing is unavailable or fails.

#### Scenario: 重置密码自动复制成功

- **WHEN** an admin copies a generated reset password and Clipboard writing succeeds
- **THEN** the dialog SHALL show a success status such as `密码已复制`
- **AND** it SHALL keep existing guidance that the password must be safely delivered and cannot be viewed again after closing.

#### Scenario: 重置密码自动复制失败

- **WHEN** Clipboard API is unavailable or Clipboard writing fails while copying a generated reset password
- **THEN** the dialog SHALL focus and select the generated password input or provide an equivalent manual-copy path
- **AND** the dialog SHALL show manual-copy guidance using `role="status"` or an equivalent accessible feedback pattern
- **AND** it SHALL NOT log or emit the generated password as telemetry.

#### Scenario: 重置密码弹窗布局不回归

- **WHEN** the reset-password result dialog displays copy success, failure, or manual fallback guidance
- **THEN** the modal width, body scroll, input visibility, and footer buttons SHALL remain stable and reachable
- **AND** the implementation SHALL NOT use `window.confirm` for this copy flow.

### Requirement: Web 管理端复制交互复用边界

Web 管理端 copy interactions SHALL prefer the shared Clipboard copy helper or an equivalent normalized pattern when adding or refactoring copy buttons for already-authorized visible text.

#### Scenario: 新增管理端复制入口

- **WHEN** developers add a new admin copy action for visible text
- **THEN** the implementation SHALL use the shared Clipboard helper or document why an equivalent platform-specific path is required
- **AND** it SHALL handle success, API unavailable, write failure, empty value, and manual-copy fallback where applicable.

#### Scenario: 店主 Web 与小程序边界

- **WHEN** this change is implemented
- **THEN** Web catalog and miniapp copy behavior SHALL remain unchanged
- **AND** miniapp Clipboard API adaptation SHALL require a separate requirement or change.

### Requirement: Web 管理端移动端基础适配矩阵

Web 客户端 MUST 为当前已实现的 Web 管理端 `/admin/*` 页面提供移动端基础可用验收矩阵。适用页面 MUST 包含 `/admin/login`、`/admin/dashboard`、`/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/profile`、`/admin/users`、`/admin/logs`、`/admin/api-docs`、`/admin/settings/:tab` 与 `/admin/forbidden`。本能力 MUST 仅作用于 Web 管理端，MUST NOT 修改店主 Web 展示端、微信小程序、后端 API、数据库、OpenAPI、Orval、Docker Compose、Nginx、MinIO 或媒体上传后端链路。

#### Scenario: 移动端验收视口覆盖

- **WHEN** 实现或验收本 Change
- **THEN** MUST 覆盖 `375x812`、`390x844`、`768x1024` 与 `1440x1024` 视口
- **AND** `1440x1024` MUST 作为桌面回归视口
- **AND** 验收记录 MUST 标明每个视口是否存在页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选或分页不可操作。

#### Scenario: 非目标端和后端契约不受影响

- **WHEN** 本 Change 实现完成
- **THEN** 店主 Web 展示端与微信小程序页面 MUST 不受影响
- **AND** 后端 API 请求、响应、错误码、OpenAPI、Orval、SQLite/MySQL schema、Pydantic Schema、Docker Compose、MinIO 与媒体上传后端链路 MUST 保持不变
- **AND** 若实现阶段发现必须触及上述范围，MUST 回到需求评审或拆分独立 REQ/Change。

#### Scenario: 登录和无权限页移动端回归

- **WHEN** 用户在 `375x812` 或 `390x844` 访问 `/admin/login`
- **THEN** 登录页 MUST 保持 `<1024px` 单栏契约，左侧品牌区隐藏，登录表单居中且最大宽度不超过既有约束
- **AND** 账号、密码、记住登录状态、登录按钮和语言占位 MUST 可见且可操作
- **WHEN** 用户在移动视口访问 `/admin/forbidden`
- **THEN** 无权限页文案和返回或跳转入口 MUST 可读、可点击且不溢出。

### Requirement: Web 管理端列表与分页移动端基础可用

Web 管理端列表型页面 MUST 在手机和小屏平板视口下保持筛选区、指标卡、表格、分页和行内操作基础可用。适用页面 MUST 包含 `/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/users`、`/admin/logs` 与 `/admin/api-docs`。列表页 MUST 保留既有管理端列表横切一致性契约，包括模块顺序、指标卡 DOM、固定 toast、DS confirm modal、固定操作列与统一分页 DOM。

#### Scenario: 筛选区移动端降级

- **WHEN** 用户在 `≤1023px` 视口访问任一适用列表页
- **THEN** 筛选区 MUST 降为 2 列、1 列或等价适配布局
- **AND** 在 `≤639px` 视口下筛选输入框、选择框、重置按钮和其他筛选控件 MUST 不重叠、不超出父容器且可键盘聚焦
- **AND** 筛选控件变化或重置后 MUST 保持既有业务筛选行为和权限边界。

#### Scenario: 表格滚动限制在容器内

- **WHEN** 任一适用列表页的表格内容宽于移动视口
- **THEN** 横向滚动 MUST 限制在 `table-card` 或等价表格容器内
- **AND** 页面 body、Shell、`.main-content` 与 `.content-inner` MUST NOT 出现不可控横向滚动
- **AND** 关键标识列、状态列和操作列 MUST 可访问；隐藏次要列时 MUST NOT 隐藏核心操作。

#### Scenario: 分页移动端可操作

- **WHEN** 任一适用列表页在 `375px` 宽度展示分页
- **THEN** 分页 MUST 使用左侧 `page-summary` 与右侧 `page-right` 的统一结构
- **AND** `.page-buttons`、上一页、下一页、每页条数和总数摘要 MUST 可换行或分组展示
- **AND** 页码和每页条数控件 MUST 不互相覆盖，且可点击页码数量仍 MUST 不超过 5 个。

#### Scenario: 列表横切 AC 保持

- **WHEN** 本 Change 触及任一适用列表页
- **THEN** 指标卡 MUST 保留 `.metric-label`、`.metric-value`、`.metric-desc` 或等价共享结构
- **AND** 操作成功或失败反馈 MUST 使用 fixed toast 或等价固定反馈区域，不得用文档流 notice 推挤 hero、筛选区或表格
- **AND** 启停、上下架、冻结、删除、重置密码等风险操作 MUST 使用 DS confirm modal，MUST NOT 使用 `window.confirm`。

### Requirement: Web 管理端表单弹窗与抽屉移动端基础可用

Web 管理端表单页、业务弹窗、确认弹窗与日志详情抽屉 MUST 在 `375px` 宽度及移动视口高度下保持可读、可滚动、可关闭和可提交。适用范围 MUST 包含品牌、Banner、类目、规格、SKU、用户、重置密码、修改密码、系统设置确认、日志详情抽屉以及已有上传控件所在弹窗或表单。

#### Scenario: 业务弹窗窄屏可操作

- **WHEN** 用户在 `375px` 宽度打开新增、编辑、状态确认、删除、重置密码、修改密码或系统设置确认弹窗
- **THEN** 弹窗 MUST 不超出视口宽度
- **AND** 头部标题、关闭按钮、内容区和底部操作区域 MUST 可访问
- **AND** 矮视口下弹窗 body MUST 可滚动，底部主操作按钮不得丢失。

#### Scenario: 宽弹窗保留专属宽度策略

- **WHEN** 用户在移动视口打开 SKU、Banner 或等价大表单弹窗
- **THEN** 弹窗 MUST 保留专属 card class 或等价宽度策略，MUST NOT 同时挂载通用 `modal-card` 与专属类导致 CSS 层叠覆盖
- **AND** 实现验收 MUST 检查 computed width 与 max-width，而不只检查源 CSS
- **AND** 关闭按钮、取消按钮和主操作按钮 MUST 可点击。

#### Scenario: 表单和设置页移动端可读

- **WHEN** 用户在移动视口访问 `/admin/profile` 或 `/admin/settings/:tab`
- **THEN** 主信息、账号安全、设置导航、配置字段、保存、重置和确认入口 MUST 单列或等价可读布局展示
- **AND** 全页主要保存 CTA MUST 仅保留一处
- **AND** dirty Tab 切换、恢复默认、修改密码取消等风险操作 MUST 使用 DS modal，MUST NOT 使用 `window.confirm` 或 `window.alert`。

#### Scenario: 日志详情抽屉移动端可关闭可滚动

- **WHEN** 用户在手机宽度打开 `/admin/logs` 的日志详情抽屉
- **THEN** 抽屉 MUST 可关闭
- **AND** 详情内容 MUST 可滚动查看
- **AND** 抽屉宽度 MUST NOT 导致页面整体横向失控滚动。

#### Scenario: 上传控件移动端状态不回归

- **WHEN** 用户在移动视口使用品牌 Logo、Banner 图片、SKU 图片/视频或用户头像等已有上传控件
- **THEN** 上传控件 MUST 保持 `idle -> uploading -> done/failed` 或等价状态机可见
- **AND** 同会话上传成功后 MUST 即时回显缩略图或文件卡片
- **AND** 上传失败信息 MUST 展示在控件附近、既有错误区域或 fixed toast 中，且不得遮挡底部操作按钮
- **AND** 本 Change MUST NOT 新增媒体 API、存储桶、上传大小限制、Nginx 或 Docker 配置。

### Requirement: Web 管理端移动端 smoke 验收

Web 管理端移动端适配实现 MUST 补充 Playwright 或等价浏览器 smoke 验收。smoke MUST 以固定视口和必测页面矩阵验证基础可用性，并在 Change trace 或等价验收记录中说明结果、N/A 理由和剩余风险。

#### Scenario: 必测页面 smoke 覆盖

- **WHEN** 实现阶段运行移动端 smoke 验收
- **THEN** 必测路由 MUST 至少包含 `/admin/login`、`/admin/dashboard`、`/admin/tile-skus`、`/admin/brands`、`/admin/users`、`/admin/logs` 与 `/admin/settings/basic`
- **AND** smoke MUST 覆盖 `375x812`、`390x844`、`768x1024` 与 `1440x1024`
- **AND** 每个必测路由 MUST 记录页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选或分页不可操作检查结果。

#### Scenario: 测试命令和截图证据

- **WHEN** 本 Change apply 完成
- **THEN** `pnpm --dir src/web test` 或项目等价前端测试 MUST 通过；若只执行子集，MUST 在 trace 中记录原因和剩余风险
- **AND** SHOULD 补充移动端 Playwright screenshot、trace 或等价截图，覆盖至少一个宽表格页面、一个业务弹窗、一个 Shell/Dashboard 页面和一个设置或表单页面
- **AND** 本 Change 不要求 Orval；若实现阶段改 API，MUST 重新运行 OpenAPI/Orval 门禁。

