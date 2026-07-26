## 1. 准备与定位

- [x] 1.1 阅读 BUG-0024、BUG-0025 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `ChangePasswordModal.tsx`、`password-change-modal.css` 与 `ChangePasswordModal.test.tsx`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO、Docker compose 变更

## 2. 前端修复（BUG-0024）

- [x] 2.1 拆分 `oldPasswordError` / `newPasswordError`；保留 `confirmError`
- [x] 2.2 客户端新密码规则校验写入 `newPasswordError`；原密码 API 40020 写入 `oldPasswordError`
- [x] 2.3 API catch 按 `error_code` 分流：40021/40022/40023/42901 → 新密码；40020 → 原密码
- [x] 2.4 将 `oldPasswordError` / `newPasswordError` 分别传入对应 `PasswordField` 的 `error` prop
- [x] 2.5 提交前清空各字段错误；错误 input 应用 `error` class

## 3. 前端修复（BUG-0025）

- [x] 3.1 为 `PasswordField` 增加 `.password-input-wrap`（或等价）包裹 input + `toggle-pass`
- [x] 3.2 将 `.toggle-pass` 绝对定位绑定至 wrap（非 `.password-field`）；`error-text` 置于 wrap 外
- [x] 3.3 更新 `password-change-modal.css`；MUST NOT 使用裸 Hex
- [x] 3.4 确认有 error 时三字段 toggle 垂直对齐一致

## 4. 测试

- [x] 4.1 新增 Vitest：客户端策略失败 → 错误在新密码字段容器内
- [x] 4.2 新增 Vitest：mock API 40022 → 「新密码过于常见」在新密码下，不在原密码下
- [x] 4.3 新增/保留：原密码 40020、确认不一致、成功提交用例
- [x] 4.4 SHOULD：确认不一致时 toggle 位于 input-wrap 内（BUG-0025 DOM 断言）
- [x] 4.5 更新 Vitest：dirty 表单点击「取消」→ MUST NOT 调用 `window.confirm`；`onClose` 被调用（BUG-0026）
- [x] 4.6 运行 `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal`

## 5. 前端修复（BUG-0026）

- [x] 5.1 删除 `isDirty` 与 `window.confirm`；`requestClose` 直接 `onClose()`
- [x] 5.2 确认 ×、Esc、遮罩仍绑定 `requestClose` 且行为一致
- [x] 5.3 保留 `open` 时 reset 逻辑（再次打开表单为空）

## 6. 验收与追溯

- [x] 6.1 复现 BUG-0024 截图场景：常见密码失败 → 错误在新密码字段下（vitest）
- [x] 6.2 复现 BUG-0025 截图场景：有 error 时 toggle 与无 error 字段对齐（CSS + DOM）
- [x] 6.3 复现 BUG-0026 截图场景：dirty 后点取消 → 直接关闭，无浏览器对话框（vitest）
- [x] 6.4 对照 BUG-0024 acceptance AC-001～AC-010 勾选
- [x] 6.5 对照 BUG-0025 acceptance AC-001～AC-010 勾选
- [x] 6.6 对照 BUG-0026 acceptance AC-001～AC-011 勾选
- [x] 6.7 填写本 change `trace.md` 验收结论
- [x] 6.8 更新 BUG-0024/0025/0026 `trace.md` 中 `openspec_changes` 状态（apply 后 → applied）
- [x] 6.9 评估 `docs/knowledge-base/incidents/`（本缺陷为 UI 表单，通常不需要）

## 7. 归档准备

- [x] 7.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-change-password-modal-errors`
