---
requirement_id: REQ-0015-password-change
title: 管理端修改密码（侧栏入口 + 居中弹窗）
terminal: web-admin
version: v1
status: approved
owner: product
source: issues/requirements/archive/REQ-0015-password-change/capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
created_at: 2026-06-28 09:55:31
updated_at: 2026-06-28 10:01:12
---

# REQ-0015 管理端修改密码（侧栏入口 + 居中弹窗）

## 1. 需求背景

管理后台左侧底部用户菜单（`REQ-0004-admin-home`）包含「个人资料、密码修改、退出登录」。当前「密码修改」为占位入口。本期补齐**登录用户修改本人密码**能力，降低管理员通过用户管理「重置密码」的人工成本。

本需求基于用户管理列表页视觉与 `rules/ui-design.md` 工业石材暗色旗舰风，采用**居中弹窗**承载表单，不改变各业务页主体信息架构。原型优先级见 `prototype/web/password-change-modal.html` > `password-change-modal.png` > `password-change-modal-context.md`。

`/req-explore` 已确认：API 路径 `POST /api/v1/admin/profile/password`；改密成功后**全端 token 失效**（`users.token_version`）；本期启用弱密码校验与改密限流；与 `REQ-0014-profile-page` **共享弹窗组件**，无独立路由。

## 2. 目标用户

| 角色 | 权限 |
|------|------|
| 后台管理员 | 可修改本人密码 |
| 后台运营 / 内部员工 | 可修改本人密码 |
| 前台用户（店主端） | 不进入管理后台，本需求不覆盖 |

## 3. 范围

### 3.1 本期包含

- 侧栏底部用户菜单「密码修改」入口（替换现有 `onPlaceholder` 占位）
- 520px 居中弹窗：`ChangePasswordModal`（原密码 / 新密码 / 确认新密码）
- 密码显隐切换、前端即时校验、规则提示列表、inline 错误态
- 保存 / 取消 / 关闭（×、Esc）；脏表单关闭二次确认
- 保存中 loading；成功后 Toast + 清理登录态 + 跳转 `/admin/login`
- 后端 `POST /api/v1/admin/profile/password`；`users.token_version` 迁移与 JWT `tv` 校验
- 服务端密码策略、弱密码表、改密失败/成功频率限流
- `AdminLayout` 托管 modal；预留 `openChangePasswordModal` 供 `REQ-0014` 账号安全卡片复用
- OpenAPI / Orval 同步；前后端测试

### 3.2 本期不包含

- 忘记密码、短信 / 邮箱 / 图形验证码
- 管理员替他人重置密码（已有 `POST /api/v1/admin/users/{id}/reset-password`，见 `REQ-0005-user-management`）
- 多因素认证
- 独立页面路由（如 `/admin/profile/password`）
- 店主端 Web、微信小程序
- 历史密码 N 代不可重复（后续增强）

## 4. 入口与 UI 形态

### 4.1 入口

- 位置：管理后台 `AdminSidebar` 底部 `AdminUserMenu`
- 用户点击用户信息卡展开菜单：个人资料 → **密码修改** → 分隔线 → 退出登录
- 点击「密码修改」MUST 打开 `ChangePasswordModal`（非跳转页面）

### 4.2 弹窗形态

- 宽度 **520px**；居中；遮罩语义 token（原型 `rgba(0,0,0,.62)`，实现 MUST 使用 DS semantic class，禁止裸 Hex）
- 标题：**修改密码**；副标题展示当前账号显示名（如「当前账号：Admin User」）
- 说明区：左侧 2px 品牌金竖线 + 安全提示文案
- 弹窗打开时主体 MUST NOT 滚动；背景可识别但不可操作

### 4.3 与 REQ-0014 协作

- `ChangePasswordModal` MUST 由 `AdminLayout` 统一挂载与开关
- `REQ-0014-profile-page` 账号安全卡片「修改密码」按钮 MUST 调用同一 `openChangePasswordModal()`，不得重复实现表单
- REQ-0015 可独立先交付（侧栏入口）；REQ-0014 后接 callback 即可

## 5. 功能要求

### FR-001 表单字段

| 字段 | 类型 | 必填 | 规则 | 占位文案 |
|------|------|------|------|----------|
| 原密码 | password | 是 | 非空；提交时后端校验 | 请输入当前登录密码 |
| 新密码 | password | 是 | 8–32 位；至少字母+数字；≠ 原密码 | 请输入新密码 |
| 确认新密码 | password | 是 | 必须与新密码一致 | 请再次输入新密码 |

每个字段 MUST 支持「显示 / 隐藏」切换；SHOULD 复用 `features/auth/components/PasswordInput` 或等价 DS 组件。

### FR-002 前端校验（即时 + 提交）

- 新密码长度 8–32
- 新密码至少包含字母和数字
- 新密码不能与原密码相同（前端明文比对；后端 hash 比对）
- 确认新密码必须与新密码一致
- 新密码下方 MUST 展示三条规则提示；满足项 MAY 切换为成功态（绿色）

### FR-003 打开 / 关闭交互

**打开：**

- 点击菜单「密码修改」→ 打开弹窗
- 默认聚焦「原密码」
- 禁止页面主体滚动

**关闭：**

- 右上角 ×、取消、Esc
- 若任一字段有输入，关闭前 MUST 二次确认：`当前填写内容尚未保存，确认关闭吗？`

### FR-004 提交与成功反馈

1. 点击「保存修改」→ 前端校验
2. 校验通过 → 按钮 loading「保存中…」，禁用重复提交
3. 调用 `POST /api/v1/admin/profile/password`
4. 成功 → Toast：`密码修改成功，请使用新密码重新登录。`
5. 调用 `authStore.logout()`，跳转 `/admin/login`

