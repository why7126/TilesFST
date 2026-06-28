---
title: 业务流程
purpose: 描述管理端修改密码交互与 API 流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
note: REQ-0015-password-change
created_at: 2026-06-28 09:57:09
updated_at: 2026-06-28 09:57:09
---

# 业务流程

## 1. 与父需求 / 姊妹 REQ 的差异

```text
REQ-0004-admin-home          侧栏用户菜单定义入口（密码修改原为 placeholder）
REQ-0015-password-change     实现改密弹窗 + API + 安全策略
REQ-0014-profile-page        个人资料页；Out 不含改密实现；按钮调用同一 openChangePasswordModal
REQ-0005-user-management     管理员 reset-password：替他人生成随机密码，无需原密码
```

| 能力 | REQ-0005 reset-password | REQ-0015 change password |
|------|-------------------------|---------------------------|
| 操作者 | 管理员 | 本人 |
| 目标用户 | 任意用户 id | 当前登录用户 |
| 原密码 | 不需要 | 必须校验 |
| 新密码来源 | 系统随机生成 | 用户输入 |
| UI | 用户列表操作 + 展示一次性密码弹窗 | 侧栏菜单 + ChangePasswordModal |

## 2. 前端入口与组件流

```text
AdminLayout
  ├── passwordModalOpen state
  ├── ChangePasswordModal
  ├── AdminSidebar → AdminUserMenu
  │     └── 「密码修改」→ openChangePasswordModal()
  └── Outlet（任意 /admin/* 页作为背景）
        └── （未来）ProfilePage「修改密码」→ 同一 openChangePasswordModal()
```

**变更前（现状）：**

```text
点击「密码修改」→ onPlaceholder() → Toast「功能建设中」
```

**变更后：**

```text
点击「密码修改」→ openChangePasswordModal() → 520px 居中弹窗
```

## 3. 修改密码主流程

```text
用户展开侧栏底部菜单 → 点击「密码修改」
  ↓
打开 ChangePasswordModal；聚焦「原密码」；body 禁止滚动
  ↓
用户填写原密码 / 新密码 / 确认新密码
  ├─ 输入过程：前端即时校验 + 规则列表状态更新
  └─ 点击「保存修改」
        ↓
     前端提交前校验（FR-002）
        ├─ 失败 → inline 错误，不请求 API
        └─ 通过 → 按钮 loading「保存中…」
              ↓
           POST /api/v1/admin/profile/password
              ├─ 401/400/429 → 展示 message，恢复按钮
              └─ 200 success
                    ↓
                 Toast「密码修改成功，请使用新密码重新登录。」
                    ↓
                 authStore.logout() → navigate /admin/login
```

## 4. 关闭弹窗流程

```text
用户点击 × / 取消 / Esc
  ↓
任一字段有内容？
  ├─ 是 → confirm「当前填写内容尚未保存，确认关闭吗？」
  │         ├─ 取消 → 保持弹窗
  │         └─ 确认 → 关闭并重置表单
  └─ 否 → 直接关闭并重置表单
```

## 5. 后端 API 流程

```text
POST /api/v1/admin/profile/password
  Authorization: Bearer <JWT with tv claim>
  Body: { old_password, new_password }
  ↓
get_current_user（jwt.tv == user.token_version）
  ↓
检查改密频率限流（24h 成功次数、15min 失败次数）
  ↓
verify_password(old_password, password_hash)
  ├─ 失败 → 记录 attempt(fail)；429 或 40020
  └─ 成功
        ↓
     validate_password(new_password) + 弱密码表 + ≠ old
        ├─ 失败 → 40021/40022/40023
        └─ 通过
              ↓
           UPDATE password_hash, token_version += 1
           记录 attempt(success)
              ↓
           return { success: true }
```

## 6. Token 失效链路

```text
改密前：JWT(tv=3) + DB(token_version=3) → 有效
改密后：DB(token_version=4)
  ├─ 旧 JWT(tv=3) → get_current_user → 401
  ├─ 其他 tab 旧 token → 401
  └─ 新 login → JWT(tv=4) → 有效
```

## 7. 依赖

| 依赖 | 说明 |
|------|------|
| REQ-0004-admin-home | AdminLayout、AdminUserMenu 壳层 |
| REQ-0001-user-login | auth store、JWT 登录、logout |
| REQ-0005-user-management | 视觉基准（用户管理列表页背景） |
| REQ-0014-profile-page | 后续共享 openChangePasswordModal（非阻塞） |
| rules/api.md | ApiResponse、错误码、Orval |
| rules/ui-design.md | 暗色旗舰风、semantic token |
