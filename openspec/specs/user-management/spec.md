# 用户管理规范

## Purpose
定义管理端用户列表、创建、更新、重置密码、状态变更、受保护账号策略和头像字段展示要求，确保管理员账号维护安全且可审计。
## Requirements
### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`。当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 或等价受控媒体 URL，且 SHOULD 对应可加载对象；若历史数据漂移导致对象缺失，系统 MUST 通过数据修复或安全 fallback 避免用户可见破损头像。

系统 MUST 以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护系统账号。用户列表中每条用户记录 MUST 返回 `is_protected` 与 `protected_reason` 字段；受保护账号 MUST 返回 `is_protected=true` 与明确中文原因，普通用户 MUST 返回 `is_protected=false` 且 `protected_reason=null`。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at、is_protected、protected_reason
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且使用受控媒体 URL

### Requirement: 管理端用户创建 API

系统 MUST 提供 `POST /api/v1/admin/users`，仅 `admin` 可调用。请求 MUST 接受 username、可选 display_name、role、可选 avatar_object_key、可选 email、可选 phone。新用户 status MUST 默认为 `active`。系统 MUST 生成满足统一基础密码策略（5-32 位、包含 ASCII 英文字符、包含 ASCII 数字）的随机初始密码，并在响应 `data.initial_password` 中一次性返回明文；数据库 MUST 仅存 bcrypt 哈希。

`email` 和 `phone` 仅作为联系信息，MUST 允许为空，MUST NOT 要求唯一，MUST NOT 影响登录、权限、密码重置或账号状态判断。`email` 非空时 MUST 校验邮箱格式；`phone` 非空时 MUST 仅允许数字、空格、`+`、`-`，且 MUST NOT 绑定单一国家或地区号码格式。空白字符串 MUST 保存为 `null`。

用户名、联系邮箱或手机号码校验失败时，系统 MUST 返回项目统一错误结构 `{ code, message, data }`，MUST NOT 将 FastAPI 默认 422 `detail` 列表作为面向前端用户的唯一错误体。

#### Scenario: 创建用户成功并保存联系信息

- **WHEN** `admin` 提交合法 username、role、可选 email、可选 phone
- **THEN** 系统返回 HTTP 200，包含用户对象与 `initial_password`
- **AND** 用户 status MUST 为 `active`
- **AND** 响应用户对象 MUST 包含保存后的 `email` 与 `phone`
- **AND** `initial_password` MUST 满足 5-32 位、包含英文字符、包含数字

#### Scenario: 创建用户时联系信息为空

- **WHEN** `admin` 提交 `email=""` 或 `phone=""`
- **THEN** 系统 MUST 成功创建用户
- **AND** 对应字段 MUST 保存并返回为 `null`

#### Scenario: 联系信息不要求唯一

- **GIVEN** 已存在某用户的 `email` 或 `phone`
- **WHEN** `admin` 创建另一个用户并提交相同 `email` 或 `phone`
- **THEN** 系统 MUST 允许创建
- **AND** MUST NOT 返回唯一性冲突错误

#### Scenario: 邮箱格式非法

- **WHEN** `admin` 提交非法 `email`
- **THEN** 系统 MUST 返回统一业务错误响应
- **AND** `message` MUST 明确说明联系邮箱格式非法或等价中文原因

#### Scenario: 手机号码格式非法

- **WHEN** `admin` 提交包含数字、空格、`+`、`-` 之外字符的 `phone`
- **THEN** 系统 MUST 返回统一业务错误响应
- **AND** `message` MUST 明确说明手机号码格式非法或等价中文原因

### Requirement: 管理端用户更新 API

系统 MUST 提供 `GET /api/v1/admin/users/{id}` 与 `PATCH /api/v1/admin/users/{id}`，仅 `admin` 可调用。GET 返回的用户对象 MUST 包含 `is_protected`、`protected_reason`、`email`、`phone`。PATCH MUST 允许更新 display_name、role、avatar_object_key、email、phone；username MUST NOT 可修改。当目标用户为受保护账号时，PATCH MUST 返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 display_name、role、avatar_object_key、email、phone 或其他用户资料字段。写入非空 `avatar_object_key` 时 SHOULD 与 profile self-service API 保持一致的对象存在性校验；若本次实现范围不修改管理员代改接口，MUST 在验收记录中说明差异和后续处理方式。

