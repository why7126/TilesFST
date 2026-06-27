## 1. 前端 — 重置密码 confirm（BUG-0017 AC-001～AC-004）

- [x] 1.1 `UserManagementPage.tsx`：「重置密码」点击打开 confirm modal，不直接调 `resetUserPassword`
- [x] 1.2 新增 `resetPasswordConfirmTarget` state；移除 `handleResetPassword` 内 `window.confirm`
- [x] 1.3 modal 标题/正文/按钮对齐 design D3；结构对齐 `statusConfirmTarget` modal
- [x] 1.4 确认后调用 API；Toast + `setResetPassword` 打开 `ResetPasswordDialog`；取消/遮罩/× 不请求

## 2. 测试

- [x] 2.1 更新 `UserManagementPage.test.tsx`：重置密码须先出 dialog；确认前 `resetUserPassword` mock 未调用
- [x] 2.2 取消/关闭 dialog 后 mock 未调用；`window.confirm` spy 断言未调用
- [x] 2.3 确认「确认重置」后 mock 被调用且结果 state 更新
- [x] 2.4 回归冻结/删除 confirm 用例仍 pass
- [x] 2.5 运行 `cd src/web && npx vitest run src/pages/admin/UserManagementPage.test.tsx`
- [x] 2.6 回归 `BrandManagementPage.test.tsx`、`TileCategoryManagementPage.test.tsx` 启停用例
- [x] 2.7 运行 `cd src/web && npm run build`

## 3. 冒烟与追溯

- [ ] 3.1 本地/Docker：`/admin/users` 重置密码 confirm 手工冒烟（待 archive 前；可选）
- [x] 3.2 填写 `openspec/changes/fix-user-reset-password-confirm-ui/trace.md` checklist（≥8 项）
- [x] 3.3 更新 `issues/bugs/BUG-0017-user-reset-password-confirm-ui-inconsistency/trace.md`（`openspec_changes.status: applied`）
- [x] 3.4 更新 `iterations/sprint-002/acceptance-report.md` BUG-0017 验收状态
- [x] 3.5 完成后 `/opsx-archive fix-user-reset-password-confirm-ui`

## 4. 知识沉淀（可选）

- [x] 4.1 本缺陷为 UI confirm 形态对齐，通常可跳过 `docs/knowledge-base/incidents/`
