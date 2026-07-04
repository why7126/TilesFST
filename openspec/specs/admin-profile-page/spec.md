# 管理端个人资料页规范

## Purpose
定义管理端个人资料 self-service API、操作记录、头像上传、备注字段和个人资料页视觉交互要求，确保 admin 与 employee 可安全维护本人资料。
## Requirements
### Requirement: 个人资料 self-service API

系统 MUST 提供当前登录用户（`admin` 或 `employee`）的个人资料 self-service API：`GET /api/v1/profile/me` 与 `PATCH /api/v1/profile/me`。接口 MUST 使用 `require_admin_access` 鉴权。`store_owner` MUST NOT 调用上述接口。

#### Scenario: 获取完整个人资料

- **WHEN** `admin` 或 `employee` 携带有效 token 请求 `GET /api/v1/profile/me`
- **THEN** 系统返回 HTTP 200
- **AND** `data` MUST 包含 id、username、display_name、role、status、email、phone、remark、avatar_object_key、avatar_url（非空时）、last_login_at、updated_at

#### Scenario: 更新个人资料

- **WHEN** 用户 PATCH 合法 `display_name`（2–32 字符）、email、phone、remark（≤200 字）
- **THEN** 系统返回 HTTP 200 与更新后 profile
- **AND** MUST 写入 `profile_activity_logs`（`action_type=profile_update`）

#### Scenario: 禁止修改只读字段

- **WHEN** PATCH 请求包含 username、role 或 status
- **THEN** 系统 MUST 忽略或返回 HTTP 400
- **AND** MUST NOT 修改对应数据库字段

#### Scenario: 运营人员可 self-service

- **WHEN** `role=employee` 调用 profile API
- **THEN** 系统 MUST 允许访问

#### Scenario: 店主被拒绝

- **WHEN** `role=store_owner` 调用 profile API
- **THEN** 系统 MUST 返回 HTTP 403

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

Web 客户端 MUST 提供 `/admin/profile` 页面，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html` 与 `profile-page.png` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。页面 MUST 仅保留 **一处**「保存修改」主 CTA，MUST 位于「基础资料」卡片底部 `profile-form-actions` 与「重置」并列；MUST NOT 在页头 `profile-page-head` 与表单底部重复渲染相同主按钮。

#### Scenario: 访问个人资料页

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 展示眉标 `SYSTEM / PROFILE`、标题「个人资料」、两列 layout（主卡片 + 侧栏卡片）
- **AND** 样式 MUST 主要来自 port CSS（如 `profile-page.css`）

#### Scenario: 单保存入口

- **WHEN** 用户查看 `/admin/profile` 页面
- **THEN** 全页 MUST 仅存在 **1** 个 accessible name 为「保存修改」的主按钮
- **AND** 该按钮 MUST 位于「基础资料」卡片底部 `profile-form-actions`
- **AND** 页头 `profile-page-head` MUST NOT 渲染「保存修改」主按钮

#### Scenario: 表单字段与只读规则

- **WHEN** 用户查看主卡片表单
- **THEN** MUST 按顺序展示：用户名（只读）、昵称、联系邮箱、手机、备注
- **AND** MUST NOT 在主卡片表单内展示所属角色、账号状态（二者仅在账号安全卡片展示）
- **AND** 昵称 MUST 必填 2–32 字符

#### Scenario: 保存 inline 成功提示

- **WHEN** 用户点击「保存修改」并成功
- **THEN** MUST 在表单底部 inline 展示「资料已更新」及时间戳
- **AND** MUST NOT 使用全局 toast 承载该成功反馈

#### Scenario: 重置表单

- **WHEN** 用户点击「重置」
- **THEN** MUST 恢复最近一次 GET profile 快照

#### Scenario: 修改密码入口

- **WHEN** 用户点击账号安全卡片「修改密码」
- **THEN** MUST 打开 REQ-0015 密码修改弹窗（共用 hook）
- **AND** MUST NOT 导航至独立改密路由

#### Scenario: 操作记录 timeline

- **WHEN** 页面加载
- **THEN** MUST 展示最近 **5** 条 activities timeline（标题、时间、摘要）
- **AND** 当记录数不足 5 时 MUST 展示实际条数
- **AND** 无数据时 MUST 展示空态文案

### Requirement: 个人资料头像 self-upload

已认证 `admin` 或 `employee` MUST 可通过授权上传接口上传本人头像（JPG/PNG/WebP，≤2MB），写入 MinIO 并更新 `avatar_object_key`。上传失败 MUST 保留旧头像并展示错误。

#### Scenario: 运营人员上传头像

- **WHEN** `employee` 在个人资料页选择合法头像文件
- **THEN** 系统 MUST 允许 upload 并成功 PATCH profile
- **AND** MUST 写入 `avatar_update` audit

#### Scenario: 上传失败保留旧头像

- **WHEN** 上传失败
- **THEN** UI MUST 展示失败原因
- **AND** MUST NOT 清除已有头像展示

### Requirement: 个人资料 PNG 视觉验收 Gate

个人资料页视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: Profile PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/profile` 与 `profile-page.png`
- **THEN** checklist（Shell、用户菜单高亮、两列 layout、save-tip、timeline、分隔线等）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md`
