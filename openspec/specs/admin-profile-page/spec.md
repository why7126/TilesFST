# 管理端个人资料页规范

## Purpose
定义管理端个人资料 self-service API、操作记录、头像上传、备注字段和个人资料页视觉交互要求，确保 admin 与 employee 可安全维护本人资料。
## Requirements
### Requirement: 个人资料 self-service API

系统 MUST 提供当前登录用户（`admin` 或 `employee`）的个人资料 self-service API：`GET /api/v1/profile/me` 与 `PATCH /api/v1/profile/me`。接口 MUST 使用 `require_admin_access` 鉴权。`store_owner` MUST NOT 调用上述接口。`PATCH /api/v1/profile/me` 写入非空 `avatar_object_key` 前 MUST 校验该 key 对应对象存在且可通过后端对象存储适配层受控读取；对象不存在、权限异常或读取失败时 MUST 返回统一错误响应，并 MUST NOT 更新用户资料。清空头像 key 的空值语义 MUST 保持可用。

#### Scenario: 获取完整个人资料

- **WHEN** `admin` 或 `employee` 携带有效 token 请求 `GET /api/v1/profile/me`
- **THEN** 系统返回 HTTP 200
- **AND** `data` MUST 包含 id、username、display_name、role、status、email、phone、remark、avatar_object_key、avatar_url（非空时）、last_login_at、updated_at

#### Scenario: 更新个人资料

- **WHEN** 用户 PATCH 合法 `display_name`（2–32 字符）、email、phone、remark（≤200 字）
- **THEN** 系统返回 HTTP 200 与更新后 profile
- **AND** MUST 写入 `profile_activity_logs`（`action_type=profile_update`）

#### Scenario: 拒绝写入不存在的头像对象 key

- **GIVEN** 当前登录用户具备 profile self-service 权限
- **WHEN** 用户 PATCH 非空 `avatar_object_key` 且该 key 对应 object 不存在或不可读
- **THEN** 系统 MUST 返回统一业务错误响应
- **AND** 用户资料中的 `avatar_object_key` MUST 保持原值
- **AND** 错误响应 MUST NOT 暴露对象存储 endpoint、bucket、access key、secret key 或底层 SDK 堆栈

#### Scenario: 允许清空头像 key

- **GIVEN** 当前登录用户已有头像 key
- **WHEN** 用户 PATCH `avatar_object_key=null` 或等价清空语义
- **THEN** 系统 MUST 成功清空头像字段
- **AND** 返回的 profile MUST 不包含可加载头像 URL 或返回空头像 URL 语义

### Requirement: 个人资料操作记录 API

系统 MUST 提供 `GET /api/v1/profile/me/activities`，返回当前用户最近 **5** 条 `profile_activity_logs`，按 `created_at` 降序。

#### Scenario: 查询操作记录

- **WHEN** 用户请求 activities
- **THEN** 系统返回 HTTP 200
- **AND** 每条记录 MUST 包含 id、action_type、summary、created_at
- **AND** 默认 limit MUST 为 **5**
- **AND** 当用户记录数超过 5 时，响应 MUST 最多包含 5 条

#### Scenario: 无记录空列表

- **WHEN** 用户无任何 audit 记录
- **THEN** 系统返回 HTTP 200 与空数组
- **AND** MUST NOT 返回错误

### Requirement: 个人资料活动审计表

系统 MUST 维护 `profile_activity_logs` 表，字段含 id、user_id、action_type、summary、metadata（JSON 可选）、created_at。`action_type` MUST 至少支持 `profile_update`、`avatar_update`、`login`。

#### Scenario: 资料更新审计

- **WHEN** 用户 PATCH profile 成功
- **THEN** 系统 MUST 插入 `profile_update` 记录
- **AND** summary MUST 为可读中文摘要（如「修改昵称与备注」）

#### Scenario: 头像更新审计

- **WHEN** 用户 avatar_object_key 变更并成功持久化
- **THEN** 系统 MUST 插入 `avatar_update` 记录

#### Scenario: 登录审计

- **WHEN** 用户登录成功
- **THEN** 系统 MUST 插入 `login` 记录（与 `login_logs` 并存）
- **AND** summary MAY 为「安全登录成功」

### Requirement: 用户备注字段

系统 MUST 在 `users` 表提供 `remark` 字段（TEXT NULL，0–200 字），供个人资料 self-service 读写。管理员用户管理 API 本期 MAY NOT 暴露 remark 编辑（仅 profile PATCH）。

