## Context

- **BUG**: `BUG-0009-tile-sku-list-ui-inconsistency`
- **Severity**: medium
- **Root cause type**: design / frontend-ui
- **Related REQ**: `REQ-0006-tile-sku-management`
- **Parent change**: `add-tile-sku-management`（in-progress，34/35 tasks）
- **Reference fix**: `fix-brand-ui-consistency`（BUG-0002 分页对齐模式）
- **Target**: `TileSkuManagementPage.tsx` + `user-management.css` 分页类名复用

## Bug Analysis Report

### 现象

1. SKU 列表底部分页与用户管理页分页视觉/结构不一致。
2. 表格卡片表头上方存在多余「SKU 列表」标题行。

### 复现路径

1. admin 登录，访问 `/admin/tile-skus`。
2. 对比 `/admin/users` 底部分页 DOM 与样式。
3. 观察 `table-card` 内 `table-head` 区块。

### 影响

- 不阻断 SKU 查询、分页、CRUD。
- 阻塞 REQ-0006 AC-051 / AC-054 UI 一致性验收。
- 不影响 API、DB、权限、MinIO。

## Root Cause

### RC-001：分页复用废弃 brand 局部 DOM

SKU 页使用 `page-left` + `brand-pagination-right`，未对齐 `UserManagementPage` 的 `page-summary` + `page-right` 模式（BUG-0002 已在品牌页修复）。

### RC-002：table-card 内臆造二级标题

`table-head`「SKU 列表」与 `page-hero`「瓷砖 SKU」重复；原型 context 与 CSS 均无此结构。

## Design Decisions

### D1：分页 DOM 对齐 UserManagementPage

```text
.pagination
├── .page-summary     「共 {total} 条」
└── .page-right
    ├── .page-buttons
    └── .page-size-wrap
```

MUST NOT 使用 `page-left`、`brand-pagination-right`。

### D2：移除 table-card 内 table-head

`table-card` MUST 直接包含 `<table>`，与用户管理页一致。默认按更新时间倒序为列表行为（AC-018），无需卡片内标题行重复说明。

### D3：不扩大行为面

本 change 不修改：

- SKU API、筛选参数、分页逻辑。
- 表格列、行操作、指标卡、筛选区。
- 数据库、Orval、MinIO。

### D4：测试策略

参考 `BrandManagementPage.test.tsx`：

- 断言 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap` 存在。
- 断言 `.page-left`、`.brand-pagination-right` 不存在。
- 断言无 `.table-head` / `.table-title`。

## Test Strategy

- Vitest + RTL：`TileSkuManagementPage` 分页 DOM 与 table 结构。
- 人工：与 `/admin/users` 分页并排对比（1440×1024）。
- 构建：`cd src/web && npx vitest run …`；`npm run build`。

## Risks

| 风险 | 缓解 |
|---|---|
| 分页文案格式差异 | 对齐用户管理：`共 {total} 条` |
| 误删排序行为 | 仅移除 UI 标题行，API 仍 `updated_at DESC` |
| 回归 add-tile-sku-management | 不改变 API 调用与筛选逻辑 |

## 原型优先级

1. `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html`
2. `prototype/images/tile-sku-management-list.png`（可选）
3. `UserManagementPage.tsx` 分页黄金参考
4. BUG-0009 acceptance.md
