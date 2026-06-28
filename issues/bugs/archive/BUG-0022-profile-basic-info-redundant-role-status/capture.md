---
bug_id: BUG-0022-profile-basic-info-redundant-role-status
status: captured
created_at: 2026-06-28 12:37:33
updated_at: 2026-06-28 12:45:00
severity_hint: low
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug: BUG-0023-profile-duplicate-save-buttons
resolution: adopted
resolution_note: BUG-0022 探索结论采纳；角色/状态仅在账号安全卡片展示；REQ-0014 AC-011 MODIFIED
---

# 现象

Web 管理端「个人资料」页（`/admin/profile`）的「基础资料」表单中展示了只读字段「所属角色」「账号状态」，而右侧「账号安全」卡片已展示相同信息（账号状态 badge、所属角色），造成信息重复、表单区域冗余。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单进入「个人资料」页（`/admin/profile`）。
3. 观察左侧「基础资料」表单底部与右侧「账号安全」卡片内容。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 「所属角色」「账号状态」仅在「账号安全」卡片展示一次；「基础资料」表单聚焦可编辑字段（昵称、邮箱、手机、备注等）。 |
| **实际** | 两处同时展示相同只读信息；用户标注红框区域为重复内容。 |

# 初步线索

- `src/web/src/pages/admin/ProfilePage.tsx` 约 290–296 行：表单内 `profile-role`、`profile-status` 只读字段。
- 同文件约 352–360 行：「账号安全」卡片内 `账号状态`、`所属角色`。
- REQ-0014 原 PRD/acceptance 曾要求表单内也含角色/状态只读字段；与用户当前 UX 反馈存在冲突，修复时需对齐 prototype 或更新 acceptance。

# 附件

- screenshots/profile-page-redundant-fields.png
