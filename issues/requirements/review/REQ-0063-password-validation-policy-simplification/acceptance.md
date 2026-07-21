---
requirement_id: REQ-0063-password-validation-policy-simplification
title: 密码校验规则简化 - 验收标准
status: pending_review
owner: product
created_at: 2026-07-20 19:53:30
updated_at: 2026-07-20 19:53:30
---

# 验收标准

## 功能 AC

- [ ] AC-001 密码长度少于 5 位时，前端字段校验失败，后端兜底校验也失败。
- [ ] AC-002 密码长度等于 5 位且包含英文字符和数字时，可通过基础密码策略校验。
- [ ] AC-003 密码长度等于 32 位且包含英文字符和数字时，可通过基础密码策略校验。
- [ ] AC-004 密码长度超过 32 位时，前端字段校验失败，后端兜底校验也失败。
- [ ] AC-005 密码缺少英文字符时校验失败，并提示“密码需包含英文字符”或等价文案。
- [ ] AC-006 密码缺少数字时校验失败，并提示“密码需包含数字”或等价文案。
- [ ] AC-007 密码包含符号且满足长度、英文、数字三类规则时可通过基础策略，除非后续 OpenSpec 明确收紧允许字符集。
- [ ] AC-008 修改本人密码、创建用户、重置密码等设置新密码入口均使用同一策略，不得出现一个入口仍要求至少 8 位、另一个入口允许 5 位的漂移。
- [ ] AC-009 管理端所有相关密码输入位置不再展示“至少 8 位”等旧规则提示。
- [ ] AC-010 后端 API 策略错误 message 与前端字段提示保持一致，无法映射到字段的服务端错误可进入固定表单错误区。
- [ ] AC-011 修改本人密码的原密码校验、新旧密码不得相同、限流、弱密码表、token 失效等既有安全能力不因本需求自动取消。
- [ ] AC-012 单元测试或集成测试覆盖 4 位失败、5 位成功、32 位成功、33 位失败、纯英文失败、纯数字失败、英文数字成功。

## UI / 交互 AC

- [ ] AC-013 密码规则提示位于新密码字段附近，不能只在提交失败后用全局 Toast 展示字段级错误。
- [ ] AC-014 修改密码弹窗在 1440px 桌面视口下保持既有 520px 窄弹窗策略，内容不因规则提示增加而溢出。
- [ ] AC-015 规则提示出现、消失或状态变化时不推挤页面主布局；弹窗内部可滚动时仅影响弹窗 body 区域。
- [ ] AC-016 管理端相关 UI 修改使用 Design System semantic token 和既有表单/弹窗组件，不新增裸 Hex。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-form-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 N/A — 本需求不新增全页表单页；若实现阶段触及设置页/表单页，页面内 accessible name 为“保存设置/保存修改”的主保存按钮必须仅 1 个，且位于表单 footer。
- [ ] AC-XCUT-002 N/A — 本需求不新增恢复默认或 dirty Tab 切换；若实现阶段触及放弃修改确认，必须使用 DS confirm modal，禁止 `window.confirm` / `window.alert`。
- [ ] AC-XCUT-003 保存或修改成功反馈必须使用 fixed toast 或既有 AdminLayout toast，不得在主表单和 summary 之间插入会导致 layout shift 的文档流 success banner。
- [ ] AC-XCUT-004 修改密码弹窗或其他密码弹窗 TSX 不得同时挂载通用 `modal-card` 与专属弹窗类；如需调整宽度，必须使用单一专属类或统一 modal semantic class。
- [ ] AC-XCUT-005 修改密码弹窗 computed width 必须与设计策略一致：窄弹窗保持 520px；如 OpenSpec 后续改为宽弹窗，必须明确 880px 并补 computed width 验收证据。
- [ ] AC-XCUT-006 弹窗在矮视口下 body scroll 无回归，规则提示较多时 footer 操作区仍可访问。

## 验收证据建议

- 后端测试：公共密码校验函数、修改密码 API、用户创建/重置相关路径。
- 前端测试：字段提示、旧文案清除、修改密码弹窗宽度和矮视口滚动。
- 文档/API：如涉及错误码或 OpenAPI message 示例，后续 Change 同步 `docs/03-api-index.md`、`docs/standards/error-codes.md` 和 Orval。
