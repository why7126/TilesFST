---
requirement_id: REQ-0019-admin-superuser-protection
title: 管理端超级管理员账号保护
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: issues/requirements/archive/REQ-0019-admin-superuser-protection/capture.md
priority: P1
parent_requirement: REQ-0005-user-management
created_at: 2026-06-30 13:11:03
updated_at: 2026-06-30 18:18:45
---

# REQ-0019 管理端超级管理员账号保护

## 1. 需求背景

管理端现有用户管理能力（`REQ-0005-user-management`）允许后台管理员编辑用户资料、重置密码、冻结、解冻和软删除用户；管理端个人密码能力（`REQ-0015-password-change`）允许登录用户修改本人密码。

项目同时通过 `.env` 配置保底超级管理员账号：

```text
ADMIN_USERNAME=admin
```

该账号承担本地开发、Docker 演示和生产部署中的系统保底登录职责。如果任何管理端用户可以通过用户管理或个人密码入口编辑、停用、删除、重置或修改该账号密码，系统可能失去保底管理员，影响运维恢复和权限安全。

本需求补齐针对 `ADMIN_USERNAME` 的账号保护策略：超级管理员账号仍使用既有 `admin` 角色模型，不新增角色枚举；但该账号在管理端被识别为受保护系统账号，后端必须强制拦截破坏性操作，前端必须给出明确不可操作状态。

## 2. 目标用户

| 角色 | 权限与影响 |
|------|------------|
| 后台管理员 | 可管理普通用户，但不可编辑、重置、修改、冻结、删除 `ADMIN_USERNAME` 对应账号 |
| 受保护超级管理员本人 | 可登录管理后台；是否允许通过个人密码入口自改密码待评审确认，本 PRD 默认纳入禁止范围 |
| 后台运营 / 内部员工 | 无用户管理权限；如具备个人密码入口，也不得影响受保护超级管理员账号 |
| 店主端用户 / 微信小程序用户 | 不涉及 |

## 3. 范围

### 3.1 本期包含

- 后端以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护超级管理员账号。
- 用户管理列表和详情接口返回该账号的受保护标识，供前端控制操作态。
- 用户管理编辑接口禁止更新该账号的昵称、角色、头像等资料。
- 用户管理重置密码接口禁止重置该账号密码。
- 用户管理状态变更接口禁止冻结、解冻、软删除该账号。
- 管理端个人修改密码接口禁止该账号通过本人入口修改密码（待评审确认）。
- 前端用户管理列表对该账号的编辑、重置密码、冻结/解冻、删除操作置灰，并展示不可操作原因。
- 后端返回统一错误码与明确中文文案，避免前端硬编码 `admin` 字符串判断。
- 补充后端集成测试与前端组件测试，覆盖受保护账号操作拦截。

### 3.2 本期不包含

- 不新增 `super_admin`、`root` 等角色枚举。
- 不改变现有 `admin` / `employee` / `store_owner` RBAC 模型。
- 不开放前端修改 `ADMIN_USERNAME`。
- 不移除或禁止运维级启动恢复机制（如 `ADMIN_RESET_PASSWORD_ON_STARTUP`），除非后续评审明确要求。
- 不涉及店主 Web 展示端和微信小程序。
- 不新增多因素认证、审计报表或完整 RBAC 能力点体系。

## 4. 术语与判定规则

### 4.1 受保护超级管理员账号

受保护超级管理员账号是指：

```text
users.username == settings.admin_username.strip()
```

判定规则：

- `ADMIN_USERNAME` 未配置或为空时，后端 MUST 回退默认值 `admin`。
- 比较前 SHOULD 对配置值做 `strip()`，并遵循现有用户名大小写规范；若数据库用户名统一小写，比较也应使用小写归一化。
- 前端 MUST 使用后端返回字段判断受保护状态，MUST NOT 写死 `admin`。

### 4.2 建议 API 字段

用户列表与详情中的用户对象 SHOULD 增加：

```json
{
  "is_protected": true,
  "protected_reason": "系统保底管理员账号不允许编辑、重置密码或停用"
}
```

字段语义：

- `is_protected=true`：前端需要置灰受限操作。
- `protected_reason`：用于按钮 `title`、提示文案或弹窗说明。
- 普通用户返回 `is_protected=false`，`protected_reason=null`。

## 5. 功能要求

### FR-001 后端识别受保护账号

- 后端 MUST 提供统一的受保护账号判定逻辑，避免在多个 Service 中重复写字符串判断。
- 判定逻辑 MUST 读取 `settings.admin_username`，不得硬编码 `admin`。
- 用户列表、用户详情和相关 Service 操作 MUST 复用同一判定逻辑。

### FR-002 用户列表与详情标识

- `GET /api/v1/admin/users` 返回的每条用户记录 MUST 包含受保护标识。
- `GET /api/v1/admin/users/{id}` 返回的用户详情 MUST 包含受保护标识。
- API 字段命名 MUST 遵守现有 OpenAPI / Orval 生成规则。

### FR-003 禁止编辑受保护账号