`email` 与 `phone` 字段缺省时 MUST 保持原值；显式传入 `null` 或空白字符串时 MUST 清空对应字段。

#### Scenario: 更新昵称、角色与联系信息

- **WHEN** `admin` PATCH 合法 display_name、role、email、phone
- **THEN** 系统返回 HTTP 200 与更新后用户对象
- **AND** 响应用户对象 MUST 包含更新后的 `email` 与 `phone`

### Requirement: 管理端重置密码 API

系统 MUST 提供 `POST /api/v1/admin/users/{id}/reset-password`，仅 `admin` 可调用。系统 MUST 生成满足统一基础密码策略（5-32 位、包含 ASCII 英文字符、包含 ASCII 数字）的随机密码，并在响应中一次性返回明文；后续 GET 接口 MUST NOT 再返回该密码。当目标用户为受保护账号时，系统 MUST 返回 HTTP 403 与已登记错误码，MUST NOT 生成新随机明文密码，MUST NOT 更新 `password_hash`。

#### Scenario: 重置密码成功

- **WHEN** `admin` 对存在且非 `deleted` 的用户调用重置密码
- **THEN** 系统返回 HTTP 200，`data.password` 为一次性明文
- **AND** 用户 password_hash MUST 已更新
- **AND** 生成密码 MUST 满足 5-32 位、包含英文字符、包含数字

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

#### Scenario: 用户列表头像加载失败兜底

- **GIVEN** 用户列表记录包含非空 `avatar_url`
- **WHEN** 头像图片加载失败
- **THEN** 用户列表 MUST 显示 initials fallback
- **AND** MUST NOT 展示破损图片
- **AND** 表格行高与布局 MUST 保持稳定

### Requirement: 管理端用户表单弹窗

Web 客户端 MUST 提供添加/编辑用户弹窗，视觉对齐 `user-management-modal.html` / `user-management-modal.png`。弹窗字段 MUST 为单列，顺序固定为：用户名、头像、昵称、联系邮箱、手机号码、角色。弹窗整体 MUST 靠近视口顶部展示，避免因垂直居中在顶部留下过大空隙；弹窗标题区 MUST 紧凑展示，避免标题上方出现过大空隙；若使用专属样式作用域，MUST 保持 `modal-card` 宽度来源单一，避免与专属 card 类双挂载。弹窗 MUST NOT 展示状态字段。头像区 MUST 支持选择文件后立即上传、上传进度反馈、上传成功预览更新与失败重试，行为 MUST 对齐已修复的品牌 Logo 弹窗（`idle → uploading → uploaded / failed` 状态机）。编辑时 MUST 回显已有头像图片、联系邮箱和手机号码。添加用户成功且 API 返回 `initial_password` 时，Web 客户端 MUST 展示一次性密码结果弹窗，并 MUST 提供可靠复制、成功反馈和剪贴板失败 fallback。

#### Scenario: 添加用户弹窗包含联系信息

- **WHEN** 用户点击「添加用户」
- **THEN** MUST 打开弹窗，字段顺序为用户名、头像、昵称、联系邮箱、手机号码、角色
- **AND** 联系邮箱和手机号码均可为空
- **AND** 弹窗整体不应因垂直居中在视口顶部留下过大空隙
- **AND** 弹窗标题上方不应出现过大空隙
- **AND** 提交成功后 MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password` MUST 展示一次性密码弹窗与复制按钮

#### Scenario: 编辑用户弹窗回填并清空联系信息

- **WHEN** 用户点击「编辑」
- **THEN** 用户名字段 MUST 只读
- **AND** 已有头像 MUST 展示图片预览
- **AND** 联系邮箱与手机号码 MUST 回填当前值
- **WHEN** 管理员清空联系邮箱或手机号码并保存
- **THEN** Web 客户端 MUST 提交空值语义
- **AND** 保存成功后再次打开编辑弹窗，对应字段 MUST 为空

#### Scenario: 字段级错误提示

- **WHEN** 联系邮箱或手机号码校验失败
- **THEN** Web 客户端 MUST 在对应字段或字段组附近展示可理解错误提示
- **AND** MUST NOT 仅依赖全局 Toast

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

