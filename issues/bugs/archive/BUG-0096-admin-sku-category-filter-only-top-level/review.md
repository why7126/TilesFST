---
bug_id: BUG-0096-admin-sku-category-filter-only-top-level
title: 管理后台瓷砖 SKU 页类目筛选只能选择一级类目
status: done
severity: medium
review_result: approved
reviewed_at: 2026-07-31 15:13:05
reviewer: product
hotfix_required: false
created_at: 2026-07-31 15:13:05
updated_at: 2026-07-31 21:39:43
---

# Review

## 评审结论

确认修复，状态为 `approved`。该 BUG 可进入 `/bug-opsx` 创建修复 Change，也可纳入 Sprint 正式范围。

管理后台瓷砖 SKU 页已有类目筛选能力，但当前筛选控件只展示一级类目，无法选择二级、三级或更深层级类目。经代码复核，SKU 页使用会跳过 `level >= 2` 的类目选项构造逻辑；同时产品口径已确认：选择父类目时应包含所有子孙类目 SKU，UI 形态应采用级联选择控件。

## 评审清单

- [x] 可复现或根因充分：用户截图确认当前下拉只展示一级类目；代码确认 SKU 页筛选控件只取一级类目，后端 `category_id` 当前为精确匹配。
- [x] 严重等级合理：严重等级为 `medium`，不阻断 SKU 基础维护，但影响按细分类目查找、巡检和批量维护效率。
- [x] 回归验收明确：acceptance.md 已覆盖各层级类目展示、级联选择、父类目包含子孙 SKU、组合筛选、重置和回归测试。
- [x] 是否需 hotfix 路径：不需要 hotfix，可随常规 BUG 修复流程进入 OpenSpec Change 与 Sprint。

## 批准范围

- 管理后台 SKU 页类目筛选改为级联选择控件。
- 类目筛选可选择当前类目树中的各层级类目。
- 选择父类目时，筛选结果必须包含该父类目下所有子孙类目的 SKU。
- 保留「全部类目」与重置能力。
- 保持关键词、品牌、类目、状态、素材完整度组合筛选可用。
- 补充前后端回归测试，确认前端筛选控件与后端类目过滤语义一致。

## 后续动作

下一步执行 `/bug-opsx BUG-0096`，创建对应修复 Change。