- `PATCH /api/v1/admin/users/{id}` 当目标用户为受保护账号时 MUST 拒绝。
- 拒绝范围包括但不限于：`display_name`、`role`、`avatar_object_key`。
- 后端 MUST 返回统一错误码与明确文案，不得静默忽略。
- 前端在 `is_protected=true` 时 MUST 禁用「编辑」入口，并展示原因。

### FR-004 禁止重置受保护账号密码

- `POST /api/v1/admin/users/{id}/reset-password` 当目标用户为受保护账号时 MUST 拒绝。
- 后端 MUST NOT 生成新随机密码，MUST NOT 更新 `password_hash`。
- 前端在 `is_protected=true` 时 MUST 禁用「重置密码」入口，并展示原因。

### FR-005 禁止冻结、解冻和删除受保护账号

- `PATCH /api/v1/admin/users/{id}/status` 当目标用户为受保护账号时 MUST 拒绝任意状态变更。
- 受保护账号 MUST 保持可登录所需的有效状态，避免系统失去保底管理员。
- 前端在 `is_protected=true` 时 MUST 禁用「冻结 / 解冻」与「删除」入口，并展示原因。

### FR-006 禁止本人修改受保护账号密码

- `POST /api/v1/admin/profile/password` 当当前登录用户为受保护账号时 MUST 拒绝修改密码。
- 后端 MUST NOT 校验通过后更新 `password_hash`，MUST NOT 递增 `token_version`。
- 前端可保留「密码修改」入口，但提交后 MUST 使用接口返回 message 展示不可修改原因。
- 本项为待评审确认项：若产品允许超级管理员本人自改密码，则需在评审中明确移除本 FR，并补充替代安全策略。

### FR-007 错误码与响应

建议新增统一错误：

| 场景 | HTTP | code | message |
|------|------|------|---------|
| 受保护账号不可操作 | 403 | 待登记 | 系统保底管理员账号不允许执行该操作 |

要求：

- 错误码 MUST 登记到后端错误码定义与 `docs/standards/error-codes.md`。
- API 响应 MUST 保持统一结构。
- 前端 MUST 优先展示接口返回 `message`。

### FR-008 前端操作态

用户管理列表中，当 `user.is_protected=true`：

- 「编辑」按钮置灰。
- 「重置密码」按钮置灰。
- 「冻结 / 解冻」按钮置灰。
- 「删除」按钮置灰。
- 置灰按钮 SHOULD 使用 `title` 或等价提示展示 `protected_reason`。
- 不应只隐藏操作；保留不可操作状态更利于管理员理解系统保护规则。

### FR-009 运维恢复边界

- 本需求不禁止 `.env` 配置的启动恢复能力。
- 如 `ADMIN_RESET_PASSWORD_ON_STARTUP=true` 且 `ADMIN_INITIAL_PASSWORD` 已配置，后端启动种子逻辑仍 MAY 按既有策略恢复该账号密码。
- 该能力属于部署 / 运维级恢复，不属于管理端用户操作。

### FR-010 测试要求

后端测试 MUST 覆盖：

- 用户列表返回 `is_protected=true`。
- 编辑受保护账号返回错误，数据库字段不变。
- 重置受保护账号密码返回错误，旧密码仍可登录或 `password_hash` 不变。
- 冻结 / 删除受保护账号返回错误，状态不变。
- 当前登录用户为受保护账号时，个人改密接口按评审结论拒绝或允许。

前端测试 SHOULD 覆盖：

- 受保护账号行操作按钮置灰。
- 置灰按钮展示不可操作原因。
- 普通用户操作不受影响。

## 6. UI 约束

- 页面仍沿用 `REQ-0005-user-management` 的用户管理列表与弹窗视觉，不新增独立页面。
- 禁用态按钮 MUST 与现有 `user-management.css` 中禁用样式一致。
- 提示文案使用中文，保持克制、明确，不使用技术异常堆栈。
- TSX 中不得硬编码 `admin` 作为保护判断，必须依赖后端字段。
- UI 样式须遵守 `rules/ui-design.md` 的 Design Token 和现有管理端 CSS Port 约束。

## 7. 关联需求

| REQ | 关系 |
|-----|------|
| REQ-0005-user-management | 父需求；用户列表、编辑、重置密码、状态变更均来自该能力 |
| REQ-0015-password-change | 相关需求；个人密码修改入口需要按本需求处理受保护账号 |
| REQ-0014-profile-page | 潜在相关；如个人资料页提供账号安全卡片，需复用相同保护策略 |

## 8. 待评审确认

- “任何用户”是否最终包含超级管理员本人；本 PRD 默认包含。
- 是否允许编辑受保护账号的非安全资料（昵称、头像）；本 PRD 默认不允许。
- 错误码具体数值由 API 治理阶段登记确认。
- 前端提示采用 `title`、Toast 还是轻量说明文案，由 UI 验收阶段确认。

## 9. 状态

| 字段 | 值 |
|------|-----|
| requirement_id | REQ-0019-admin-superuser-protection |
| status | in_sprint |
| priority | P1 |
| terminal | web-admin |
| parent_requirement | REQ-0005-user-management |
| expected_openspec_change | update-admin-superuser-protection |
