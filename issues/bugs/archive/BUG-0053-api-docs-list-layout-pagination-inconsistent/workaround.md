---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表分页与冗余系统接口信息临时规避方案
severity: medium
status: pending_review
owner: product
created_at: 2026-07-01 13:53:45
updated_at: 2026-07-01 13:53:45
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
---

# 临时规避方案

## 当前可用规避

在正式修复前，管理员可通过以下方式降低影响：

1. 使用 `/admin/api-docs` 页面顶部筛选条件缩小接口范围，例如按 Method、Tag、Auth 或关键字过滤。
2. 使用浏览器页面查找快速定位 Path、Summary 或 Orval 方法名。
3. 需要查看完整原始接口清单时，临时打开 `/openapi.json` 或 Swagger UI。

## 局限

- 上述方式不能提供与 SKU 页一致的分页体验。
- 筛选结果较多时仍需要滚动查看长表格。
- 无法消除「系统接口」信息造成的信息层级干扰。
- `/openapi.json` 与 Swagger UI 不能完全替代管理端接口目录，因为 schema 外路由、Orval 状态和环境策略仍以 `/admin/api-docs` 页面聚合展示更清晰。

## 是否需要临时开关

不需要。

该缺陷不影响权限、安全或核心业务写入，不建议通过临时配置隐藏接口文档页。应通过常规 fix 对齐列表 UI 与分页交互。

## Hotfix 判断

不建议 hotfix。

理由：

- 影响范围集中在 Web 管理端接口文档页。
- 不阻断管理员访问接口目录。
- 不涉及数据损坏、权限越权、生产安全或核心交易链路。
- 可纳入常规 `fix-api-docs-list-layout-pagination-inconsistent` OpenSpec Change 修复。
