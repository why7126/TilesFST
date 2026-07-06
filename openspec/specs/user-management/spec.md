# 用户管理规范

## Purpose
定义管理端用户列表、创建、更新、重置密码、状态变更、受保护账号策略和头像字段展示要求，确保管理员账号维护安全且可审计。
## Requirements
### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`（当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 形式且浏览器可加载）。

系统 MUST 以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护系统账号。用户列表中每条用户记录 MUST 返回 `is_protected` 与 `protected_reason` 字段；受保护账号 MUST 返回 `is_protected=true` 与明确中文原因，普通用户 MUST 返回 `is_protected=false` 且 `protected_reason=null`。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at、is_protected、protected_reason
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且可加载

#### Scenario: 受保护账号在列表中带保护标识

- **GIVEN** `ADMIN_USERNAME=admin`
- **AND** 数据库存在 username 为 `admin` 的用户
- **WHEN** `admin` 请求 `GET /api/v1/admin/users`
- **THEN** 该用户记录 MUST 返回 `is_protected=true`
- **AND** `protected_reason` MUST 为明确中文说明
- **AND** 其他普通 `role=admin` 用户 MUST 返回 `is_protected=false`

#### Scenario: 非管理员被拒绝

- **WHEN** `employee` 或 `store_owner` 请求 `GET /api/v1/admin/users`
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

### Requirement: 管理端用户创建 API

系统 MUST 提供 `POST /api/v1/admin/users`，仅 `admin` 可调用。请求 MUST 接受 username、可选 display_name、role、可选 avatar_object_key。新用户 status MUST 默认为 `active`。系统 MUST 生成随机初始密码并在响应 `data.initial_password` 中一次性返回明文；数据库 MUST 仅存 bcrypt 哈希。

用户名校验失败时，系统 MUST 返回项目统一错误结构 `{ code, message, data }`，MUST NOT 将 FastAPI 默认 422 `detail` 列表作为面向前端用户的唯一错误体。`message` MUST 明确指出用户名字段与具体原因，至少覆盖长度、首字符、字符集、连续特殊符号与保留字。用户名长度不足或超长 SHOULD 返回 HTTP 400 与 `USER_INVALID_USERNAME`；若实现保留 HTTP 422，响应体仍 MUST 符合统一错误结构且包含明确中文 `message`。

#### Scenario: 创建用户成功

- **WHEN** `admin` 提交合法 username（4–32 位及格式规则）、role 与可选字段
- **THEN** 系统返回 HTTP 200，包含用户对象与 `initial_password`
- **AND** 用户 status MUST 为 `active`

#### Scenario: 用户名重复

- **WHEN** username 已存在
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `USER_USERNAME_TAKEN`
- **AND** 错误响应 MUST 保持统一 `{ code, message, data }` 结构

#### Scenario: 用户名长度不足

- **WHEN** `admin` 提交 `username="abc"` 创建用户
- **THEN** 系统 MUST 返回 HTTP 400 或统一 envelope 的 HTTP 422
- **AND** 响应体 MUST 包含 `code`、`message`、`data`
- **AND** 响应体 MUST NOT 仅包含 FastAPI 默认 `detail` 列表
- **AND** `message` MUST 明确说明用户名长度须为 4-32 位或等价中文原因

#### Scenario: 用户名格式非法

- **WHEN** username 不满足 4–32 位、字符集、保留字或连续特殊符号规则
- **THEN** 系统 MUST 返回 HTTP 400 或统一 envelope 的 HTTP 422
- **AND** 错误码 MUST 表示 `USER_INVALID_USERNAME` 或等价已登记用户校验错误
- **AND** `message` MUST 明确指出对应用户名规则

#### Scenario: 创建用户校验不影响重复用户名

- **GIVEN** 数据库已存在 username 为 `store_user_01` 的用户
- **WHEN** `admin` 再次提交同名用户
- **THEN** 系统 MUST 返回 HTTP 409
- **AND** 错误码与文案 MUST 仍明确表示用户名已存在

### Requirement: 管理端用户更新 API

系统 MUST 提供 `GET /api/v1/admin/users/{id}` 与 `PATCH /api/v1/admin/users/{id}`，仅 `admin` 可调用。GET 返回的用户对象 MUST 包含 `is_protected` 与 `protected_reason`。PATCH MUST 允许更新 display_name、role、avatar_object_key；username MUST NOT 可修改。当目标用户为受保护账号时，PATCH MUST 返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 display_name、role、avatar_object_key 或其他用户资料字段。

