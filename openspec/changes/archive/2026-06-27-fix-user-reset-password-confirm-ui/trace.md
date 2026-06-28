---
created_at: 2026-06-27 13:34:57
updated_at: 2026-06-27 13:37:39
---

# fix-user-reset-password-confirm-ui — Trace

| 字段 | 值 |
|---|---|
| change_id | fix-user-reset-password-confirm-ui |
| bug_id | BUG-0017-user-reset-password-confirm-ui-inconsistency |
| requirement_id | REQ-0005-user-management |
| iteration | sprint-002 |
| type | fix |
| status | archived |

## 手工验收 Checklist（≥8 项）

- [x] `/admin/users` 点击「重置密码」先出 DS modal，非 `window.confirm`（Vitest）
- [x] 确认前 `resetUserPassword` mock 未调用（Vitest）
- [x] 取消/遮罩/× 不调用 API（Vitest 取消路径）
- [x] 确认后 Toast「密码已重置」（Vitest）
- [x] 确认后调用 `resetUserPassword`（Vitest）
- [x] modal 结构对齐同页冻结 confirm（`modal-backdrop` / `modal-card`）
- [x] 同页冻结/删除 confirm 无回归（Vitest 7/7）
- [x] 品牌/类目启停 confirm 无回归（Vitest 10/10）
- [x] `npm run build` 通过
- [ ] Docker 手工冒烟（3.1，archive 前建议）

## 关联文档

| 文档 | 路径 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/` |
| acceptance | `issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/acceptance.md` |
| 类目 confirm 参考 | `src/web/src/pages/admin/TileCategoryManagementPage.tsx` |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 13:34:57 | `/bug-opsx` | 创建 change + artifacts |
| 2026-06-27 13:37:39 | `/opsx-apply` | 重置密码 confirm modal + Vitest + build |
| 2026-06-27 13:40:00 | `openspec archive -y` | synced `web-client` spec（+1 requirement）；archived |
