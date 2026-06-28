---
change_id: add-admin-sidebar-collapse
requirement_id: REQ-0011-admin-sidebar-expand-collapse
status: applied
created_at: 2026-06-27 10:55:42
updated_at: 2026-06-27 11:03:00
---

# Change Trace — add-admin-sidebar-collapse

## 关联

| 类型 | ID |
|---|---|
| REQ | REQ-0011-admin-sidebar-expand-collapse |
| 父 REQ | REQ-0010-product-version-display |
| Sprint | sprint-002 |

## 原型验收（apply 阶段）

| 检查项 | 路径 | 状态 |
|---|---|---|
| Expanded HTML | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-expanded.html` | pass（结构对齐：sidebar-head、chevron、264px） |
| Collapsed HTML | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapsed.html` | pass（72px、brand-mark、icon-only nav/user） |
| PNG expanded | `prototype/web/images/admin-sidebar-expanded.png` | 待导出（非阻塞） |
| PNG collapsed | `prototype/web/images/admin-sidebar-collapsed.png` | 待导出（非阻塞） |
| SoulKing 参考 | `/req-capture` 附件 | 参照 |

## 实现摘要

| 文件 | 变更 |
|---|---|
| `AdminLayout.tsx` | `sidebarCollapsed` state、`data-sidebar-state`、localStorage |
| `AdminSidebar.tsx` | `.sidebar-head`、chevron、`.brand-mark`、nav `aria-label` |
| `admin-home.css` | `--admin-sidebar-width`、collapsed 裁剪、220ms transition、mobile 隐藏 toggle |
| `admin-sidebar-preference.ts` | localStorage 读写 |
| Vitest | `AdminSidebar.collapse.test.tsx`、`AdminLayout.test.tsx` |

## 测试

- `npx vitest run` — 78 passed
- `npx vite build` — success

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 10:55:42 | `/req-opsx` | 创建 change；proposal/design/specs/tasks |
| 2026-06-27 11:03:00 | `/opsx-apply` | 实现侧栏折叠；tasks 20/20 |