#### Scenario: 更新昵称与角色

- **WHEN** `admin` PATCH 合法 display_name（可为空，最多 32 字符）与 role
- **THEN** 系统返回 HTTP 200 与更新后用户对象

#### Scenario: 详情返回受保护标识

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `GET /api/v1/admin/users/{id}`
- **THEN** 响应用户对象 MUST 包含 `is_protected=true`
- **AND** `protected_reason` MUST 为明确中文说明

#### Scenario: 禁止修改用户名

- **WHEN** 请求体包含 username 字段试图修改
- **THEN** 系统 MUST 忽略或返回 HTTP 400

#### Scenario: 受保护账号禁止编辑

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `PATCH /api/v1/admin/users/{id}` 修改 display_name、role 或 avatar_object_key
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 数据库中的 display_name、role、avatar_object_key MUST 保持不变

### Requirement: 管理端重置密码 API

系统 MUST 提供 `POST /api/v1/admin/users/{id}/reset-password`，仅 `admin` 可调用。系统 MUST 生成满足 **effective** 密码策略的随机密码（长度与复杂度按 `system_settings` security 分组 merge 默认值）并在响应中一次性返回明文；后续 GET 接口 MUST NOT 再返回该密码。当目标用户为受保护账号时，系统 MUST 返回 HTTP 403 与已登记错误码，MUST NOT 生成新随机明文密码，MUST NOT 更新 `password_hash`。

#### Scenario: 重置密码成功

- **WHEN** `admin` 对存在且非 `deleted` 的用户调用重置密码
- **THEN** 系统返回 HTTP 200，`data.password` 为一次性明文
- **AND** 用户 password_hash MUST 已更新
- **AND** 生成密码 MUST 满足 effective 最小长度与复杂度开关

#### Scenario: 受保护账号禁止重置密码

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `POST /api/v1/admin/users/{id}/reset-password`
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 系统 MUST NOT 生成或返回新随机密码
- **AND** 目标用户 `password_hash` MUST 保持不变

### Requirement: 管理端用户状态变更 API

系统 MUST 提供 `PATCH /api/v1/admin/users/{id}/status`，仅 `admin` 可调用，用于冻结（`disabled`）、解冻（`active`）与软删除（`deleted`）。当目标用户为受保护账号时，系统 MUST 对任意状态变更返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 status。

#### Scenario: 冻结与解冻

- **WHEN** `admin` 将 `active` 用户设为 `disabled` 或反向
- **THEN** 系统返回 HTTP 200 且 status 已更新

#### Scenario: 软删除仅从未登录用户

- **WHEN** `admin` 对 `last_login_at` 非空的用户请求 `deleted`
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `USER_CANNOT_DELETE_LOGGED_IN`

#### Scenario: 软删除成功

- **WHEN** `admin` 对从未登录用户请求 `deleted`
- **THEN** 系统返回 HTTP 200 且 status 为 `deleted`

#### Scenario: 受保护账号禁止任意状态变更

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求将该用户状态变更为 `active`、`disabled` 或 `deleted`
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 目标用户 status MUST 保持原值

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。用户列表「用户」列 MUST 在有 `avatar_url` 时展示头像图片，无头像时 MUST 展示 initials 占位；图片加载失败 MUST 稳定回退 initials 且不引起布局跳动。

#### Scenario: 管理员访问用户管理页

- **WHEN** `role=admin` 用户访问 `/admin/users`
- **THEN** MUST 展示页面标题「用户管理」、筛选区、4 指标卡、用户表格与分页
- **AND** 样式 MUST 主要来自 port CSS（`user-management.css`）
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过页面级 max-width 退回 1080px。

#### Scenario: 筛选与搜索交互

- **WHEN** 用户输入关键词或筛选项并点击「搜索」或按回车
- **THEN** 系统 MUST 带 query 重新请求列表并重置到第 1 页
- **WHEN** 用户点击「重置」
- **THEN** MUST 清空筛选并重新加载默认列表。

#### Scenario: 列表字段与分页

- **WHEN** 用户查看表格
- **THEN** MUST 展示用户（头像+用户名+昵称/邮箱）、角色、状态、最后登录、创建时间、操作列
- **AND** 有 `avatar_url` 的用户 MUST 在头像位展示图片而非仅 initials。

### Requirement: 管理端用户表单弹窗

