---
bug_id: BUG-0024-change-password-error-wrong-field
status: captured
created_at: 2026-06-28 12:47:55
updated_at: 2026-06-28 12:47:55
severity_hint: medium
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0025-change-password-toggle-button-misalignment
---

# 现象

Web 管理端「修改密码」弹窗中，与新密码相关的校验/服务端错误提示（如「新密码过于常见，请更换」）错误地显示在「原密码」输入框下方，而非「新密码」输入框下方，导致用户无法正确理解哪一项填写有误。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单打开「修改密码」弹窗。
3. 填写正确的原密码（如 `AdminPass123!`）。
4. 填写一个过于常见的新密码（如 `AdminPass123`），确认新密码保持一致。
5. 点击「保存修改」，触发服务端校验失败。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 与新密码相关的错误（客户端规则或服务端返回）应显示在「新密码」字段下方。 |
| **实际** | 错误提示「新密码过于常见，请更换」出现在「原密码」输入框下方。 |

# 初步线索

- `src/web/src/features/admin/components/ChangePasswordModal.tsx`：单一 `error` 状态同时用于客户端新密码校验与服务端错误，且仅绑定到原密码 `PasswordField` 的 `error` prop（约 186 行）；新密码字段未接收错误。

# 附件

- screenshots/change-password-error-wrong-field.png
