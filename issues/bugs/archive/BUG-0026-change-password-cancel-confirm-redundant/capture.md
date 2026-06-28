---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
status: captured
created_at: 2026-06-28 12:49:31
updated_at: 2026-06-28 12:49:31
severity_hint: low
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0024-change-password-error-wrong-field
---

# 现象

Web 管理端「修改密码」弹窗中，用户点击「取消」或按 Esc、点击遮罩关闭时，若表单已有输入内容，会弹出浏览器原生二次确认框「当前填写内容尚未保存，确认关闭吗？」。用户认为取消操作不应再出现此确认，应直接关闭弹窗。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单打开「修改密码」弹窗。
3. 在任意密码字段中输入内容（如原密码、新密码）。
4. 点击弹窗底部「取消」按钮（或按 Esc / 点击遮罩）。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 点击「取消」后直接关闭修改密码弹窗，不弹出额外确认。 |
| **实际** | 弹出浏览器原生 `window.confirm` 对话框，需再次点击「确定」才能关闭。 |

# 初步线索

- `src/web/src/features/admin/components/ChangePasswordModal.tsx` 中 `requestClose`（约 103–108 行）：`isDirty` 时调用 `window.confirm`。
- `ChangePasswordModal.test.tsx` 含对 `window.confirm` 的断言，修复时需同步更新测试。

# 附件

- screenshots/change-password-cancel-browser-confirm.png
