---
title: 用户故事
purpose: REQ-0014-profile-page 个人资料页各角色用户故事
content: 基于 requirement.md v1.1 与 prototype/web/profile-page-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 09:57:19
updated_at: 2026-06-28 18:53:00
note: REQ-0014-profile-page
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 后台运营 | P0 | 是 |
| US-002 | 后台管理员 | P0 | 是 |
| US-003 | 后台运营/管理员 | P1 | 是（依赖 REQ-0015） |
| US-004 | 店主 | P2 | 否（不得访问管理端） |

---

## US-001 后台运营维护个人资料

**作为** 后台运营人员，  
**我希望** 在管理后台查看并更新自己的头像、昵称、联系方式与备注，  
**以便** 同事能识别我并在系统通知中联系到我。

### 验收要点

- 侧栏用户菜单「个人资料」进入 `/admin/profile`，不再显示「功能建设中」占位。
- 可编辑昵称（2–32 字）、邮箱、手机、备注（≤200 字）；用户名只读；角色与账号状态在账号安全卡片查看（不在表单重复）。
- 「保存修改」成功后表单底部 inline 显示「资料已更新」及时间戳。
- 「重置」恢复进入页面时的服务端数据。
- 「更换头像」上传 JPG/PNG/WebP（≤2MB）；失败保留旧头像并提示原因。
- 右侧操作记录展示最近 **5** 条审计 timeline（v1.1；侧栏卡片轻量预览）。

### 关联功能

- FR-001、FR-002、FR-004、FR-006、FR-007

---

## US-002 后台管理员维护个人资料

**作为** 后台管理员，  
**我希望** 与运营人员一样访问个人资料页并受相同 RBAC 约束，  
**以便** 自助维护展示信息，无需他人代改。

### 验收要点

- `admin`、`employee` 均可 GET/PATCH `/api/v1/profile/me` 与 activities API。
- `employee` 可上传头像（`require_admin_access`，非 `require_system_admin`）。
- PATCH 仅能修改当前登录用户本人，不能通过 API 修改他人。
- `store_owner` 访问 profile 路由跳转 forbidden；API 返回 403。

### 关联功能

- FR-001、FR-007、API §6

---

## US-003 从个人资料页修改密码（入口）

**作为** 已登录后台用户，  
**我希望** 在个人资料页或用户菜单快速打开修改密码弹窗，  
**以便** 自主更新登录凭证。

### 验收要点

- 账号安全卡片「修改密码」与用户菜单「密码修改」均打开 **REQ-0015** 居中弹窗（非页面跳转）。
- 弹窗实现与验收归属 REQ-0015；本 REQ 仅验收入口可达、行为一致。
- REQ-0015 未交付时，入口可 stub 或同 Sprint 联调（trace 关联）。

### 关联功能

- FR-005、关联 REQ-0015-password-change

---

## US-004 店主不得访问个人资料页（边界）

**作为** 店主，  
**我希望** 无法进入管理端个人资料页，  
**以便** 权限边界与现有管理端 RBAC 一致。

### 验收要点

- `store_owner` 登录后访问 `/admin/profile` 跳转 `/admin/forbidden`。
- 不得调用 profile self-service API。

### 关联功能

- FR-001

---

## 与 REQ-0005 用户管理差异

| 维度 | REQ-0005 用户管理 | REQ-0014 个人资料 |
|---|---|---|
| 编辑对象 | 管理员编辑他人 | 用户编辑自己 |
| 入口 | SYSTEM → 用户管理 | 侧栏用户菜单 |
| API | `/api/v1/admin/users/{id}` | `/api/v1/profile/me` |
| 权限 | `require_system_admin` | `require_admin_access` |
| 角色/用户名 | 管理员可改 role | 只读 |
