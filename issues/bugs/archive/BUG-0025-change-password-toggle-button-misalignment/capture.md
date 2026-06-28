---
bug_id: BUG-0025-change-password-toggle-button-misalignment
status: captured
created_at: 2026-06-28 12:47:55
updated_at: 2026-06-28 12:47:55
severity_hint: medium
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0024-change-password-error-wrong-field
---

# 现象

Web 管理端「修改密码」弹窗中，当某密码字段下方出现错误提示后，该字段右侧「显示/隐藏」切换按钮垂直位置错位（下沉至输入框底部附近），未与输入框垂直居中对齐；其他无错误提示的字段按钮仍正常居中。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 打开「修改密码」弹窗。
3. 填写原密码、新密码与确认新密码，触发校验错误（如提交过于常见的新密码，使原密码字段下方出现错误提示）。
4. 观察出现错误提示的密码字段右侧「显示/隐藏」按钮位置。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 无论字段下方是否显示错误提示，「显示/隐藏」按钮应始终相对输入框垂直居中。 |
| **实际** | 出现错误提示后，该字段的「隐藏」按钮下沉，与新密码、确认新密码字段（无错误时）的按钮对齐不一致。 |

# 初步线索

- `PasswordField` 组件结构：`toggle-pass` 按钮与 `label/input` 同级，`error-text` 渲染在按钮之后（约 50–61 行），可能影响 `form-row` 布局或绝对定位基准。
- 样式见 `src/web/src/features/admin/styles/password-change-modal.css`。

# 附件

- screenshots/change-password-toggle-misalignment.png
