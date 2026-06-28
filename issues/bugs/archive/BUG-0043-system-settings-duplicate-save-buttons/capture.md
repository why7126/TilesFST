---
bug_id: BUG-0043-system-settings-duplicate-save-buttons
status: captured
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 17:53:48
severity_hint: low
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug: BUG-0023-profile-duplicate-save-buttons
captured_via: capture
classification_rationale: 页头与底部重复「保存设置」CTA，与用户反馈及 BUG-0023 修复模式一致，属 UI 冗余缺陷
---

# 现象

Web 管理端「系统设置」页同时存在两个「保存设置」按钮：页头右侧一处、各 Tab 面板底部操作区一处，功能相同，用户认为页头按钮多余。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置」任意 Tab（如 `/admin/settings/basic`）。
3. 观察页头 `page-hero` 右侧与面板底部 `settings-panel-footer` 的按钮组。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 删除页头右侧「保存设置」，仅保留底部「取消 / 恢复默认 / 保存设置」操作区（与个人资料页 BUG-0023 修复方向一致）。 |
| **实际** | 页头与底部各有一个「保存设置」按钮，视觉与交互重复。 |

# 初步线索

- `src/web/src/pages/admin/SystemSettingsPage.tsx`：页头与 `SettingsPanelFooter` 均渲染保存按钮。
- `SystemSettingsPage.test.tsx` 使用 `getAllByRole('button', { name: '保存设置' })` 断言双按钮。
- REQ-0017 AC-009 原要求双入口；与用户反馈及 `fix-profile-duplicate-save-buttons` 需 reconcile。

# 附件

- screenshots/
- logs/
