---
change_id: add-admin-list-foundation-components
type: add
status: proposed
source_requirement: REQ-0029-admin-list-foundation-components
created_at: 2026-07-10 08:09:52
updated_at: 2026-07-10 08:29:59
iteration: sprint-005
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - design-system
    - web-client
---

# Trace

## 来源

| 类型 | ID / 文件 | 说明 |
|---|---|---|
| Requirement | `REQ-0029-admin-list-foundation-components` | 管理端列表基础组件（MetricCard 与分页窗口工具） |
| Parent Requirement | `REQ-0028-admin-list-page-contract` | 管理端列表页模板与横切契约 |
| Related BUG | `BUG-0055-admin-list-layout-unification` | 管理端列表页一致性复盘来源 |
| Knowledge Base | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | `.metric-*` 与 `.page-*` DOM 验收基线 |

## Requirement Readiness Report

| 项 | 结果 |
|---|---|
| status gate | Pass：REQ trace status 为 `approved` |
| readiness | Partially Ready |
| 原因 | requirement、user-stories、business-flow、acceptance、trace、HTML prototype 与 context 齐全；PNG Golden Reference 暂未导出 |
| 是否阻塞 req-opsx | 否 |

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - design-system
    - web-client
```

## Conflict Report

优先级：HTML prototype > prototype context > acceptance.md > knowledge-base > rules/ui-design.md > openspec/specs。

| 来源 | 结论 |
|---|---|
| HTML prototype | 采纳 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`、`.summary-grid`、`.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` 与最多 5 页码窗口。 |
| PNG Golden Reference | 未提供；后续设计验收可补充，不阻塞本 change proposed。 |
| prototype context | 采纳首批页面建议与 REQ-0028 边界说明。 |
| acceptance.md | 采纳 AC-001 至 AC-041 与 AC-XCUT。 |
| rules/ui-design.md | 实现必须走 Design System / semantic token，不采用裸 Hex 或页面私有颜色。 |
| openspec/specs | 以 `design-system`、`web-client` delta spec 承接，避免直接修改正式 specs。 |

## PNG Checklist

| 项 | 状态 | 说明 |
|---|---|---|
| PNG Golden Reference | pending | REQ 明确可后续设计验收导出 |
| HTML prototype | ready | `prototype/web/admin-list-foundation-components.html` |
| Context | ready | `prototype/web/admin-list-foundation-components-context.md` |

## Workflow

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-07-10 08:09:52 | req.opsx | 通过 OpenSpec CLI 创建 change 并生成 proposal、design、specs、tasks。 |
| 2026-07-10 08:15:42 | sprint.propose | 纳入 sprint-005 正式范围。 |
| 2026-07-10 08:29:59 | opsx.apply | 实现管理端列表基础组件、分页窗口共享工具、Design System 示例与首批 3 页接入。 |

## Implementation Notes

- 组件位置：`MetricCard` / `MetricCardGrid` 放入 `src/web/src/shared/ui/metric-card.tsx`，原因是它们是跨管理端列表页复用的复合 UI，符合 `rules/ui-design.md` 的复用优先级。
- 工具位置：`getPaginationWindow` 放入 `src/web/src/shared/lib/pagination-window.ts`，旧 `src/web/src/features/admin/lib/pagination.ts` 保留兼容导出，避免未迁移页面导入断裂。
- 首批页面：已接入 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`，覆盖普通指标、danger / 异常描述与分页窗口使用。
- 后续推广：`BrandManagementPage` 未纳入首批，后续可连同 `UserManagementPage`、`TileSpecManagementPage`、`TileCategoryManagementPage`、`BannerManagementPage` 逐步迁移。
- 样式策略：未新增颜色 token、裸 Hex 或硬编码 `rgba(...)`；沿用既有 `.metric-*`、`.summary-grid`、`.page-*` 管理端 DOM 与样式契约。
