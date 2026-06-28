---
created_at: 2026-06-28 17:53:48
title: 缺陷追踪
purpose: BUG-0044 系统设置非 admin 可见或可访问
content: 已由 REQ-0017 主交付覆盖；归档关闭
owner: product
status: done
lifecycle_stage: archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0044-system-settings-non-admin-access
bug_name: system-settings-non-admin-access
severity: high
status: done
iteration: sprint-003
related_requirement: REQ-0017-system-settings
related_bug: null
related_change: add-system-settings
suggested_fix_change: null
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 17:53:48
  closed: 2026-06-28 19:11:39
  archived: 2026-06-28 19:11:39
openspec_changes:
  - change_id: add-system-settings
    type: add
    status: archived```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done（含关闭说明） |
| bug.md | cancelled（REQ 已覆盖，无需独立 bug 包） |
| root-cause.md | cancelled |
| workaround.md | cancelled |
| acceptance.md | cancelled |
| review.md | cancelled |

**Readiness:** Archived — REQ-0017 权限门禁已实现

## 3. 关闭依据

- 前端：`ProtectedRoute requireAdmin` + `AdminSidebar` 隐藏 `settings`
- 后端：`admin_system_settings.py` 全路由 `require_system_admin`

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 19:11:39 | 归档关闭 | plan → archive；确认 REQ-0017 已实现，直接关闭 |
| 2026-06-28 17:53:48 | `/capture` | 记录系统设置应仅 admin 可见/可访问 |