Web 客户端 MUST 提供添加/编辑用户弹窗，视觉对齐 `user-management-modal.html` / `user-management-modal.png`。弹窗字段 MUST 为单列，顺序固定为：用户名、头像、昵称、角色。弹窗 MUST NOT 展示状态字段。头像区 MUST 支持选择文件后立即上传、上传进度反馈、上传成功预览更新与失败重试，行为 MUST 对齐已修复的品牌 Logo 弹窗（`idle → uploading → uploaded / failed` 状态机）。编辑时 MUST 回显已有头像图片。添加用户成功且 API 返回 `initial_password` 时，Web 客户端 MUST 展示一次性密码结果弹窗，并 MUST 提供可靠复制、成功反馈和剪贴板失败 fallback。

#### Scenario: 添加用户弹窗

- **WHEN** 用户点击「添加用户」
- **THEN** MUST 打开弹窗，用户名可编辑且必填
- **AND** 提交成功后 MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password` MUST 展示一次性密码弹窗与复制按钮

#### Scenario: 创建用户后复制初始密码成功

- **GIVEN** `admin` 在 `/admin/users` 创建新用户成功
- **AND** API 返回 `data.initial_password`
- **WHEN** 一次性密码结果弹窗展示，管理员点击「复制密码」
- **THEN** Web 客户端 MUST 调用 Clipboard API 将当前弹窗展示的完整 `initial_password` 写入剪贴板
- **AND** MUST 展示复制成功反馈
- **AND** 粘贴内容 MUST 与弹窗展示密码一致

#### Scenario: 创建用户后剪贴板不可用 fallback

- **GIVEN** 一次性初始密码弹窗已展示
- **AND** 当前浏览器不支持 Clipboard API、剪贴板权限被拒绝，或 `writeText` 失败
- **WHEN** 管理员点击「复制密码」
- **THEN** Web 客户端 MUST NOT 静默失败
- **AND** MUST 展示失败提示或手动复制指引
- **AND** SHOULD focus/select 当前一次性密码文本，帮助管理员手动复制

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

### Requirement: 管理端用户列表行操作

用户列表操作列 MUST 提供：编辑、重置密码、冻结/解冻、删除。已冻结用户 MUST 显示「解冻」；仅 `last_login_at` 为空的用户 MUST 启用「删除」，否则删除按钮 MUST 置灰。当 `user.is_protected=true` 时，编辑、重置密码、冻结/解冻、删除按钮 MUST 保留但置灰，MUST 使用 `protected_reason` 作为 title、tooltip 或等价原因提示，且 MUST NOT 打开确认弹窗或调用对应 API。前端 MUST NOT 通过硬编码 `admin` 或 role 判断保护状态。重置密码成功且 API 返回 `data.password` 时，Web 客户端 MUST 展示一次性密码结果弹窗，并 MUST 提供可靠复制、成功反馈和剪贴板失败 fallback。一次性密码关闭后 MUST NOT 再次展示同一密码。

#### Scenario: 重置密码交互

- **WHEN** 用户确认重置密码且 API 成功
- **THEN** MUST 在二次弹窗展示一次性密码与复制按钮
- **AND** 关闭后 MUST NOT 再次展示同一密码

#### Scenario: 重置密码后复制新随机密码成功

- **GIVEN** `admin` 对非受保护用户确认重置密码成功
- **AND** API 返回 `data.password`
- **WHEN** 一次性密码结果弹窗展示，管理员点击「复制密码」
- **THEN** Web 客户端 MUST 调用 Clipboard API 将当前弹窗展示的完整 `password` 写入剪贴板
- **AND** MUST 展示复制成功反馈
- **AND** 粘贴内容 MUST 与弹窗展示密码一致

#### Scenario: 重置密码后剪贴板不可用 fallback

- **GIVEN** 一次性随机密码弹窗已展示
- **AND** 当前浏览器不支持 Clipboard API、剪贴板权限被拒绝，或 `writeText` 失败
- **WHEN** 管理员点击「复制密码」
- **THEN** Web 客户端 MUST NOT 静默失败
- **AND** MUST 展示失败提示或手动复制指引
- **AND** SHOULD focus/select 当前一次性密码文本，帮助管理员手动复制

#### Scenario: 一次性密码安全边界

- **WHEN** Web 客户端展示创建用户或重置密码后的一次性密码结果弹窗
- **THEN** 弹窗 MUST 继续提示「关闭后不可再次查看」或等价风险说明
- **AND** Web 客户端 MUST NOT 新增再次查询一次性明文密码的接口或入口
- **AND** Web 客户端 MUST NOT 将一次性明文密码写入 localStorage、sessionStorage、URL、日志、审计事件或长期文档

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

