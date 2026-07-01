---
title: 业务流程
purpose: REQ-0019 管理端超级管理员账号保护业务流程与边界
content: 基于 requirement.md、REQ-0005 与 REQ-0015 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD、评审结论或实现策略变更时同步更新
owner: product
status: draft
note: REQ-0019-admin-superuser-protection
created_at: 2026-06-30 13:56:49
updated_at: 2026-06-30 13:56:49
---

# 业务流程

## 1. 总体流程

```text
.env / Settings
ADMIN_USERNAME（默认 admin）
        │
        ▼
后端统一判定 is_protected
        │
        ├───────────────┬────────────────┬──────────────────┐
        ▼               ▼                ▼                  ▼
用户列表/详情       编辑用户 PATCH     重置密码 POST       状态 PATCH
返回保护标识        后端拒绝           后端拒绝            后端拒绝
        │               │                │                  │
        ▼               ▼                ▼                  ▼
前端置灰操作        不写资料字段        不生成随机密码      不冻结/删除
```

## 2. 用户管理列表流程

```text
管理员进入 /admin/users
        │
        ▼
GET /api/v1/admin/users
        │
        ▼
后端逐条计算 is_protected / protected_reason
        │
        ├─ 普通用户：操作按钮按 REQ-0005 原规则展示
        │
        └─ 受保护账号：编辑 / 重置密码 / 冻结 / 删除置灰
```

## 3. 用户编辑保护流程

```text
管理员尝试编辑用户
        │
        ▼
PATCH /api/v1/admin/users/{id}
        │
        ▼
后端查询目标用户
        │
        ├─ 用户不存在：404 USER_NOT_FOUND
        ├─ 非受保护账号：沿用 REQ-0005 编辑流程
        └─ 受保护账号：403 USER_PROTECTED_ACCOUNT（建议）
                 │
                 ▼
          display_name / role / avatar_object_key 均不变
```

## 4. 重置密码保护流程

```text
管理员点击「重置密码」
        │
        ├─ 前端 is_protected=true：按钮置灰，不打开确认弹窗
        │
        └─ 绕过前端直接请求 API
                │
                ▼
        POST /api/v1/admin/users/{id}/reset-password
                │
                ▼
        后端判定受保护账号
                │
                └─ 拒绝：不生成随机密码、不更新 password_hash
```

## 5. 状态变更保护流程

```text
管理员尝试冻结 / 解冻 / 删除
        │
        ├─ 前端 is_protected=true：按钮置灰
        │
        └─ 绕过前端直接请求 API
                │
                ▼
        PATCH /api/v1/admin/users/{id}/status
                │
                ▼
        后端判定受保护账号
                │
                └─ 拒绝：status 不变
```

## 6. 本人修改密码流程（待评审确认）

```text
受保护账号本人打开「密码修改」
        │
        ▼
POST /api/v1/admin/profile/password
        │
        ▼
后端判定 current_user.username == ADMIN_USERNAME
        │
        └─ 默认策略：拒绝
              ├─ 不更新 password_hash
              ├─ 不递增 token_version
              └─ 前端展示接口 message
```

> 若评审确认允许受保护账号本人自改密码，本流程需调整为“仅禁止用户管理重置和状态变更”，并在 acceptance 中更新 AC-016/AC-031。

## 7. 与父需求 REQ-0005 的差异

| 能力 | REQ-0005 原规则 | REQ-0019 补充规则 |
|------|-----------------|-------------------|
| 角色模型 | `admin` 可管理用户 | 不新增角色，`ADMIN_USERNAME` 账号加保护标识 |
| 编辑用户 | 管理员可编辑普通用户资料 | 受保护账号不可编辑 |
| 重置密码 | 管理员可重置用户密码 | 受保护账号不可重置 |
| 状态变更 | 管理员可冻结/解冻/软删除用户 | 受保护账号不可状态变更 |
| 前端操作列 | 按用户状态决定按钮可用性 | 额外按 `is_protected` 置灰 |

## 8. 依赖与边界

```text
REQ-0005 用户管理
   └─ REQ-0019 保护策略扩展
        ├─ 用户列表/详情 API 字段扩展
        ├─ 用户编辑/重置/状态 API 拦截
        └─ 管理端列表行操作禁用态

REQ-0015 修改密码
   └─ REQ-0019 可选约束：受保护账号本人改密禁止
```

## 9. 风险

| 风险 | 说明 | 缓解 |
|------|------|------|
| 前端硬编码 `admin` | 与 `.env ADMIN_USERNAME` 不一致 | 后端返回 `is_protected`，前端只消费字段 |
| 只做前端置灰 | API 被直接调用时仍可破坏账号 | 后端 Service 层强校验 |
| 新增角色扩大范围 | 牵动 RBAC、筛选、迁移和文案 | 本期不新增角色，仅账号保护 |
| 禁止本人改密争议 | 产品可能希望超级管理员可自改密码 | 保留待评审项，评审后更新 acceptance |
