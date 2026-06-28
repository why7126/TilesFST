---
req_id: REQ-0014-profile-page
status: in_sprint
created_at: 2026-06-28 09:36:56
updated_at: 2026-06-28 18:53:00
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0004-admin-home
---

# 一句话

实现 Web 管理后台「个人资料」页面：登录用户查看与维护头像、昵称、联系方式与备注；含账号安全与操作记录侧栏卡片；入口来自侧栏底部用户菜单。

# 原始描述

实现个人资料功能。用户已提供 PRD 草稿与原型资产（见 `prototype/`）。

## 背景与目标

个人资料页面用于后台登录用户查看与维护自身基础资料，入口来自左侧导航底部用户菜单的「个人资料」。页面需要继承管理后台暗色旗舰风，保持与首页、SKU 管理页、用户菜单一致的布局、色彩、边框、按钮与表单交互。

## 页面范围

- **In**：Web 管理后台「个人资料」页面
- **Out**：用户管理中管理员编辑他人资料；密码修改完整流程（由 `REQ-0015-password-change` 弹窗实现；本页仅提供入口）

## 信息架构

1. 左侧后台导航：保留现有 OPERATIONS 与 SYSTEM 导航，底部用户菜单展开个人资料、密码修改、退出登录
2. 顶部标题区：眉标 `SYSTEM / PROFILE`、页面标题「个人资料」、页面说明
3. 个人资料主卡片：头像、账号身份摘要、基础资料表单
4. 账号安全卡片：登录账号、角色、账号状态、最后登录时间、修改密码入口
5. 操作记录卡片：最近资料变更、最近登录、头像更新等审计记录

## 字段与规则（摘要）

| 模块 | 字段 | 必填 | 规则 |
|---|---|---|---|
| 头像 | 当前头像 | 否 | JPG/PNG/WebP，建议 400×400，最大 2MB |
| 基础资料 | 用户名 | 是 | 只读，系统登录名 |
| 基础资料 | 昵称 | 是 | 2–32 字符（与 admin 用户管理一致） |
| 基础资料 | 联系邮箱 | 否 | 邮箱格式 |
| 基础资料 | 手机号码 | 否 | 中国大陆手机号格式 |
| 基础资料 | 备注说明 | 否 | 最多 200 字 |
| 账号安全 | 所属角色 | — | 只读，不在基础资料表单重复（BUG-0022） |
| 账号安全 | 账号状态 | — | 只读，不在基础资料表单重复（BUG-0022） |

## 交互要点

- 用户名只读；角色与账号状态仅在账号安全卡片展示（不在基础资料表单重复）
- 「更换头像」展示上传操作（原型阶段可点击按钮表达）
- 「保存修改」校验昵称/邮箱/手机号；「重置」恢复进入页面时数据
- 「修改密码」打开 `REQ-0015` 居中弹窗（非独立路由）
- 用户菜单「个人资料」高亮；退出登录与前两项之间有分隔线

## 原型资产（已落盘）

- `prototype/web/profile-page.html` — 开发优先参考
- `prototype/images/profile-page.png` — Golden Reference
- `prototype/web/profile-page-context.md` — 布局与一致性 checklist

## 关联

- 父需求 `REQ-0004-admin-home`：侧栏用户菜单已定义「个人资料」占位入口，本期实现完整页面
- 视觉继承：SKU 管理页、admin-home 暗色旗舰风
- 姊妹需求 `REQ-0015-password-change`：共享用户菜单；profile 页「修改密码」与其共用弹窗入口

# 待澄清

- [ ] 后端 self-service API 路径命名（建议 `GET/PATCH /api/v1/auth/me/profile` 或 `/api/v1/profile`）
- [x] 操作记录展示条数上限：**5** 条（v1.1 修订，自 10–20 建议值收紧）
- [ ] 头像上传失败提示形态（inline / 字段旁文案，与 `UserFormModal` 对齐）
- [ ] `AdminUserMenu` 与 REQ-0015 菜单改造是否同 Sprint 一次交付

# 探索结论

（/req-explore 2026-06-28；决策确认 2026-06-28 09:51:20；操作记录拍板 2026-06-28 09:54:52）

## 范围与定位

- **单 REQ**：`/admin/profile` 独立页面；OpenSpec 预期 `add-admin-profile-page`（或同类 `add-*`）
- **父需求** `REQ-0004-admin-home`：替换用户菜单「个人资料」占位（`onPlaceholder`）
- **不重复** `REQ-0005-user-management`：admin 编辑他人 vs 用户编辑自己，API 与 UI 分离

## 已确认决策

| # | 议题 | 结论 |
|---|------|------|
| 1 | 备注字段 | **本期加 DB 列**（如 `users.remark`，max 200 字）；self PATCH 可写 |
| 2 | 昵称长度 | **沿用 admin 32**（`display_name` max_length=32）；PRD 原 2–20 以 admin 为准 |
| 3 | 修改密码入口 | **打开 REQ-0015 弹窗**；profile 账号安全卡片与用户菜单共用同一 modal 触发 |
| 4 | 角色范围 | **admin + employee** 均可访问并编辑个人资料（`require_admin_access`，非 `require_system_admin`） |
| 5 | 保存成功提示 | **inline「资料已更新」**（原型 `save-tip` 区域，非 toast） |
| 6 | 操作记录 | **完整审计（方案 A）**：新建审计表；记录资料更新、头像更新、登录等；操作记录卡片从 API 拉取 |

## 操作记录（完整审计）

- **新建表**（建议 `profile_activity_logs` 或项目统一 audit 命名）：`user_id`、`action_type`（如 `profile_update` / `avatar_update` / `login`）、`summary`、`metadata`（JSON，可选）、`created_at`
- **写入时机**：self PATCH 保存资料、头像 object_key 变更、登录成功（可与现有 `login_logs` 双写或 login 事件写入 audit）
- **读取**：`GET /api/v1/.../profile/activities`（或合入 profile GET）；默认最近 **5** 条（v1.1），按时间倒序
- **展示**：对齐原型 timeline（标题 + 时间 + 摘要，如「资料更新 · 修改昵称与备注」）

## 现状差距（实现要点）

```text
后端  GET/PATCH 当前用户 profile     → 新建（扩展 /auth/me 或独立 router）
      users.remark 列                 → 本期 migration
      profile_activity_logs 表       → 本期 migration + 写入/查询 service
      头像 upload 权限                → 从 require_system_admin 放宽至 require_admin_access
      UserProfile schema              → 扩展 avatar_url/email/phone/remark/last_login_at 等

前端  /admin/profile 路由 + 页面     → 新建 ProfilePage
      AdminUserMenu 个人资料          → navigate('/admin/profile')；pathname 高亮
      修改密码                        → 依赖 REQ-0015 modal（共用 hook/组件）
      getUserEmail 假数据             → 改用真实 email 字段
      操作记录 timeline               → 消费 activities API
```

## 容量粗估

- **含完整审计**：约 **3.5–4 人日**（含 migration、audit service、前后端联调）
- 与 **REQ-0015** 菜单改造建议同迭代紧耦合交付

## 下一步

1. `/req-generate REQ-0014-profile-page`
2. `/req-complete` 时同步 acceptance：remark 列、完整审计、昵称 32、REQ-0015 弹窗入口、inline 保存提示
