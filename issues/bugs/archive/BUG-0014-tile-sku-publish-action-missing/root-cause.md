---
bug_id: BUG-0014-tile-sku-publish-action-missing
status: pending_review
created_at: 2026-06-27 12:18:20
updated_at: 2026-06-27 12:18:20
root_cause_type: code
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code**（前端 UI 条件渲染） |
| 引入阶段 | `add-tile-sku-management` apply |
| 责任模块 | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 关联后端 | 无缺陷；`TileSkuAdminService.publish_sku` 已实现 |

## 2. 直接原因

操作列对 publish 按钮使用了错误的三元表达式（约 L349–365）：

```tsx
item.status === 'PUBLISHED'
  ? <下架按钮>
  : item.status !== 'DISABLED'
    ? <上架按钮>
    : null
```

当 `status === 'DISABLED'`（已下架）时，渲染结果为 `null`，**上架/恢复按钮被省略**。

`handlePublish` 与 `publishTileSku` API 封装已存在且可调用，缺陷仅为按钮未挂载。

## 3. 根本原因

1. **实现时对 DISABLED 状态的语义误判**：下架（unpublish）将 status 设为 `DISABLED` 后，开发可能将「已下架」视为无需再展示 publish 操作的终态，与 REQ-0006 `business-flow.md` §6「草稿 / 已停用 / 待完善 → 上架或恢复」矛盾。
2. **未对齐 BUG-0001 修复经验**：同类管理列表（类目停用行须展示「启用」）已在 `fix-tile-category-enable-action` 中确立「启停按钮始终存在 + 删除独立」模式，SKU 页 apply 时未复用同一结构。
3. **验收与自动化未覆盖 DISABLED 行操作列**：`add-tile-sku-management` trace 标注 publish/unpublish pass，但 vitest 仅覆盖 DRAFT 列表项与分页 DOM；AC-018 / AC-037 未在页面测试中断言 `DISABLED` 行 MUST 含 publish 入口。

## 4. 触发条件

同时满足即可稳定复现：

- 访问 `/admin/tile-skus`
- 列表中存在 `status === 'DISABLED'` 的 SKU 行（典型路径：先上架再下架）

不满足时（`DRAFT` / `NEEDS_COMPLETION`）正常显示「上架」，进一步印证条件仅错误排除 `DISABLED`。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| 后端未实现 publish API | 否；`POST .../publish` 存在且 `publish_sku` 不限制来源 status |
| 权限拦截 | 否；问题为按钮未渲染 |
| 新需求缺失 | 否；REQ-0006 FR-007、AC-018、AC-037 已覆盖 |
| 与 `canDeleteTileSku` 错误绑定 | 否（不同于 BUG-0001）；删除按钮独立渲染，publish 被显式 `!== 'DISABLED'` 排除 |

## 6. 修复方向

对齐 `TileCategoryManagementPage`（BUG-0001 修复后）与 REQ-0006 业务流：

- `PUBLISHED` 行：`编辑` + `下架` + `删除`（删除置灰）
- `DISABLED` 行：`编辑` + `恢复`（或「上架」）+ `删除`（可删）
- `DRAFT` / `NEEDS_COMPLETION` 行：`编辑` + `上架` + `删除`（可删）

无需数据库、API、Orval 变更。建议 Change：`fix-tile-sku-publish-action-missing`。
