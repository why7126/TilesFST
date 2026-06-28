---
title: 需求验收标准
purpose: 个人资料页、self-service API、审计与 UI 验收
content: 基于 requirement.md v1.1 与 prototype/web/profile-page-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 09:57:19
updated_at: 2026-06-28 18:53:00
note: REQ-0014-profile-page
---

# 验收标准

## 1. 功能验收 — 访问与导航

- [ ] **AC-001** 已登录 `admin`/`employee` 可访问 `/admin/profile`；未登录跳转 `/admin/login`。
- [ ] **AC-002** `store_owner` 访问 `/admin/profile` 跳转 `/admin/forbidden`。
- [ ] **AC-003** 侧栏用户菜单「个人资料」导航至 `/admin/profile`，不再触发占位 toast。
- [ ] **AC-004** 在 profile 页时用户菜单「个人资料」高亮（`active` 态）；「密码修改」与「退出登录」之间有 0.5px 分隔线。
- [ ] **AC-005** 页头眉标 `SYSTEM / PROFILE`、标题「个人资料」、说明文案与 prototype 一致。

## 2. 功能验收 — 页面布局与视觉

- [ ] **AC-006** 两列布局：左 `1fr` 个人资料主卡片，右 `360px` 账号安全 + 操作记录（`profile-layout`）。
- [ ] **AC-007** 与 `prototype/images/profile-page.png` 并排验收：侧栏、卡片、按钮、输入框、timeline 视觉一致（1440×1024）。
- [ ] **AC-008** 使用 semantic token；禁止新增裸 Hex；主 CTA「保存修改」为品牌金实底。
- [ ] **AC-009** 输入框高度约 38px；卡片 0.5px 边框、3px 圆角、暗色半透明背景。

## 3. 功能验收 — 个人资料表单

- [ ] **AC-010** 身份条含：头像、昵称、角色摘要、邮箱、最近登录、标签区、「更换头像」。
- [ ] **AC-011** 字段顺序：用户名（只读）、昵称、联系邮箱、手机、备注；**MUST NOT** 在表单内重复展示所属角色、账号状态（二者仅在账号安全卡片展示，见 AC-022；BUG-0022 UX 定稿）。
- [ ] **AC-012** 昵称必填，2–32 字符；空值提示「请输入昵称」；超长提示「昵称长度为 2–32 个字符」。
- [ ] **AC-013** 邮箱格式错误提示「请输入正确的邮箱地址」；手机号格式错误提示「请输入正确的手机号」。
- [ ] **AC-014** 备注最多 200 字；超长提示「备注说明不能超过 200 字」。
- [ ] **AC-015** 「重置」恢复进入页面时 GET 快照；「保存修改」提交 PATCH 仅含可写字段。
- [ ] **AC-016** 保存成功后表单底部 inline「资料已更新」+ 时间戳（**非 toast**）。
- [ ] **AC-017** 页头与卡片内「保存修改」行为一致。

## 4. 功能验收 — 头像上传

- [ ] **AC-018** 支持 JPG/PNG/WebP，最大 2MB；走 `POST /api/v1/uploads` + MinIO。
- [ ] **AC-019** `employee` 角色可上传头像（`require_admin_access`）。
- [ ] **AC-020** 上传失败展示错误原因，保留旧头像；交互与 `UserFormModal` 对齐。
- [ ] **AC-021** 头像变更 persisted 后写入 `profile_activity_logs`（`avatar_update`）。

## 5. 功能验收 — 账号安全卡片

- [ ] **AC-022** 展示：登录账号、账号状态 badge、所属角色、最后登录（含 UA 摘要，若 API 提供）。
- [ ] **AC-023** 「修改密码」打开 REQ-0015 密码修改弹窗（非路由跳转）；与用户菜单入口共用同一 modal 机制。

## 6. 功能验收 — 操作记录

- [ ] **AC-024** 从 `GET /api/v1/profile/me/activities` 加载最近 **5** 条（v1.1），timeline 倒序；记录数不足 5 时展示实际条数。
- [ ] **AC-025** 至少展示三类：`profile_update`（资料更新）、`login`（登录后台）、`avatar_update`（头像更新）。
- [ ] **AC-026** 每条含：标题、时间、summary 副文案（对齐 prototype 示例格式）。
- [ ] **AC-027** 无数据时展示空态，页面不报错。
- [ ] **AC-028** 登录成功双写 audit（与 `login_logs` 并存）；PATCH 成功写 `profile_update`。

## 7. 接口验收

| 接口 | 说明 |
|---|---|
| `GET /api/v1/profile/me` | 完整 profile（avatar_url、remark、last_login_at 等） |
| `PATCH /api/v1/profile/me` | 更新 display_name、email、phone、remark、avatar_object_key |
| `GET /api/v1/profile/me/activities` | limit 默认 **5**（v1.1） |
| `POST /api/v1/uploads` | 头像；admin + employee 可调用 |

- [ ] **AC-029** 路径符合 `rules/api.md`；统一 `ApiResponse` 包装。
- [ ] **AC-030** PATCH 仅允许修改 token 对应用户；不可改 username/role/status。
- [ ] **AC-031** OpenAPI 更新 + Orval 重新生成前端客户端。
- [ ] **AC-032** `store_owner` 调用 profile API 返回 403。

## 8. 数据验收

- [ ] **AC-033** Migration 新增 `users.remark` TEXT NULL（0–200 字）。
- [ ] **AC-034** Migration 新建 `profile_activity_logs`（id、user_id、action_type、summary、metadata、created_at）。
- [ ] **AC-035** `action_type` 枚举至少含 `profile_update`、`avatar_update`、`login`。

## 9. 技术验收

- [ ] **AC-036** 后端 pytest：GET/PATCH profile、activities、RBAC、审计写入、校验错误。
- [ ] **AC-037** 前端 vitest：ProfilePage 校验、重置、保存 mock、菜单导航。
- [ ] **AC-038** 侧栏邮箱优先使用真实 `email`（FR-008）；无 email 时 fallback 行为 documented。
- [ ] **AC-039** `trace.md` PNG 并排 checklist 在 `/opsx-apply` 阶段填写。

## 10. 原型 trace checklist（开发阶段）

| 检查项 | HTML | PNG | 实现 |
|---|---|---|---|
| 侧栏 264px + 用户菜单高亮 | ✓ | ✓ | |
| profile-layout 两列 | ✓ | ✓ | |
| 身份条 + 表单字段顺序 | ✓ | ✓ | |
| save-tip inline 成功态 | ✓ | ✓ | |
| 账号安全 + 修改密码按钮 | ✓ | ✓ | |
| 操作记录 timeline | ✓ | ✓ | |
| 退出登录分隔线 | ✓ | ✓ | |

## 11. 范围外（不验收）

- REQ-0015 弹窗内表单、校验、改密 API、成功后 re-login（归属 REQ-0015）。
- 管理员在用户管理页编辑他人资料。
- 导出操作记录、管理员查看他人 audit。
