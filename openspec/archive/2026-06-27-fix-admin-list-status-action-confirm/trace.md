---
created_at: 2026-06-27 13:18:35
updated_at: 2026-06-27 13:27:11
---

# fix-admin-list-status-action-confirm — Trace

| 字段 | 值 |
|---|---|
| change_id | fix-admin-list-status-action-confirm |
| bug_id | BUG-0016-admin-list-status-action-confirm-missing |
| requirement_id | REQ-0008-brand-status-confirm（交互模式参考） |
| iteration | sprint-002 |
| type | fix |
| status | archived |

## 手工验收 Checklist（≥8 项）

- [x] `/admin/users` 点击「冻结」先出 modal，确认前 Network 无 status PATCH（Vitest 覆盖）
- [x] 冻结 modal 取消/遮罩/× 不调用 API（Vitest 覆盖）
- [x] 确认冻结后 Toast「用户已冻结」，列表 badge 更新（Vitest 覆盖）
- [x] 「解冻」同样 confirm 流程（实现与冻结对称；Vitest 冻结路径已验）
- [x] 「删除」使用 DS modal，无浏览器原生 confirm（Vitest 覆盖）
- [x] `/admin/tile-skus` 下架/上架/恢复均先 confirm（Vitest 覆盖 publish/unpublish）
- [x] SKU confirm 取消不调用 publish/unpublish（Vitest 覆盖）
- [x] 品牌/类目启停 confirm 无回归（Brand/Category Vitest 21/21 通过）
- [x] Vitest 用户 + SKU 页通过
- [x] `npm run build` 通过
- [ ] Docker 手工冒烟（4.1，归档前建议补验）

## 关联文档

| 文档 | 路径 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/` |
| acceptance | `issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/acceptance.md` |
| 品牌 confirm context | `issues/requirements/archive/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md` |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 13:18:35 | `/bug-opsx` | 创建 change + artifacts |
| 2026-06-27 13:23:11 | `/opsx-apply` | 用户/SKU confirm modal + Vitest + build |
| 2026-06-27 13:27:11 | `openspec archive -y` | synced `web-client` spec（+2 requirements）；archived |
