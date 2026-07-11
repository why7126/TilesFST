---
requirement_id: REQ-0032-clipboard-copy-helper-best-practice
title: Clipboard 复制交互沉淀共享 helper 或 best-practice 验收标准
status: archived
created_at: 2026-07-11 16:04:55
updated_at: 2026-07-11 20:10:50
---

# Acceptance Criteria

## 功能 AC

- [ ] AC-001 共享 helper 存在：Web 前端存在 `copyTextToClipboard` 或等价 helper，调用方无需直接重复编写 `navigator.clipboard?.writeText` 分支。
- [ ] AC-002 空值处理：待复制文本为 `null`、`undefined`、空字符串或仅空白时，helper 返回 `empty` 或等价状态，且不得调用 Clipboard API。
- [ ] AC-003 成功路径：Clipboard API 可用且 `writeText` resolve 时，helper 返回 `success`，并保留归一化后的复制文本供调用方按需使用。
- [ ] AC-004 API 不存在：`navigator.clipboard` 或 `writeText` 不存在时，helper 返回 `unavailable`，并在提供 fallback 回调时触发 fallback。
- [ ] AC-005 写入失败：`writeText` reject 或抛错时，helper 返回 `failed`，并在提供 fallback 回调时触发 fallback。
- [ ] AC-006 fallback 稳定性：fallback 回调自身抛错时不得导致页面崩溃，调用方仍可展示手动复制提示。
- [ ] AC-007 UI 解耦：helper 不直接调用 toast、dialog、埋点或页面专属 DOM；业务反馈由调用方根据结构化结果处理。
- [ ] AC-008 日志审计迁移：日志审计复制 `request_id` 接入 helper 后，成功提示、失败提示、API 不存在提示和 `copy_request_id` 成功埋点均保持可测。
- [ ] AC-009 重置密码迁移：重置密码弹窗接入 helper 后，复制失败或 API 不存在时仍会聚焦并选中随机密码输入框。
- [ ] AC-010 敏感信息保护：helper 和测试不得把随机密码、token、Authorization、Cookie、对象存储 key 等敏感内容写入日志或错误消息。
- [ ] AC-011 前端测试：helper 单元测试覆盖 success、failed、unavailable、empty、fallback 被调用和 fallback 抛错不崩溃。
- [ ] AC-012 代表场景测试：日志审计页与重置密码弹窗保留或补充测试，覆盖用户可见文案与关键副作用不回退。
- [ ] AC-013 文档沉淀：Web README、Design System 说明或 Change design 中记录复制 helper 的使用边界：helper 负责复制结果，调用方负责文案、toast 和埋点。

## 非功能 AC

- [ ] AC-014 兼容性：在 Clipboard API 不可用、浏览器拒绝写入、非安全上下文等情况下，用户可获得明确手动复制路径。
- [ ] AC-015 可访问性：复制结果反馈使用 `role="status"`、toast 或等价可访问机制，读屏用户可感知结果。
- [ ] AC-016 范围控制：实现不得新增后端 API、数据库字段、Orval 生成物、Docker Compose 配置或小程序复制适配。
- [ ] AC-017 Design System：新增或调整 UI 反馈不得引入裸 Hex，不得绕过现有按钮、toast、弹窗和 semantic token 规则。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防 Sprint 002/003/005 复发类缺陷

- [ ] AC-XCUT-001 日志审计列表若因复制交互改动分页区，分页 DOM MUST 保持用户管理基准结构：左侧 `page-summary`，右侧 `page-right`，不得因复制按钮调整破坏分页结构。
- [ ] AC-XCUT-002 日志审计列表复制成功/失败提示 MUST 使用 fixed toast 或等价不占文档流反馈，不得引起 hero、筛选区、表格或分页纵向位移。
- [ ] AC-XCUT-003 若复制能力实现中触发状态变更、危险操作或二次确认场景，MUST 使用 Design System confirm modal；N/A — 本 REQ 默认只读复制，不包含启停、删除、冻结等状态变更。
- [ ] AC-XCUT-004 本 REQ 相关实现 MUST NOT 引入 `window.confirm`。
- [ ] AC-XCUT-005 重置密码弹窗若调整 TSX className，MUST NOT 同时挂载通用 `modal-card` 与专属弹窗类，避免 CSS 层叠覆盖弹窗宽度。
- [ ] AC-XCUT-006 重置密码弹窗完成后 MUST 在 1440px 视口验证 Computed width 与既有设计一致；若本需求未改弹窗容器宽度，需在验收记录中注明 N/A — 未触达容器宽度。
- [ ] AC-XCUT-007 重置密码弹窗在矮视口下 body scroll MUST 无回归，复制失败后的手动复制提示不得遮挡输入框或页脚按钮。
- [ ] AC-XCUT-008 Sprint 005 复盘中的 Clipboard fallback 模式 MUST 被覆盖：成功、reject、API 不存在、手动复制 fallback 均有自动化测试或等价验收记录。
