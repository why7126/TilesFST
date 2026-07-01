---
title: 需求验收标准
purpose: REQ-0019 管理端超级管理员账号保护验收标准
content: 基于 requirement.md、business-flow.md 与 knowledge-base 横切规则生成
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD、评审结论或原型变更时同步更新
owner: product
status: draft
note: REQ-0019-admin-superuser-protection
created_at: 2026-06-30 13:56:49
updated_at: 2026-06-30 13:56:49
---

# 验收标准

## 1. 保护账号识别（FR-001、FR-002）

- [ ] **AC-001** 后端 MUST 以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护账号，默认值为 `admin`。
- [ ] **AC-002** 识别逻辑 MUST 对配置值做 `strip()`，并按现有用户名规范完成大小写归一化。
- [ ] **AC-003** `GET /api/v1/admin/users` 返回的每条用户记录 MUST 包含 `is_protected` 与 `protected_reason` 字段。
- [ ] **AC-004** `GET /api/v1/admin/users/{id}` 返回的用户详情 MUST 包含 `is_protected` 与 `protected_reason` 字段。
- [ ] **AC-005** `ADMIN_USERNAME` 对应账号返回 `is_protected=true`；普通管理员返回 `is_protected=false`。
- [ ] **AC-006** 前端 MUST NOT 通过硬编码 `admin` 判断保护状态，只能消费后端字段。

## 2. 用户编辑保护（FR-003）

- [ ] **AC-007** `PATCH /api/v1/admin/users/{id}` 对受保护账号 MUST 返回错误响应，HTTP 建议 403。
- [ ] **AC-008** 编辑受保护账号失败后，`display_name`、`role`、`avatar_object_key` MUST 保持不变。
- [ ] **AC-009** 普通用户编辑流程 MUST 保持 REQ-0005 既有行为。
- [ ] **AC-010** 前端列表中受保护账号「编辑」按钮 MUST 置灰，并展示 `protected_reason`。

## 3. 重置密码保护（FR-004）

- [ ] **AC-011** `POST /api/v1/admin/users/{id}/reset-password` 对受保护账号 MUST 返回错误响应，HTTP 建议 403。
- [ ] **AC-012** 重置受保护账号失败后，后端 MUST NOT 生成随机明文密码。
- [ ] **AC-013** 重置受保护账号失败后，`password_hash` MUST 保持不变，原密码登录能力不被破坏。
- [ ] **AC-014** 前端列表中受保护账号「重置密码」按钮 MUST 置灰，并展示 `protected_reason`。

## 4. 状态变更保护（FR-005）

- [ ] **AC-015** `PATCH /api/v1/admin/users/{id}/status` 对受保护账号请求 `active`、`disabled` 或 `deleted` 均 MUST 返回错误响应。
- [ ] **AC-016** 状态变更失败后，受保护账号 `status` MUST 保持原值，且不得被软删除。
- [ ] **AC-017** 前端列表中受保护账号「冻结 / 解冻」与「删除」按钮 MUST 置灰，并展示 `protected_reason`。
- [ ] **AC-018** 普通用户冻结、解冻、删除规则 MUST 保持 REQ-0005 既有行为。

## 5. 本人修改密码保护（FR-006，待评审确认）

- [ ] **AC-019** 默认策略下，当前登录用户为受保护账号时，`POST /api/v1/admin/profile/password` MUST 返回错误响应。
- [ ] **AC-020** 默认策略下，受保护账号本人改密失败后，`password_hash` MUST 保持不变。
- [ ] **AC-021** 默认策略下，受保护账号本人改密失败后，`token_version` MUST 不递增，旧 token 行为不因失败请求改变。
- [ ] **AC-022** 前端改密弹窗 MUST 展示接口返回 message，不得显示通用不明错误。
- [ ] **AC-023** 若评审确认允许受保护账号本人改密，AC-019~AC-022 MUST 在 review 中明确调整。

## 6. 错误码与 API 治理（FR-007）

- [ ] **AC-024** 后端 MUST 新增或复用清晰错误码表示“系统保底管理员账号不允许执行该操作”。
- [ ] **AC-025** 错误码 MUST 登记到后端错误码定义与 `docs/standards/error-codes.md`。
- [ ] **AC-026** API 响应 MUST 保持统一结构：`code`、`message`、`data`。
- [ ] **AC-027** OpenAPI MUST 暴露新增字段；API 变更后 MUST 执行 Orval 生成前端类型和客户端。

## 7. 前端 UI 与交互（FR-008、UI 约束）

- [ ] **AC-028** 受保护账号行必须保留操作按钮但置灰，不应完全隐藏，便于管理员理解保护规则。
- [ ] **AC-029** 置灰按钮样式 MUST 对齐用户管理页现有 disabled link button 风格。
- [ ] **AC-030** `protected_reason` SHOULD 通过 `title`、tooltip 或等价方式展示。
- [ ] **AC-031** 用户列表 prototype `prototype/web/admin-superuser-protection.html` MUST 作为实现时的轻量视觉参考。
- [ ] **AC-032** PNG Golden 可后续导出；未导出前需在 trace 中标注为非阻塞。

## 8. 运维恢复边界（FR-009）

- [ ] **AC-033** 本需求 MUST NOT 删除或禁用 `.env` 级 `ADMIN_RESET_PASSWORD_ON_STARTUP` 恢复机制。
- [ ] **AC-034** 管理端用户操作保护与部署 / 运维级恢复机制的边界 MUST 在 change design 中说明。
- [ ] **AC-035** 不得新增 `super_admin` / `root` 角色枚举，除非另起 REQ 和 OpenSpec Change。

## 9. 自动化测试

- [ ] **AC-036** pytest 覆盖用户列表返回受保护标识。
- [ ] **AC-037** pytest 覆盖编辑受保护账号被拒绝且字段不变。
- [ ] **AC-038** pytest 覆盖重置受保护账号密码被拒绝且 `password_hash` 不变。
- [ ] **AC-039** pytest 覆盖冻结 / 删除受保护账号被拒绝且 `status` 不变。
- [ ] **AC-040** pytest 覆盖本人修改密码策略（按评审结论拒绝或允许）。
- [ ] **AC-041** Vitest / Testing Library 覆盖受保护账号行操作按钮置灰和普通用户不受影响。

## 10. OpenSpec 与 trace

- [ ] **AC-042** 完成 req-review 后，MUST 通过 `/req-opsx REQ-0019-admin-superuser-protection` 创建 `update-admin-superuser-protection`。
- [ ] **AC-043** Change design MUST 引用 `trace.md` 的 `knowledge_base_refs`。
- [ ] **AC-044** Change tasks MUST 包含后端集成测试、前端列表按钮测试、Orval 生成与错误码文档同步。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] **AC-XCUT-001** 用户管理页分页 DOM 在实现后 MUST 仍对齐 `/admin/users` 基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数；本 REQ 不得为受保护账号保护改写分页结构。
- [ ] **AC-XCUT-002** 受保护账号操作失败或成功反馈 MUST 使用 fixed toast / 既有 AdminToast 模式，MUST NOT 使用文档流 notice 推挤 hero、筛选区或表格。
- [ ] **AC-XCUT-003** 状态变更类操作（普通用户冻结/解冻/删除）仍 MUST 使用 DS confirm modal；本 REQ 不得引入 `window.confirm`。
- [ ] **AC-XCUT-004** 受保护账号按钮置灰后，普通用户重置密码、冻结/解冻、删除确认流程 MUST 保持 DS confirm modal，且无 `window.confirm`。
