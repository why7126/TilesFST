---
req_id: REQ-0015-password-change
status: exploring
created_at: 2026-06-28 09:41:12
updated_at: 2026-06-28 09:47:30
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0004-admin-home
---

# 一句话

实现 Web 管理后台「修改密码」能力：侧栏底部用户菜单入口 + 居中弹窗表单（原密码 / 新密码 / 确认新密码），含校验、显隐切换与修改成功后重新登录。

# 原始描述

实现修改密码功能。用户已提供 PRD 草稿与原型资产（见 `prototype/web/`）。

## 背景与目标

管理后台左侧底部用户菜单包含「个人资料、密码修改、退出登录」。本期补齐「修改密码」，使登录用户可在登录态下自主修改本人密码，降低管理员人工重置成本。采用居中弹窗承载表单，不改变用户管理页等信息架构；视觉继承用户管理列表页与 `ui-design.md` 工业石材暗色旗舰风。

## 范围

- **In**：侧栏用户菜单「密码修改」入口；520px 居中弹窗；原密码 / 新密码 / 确认新密码三字段；密码显隐切换；前端即时校验与规则提示；保存 / 取消 / 关闭（含 Esc、脏表单二次确认）；保存中 loading；成功后 Toast 并清理登录态跳转登录页；`POST /api/v1/admin/profile/password`
- **Out**：忘记密码；短信 / 邮箱 / 图形验证码；管理员替他人重置密码；多因素认证

## 表单与校验（摘要）

| 字段 | 必填 | 规则 |
|---|---|---|
| 原密码 | 是 | 非空；提交时后端校验是否正确 |
| 新密码 | 是 | 8–32 位；至少含字母与数字；不能与原密码相同 |
| 确认新密码 | 是 | 必须与新密码一致 |

后端二次校验：原密码正确性、服务端密码策略、修改频率限制。

## 交互要点

- 入口：用户卡展开菜单 → 点击「密码修改」打开弹窗，默认聚焦原密码，禁止主体滚动
- 关闭：右上角 ×、取消、Esc；有未保存输入时二次确认
- 提交：前端校验 → loading「保存中…」→ 调用接口 → 成功提示「密码修改成功，请使用新密码重新登录」→ 清理 token 跳转登录页
- 错误态：字段下 inline 文案（如「两次输入的新密码不一致」「原密码不正确，请重新输入」）

## 安全要求（摘要）

- 密码禁止明文持久化、禁止写入 URL / 日志 / 埋点
- 接口须登录态；成功后全端 token 失效（`users.token_version` + JWT `tv` 校验）

## 原型资产（已落盘）

- `prototype/web/password-change-modal.html` — 开发优先参考
- `prototype/web/password-change-modal.png` — Golden Reference
- `prototype/web/password-change-modal-context.md` — 布局与一致性 checklist

## 关联

- 父需求 `REQ-0004-admin-home`：侧栏底部用户菜单定义入口
- 姊妹需求 `REQ-0014-profile-page`：个人资料页 Out 范围外独立实现修改密码；两需求共享用户菜单入口形态

# 待澄清

- [x] 修改密码 API 路径是否与现有 API 治理对齐 → 见探索结论 §1
- [x] 成功后是否强制全端 token 失效 vs 仅当前 session → 见探索结论 §2
- [x] 修改频率限流与弱密码策略是否本期启用 → 见探索结论 §3
- [x] 弹窗与 `REQ-0014` 个人资料页「修改密码」入口是否共用同一组件 / 路由策略 → 见探索结论 §4

# 探索结论

> 记录时间：2026-06-28 09:47:30 · `/req-explore REQ-0015`

## 1. API 路径

**决策**：`POST /api/v1/admin/profile/password`；新建 `admin_profile` 路由组（prefix `/admin/profile`）。

- 与现有 `/api/v1/admin/*` 治理一致；`/auth/*` 保留无登录态 login/logout。
- 同组预留 `GET/PATCH /api/v1/admin/profile` 供 `REQ-0014-profile-page`。
- 请求体 `{ old_password, new_password }`；响应 `ApiResponse<{ success: true }>`。
- 需同步 error_codes、API 索引、Orval。

## 2. Token 策略

**决策**：改密成功后 **全端 token 失效**（非仅清当前浏览器 session）。

- 现状 JWT 无状态，`logout` 仅客户端清 token，旧 JWT 在 `exp` 前仍有效。
- 实现：`users.token_version`（默认 0）；login 时 JWT 含 `tv`；改密成功 `token_version += 1`；`get_current_user` 校验 `jwt.tv == db.token_version`，否则 401。
- 前端：成功后 `authStore.logout()` + 跳转 `/admin/login`。

## 3. 限流与弱密码（本期启用）

**决策**：本期启用服务端弱密码校验与改密频率限制。

| 能力 | 规则 |
|---|---|
| 复杂度 | 8–32 位；至少字母+数字；不能与原密码相同（前后端一致） |
| 弱密码 | 静态常见弱密码表（约 50–100 条） |
| 失败限流 | 15 分钟内原密码错误 ≥ 5 次 → 429 |
| 成功频率 | 24 小时内成功改密 ≥ 3 次 → 429 |

- 扩展 `user_validation.py` 新增 `validate_password()`；轻量 attempt 记录表。
- 建议错误码：40020 原密码错误、40021 策略不符、40022 弱密码、40023 与原密码相同、42901 过于频繁。

## 4. 弹窗与 REQ-0014 入口策略

**决策**：共享 `ChangePasswordModal` 组件，**无独立路由**；由 `AdminLayout` 托管 modal 开关。

```text
AdminLayout
├── ChangePasswordModal（520px 居中，唯一实现）
├── AdminUserMenu「密码修改」→ openModal()
└── ProfilePage（REQ-0014）账号安全卡片「修改密码」→ 同一 openModal()
```

- `AdminUserMenu` 由 `onPlaceholder()` 改为 `onChangePassword()`。
- REQ-0015 可独立先交付（侧栏入口）；REQ-0014 后接同一 callback。
- **REQ-0014 协调**：capture 中「跳转独立页面」应改为「打开共享修改密码弹窗」（REQ-0014 `/req-complete` 时修正）。

## 5. 与 REQ-0005 边界

- `POST /api/v1/admin/users/{id}/reset-password`：管理员替他人生成随机密码，无需原密码。
- REQ-0015：登录用户改本人密码，须校验原密码。能力不重复。

## 6. 工作量粗估

后端 API + migration + validation + 限流 ≈ 1.5d；前端 Modal + 菜单接入 + Orval ≈ 1d；测试 ≈ 0.5d → **约 3 人日**，适合单 Sprint 一项。
