---
title: 根因分析
purpose: BUG-0001 直接原因与根本原因
bug_id: BUG-0001-tile-category-enable-missing
status: draft
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code**（前端 UI 条件渲染） |
| 引入阶段 | `add-tile-category-management` apply |
| 责任模块 | `src/web/src/pages/admin/TileCategoryManagementPage.tsx` |

## 2. 直接原因

操作列对「启用」按钮使用了错误的三元表达式：

```tsx
category.status === 'ENABLED'
  ? <停用按钮>
  : deletable ? null : <启用按钮>
```

当 `deletable === true`（`status === 'DISABLED'` 且 `sku_count === 0`）时，渲染结果为 `null`，**启用按钮被省略**。

这与 `canDeleteCategory` 的设计意图不符：`canDeleteCategory` 仅应控制 **删除** 是否可点击，不应影响 **启用/停用** 切换的展示。

## 3. 根本原因

1. **实现时误读 HTML 原型**：列表 HTML 中停用且 SKU=0 的样例行（「样板专区」）仅绘制「编辑 + 删除」，未画「启用」，开发将其当作互斥逻辑（「能删就不能启」）。
2. **验收标准未在 UI 测试覆盖**：`tile-categories-api.test.ts` 仅测 `canDeleteCategory` 函数，未测页面操作列组合；AC-015 未在 vitest 中断言停用+SKU=0 行必须含「启用」。
3. **参考实现未对齐**：同 Sprint 的 `BrandManagementPage` 已采用「启停按钮始终存在 + 删除独立」模式，类目页未复用同一结构。

## 4. 触发条件

同时满足：

- 类目 `status === 'DISABLED'`
- 类目 `sku_count === 0`（或汇总为 0，与 API 返回一致）

不满足时（停用但 SKU>0）反而显示「启用」，进一步印证条件写反。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| 后端未实现 enable API | 否；`enableCategory` / `POST .../enable` 存在 |
| 权限拦截 | 否；问题为按钮未渲染 |
| 新需求缺失 | 否；REQ-0005 FR-005 / AC-015 已覆盖 |

## 6. 修复方向

对齐 `BrandManagementPage`：

- 停用行：`编辑` + `启用` + `删除`（删除按 deletable）
- 启用行：`编辑` + `停用`（无删除）

无需数据库、API、Orval 变更。
