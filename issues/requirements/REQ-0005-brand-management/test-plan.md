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
| AC-001 ~ AC-004 | 访问、布局、无导出批量 | ✓ | ✓ | ✓ |
| AC-005 ~ AC-006 | 指标卡 | ✓ | ✓ | ✓ |
| AC-007 ~ AC-009 | 搜索筛选重置 | ✓ | ✓ | ✓ |
| AC-010 ~ AC-012 | 列表列与操作 | ✓ | ✓ | ✓ |
| AC-013 ~ AC-016 | 删除规则前后端 | ✓ | ✓ | ✓ |
| AC-017 ~ AC-019 | 分页与 page_size | ✓ | ✓ | ✓ |
| AC-020 ~ AC-026 | 弹窗字段与校验 | ✓ | ✓ | ✓ |
| AC-027 ~ AC-029 | API 与权限 | — | ✓ | — |
| AC-030 ~ AC-032 | 数据与 MinIO | — | ✓ | — |
| AC-033 ~ AC-036 | 技术、单测、集成 | ✓ | ✓ | — |
| AC-037 ~ AC-039 | 视觉/HTML 并排 | — | — | ✓ |

## 2. 建议测试文件

```text
src/backend/tests/test_admin_brands.py
  - list with filters and summary
  - create default ENABLED
  - name duplicate → BRAND_NAME_DUPLICATED
  - delete forbidden when sku_count > 0 or ENABLED
  - delete allowed when sku_count=0 and DISABLED
  - enable / disable

src/web/src/pages/admin/BrandManagementPage.test.tsx
  - delete button disabled/enabled matrix
  - page_size change resets page
  - no export / batch UI

src/web/src/features/admin/components/BrandFormModal.test.tsx
  - field order
  - sort_order positive integer validation
  - no status field in DOM
```

## 3. 删除规则矩阵（必测）

| sku_count | status | 前端删除 | 后端 DELETE |
|---:|---|---|---|
| 0 | DISABLED | 可点 | 200 |
| 0 | ENABLED | 置灰 | 409 FORBIDDEN |
| >0 | DISABLED | 置灰 | 409 FORBIDDEN |
| >0 | ENABLED | 置灰 | 409 FORBIDDEN |

## 4. 手工冒烟用例

1. 新增品牌 → 列表出现 → 默认启用 → 弹窗无状态字段。
2. 停用 SKU=0 的品牌 → 删除可点 → 确认删除成功。
3. 启用状态 SKU=0 品牌 → 删除置灰 + tooltip。
4. 重复品牌名称 → 表单与服务端错误提示一致。
5. 切换每页 50 条 → 回到第 1 页，筛选条件保留。
6. 上传 Logo → 列表缩略图更新。

## 5. OpenSpec 阶段（本次未创建）

- 实现前执行 `/requirement-to-opsx REQ-0005-brand-management`。
- 建议 change_id：`add-brand-management`。
