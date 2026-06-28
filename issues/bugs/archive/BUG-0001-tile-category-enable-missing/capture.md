---
bug_id: BUG-0001-tile-category-enable-missing
status: captured
recorded_at: 2026-06-20
severity_hint: high
environment: local|docker
related_requirement: REQ-0005-tile-category-management
related_change: add-tile-category-management
---

# 现象

瓷砖类目管理页（`/admin/tile-categories`）中，**已停用且 SKU 数量 = 0** 的类目行，操作列仅展示「编辑」「删除」，**缺少「启用」入口**，无法将类目重新启用。

# 复现步骤

1. 以 admin 登录管理端，进入「瓷砖类目」。
2. 找到或创建一条 **状态 = 停用** 且 **SKU 数量 = 0** 的类目（例如原型中的「样板专区」类行）。
3. 查看该行操作列。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 操作列展示「编辑」「启用」；若满足删除条件则 additionally 展示「删除」（见 `REQ-0005-tile-category-management` AC-015、FR-005）。后端 `POST .../enable` 已存在且可用。 |
| **实际** | 停用 + SKU=0 行仅「编辑」「删除」，无「启用」。停用 + SKU>0 行反而显示「启用」（删除按钮置灰）。 |

# 根因线索（待 /bug-generate 确认）

`TileCategoryManagementPage.tsx` 操作列条件渲染：

```tsx
{category.status === 'ENABLED' ? (停用) : deletable ? null : (启用)}
```

当 `deletable === true`（停用且 SKU=0）时错误渲染为 `null`，与 `canDeleteCategory` 语义混用。

# 附件

- 代码：`src/web/src/pages/admin/TileCategoryManagementPage.tsx`（约 L335–351）
- 需求：`issues/requirements/archive/REQ-0005-tile-category-management/acceptance.md` AC-015
- 对比：品牌管理页停用行展示「启用」+「删除」模式
