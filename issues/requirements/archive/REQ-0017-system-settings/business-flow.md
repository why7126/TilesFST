---
title: 业务流程
purpose: 系统设置访问、分组 Tab、保存/恢复默认与审计主流程
content: 基于 requirement.md v1 与 prototype/web/system-settings-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 11:18:24
updated_at: 2026-06-28 11:18:24
note: REQ-0017-system-settings
---

# 业务流程

## 1. 流程总览

```text
后台管理员登录（role=admin）
  ↓
侧栏 SYSTEM → 「系统设置」
  ↓
GET /admin/settings → redirect /admin/settings/basic
  ↓
GET /api/v1/admin/system-settings/{group}
  ↓
┌─────────────────────────────────────────────────────────────┐
│ SystemSettingsPage                                           │
│  ├─ settings-nav：5 Tab 切换（子路由）                         │
│  ├─ summary-grid：当前分组摘要                               │
│  ├─ settings-panel：表单编辑                                 │
│  ├─ dirty → 「有未保存修改」                                 │
│  ├─ 保存 → PATCH {group} → inline 成功提示                   │
│  ├─ 取消 → 恢复 GET 快照                                     │
│  ├─ 恢复默认 → 确认 → POST .../reset                         │
│  └─ P2：每次保存/reset → audit_logs                          │
└─────────────────────────────────────────────────────────────┘
```

## 2. 与父需求 REQ-0004 差异

| 对比项 | REQ-0004（占位） | REQ-0017（本期） |
|---|---|---|
| 系统设置入口 | 无 path / 无效点击 | `path: '/admin/settings'` |
| 页面 | 无 | 5 Tab 系统设置 Shell + API |
| 权限 | 未定义 | 仅 `admin`；`employee` 不可见 |
| 配置存储 | `.env` 分散 | SQLite `system_settings` + env merge |

## 3. 访问与权限

```text
JWT → ProtectedRoute（admin shell）
  ├─ role = admin → 允许 /admin/settings/*
  ├─ role = employee → 侧栏隐藏；直链 /admin/forbidden
  └─ store_owner → /admin/forbidden

API → require_system_admin
  ├─ role = admin → 允许 system-settings *
  └─ employee / store_owner → 403
```

## 4. Tab 导航（子路由）

```text
/admin/settings
  └─ redirect → /admin/settings/basic

settings-nav 点击
  ├─ 基础信息      → /admin/settings/basic
  ├─ 安全策略      → /admin/settings/security      （P1）
  ├─ 媒体与存储    → /admin/settings/media         （P0）
  ├─ 通知设置      → /admin/settings/notification  （P3）
  └─ 审计配置      → /admin/settings/audit         （P2）

切换 Tab 时：
  ├─ 若有 dirty → 提示离开（实现二选一：confirm 或 auto-discard，OpenSpec 定）
  └─ GET 新 group 配置
```

## 5. 加载分组配置

```text
进入 /admin/settings/{group}
  ↓
GET /api/v1/admin/system-settings/{group}
  ↓
响应 = effective 值（DB ?? env 默认）+ 只读字段（bucket、key 规则等）
  ↓
渲染 page-hero + summary-grid + settings-panel
  ↓
侧栏「系统设置」active；settings-nav 当前 Tab active（品牌金）
```

## 6. 保存设置

```text
用户编辑可写字段
  ↓
dirty = true → 展示「有未保存修改」
  ↓
点击「保存设置」（页头或底部，行为一致）
  ↓
前端校验（必填、格式、范围）
  ↓
PATCH /api/v1/admin/system-settings/{group}
  ↓
成功：
  ├─ 更新 baseline；dirty = false
  ├─ inline 成功提示（save-tip 风格）
  ├─ P2+：audit_logs（settings_update, metadata=diff）
  └─ 策略级 key 立即生效于后续 upload/auth（FR-004）
失败：
  └─ 字段级或表单级错误
```

## 7. 恢复默认

```text
点击「恢复默认」
  ↓
二次确认（说明将丢失当前分组自定义）
  ↓
POST /api/v1/admin/system-settings/{group}/reset
  ↓
成功：
  ├─ 删除 DB 覆盖或写回 seed
  ├─ 重新 GET effective 值渲染表单
  ├─ P2+：audit_logs（settings_reset）
  └─ inline 提示
```

## 8. 取消编辑

```text
dirty 状态
  ↓
点击「取消」
  ↓
丢弃本地 state，恢复最近一次 GET 快照
  ↓
清除 dirty 提示与 inline 错误
```

## 9. 媒体限制生效（跨模块）

```text
管理员 PATCH media.max_image_size_mb = 5
  ↓
UploadService.get_effective_settings()
  ↓
后续 POST /uploads（任意业务）
  ↓
按 effective 5MB 校验（非进程启动 snapshot）
```

## 10. 安全策略联动（P1）

```text
PATCH security.password_min_length = 10
  ↓
UserAdminService.reset_password / REQ-0015 change_password
  ↓
共用 validate_password_policy(password, effective_security_settings)
  ↓
不满足 → 422 + 业务错误码
```

## 11. 审计 Tab 最近变更（P2）

```text
GET /api/v1/admin/system-settings/audit/recent?limit=10
  ↓
查询 audit_logs WHERE domain=system_settings ORDER BY created_at DESC
  ↓
渲染：修改人、时间、summary
  ↓
无数据 → 空态
```

## 12. 与 REQ-0014 审计统一

```text
profile PATCH / login 成功
  ↓
写入 audit_logs（domain=profile, action_type=profile_update|login）
  ↓
（若 REQ-0014 已建 profile_activity_logs → 迁移或双写至 audit_logs）

system-settings PATCH / reset
  ↓
写入 audit_logs（domain=system_settings）
```

## 13. Phase 交付顺序（Sprint 建议）

```text
P0：路由 + Shell + basic + media
  ↓
P1：security（+ 可选 P1b 锁定）
  ↓
P2：audit_logs 全量 + audit Tab
  ↓
P3：notification Tab（无发信引擎）
```