### FR-005 错误提示（前端 inline / 接口 message）

| 场景 | 提示文案 |
|------|----------|
| 原密码为空 | 请输入当前登录密码 |
| 原密码错误 | 原密码不正确，请重新输入 |
| 新密码为空 | 请输入新密码 |
| 新密码长度不足 | 新密码至少需要 8 位 |
| 新密码缺少字母或数字 | 新密码需至少包含字母和数字 |
| 新旧密码一致 | 新密码不能与原密码相同 |
| 确认密码为空 | 请再次输入新密码 |
| 两次密码不一致 | 两次输入的新密码不一致 |
| 弱密码 / 策略不符 | 使用接口返回 message |
| 修改过于频繁 | 使用接口返回 message |
| 请求失败 | 修改失败，请稍后重试 |

### FR-006 后端 API — 修改密码

**路径：** `POST /api/v1/admin/profile/password`

**鉴权：** MUST 要求有效登录态（Bearer JWT）。

**请求体：**

```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**成功响应**（统一 `ApiResponse`）：

```json
{
  "code": 0,
  "message": "success",
  "data": { "success": true }
}
```

**服务端 MUST 校验：**

- 原密码正确（bcrypt）
- 新密码复杂度（与 FR-002 一致）
- 新密码 ≠ 原密码
- 弱密码表命中 → 拒绝
- 改密频率限制（见 FR-008）

**副作用：** 更新 `password_hash`；`token_version += 1`；记录 attempt 日志。

**路由组：** 新建 `admin_profile`，prefix `/admin/profile`；同组预留 `GET/PATCH` 供 `REQ-0014`。

### FR-007 全端 Token 失效

- `users` 表 MUST 新增 `token_version INTEGER NOT NULL DEFAULT 0`
- 登录签发 JWT MUST 含 claim `tv`（当前 `token_version`）
- `get_current_user` MUST 校验 `jwt.tv == user.token_version`，否则 401
- 改密成功 MUST `token_version += 1`，使**所有已签发 JWT**（含 remember_me 长 token、其他 tab / 设备）失效
- 前端成功回调 MUST 清本地 token 并跳转登录页

### FR-008 弱密码与限流（本期启用）

| 能力 | 规则 |
|------|------|
| 弱密码 | 静态常见弱密码表（约 50–100 条，如 `password`、`12345678`、`admin123`） |
| 失败限流 | 15 分钟内原密码错误 ≥ 5 次 → HTTP 429 |
| 成功频率 | 24 小时内成功改密 ≥ 3 次 → HTTP 429 |

- MUST 扩展 `user_validation.py`（如 `validate_password()`）
- MUST 轻量 attempt 记录（专用表或 audit 表，含 `user_id`、`success`、`created_at`）
- 建议错误码（实现时登记 `error_codes.py` 与 `docs/standards/error-codes.md`）：

| code | HTTP | 说明 |
|------|------|------|
| 40020 | 400 | 原密码不正确 |
| 40021 | 400 | 新密码不符合策略 |
| 40022 | 400 | 弱密码 |
| 40023 | 400 | 新密码不能与原密码相同 |
| 42901 | 429 | 修改密码过于频繁 |

### FR-009 安全约束

- 密码 MUST NOT 明文持久化（localStorage、数据库除 hash 外）
- MUST NOT 写入 URL、日志、埋点
- 接口 MUST 仅允许修改**当前登录用户本人**密码
- 密码错误限流 MUST 在后端强制执行

### FR-010 前端架构

- `AdminLayout` MUST 持有 `passwordModalOpen` 与 `openChangePasswordModal` / `closeChangePasswordModal`
- `AdminUserMenu` MUST 将「密码修改」从 `onPlaceholder` 改为 `onChangePassword`
- `ChangePasswordModal` MUST 置于 `features/admin/components/`（或经 OpenSpec 批准的 DS 目录）
- MUST NOT 在 `pages/` 内重复实现弹窗表单
- 样式 MUST 使用 semantic token（`bg-surface`、`text-brand-gold`、`border-border-focus` 等）

### FR-011 测试

- 后端：改密成功、原密码错误、弱密码、限流、`token_version` 递增后旧 JWT 401
- 前端：菜单打开弹窗、字段校验、显隐切换、脏关闭确认、成功 logout 跳转
- 集成：Orval 生成客户端调用成功

## 6. UI 约束

- 视觉 MUST 与用户管理页、admin-home 壳层一致（Sidebar 264px、暗色半透明卡片、0.5px 边框、2–3px 圆角、品牌金主按钮）
- 输入框高度 44px；focus 品牌金边框；错误危险色边框 + 字段下文案
- 弹窗 footer：取消（幽灵）+ 保存修改（品牌金实底），高度 40px
- 原型验收：1440×1024 下与用户管理页背景并排对照 `prototype/web/password-change-modal.png`

## 7. 关联需求

| REQ | 关系 |
|-----|------|
| REQ-0004-admin-home | 父需求；侧栏用户菜单入口 |
| REQ-0014-profile-page | 姊妹需求；共享 `ChangePasswordModal`；个人资料页不提供独立改密实现 |
| REQ-0005-user-management | 边界；管理员 `reset-password` 与他人生成随机密码，非本需求 |

## 8. 状态

| 字段 | 值 |
|------|-----|
| requirement_id | REQ-0015-password-change |
| status | pending_review |
| priority | P1 |
| terminal | web-admin |
| parent_requirement | REQ-0004-admin-home |
