## Context

- **缺陷**：BUG-0001；severity **high**；status **approved**。
- **现状**：`TileCategoryManagementPage.tsx` L335–351 在 `deletable === true` 时不渲染「启用」。
- **正确参考**：`BrandManagementPage.tsx` — 启停按钮与删除按钮独立。
- **需求依据**：`REQ-0005-tile-category-management` AC-015（编辑、启用/停用）；AC-016/017 删除规则不变。
- **原型冲突**：HTML 样例停用行仅「编辑+删除」无「启用」；以 **acceptance + BUG 验收** 为准。

## Conflict Resolution

| 检查项 | HTML 原型 | 当前实现 | REQ acceptance | 决议 |
|--------|-----------|----------|----------------|------|
| 停用+SKU=0 行操作 | 编辑、删除 | 编辑、删除 | 编辑、**启用**、删除 | **MODIFIED** 以 AC-015 为准 |
| 启停 vs 删除 | 未显式分离 | 错误绑定 deletable | 独立规则 | **MODIFIED** 对齐 BrandManagementPage |

## Goals / Non-Goals

**Goals:**

- 停用行（任意 SKU）均展示「启用」并可调用已有 `enableCategory`。
- 启用行展示「停用」；删除规则不变。
- vitest 覆盖 BUG acceptance AC-009、AC-010。
- 弹窗、树、筛选、指标卡、分页零回归。

**Non-Goals:**

- 后端 API、OpenAPI、Orval 变更。
- 修改 HTML 原型文件（可选后续同步）。
- 「调整排序」占位实现。

## Decisions

### D1：复用 BrandManagementPage 操作列结构

```tsx
<button>{status === 'DISABLED' ? '启用' : '停用'}</button>
<button disabled={!deletable}>删除</button> // 仅 DISABLED 行展示
```

### D2：测试策略

- 新增 `TileCategoryManagementPage.test.tsx`（mock API）。
- 不新增后端 pytest（API 已正确）。

## Risks

| 风险 | 缓解 |
|------|------|
| add-tile-category-management 未 archive | delta MODIFIED 标题须与 add change 中「管理端瓷砖类目管理页」一致 |
| 原型 PNG 并排 | 修复后以 acceptance 手工冒烟为主 |
