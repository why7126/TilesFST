---
title: 测试计划
purpose: add-tile-category-management 验收标准到测试用例映射
content: AC → unit / integration / manual
source: issues/requirements/REQ-0005-tile-category-management/test-plan.md
owner: product
status: draft
note: 实现阶段由 /opsx-apply 执行
---

# 测试计划

## 1. 映射总览

| AC 范围 | unit | integration | manual |
|---|---|:---:|:---:|
| AC-001 ~ AC-004 访问布局无导出 | ✓ | ✓ | ✓ |
| AC-005 ~ AC-006 指标卡 | ✓ | ✓ | ✓ |
| AC-007 ~ AC-009 检索 | ✓ | ✓ | ✓ |
| AC-010 ~ AC-012 类目树联动 | ✓ | ✓ | ✓ |
| AC-013 ~ AC-015 列表工具栏 | ✓ | ✓ | ✓ |
| AC-016 ~ AC-019 删除规则 | ✓ | ✓ | ✓ |
| AC-020 ~ AC-022 分页 | ✓ | ✓ | ✓ |
| AC-023 ~ AC-028 弹窗 | ✓ | ✓ | ✓ |
| AC-029 ~ AC-030 层级 | ✓ | ✓ | ✓ |
| AC-031 ~ AC-033 API | — | ✓ | — |
| AC-034 ~ AC-036 数据 | — | ✓ | — |
| AC-037 ~ AC-040 技术 | ✓ | ✓ | — |
| AC-041 ~ AC-043 视觉 | — | — | ✓ |

## 2. 必测矩阵

见 `issues/requirements/REQ-0005-tile-category-management/test-plan.md` §3–§4（删除规则、层级深度）。

## 3. 建议测试文件

- `src/backend/tests/test_admin_tile_categories.py`
- `src/web/src/pages/admin/TileCategoryManagementPage.test.tsx`
- `src/web/src/features/admin/components/CategoryFormModal.test.tsx`
