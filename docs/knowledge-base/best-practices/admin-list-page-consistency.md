---
title: 管理端列表页一致性最佳实践
purpose: 预防管理端多列表页分页、反馈、操作列重复不一致类 BUG
content: 提炼自 Sprint 002 BUG-0002、0009、0015、0016 等
source: /sprint-exps sprint-002
update_method: 新模式或新页面时更新
owner: 前端负责人
status: draft
created_at: 2026-06-27 16:15:00
updated_at: 2026-06-27 16:15:00
note: 个案见 issues/bugs/；本文写模式与预防
---

# 管理端列表页一致性最佳实践

## 背景

Sprint 002 中用户、品牌、类目、SKU 四个列表页分别 port CSS，导致：

- 分页 DOM 与用户管理基准不一致（`BUG-0009`）
- 文档流 `.admin-notice` 推挤布局（`BUG-0015`，与 `BUG-0003` 同类）
- 状态操作缺少二次确认（`BUG-0016`）
- 停用行操作列逻辑与品牌页不一致（`BUG-0001`、`BUG-0014`）

## 必须对齐的基准

**视觉与 DOM 基准页**：`/admin/users`（`UserManagementPage` + `user-management.css`）

| 区域 | 要求 |
|------|------|
| 分页 | 左侧 `page-summary`「共 N 条/个」；右侧 `page-right` 页码 + 每页条数 |
| 表格卡片 | `table-card` 内 **无** 与 `page-head` 重复的 section 标题 |
| 操作反馈 | **fixed toast**（`fix-admin-list-status-toast-layout`），禁止 hero 前文档流 notice |
| 危险操作 | 启停、冻结、上架/下架、删除、重置密码 **MUST** DS confirm modal |
| 操作列 | 启用/停用/上架条件 **对齐品牌管理** 模式（对照 `BrandManagementPage`） |

## 实现优先级

```text
1. src/web/src/shared/templates/AdminListPage（或等价模板）
2. 共享 FixedAdminToast + AdminConfirmModal
3. 单页 port CSS 仅覆盖页面特有列与筛选，不重写分页/notice
```

## 验收 gate（新增列表页 MUST）

- [ ] 1440×1024 与用户管理分页 DOM 并排 diff pass
- [ ] 操作成功/失败 toast 不引起 hero/表格纵向位移
- [ ] 状态变更类操作均有 confirm；无 `window.confirm`
- [ ] Vitest：分页结构 smoke 或 snapshot（可选）

## 关联 BUG（个案）

- `issues/bugs/BUG-0002-brand-ui-inconsistency/`
- `issues/bugs/BUG-0009-tile-sku-list-ui-inconsistency/`
- `issues/bugs/BUG-0015-admin-list-status-tips-layout-shift/`
- `issues/bugs/BUG-0016-admin-list-status-action-confirm-missing/`

## 参考

- `rules/ui-design.md` 管理端列表章节
- `iterations/sprint-002/retrospectives` → `sprint-002-retrospective.md` §4