#### Scenario: 备注长度校验

- **WHEN** PATCH remark 超过 200 字
- **THEN** 系统 MUST 返回 HTTP 400 及校验错误

### Requirement: 管理端个人资料页面

Web 客户端 MUST 提供 `/admin/profile` 页面，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html` 与 `profile-page.png` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。页面 MUST 仅保留 **一处**「保存修改」主 CTA，MUST 位于「基础资料」卡片底部 `profile-form-actions` 与「重置」并列；MUST NOT 在页头 `profile-page-head` 与表单底部重复渲染相同主按钮。个人资料页头像图片加载失败时 MUST 稳定回退到当前用户 initials，占位尺寸 MUST 保持稳定且 MUST NOT 展示破损图片。

#### Scenario: 访问个人资料页

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 展示眉标 `SYSTEM / PROFILE`、标题「个人资料」、两列 layout（主卡片 + 侧栏卡片）
- **AND** 样式 MUST 主要来自 port CSS（如 `profile-page.css`）

#### Scenario: 个人资料头像加载失败兜底

- **GIVEN** `/api/v1/profile/me` 返回非空 `avatar_url`
- **WHEN** 该头像图片加载失败
- **THEN** 个人资料页 MUST 显示当前用户 initials fallback
- **AND** MUST NOT 展示破损图片
- **AND** fallback 前后头像区域尺寸 MUST 保持稳定

### Requirement: 个人资料头像 self-upload

已认证 `admin` 或 `employee` MUST 可通过授权上传接口上传本人头像（JPG/PNG/WebP，≤2MB），写入 MinIO 或 S3 兼容对象存储，并更新 `avatar_object_key`。上传失败 MUST 保留旧头像并展示错误。上传成功后用于 profile 更新的 `object_key` MUST 能通过后端受控 `/media/{object_key}` 或等价 URL 读取。头像上传链路 MUST 避免 WebP thumbnail 生成长尾阻塞接口到 30 秒级，并 MUST 通过阶段级 Task Trace spans 保留慢点归属。

#### Scenario: 运营人员上传头像

- **WHEN** `employee` 在个人资料页选择合法头像文件
- **THEN** 系统 MUST 允许 upload 并成功 PATCH profile
- **AND** MUST 写入 `avatar_update` audit

#### Scenario: 上传头像后对象与 URL 可读

- **GIVEN** 用户通过个人资料页上传合法头像且上传接口返回 `object_key`
- **WHEN** 用户使用该 `object_key` 保存个人资料
- **THEN** profile 更新 MUST 成功
- **AND** `/media/{object_key}` 或等价受控 URL MUST 返回可读图片
- **AND** `GET /api/v1/profile/me` 返回的 `avatar_url` MUST 与受控媒体读取策略一致

#### Scenario: WebP 头像 thumbnail 生成不造成 30 秒级等待

- **GIVEN** 已认证 `admin` 或 `employee` 上传 127KB 级合法 WebP 头像
- **WHEN** 后端同步处理原图写入和适用的 thumbnail / display 派生图
- **THEN** 上传接口 MUST NOT 因 `thumbnail_generate` 阶段阻塞到 30 秒级等待
- **AND** Task Trace MUST 记录 `thumbnail_generate` 阶段耗时与状态
- **AND** `original_put_object`、`thumbnail_put_object` 或等价对象写入阶段 MUST 与派生图生成阶段分开记录
- **AND** 验收 MUST 使用同一样本或等价 WebP 样本记录接口总耗时、阶段耗时和 request/task trace id 摘要

#### Scenario: 头像派生图生成失败或降级可解释

- **GIVEN** 头像 thumbnail 或 display 生成失败、超时保护触发或按策略跳过
- **WHEN** 上传接口返回成功或失败
- **THEN** 系统 MUST 保留已完成阶段 spans
- **AND** 失败或跳过阶段 MUST 有脱敏错误摘要、状态或稳定跳过依据
- **AND** 上传响应 MUST NOT 返回不存在或不可读的 thumbnail / display key
- **AND** 上传失败时 MUST 保留旧头像并向管理端展示可理解失败态

### Requirement: 个人资料 PNG 视觉验收 Gate

个人资料页视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: Profile PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/profile` 与 `profile-page.png`
- **THEN** checklist（Shell、用户菜单高亮、两列 layout、save-tip、timeline、分隔线等）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md`

