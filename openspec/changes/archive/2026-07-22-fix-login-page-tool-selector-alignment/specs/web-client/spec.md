## MODIFIED Requirements

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
