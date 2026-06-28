---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
status: pending_review
created_at: 2026-06-28 17:46:25
updated_at: 2026-06-28 18:05:06
severity_hint: medium
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0019-user-modal-avatar-upload-display
---

# 现象

Web 管理端侧边栏底部用户菜单栏（`AdminUserMenu`）未显示用户头像。用户已在个人资料或用户管理中上传头像后，侧栏触发区仍无法看到头像图片，与个人资料页、用户列表等处的头像展示不一致。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入「个人资料」上传并保存头像（或确保当前账号已有 `avatar_url`）。
3. 观察侧边栏底部用户菜单触发区（显示用户名、邮箱与 chevron 的区域）。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 侧栏用户菜单应显示当前用户头像图片；无头像时可回退为首字母占位，与 Profile 页、用户列表等行为一致。 |
| **实际** | 侧栏用户菜单未显示用户头像（仅首字母占位或未正确渲染 `avatar_url`）。 |

# 初步线索

- `src/web/src/features/admin/components/AdminUserMenu.tsx` 第 101 行：`.avatar` 仅渲染 `initials` 文本，未使用 `user.avatar_url`。
- 对比：`ProfilePage.tsx` 与 `UserManagementPage.tsx` 已在有 `avatar_url` 时渲染 `<img>` 并支持 fallback。

# 附件

- screenshots/（待补充）
- logs/
