---
title: 需求验收标准
purpose: REQ-0003 登录页记住凭证与密码显隐验收
content: 基于 requirement.md 与 prototype/web/login-form-enhancements-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0003-login-remember-autofill
---

# 验收标准

## 1. 记住登录状态 · 自动填充

- [ ] **AC-001** 勾选「记住登录状态」且登录成功后，本地持久化 username 与 password（可经 DevTools → Application → localStorage 验证专用 key）。
- [ ] **AC-002** 关闭标签页或浏览器后再次打开 `/admin/login`，用户名、密码已自动填充，复选框为勾选。
- [ ] **AC-003** 未勾选「记住登录状态」登录成功后，本地不再保留（或已清除）上次保存的 username/password。
- [ ] **AC-004** 自动填充后用户修改账号或密码并成功登录（且勾选记住），以最新成功值更新本地存储。
- [ ] **AC-005** 登录失败时不更新本地已保存凭证。
- [ ] **AC-006** 勾选记住时，`remember_me=true` 仍传后端，JWT 长有效期行为与现网一致（7 天 localStorage token）。
- [ ] **AC-007** 未勾选时 JWT 短有效期行为与现网一致（sessionStorage）。

## 2. 登出与清除

- [ ] **AC-008** 退出登录后，本地保存的登录凭证被清除。
- [ ] **AC-009** 退出后再次进入登录页，表单为空，记住复选框未勾选（除非用户重新勾选并成功登录）。

## 3. 密码显示/隐藏

- [ ] **AC-010** 密码框右侧（或规范位置）有显隐切换按钮/图标。
- [ ] **AC-011** 默认密文显示；点击后切换明文，再点击恢复密文。
- [ ] **AC-012** 切换显隐不清空密码值（含自动填充的密码）。
- [ ] **AC-013** 显隐控件具备 `aria-label`（或等价）且可键盘聚焦操作。
- [ ] **AC-014** 样式符合登录页 CSS Port，无裸 Hex。

## 4. 安全与回归

- [ ] **AC-015** 密码不出现在服务端日志、数据库明文字段。
- [ ] **AC-016** 现有登录校验（空账号/空密码、401 提示）无回归。
- [ ] **AC-017** `REQ-0003-login-left-panel-refine` 左栏布局、隐藏忘记密码等已落地项无回归。
- [ ] **AC-018** 单元测试覆盖：凭证 save/clear/load、登出清除、显隐切换状态。
- [ ] **AC-019** `npm run build` 与 auth 相关 vitest 通过。

## 5. 技术流程

- [ ] **AC-020** 变更经 OpenSpec change（建议 `add-login-remember-autofill`）进入开发。
- [ ] **AC-021** 若 delta spec 修改 web-client「记住我」场景，归档时标题与 `openspec/specs/` 一致。

## 6. 不在本期

- 找回密码、企业微信登录、加密硬件存储、跨设备同步凭证。
