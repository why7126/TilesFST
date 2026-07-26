## Context

- **缺陷**：BUG-0014；severity **high**；status **approved** / **in_sprint**。
- **现状**：`TileSkuManagementPage.tsx` L349–365 在 `status === 'DISABLED'` 时不渲染 publish 按钮。
- **正确参考**：`TileCategoryManagementPage.tsx`（BUG-0001 修复后）— 启停/恢复按钮与删除独立；`handlePublish` / `publishTileSku` 已存在。
- **需求依据**：`REQ-0006-tile-sku-management` AC-018（编辑、上下架/恢复）、AC-037（草稿/已停用可恢复或上架）；`business-flow.md` §6。
- **后端**：`TileSkuAdminService.publish_sku` 不限制来源 status，仅校验主图与必填项。

## Conflict Resolution

| 检查项 | 当前实现 | REQ acceptance | 决议 |
|--------|----------|----------------|------|
| DISABLED 行操作 | 编辑、删除 | 编辑、**恢复/上架**、删除 | **MODIFIED** 以 AC-018/AC-037 为准 |
| publish vs delete | 独立（delete 已正确） | 独立规则 | **MODIFIED** 移除 `!== 'DISABLED'` 排除 |

## Goals / Non-Goals

**Goals:**

- `DISABLED` 行展示「恢复」并可调用已有 `handlePublish` / `publishTileSku`。
- `DRAFT` / `NEEDS_COMPLETION` 行展示「上架」；`PUBLISHED` 行展示「下架」；删除规则不变。
- vitest 覆盖 BUG acceptance AC-001、AC-002、AC-009。
- 筛选、指标卡、分页、弹窗零回归。

**Non-Goals:**

- 后端 API、OpenAPI、Orval 变更。
- 状态操作确认弹窗（属 BUG-0016 范围，本 change 不强制引入）。
- 修改 HTML 原型文件。

## Decisions

### D1：操作列结构

```tsx
{item.status === 'PUBLISHED' ? (
  <button onClick={handleUnpublish}>下架</button>
) : (
  <button onClick={handlePublish}>
    {item.status === 'DISABLED' ? '恢复' : '上架'}
  </button>
)}
```

删除按钮保持现有 `canDeleteTileSku` 逻辑，与 publish 独立。

### D2：测试策略

- 扩展 `TileSkuManagementPage.test.tsx`（mock API），新增 DISABLED / PUBLISHED 列表项用例。
- 可选：后端 pytest 补充 `DISABLED → publish → PUBLISHED`（非必须，API 逻辑已覆盖 DRAFT 路径）。

## Risks

| 风险 | 缓解 |
|------|------|
| add-tile-sku-management 未 archive | delta MODIFIED 标题须与 add change 中「管理端瓷砖 SKU 管理页」一致 |
| BUG-0016 确认弹窗 | 本 change 不阻塞；可在后续 change 统一加 confirm |
| publish 校验失败 | 保持现有 `getErrorMessage` Toast，AC-005 覆盖 |
