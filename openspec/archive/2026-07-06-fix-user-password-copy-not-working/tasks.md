---
title: 管理端一次性密码复制可靠性修复任务
purpose: 跟踪 BUG-0059 fix change 的实现、测试与验收
created_at: 2026-07-06 15:33:45
updated_at: 2026-07-06 16:05:44
status: archived
owner: frontend
related_bug: BUG-0059-user-password-copy-not-working
---

# Tasks

## 1. 复核与准备

- [x] 1.1 对照 `issues/bugs/archive/BUG-0059-user-password-copy-not-working/bug.md`、`root-cause.md`、`acceptance.md` 确认修复范围。
- [x] 1.2 对照 `openspec/specs/user-management/spec.md` 中「管理端用户表单弹窗」「管理端用户列表行操作」确认 delta spec 标题一致。
- [x] 1.3 对照 `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`，确认本修复不引入弹窗宽度 CSS 层叠回归。

## 2. 前端修复

- [x] 2.1 更新 `src/web/src/features/admin/components/ResetPasswordDialog.tsx`，检测 `navigator.clipboard?.writeText` 可用性。
- [x] 2.2 成功复制时展示明确成功反馈，且反馈具备 `aria-live` 或等价可访问性语义。
- [x] 2.3 Clipboard API 不存在或写入失败时展示失败提示/手动复制指引。
- [x] 2.4 失败 fallback 尽可能 focus/select 当前一次性密码输入框，帮助管理员手动复制。
- [x] 2.5 保持「关闭后不可再次查看」风险提示清晰可见。
- [x] 2.6 不将一次性明文密码写入 localStorage、sessionStorage、URL、日志、审计事件或长期文档。
- [x] 2.7 若新增样式，使用既有 semantic token / CSS 变量，不新增裸 Hex。

## 3. 回归测试

- [x] 3.1 新增 `ResetPasswordDialog` 组件测试。
- [x] 3.2 覆盖复制成功路径，断言 `navigator.clipboard.writeText` 使用当前展示密码调用。
- [x] 3.3 覆盖复制成功反馈。
- [x] 3.4 覆盖 `writeText` reject 时的失败提示或手动复制指引。
- [x] 3.5 覆盖 Clipboard API 不存在时的 fallback 行为。
- [x] 3.6 覆盖一次性密码安全提示仍展示。
- [x] 3.7 复核 `UserManagementPage.test.tsx` 中 reset-password 链路，不因新增组件测试而弱化页面级回归。

## 4. 验证

- [x] 4.1 运行相关前端测试，例如 `pnpm --dir src/web test -- ResetPasswordDialog UserManagementPage` 或项目等价命令。
- [x] 4.2 如修改样式，运行或补充弹窗 CSS 层叠相关测试，确保 modal 宽度不回归。
- [x] 4.3 确认无需运行 Orval；若 API 契约被意外修改，停止并补充 API 文档、OpenAPI 与 Orval 生成物。
- [x] 4.4 记录验证结果到 change trace 或 BUG trace。

## 5. 收尾

- [x] 5.1 更新 `issues/bugs/archive/BUG-0059-user-password-copy-not-working/trace.md` 的 apply/验证记录。
- [x] 5.2 如修复经验可复用，评估是否补充 `docs/knowledge-base/incidents/` 或 best-practices；若无新增模式，在 trace 中说明 N/A。
- [x] 5.3 完成后执行 `/opsx-archive fix-user-password-copy-not-working`。
