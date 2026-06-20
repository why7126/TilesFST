---
bug_id: BUG-0001-tile-category-enable-missing
title: 瓷砖类目停用行缺少「启用」操作入口
status: done
iteration: sprint-002
severity: high
environment: local|docker
recorded_at: 2026-06-20
related_requirement: REQ-0005-tile-category-management
related_change: add-tile-category-management
suggested_fix_change: fix-tile-category-enable-action
---

# BUG-0001 瓷砖类目停用行缺少「启用」操作入口

## 1. 摘要

管理端瓷砖类目列表页，对 **已停用且 SKU 数量为 0** 的类目行，操作列未展示「启用」按钮，导致运营无法通过 UI 重新启用该类目。后端 `POST /api/v1/admin/tile-categories/{id}/enable` 已实现且可用，缺陷限定于前端操作列条件渲染逻辑。

## 2. 影响范围

| 维度 | 说明 |
|---|---|
| 终端 | Web 管理端 `/admin/tile-categories` |
| 用户 | 后台管理员、运营 |
| 数据 | 无数据损坏；停用类目无法通过 UI 恢复启用 |
| 后端 / API | 无变更需求 |
| 小程序 / 店主端 | 不涉及 |

## 3. 复现

### 前置条件

- 已部署或本地运行 sprint-002 类目管理能力（`add-tile-category-management`）
- 使用 `role=admin` 账号登录

### 步骤

1. 访问 `/admin/tile-categories`。
2. 将某类目 **停用**，且确保其 **SKU 数量 = 0**（或筛选状态下拉选「停用」找到此类目）。
3. 观察该行「操作」列。

### 实际结果

- 展示：**编辑**、**删除**
- 不展示：**启用**

### 期望结果

- 展示：**编辑**、**启用**、**删除**（删除可点，因满足 SKU=0 且停用）
- 与 `REQ-0005-tile-category-management` AC-015、FR-005 一致
- 行为对齐品牌管理页：停用行始终有启用/停用切换，删除独立按 `canDelete*` 控制

## 4. 对比：品牌管理（正确参考）

品牌页对任意行均渲染启用/停用切换按钮，删除按钮独立判断 `canDeleteBrand`：

```tsx
{brand.status === 'DISABLED' ? '启用' : '停用'}
```

类目页错误地将 `canDeleteCategory` 与「是否展示启用」绑定。

## 5. 修复建议（供 bug-opsx）

1. `TileCategoryManagementPage.tsx`：停用行 **始终** 展示「启用」；启用行展示「停用」。
2. 「删除」仍仅对 `status === 'DISABLED'` 行展示，且 `disabled={!deletable}`。
3. 补充 vitest：停用 + SKU=0 行应同时存在「启用」「删除」文案（可 mock 列表数据）。
4. 回归：启用行仍仅「编辑」「停用」，无删除。

## 6. 关联验收

- 父需求 AC-015、AC-016、AC-017
- OpenSpec（待建）：`fix-tile-category-enable-action`
