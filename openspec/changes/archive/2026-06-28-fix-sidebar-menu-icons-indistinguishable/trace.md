---
created_at: 2026-06-28 10:40:00
updated_at: 2026-06-28 12:05:00
---

# fix-sidebar-menu-icons-indistinguishable — Trace

| 字段 | 值 |
|---|---|
| change_id | fix-sidebar-menu-icons-indistinguishable |
| bug_id | BUG-0021-sidebar-menu-icons-indistinguishable |
| requirement_id | REQ-0011-admin-sidebar-expand-collapse（父需求，已 archive） |
| iteration | sprint-003 |
| type | fix |
| status | applied |

## 关联文档

| 文档 | 路径 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/` |
| acceptance | `issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/acceptance.md` |
| collapsed 原型 | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapsed.html` |
| Sprint | `iterations/change/sprint-003/sprint.yaml` |

## 视觉验收（AC-010）

| 视口 | 结论 |
|---|---|
| 1280×1024 expanded | Lucide 16px 图标与 label 并排；active/hover 无回归 |
| 1280×1024 collapsed | 首页/ SKU/ 品牌等图标形状可区分；Vitest `AdminSidebar.icons.test.tsx` 覆盖 SVG 差异 |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 12:05:00 | `/sprint-apply` | admin-nav icon 映射 + AdminSidebar SVG + CSS + vitest |
| 2026-06-28 10:40:00 | `/bug-opsx` | 创建 change + artifacts |
