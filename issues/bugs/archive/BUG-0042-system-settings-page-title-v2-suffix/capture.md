---
bug_id: BUG-0042-system-settings-page-title-v2-suffix
status: captured
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 17:53:48
severity_hint: low
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug:
captured_via: capture
classification_rationale: 页头眉标文案与 REQ-0017 AC-006（SYSTEM / SETTINGS）及 prototype 不一致，属已实现页面的 UI 文案偏差
---

# 现象

Web 管理端「系统设置」页标题区眉标显示为 `SYSTEM / SYSTEM SETTINGS / V2`，末尾多余的 `/ V2` 与需求及原型不一致。

# 复现步骤

1. 以 `admin` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 侧栏进入「系统设置」（`/admin/settings/basic`）。
3. 观察页头 `page-hero` 区域眉标（eyebrow）文案。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 眉标为 `SYSTEM / SYSTEM SETTINGS`，不含版本后缀。 |
| **实际** | 眉标为 `SYSTEM / SYSTEM SETTINGS / V2`。 |

# 初步线索

- `src/web/src/pages/admin/SystemSettingsPage.tsx` 约 798 行：`<p className="eyebrow">SYSTEM / SYSTEM SETTINGS / V2</p>`。
- REQ-0017 AC-006 要求页头眉标含 `SYSTEM / SETTINGS`；prototype 无 `V2` 后缀。

# 附件

- screenshots/
- logs/
