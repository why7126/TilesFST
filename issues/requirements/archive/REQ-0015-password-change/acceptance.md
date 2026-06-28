---
title: 需求验收标准
purpose: REQ-0015 管理端修改密码验收标准
content: 基于 requirement.md 与 prototype/web/password-change-modal-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0015-password-change
created_at: 2026-06-28 09:57:09
updated_at: 2026-06-28 09:57:09
---

# 验收标准

## 1. 入口与弹窗（FR-001 ~ FR-003、FR-010）

- [ ] **AC-001** 侧栏用户菜单点击「密码修改」MUST 打开居中弹窗，MUST NOT 跳转独立路由。
- [ ] **AC-002** 弹窗宽度 520px；标题「修改密码」；副标题展示当前账号显示名。
- [ ] **AC-003** 说明区含安全提示文案；左侧 2px 品牌金竖线（semantic token 实现）。
- [ ] **AC-004** 三字段：原密码、新密码、确认新密码；占位文案与 requirement FR-001 一致。
- [ ] **AC-005** 每字段 MUST 支持「显示 / 隐藏」切换。
- [ ] **AC-006** 打开弹窗后默认聚焦原密码；页面主体不可滚动。
- [ ] **AC-007** ×、取消、Esc 可关闭；有输入时 MUST 二次确认「当前填写内容尚未保存，确认关闭吗？」。
- [ ] **AC-008** `ChangePasswordModal` 由 `AdminLayout` 挂载；`AdminUserMenu` 使用 `onChangePassword`，不再走 placeholder。
- [ ] **AC-009** 弹窗 `role="dialog"`、`aria-modal="true"`，`aria-labelledby` 指向标题。

## 2. 前端校验与状态（FR-002、FR-004、FR-005）

- [ ] **AC-010** 新密码 8–32 位、至少字母+数字、不能与原密码相同；确认须一致。
- [ ] **AC-011** 新密码下方展示三条规则；满足项可切换成功态。
- [ ] **AC-012** 错误场景 inline 文案与 FR-005 表一致（含「两次输入的新密码不一致」等）。
- [ ] **AC-013** 提交时前端校验失败 MUST NOT 调用 API。
- [ ] **AC-014** 保存中按钮禁用、文案「保存中…」；不可重复提交。
- [ ] **AC-015** 成功 Toast：「密码修改成功，请使用新密码重新登录。」；随后跳转 `/admin/login`。

## 3. 后端 API（FR-006 ~ FR-008）

- [ ] **AC-016** `POST /api/v1/admin/profile/password` 须 Bearer 登录态；仅修改当前用户本人密码。
- [ ] **AC-017** 请求体 `{ old_password, new_password }`；成功 `ApiResponse` `data.success === true`。
- [ ] **AC-018** 原密码错误返回 400 + 登记错误码（建议 40020）；并记录失败 attempt。
- [ ] **AC-019** 弱密码、策略不符、与原密码相同返回对应 400 错误码（40021–40023）。
- [ ] **AC-020** 15 分钟内原密码错误 ≥ 5 次 → 429（建议 42901）。
- [ ] **AC-021** 24 小时内成功改密 ≥ 3 次 → 429。
- [ ] **AC-022** 成功后更新 `password_hash` 且 `token_version += 1`。
- [ ] **AC-023** OpenAPI 更新；Orval 重生成；`docs/03-api-index.md` 与 error-codes 同步。

## 4. Token 全端失效（FR-007）

- [ ] **AC-024** 登录 JWT MUST 含 `tv` claim，值为签发时 `token_version`。
- [ ] **AC-025** 改密成功后，改密前签发的 JWT 调用 `/api/v1/auth/me` 或其它受保护接口 MUST 401。
- [ ] **AC-026** 前端成功后清 localStorage token 与 remember 凭证（`clearLoginCredentials`）。

## 5. 安全（FR-009）

- [ ] **AC-027** 密码 MUST NOT 写入 URL、console 日志、埋点。
- [ ] **AC-028** 后端 MUST NOT 在响应中回显明文密码。

## 6. 视觉与原型（UI 约束）

- [ ] **AC-029** 1440×1024 下与 `prototype/web/password-change-modal.png` 并排验收（Sidebar、遮罩、弹窗、按钮、输入框）。
- [ ] **AC-030** TSX/CSS MUST 使用 semantic token；无裸 Hex。
- [ ] **AC-031** 输入框高度 44px；focus 品牌金边框；错误危险色边框。
- [ ] **AC-032** Footer：取消（幽灵）+ 保存修改（品牌金实底），高度 40px。

## 7. REQ-0014 协作（非阻塞，接口预留）

- [ ] **AC-033** `AdminLayout` 暴露 `openChangePasswordModal`（或等价 context），供后续 Profile 页复用。
- [ ] **AC-034** MUST NOT 在 Profile 路由重复实现改密表单（REQ-0015 交付时 Profile 可未上线）。

## 8. 回归

- [ ] **AC-035** 侧栏用户菜单「个人资料」placeholder 行为不变（直至 REQ-0014）。
- [ ] **AC-036** 「退出登录」流程无回归。
- [ ] **AC-037** 用户管理「重置密码」与其它 `/admin/*` 页面无布局回归。
- [ ] **AC-038** 未登录访问改密 API → 401。

## 9. 自动化与构建

- [ ] **AC-039** pytest：改密成功、原密码错误、弱密码、限流、旧 JWT 401。
- [ ] **AC-040** vitest：菜单打开弹窗、字段校验、脏关闭 confirm、成功 logout 跳转。
- [ ] **AC-041** `cd src/web && npm run build` 通过。
- [ ] **AC-042** 后端测试套件通过。

## 10. OpenSpec 与 trace

- [ ] **AC-043** 变更经 OpenSpec `add-*` 或 `fix-*` change 进入开发并 archive。
- [ ] **AC-044** `trace.md` PNG/HTML 并排 checklist 已勾选。
