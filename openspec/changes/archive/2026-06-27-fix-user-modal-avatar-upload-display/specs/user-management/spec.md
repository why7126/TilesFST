# user-management Specification Delta

## MODIFIED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`（当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 形式且浏览器可加载）。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且可加载

#### Scenario: 非管理员被拒绝

- **WHEN** `employee` 或 `store_owner` 请求 `GET /api/v1/admin/users`
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容 max-width 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。用户列表「用户」列 MUST 在有 `avatar_url` 时展示头像图片，无头像时 MUST 展示 initials 占位；图片加载失败 MUST 稳定回退 initials 且不引起布局跳动。

#### Scenario: 管理员访问用户管理页

- **WHEN** `role=admin` 用户访问 `/admin/users`
- **THEN** MUST 展示页面标题「用户管理」、筛选区、4 指标卡、用户表格与分页
- **AND** 样式 MUST 主要来自 port CSS（`user-management.css`）

#### Scenario: 筛选与搜索交互

- **WHEN** 用户输入关键词或筛选项并点击「搜索」或按回车
- **THEN** 系统 MUST 带 query 重新请求列表并重置到第 1 页
- **WHEN** 用户点击「重置」
- **THEN** MUST 清空筛选并重新加载默认列表

#### Scenario: 列表字段与分页

- **WHEN** 用户查看表格
- **THEN** MUST 展示用户（头像+用户名+昵称/邮箱）、角色、状态、最后登录、创建时间、操作列
- **AND** 有 `avatar_url` 的用户 MUST 在头像位展示图片而非仅 initials
- **AND** 分页 MUST 支持 10/20/50 与范围展示如 `1-10 / N`

### Requirement: 管理端用户表单弹窗

Web 客户端 MUST 提供添加/编辑用户弹窗，视觉对齐 `user-management-modal.html` / `user-management-modal.png`。弹窗字段 MUST 为单列，顺序固定为：用户名、头像、昵称、角色。弹窗 MUST NOT 展示状态字段。头像区 MUST 支持选择文件后立即上传、上传进度反馈、上传成功预览更新与失败重试，行为 MUST 对齐已修复的品牌 Logo 弹窗（`idle → uploading → uploaded / failed` 状态机）。编辑时 MUST 回显已有头像图片。

#### Scenario: 添加用户弹窗

- **WHEN** 用户点击「添加用户」
- **THEN** MUST 打开弹窗，用户名可编辑且必填
- **AND** 提交成功后 MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password` MUST 展示一次性密码弹窗与复制按钮

#### Scenario: 编辑用户弹窗

- **WHEN** 用户点击「编辑」
- **THEN** 用户名字段 MUST 只读
- **AND** 已有头像 MUST 展示图片预览
- **AND** 提交成功后 MUST Toast「用户信息已更新」

#### Scenario: 更换头像上传与预览

- **WHEN** admin 在弹窗点击「更换头像」并选择合法 JPG/PNG/WebP
- **THEN** 系统 MUST 立即触发上传并进入 uploading 状态
- **AND** MUST 展示进度条或等价进度反馈
- **AND** 上传成功后 MUST 更新弹窗头像预览与待保存的 `avatar_object_key`
- **AND** 上传中 MUST 禁止提交保存
- **AND** 上传失败 MUST 展示错误并允许重试

#### Scenario: 保存后头像持久可见

- **WHEN** admin 更换头像并保存用户
- **THEN** 再次打开编辑弹窗 MUST 回显最新头像
- **AND** 用户列表 MUST 展示最新头像图片
