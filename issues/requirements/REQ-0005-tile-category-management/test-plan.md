---
title: 测试计划
purpose: REQ-0005 验收标准到测试用例映射
content: AC → unit / integration / manual
source: acceptance.md + business-flow.md
owner: product
status: draft
note: 实现阶段由 /opsx-apply 执行
---

# 测试计划

## 1. 映射总览

| AC | 描述摘要 | unit | integration | manual |
|---|---|:---:|:---:|:---:|
| AC-001 ~ AC-004 | 访问、布局、无导出 | ✓ | ✓ | ✓ |
| AC-005 ~ AC-006 | 指标卡 | ✓ | ✓ | ✓ |
| AC-007 ~ AC-009 | 检索与重置 | ✓ | ✓ | ✓ |
| AC-010 ~ AC-012 | 类目树联动 | ✓ | ✓ | ✓ |
| AC-013 ~ AC-015 | 列表与工具栏 | ✓ | ✓ | ✓ |
| AC-016 ~ AC-019 | 删除规则前后端 | ✓ | ✓ | ✓ |
| AC-020 ~ AC-022 | 分页与 page_size | ✓ | ✓ | ✓ |
| AC-023 ~ AC-028 | 弹窗字段与校验 | ✓ | ✓ | ✓ |
| AC-029 ~ AC-030 | 三级层级约束 | ✓ | ✓ | ✓ |
| AC-031 ~ AC-033 | API 与权限 | — | ✓ | — |
| AC-034 ~ AC-036 | 数据与迁移 | — | ✓ | — |
| AC-037 ~ AC-040 | 技术、单测、集成 | ✓ | ✓ | — |
| AC-041 ~ AC-043 | 视觉/HTML 并排 | — | — | ✓ |

## 2. 建议测试文件

```text
src/backend/tests/test_admin_tile_categories.py
  - list with filters, parent_id, summary
  - tree with sku_count and level indent
  - create level-1 without parent
  - create under level-2 → level-3 OK
  - create under level-3 → MAX_DEPTH_EXCEEDED
  - code duplicate → CATEGORY_CODE_DUPLICATED
  - delete forbidden when sku_count > 0 or ENABLED
  - delete allowed when sku_count=0 and DISABLED
  - enable / disable

src/web/src/pages/admin/TileCategoryManagementPage.test.tsx
  - tree node click filters list
  - delete link only on disabled zero-sku row
  - no export UI
  - toolbar only「调整排序」
  - page_size 10/20/50

src/web/src/features/admin/components/CategoryFormModal.test.tsx
  - single-column field order
  - sort_order positive integer
  - parent level-3 blocks save
```

## 3. 删除规则矩阵（必测）

| sku_count | status | 前端删除入口 | 后端 DELETE |
|---:|---|---|---|
| 0 | DISABLED | 展示可点 | 200 |
| 0 | ENABLED | 不展示 | 409 FORBIDDEN |
| >0 | DISABLED | 不展示 | 409 FORBIDDEN |
| >0 | ENABLED | 不展示 | 409 FORBIDDEN |

## 4. 层级深度矩阵（必测）

| 上级层级 | 新建子级 | 期望 |
|---|---|---|
| 无（根） | 一级 | 成功 |
| 一级 | 二级 | 成功 |
| 二级 | 三级 | 成功 |
| 三级 | 四级 | 拒绝 MAX_DEPTH |

## 5. 手工冒烟用例

1. 打开页面 → 四指标卡 + 类目树 + 列表与 HTML 布局一致。
2. 点击「按材质」树节点 → 列表仅显示该节点及子级。
3. 新增一级类目 → 树与列表刷新 → 默认启用。
4. 在二级下新增三级 → 成功；尝试在三级下新增 → 前端/服务端拒绝。
5. 停用 SKU=0 的类目 → 出现删除 → 确认删除成功。
6. 启用状态或 SKU>0 的行 → 无删除入口。
7. 重复类目编码 → 表单与服务端错误一致。
8. 切换每页 20 条 → 回到第 1 页，筛选条件保留。
9. 确认页面无「导出」按钮。

## 6. OpenSpec 阶段（本次未创建）

- 实现前执行 `/requirement-to-opsx REQ-0005-tile-category-management`。
- 建议 change_id：`add-tile-category-management`。
