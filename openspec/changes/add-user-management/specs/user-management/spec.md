## ADDED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key（或 avatar_url）、email、phone、last_login_at、created_at

#### Scenario: 非管理员被拒绝

- **WHEN** `employee` 或 `store_owner` 请求 `GET /api/v1/admin/users`
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

### Requirement: 管理端用户创建 API

系统 MUST 提供 `POST /api/v1/admin/users`，仅 `admin` 可调用。请求 MUST 接受 username、可选 display_name、role、可选 avatar_object_key。新用户 status MUST 默认为 `active`。系统 MUST 生成随机初始密码并在响应 `data.initial_password` 中一次性返回明文；数据库 MUST 仅存 bcrypt 哈希。

#### Scenario: 创建用户成功

- **WHEN** `admin` 提交合法 username（4–32 位及格式规则）、role 与可选字段
- **THEN** 系统返回 HTTP 200，包含用户对象与 `initial_password`
- **AND** 用户 status MUST 为 `active`

#### Scenario: 用户名重复

- **WHEN** username 已存在
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `USER_USERNAME_TAKEN`

#### Scenario: 用户名格式非法

- **WHEN** username 不满足 4–32 位、字符集、保留字或连续特殊符号规则
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `USER_INVALID_USERNAME`

### Requirement: 管理端用户更新 API

系统 MUST 提供 `GET /api/v1/admin/users/{id}` 与 `PATCH /api/v1/admin/users/{id}`，仅 `admin` 可调用。PATCH MUST 允许更新 display_name、role、avatar_object_key；username MUST NOT 可修改。

#### Scenario: 更新昵称与角色

- **WHEN** `admin` PATCH 合法 display_name（可为空，最多 32 字符）与 role
- **THEN** 系统返回 HTTP 200 与更新后用户对象

#### Scenario: 禁止修改用户名

- **WHEN** 请求体包含 username 字段试图修改
- **THEN** 系统 MUST 忽略或返回 HTTP 400

### Requirement: 管理端重置密码 API

系统 MUST 提供 `POST /api/v1/admin/users/{id}/reset-password`，仅 `admin` 可调用。系统 MUST 生成 ≥12 位随机密码（含大小写、数字、特殊字符，排除易混淆字符）并在响应中一次性返回明文；后续 GET 接口 MUST NOT 再返回该密码。

#### Scenario: 重置密码成功

- **WHEN** `admin` 对存在且非 `deleted` 的用户调用重置密码
- **THEN** 系统返回 HTTP 200，`data.password` 为一次性明文
- **AND** 用户 password_hash MUST 已更新

### Requirement: 管理端用户状态变更 API

系统 MUST 提供 `PATCH /api/v1/admin/users/{id}/status`，仅 `admin` 可调用，用于冻结（`disabled`）、解冻（`active`）与软删除（`deleted`）。

#### Scenario: 冻结与解冻

- **WHEN** `admin` 将 `active` 用户设为 `disabled` 或反向
- **THEN** 系统返回 HTTP 200 且 status 已更新

#### Scenario: 软删除仅从未登录用户

- **WHEN** `admin` 对 `last_login_at` 非空的用户请求 `deleted`
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `USER_CANNOT_DELETE_LOGGED_IN`

#### Scenario: 软删除成功

- **WHEN** `admin` 对从未登录用户请求 `deleted`
- **THEN** 系统返回 HTTP 200 且 status 为 `deleted`

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容 max-width 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。

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
- **AND** 分页 MUST 支持 10/20/50 与范围展示如 `1-10 / N`

### Requirement: 管理端用户表单弹窗

Web 客户端 MUST 提供添加/编辑用户弹窗，视觉对齐 `user-management-modal.html` / `user-management-modal.png`。弹窗字段 MUST 为单列，顺序固定为：用户名、头像、昵称、角色。弹窗 MUST NOT 展示状态字段。

#### Scenario: 添加用户弹窗

- **WHEN** 用户点击「添加用户」
- **THEN** MUST 打开弹窗，用户名可编辑且必填
- **AND** 提交成功后 MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password` MUST 展示一次性密码弹窗与复制按钮

#### Scenario: 编辑用户弹窗

- **WHEN** 用户点击「编辑」
- **THEN** 用户名字段 MUST 只读
- **AND** 提交成功后 MUST Toast「用户信息已更新」

### Requirement: 管理端用户列表行操作

用户列表操作列 MUST 提供：编辑、重置密码、冻结/解冻、删除。已冻结用户 MUST 显示「解冻」；仅 `last_login_at` 为空的用户 MUST 启用「删除」，否则删除按钮 MUST 置灰。

#### Scenario: 重置密码交互

- **WHEN** 用户确认重置密码且 API 成功
- **THEN** MUST 在二次弹窗展示一次性密码与复制按钮
- **AND** 关闭后 MUST NOT 再次展示同一密码

#### Scenario: 冻结解冻 Toast

- **WHEN** 冻结或解冻成功
- **THEN** MUST 分别 Toast「用户已冻结」「用户已恢复正常」

#### Scenario: 删除 Toast

- **WHEN** 软删除成功
- **THEN** MUST Toast「用户已删除」

### Requirement: 管理端用户管理 PNG 视觉验收 Gate

用户管理页视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: 列表 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/users` 与 `user-management-list.png`
- **THEN** diff checklist（Shell、筛选 6 列、4 指标卡、表格、分页、添加按钮品牌金、激活「用户管理」菜单等）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗 PNG 并排验收

- **WHEN** 团队打开添加用户弹窗并对比 `user-management-modal.png`
- **THEN** checklist（520px 宽、单列字段顺序、遮罩、主按钮品牌金等）MUST pass

### Requirement: 用户管理角色文案映射

前端 MUST 将 API 返回的 `role` 映射为产品文案： `store_owner`→「前台用户」、`employee`→「后台运营」、`admin`→「后台管理员」。状态 MUST 映射：`active`→「正常」、`disabled`→「已冻结」、`deleted`→「已删除」。

#### Scenario: 列表角色 badge

- **WHEN** 用户查看列表角色列
- **THEN** MUST 展示上述中文文案与原型 badge 风格（非原始 enum 字符串）
