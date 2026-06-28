---
bug_id: BUG-0023-profile-duplicate-save-buttons
status: captured
created_at: 2026-06-28 12:37:33
updated_at: 2026-06-28 12:37:33
severity_hint: low
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0022-profile-basic-info-redundant-role-status
---

# 现象

Web 管理端「个人资料」页同时存在两个「保存修改」按钮：页头右侧一处、基础资料表单底部一处，功能相同，用户认为多余。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入「个人资料」页（`/admin/profile`）。
3. 观察页头操作区与「基础资料」卡片底部按钮组。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 页面仅保留一处主「保存修改」入口（建议保留表单底部与「重置」并列，或仅保留页头一处），避免重复 CTA。 |
| **实际** | 页头与表单底部各有一个「保存修改」按钮，视觉与交互重复。 |

# 初步线索

- `src/web/src/pages/admin/ProfilePage.tsx` 约 200 行：页头 `保存修改`。
- 同文件约 335 行：表单底部 `保存修改`。
- `ProfilePage.test.tsx` 使用 `getAllByRole('button', { name: '保存修改' })` 说明当前实现刻意保留双按钮；REQ-0014 AC-017 要求行为一致，未禁止双按钮，与用户反馈需 reconcile。

# 附件

- screenshots/profile-page-duplicate-save-buttons.png
