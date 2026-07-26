---
title: 测试计划
purpose: add-brand-management AC → 测试映射
content: issues test-plan + change specs
owner: product
status: draft
---

# 测试计划

## 后端集成（pytest）

| 用例 | 覆盖 AC |
|---|---|
| GET brands + summary | AC-005, AC-027 |
| POST create default ENABLED | AC-026 |
| PUT update + name dup | AC-023 |
| enable/disable | AC-012 |
| DELETE 四态矩阵 | AC-013 ~ AC-016 |
| employee 200 / store_owner 403 | AC-001 |

## 前端单元（vitest）

| 用例 | 覆盖 AC |
|---|---|
| 删除按钮 disabled 矩阵 | AC-013, AC-014 |
| BrandFormModal 字段顺序 | AC-021, AC-024 |
| page_size 切换重置 page | AC-019 |
| 无导出批量 DOM | AC-004 |

## 手工冒烟

1. 新增品牌 → 列表启用态 → 弹窗无状态。
2. 停用 SKU=0 品牌 → 删除成功。
3. 启用态 SKU=0 → 删除置灰。
4. 切换每页 50 → 页码回 1，筛选保留。
