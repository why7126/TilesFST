---
bug_id: BUG-0044-system-settings-non-admin-access
status: done
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 19:11:39
severity_hint: high
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug:
captured_via: capture
classification_rationale: 系统设置属平台级配置，REQ-0017 规定仅 admin 可访问；非 admin 可见或可访问为权限偏差
closure_rationale: REQ-0017 add-system-settings 交付已含前端 requireAdmin 路由/侧栏过滤与后端 require_system_admin；非误报，属 REQ 范围已覆盖
related_change: add-system-settings
---

# 现象

「系统设置」页面及侧栏入口应对非「后台管理员」（`admin`）角色不可见且不可访问。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 仅 `admin` 侧栏可见「系统设置」；非 admin 直链 forbidden/403；API 403。 |
| **实际（核查）** | `App.tsx` `ProtectedRoute requireAdmin`；`AdminSidebar` 过滤 `settings`；`admin_system_settings` router `require_system_admin`。 |

# 处置

- **status**: `done` — 由 REQ-0017 主 change 实现，无需独立 fix change
- **归档**: `issues/bugs/archive/`

# 附件

- screenshots/
- logs/
