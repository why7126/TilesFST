---
title: 业务流程
purpose: 个人资料查看、编辑、头像上传与操作记录审计主流程
content: 基于 requirement.md v1.1 与 prototype/web/profile-page-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 09:57:19
updated_at: 2026-06-28 18:53:00
note: REQ-0014-profile-page
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
侧栏用户菜单 → 「个人资料」
  ↓
GET /api/v1/profile/me + GET .../activities
  ↓
┌──────────────────────────────────────────────────────────┐
│ /admin/profile                                            │
│  ├─ 查看身份条 + 只读字段 + 可编辑表单                      │
│  ├─ 更换头像 → POST /uploads → PATCH avatar_object_key    │
│  ├─ 保存修改 → PATCH profile/me → inline「资料已更新」      │
│  ├─ 重置 → 丢弃本地编辑，恢复 GET 快照                      │
│  ├─ 修改密码 → 打开 REQ-0015 modal（非本 REQ 表单）         │
│  └─ 操作记录 timeline ← activities API（最近 **5** 条，v1.1）      │
└──────────────────────────────────────────────────────────┘
```

## 2. 与父需求 REQ-0004 差异

| 对比项 | REQ-0004（占位） | REQ-0014（本期） |
|---|---|---|
| 个人资料入口 | `onPlaceholder` toast | `navigate('/admin/profile')` |
| 密码修改入口 | 占位 toast | REQ-0015 modal |
| 页面 | 无 | 完整 profile 页 + API |
| 用户菜单高亮 | 无 | pathname `/admin/profile` 时高亮 |

## 3. 访问与权限

```text
JWT → ProtectedRoute（admin shell）
  ├─ role ∈ {admin, employee} → 允许 /admin/profile
  └─ role = store_owner → /admin/forbidden

API → require_admin_access
  ├─ role ∈ {admin, employee} → 允许 profile/me*
  └─ store_owner → 403
```

## 4. 页面加载

```text
进入 /admin/profile
  ↓
并行请求：
  GET /api/v1/profile/me
  GET /api/v1/profile/me/activities?limit=5
  ↓
渲染：page-head + profile-card + side-stack
  ↓
侧栏用户菜单展开时「个人资料」active
```

## 5. 保存资料

```text
用户编辑 display_name / email / phone / remark
  ↓
点击「保存修改」（页头或卡片内，行为一致）
  ↓
前端校验：昵称必填 2–32、邮箱/手机格式、备注 ≤200
  ↓
PATCH /api/v1/profile/me
  ↓
成功：
  ├─ 更新表单 baseline（重置基准）
  ├─ inline save-tip「资料已更新 · {timestamp}」
  ├─ 写入 profile_activity_logs（action_type=profile_update）
  └─ 刷新 activities timeline（或 prepend 新条目）
失败：
  └─ 字段级或表单级错误提示
```

## 6. 更换头像

```text
点击「更换头像」→ 选择文件
  ↓
POST /api/v1/uploads（avatar，require_admin_access）
  ↓
成功：
  ├─ 预览新 avatar_url
  ├─ PATCH profile/me { avatar_object_key }（或合并在下次保存，以实现为准）
  ├─ 写入 profile_activity_logs（avatar_update）
  └─ 刷新 timeline
失败：
  └─ inline 错误，保留旧头像
```

> 实现策略：若头像 PATCH 与表单 PATCH 分离，须在 OpenSpec design 中明确；acceptance 要求最终 persisted 与 MinIO 一致。

## 7. 重置

```text
用户有未保存编辑
  ↓
点击「重置」
  ↓
丢弃本地 state，恢复最近一次 GET /profile/me 快照
  ↓
清除 inline 错误与 save-tip（或恢复上次成功提示策略以实现为准）
```

## 8. 修改密码（入口，REQ-0015）

```text
触发点 A：用户菜单「密码修改」
触发点 B：profile 页账号安全卡片「修改密码」
  ↓
openPasswordChangeModal()  ← 与 REQ-0015 共用
  ↓
（弹窗内流程见 REQ-0015 business-flow）
```

## 9. 审计写入（登录）

```text
POST /api/v1/auth/login 成功
  ↓
现有：update last_login_at + login_logs
  ↓
新增：profile_activity_logs（action_type=login, summary=安全登录成功）
```

## 10. 操作记录展示

```text
GET /api/v1/profile/me/activities?limit=5
  ↓
按 created_at DESC
  ↓
映射 action_type → 展示标题：
  profile_update → 「资料更新」
  avatar_update  → 「头像更新」
  login          → 「登录后台」
  ↓
timeline：标题 + 时间 + summary 副文案
  ↓
无数据 → 空态「暂无操作记录」
```

## 11. 侧栏邮箱（FR-008）

```text
AdminSidebar / AdminUserMenu
  ↓
优先展示 user.email（来自 session 或 profile）
  ↓
email 为空 → fallback（username@ 占位或「未设置邮箱」，实现时二选一并在 trace 记录）
```
