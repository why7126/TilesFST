---
change_id: fix-product-version-ui-inconsistency
type: fix
bug_id: BUG-0013-product-version-ui-inconsistency
related_requirement: REQ-0010-product-version-display
related_change: add-product-version-display
status: applied
created_at: 2026-06-27 11:03:01
updated_at: 2026-06-27 11:08:57
---

# Change 追溯

## 来源

| 项 | 值 |
|---|---|
| BUG | BUG-0013-product-version-ui-inconsistency |
| 父需求 | REQ-0010-product-version-display |
| 父 Change | add-product-version-display（功能已 apply） |
| 严重度 | medium |

## 并排验收 Checklist

| 项 | 基准 | 状态 |
|---|---|---|
| 管理端 brand-head pill | `prototype/web/product-version-sidebar-admin.html` + Golden Reference PNG | pass — Badge `version` variant + `.brand-row .version-pill` admin CSS（边框 0.5px、背景 3%、muted 文字 10px、2px 圆角） |
| 店主端 brand-head pill | `prototype/web/product-version-sidebar-catalog.html` | pass — 共用 `ProductVersionBadge` / Badge variant |
| BUG acceptance | AC-001～AC-009 | pass |
| REQ-0010 视觉 AC | AC-006、AC-013、AC-015 | pass（待 REQ-0010 验收勾选） |

## 实现摘要

- `Badge` 新增 `version` variant；`ProductVersionBadge` 薄封装 + `version-pill` class
- `admin-home.css`：`.admin-shell .brand-row .version-pill` scoped 兜底
- Vitest：`product-version-badge.test.tsx` + AdminSidebar / Sidebar 样式断言
- `/design-system` Badge 区展示 `ProductVersionBadge`
- 移除 brand 容器重复 `aria-label`，保留 pill 级 a11y

## 测试

- `npx vitest run`：80/80 passed
- `npm run build`：通过

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 11:03:01 | `/bug-opsx` | 创建 fix-product-version-ui-inconsistency |
| 2026-06-27 11:08:57 | `/opsx-apply` | 实现 Badge variant + admin CSS + 测试 |

## 知识沉淀

无需 `docs/knowledge-base/incidents/`（UI 一致性 fix，无运维 incident 价值）。
