---
change_id: fix-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表标题移除与分页一致性修复 - 任务
created_at: 2026-07-02 08:57:28
updated_at: 2026-07-02 09:05:55
source_bug: BUG-0053-api-docs-list-layout-pagination-inconsistent
status: applied
---

# Tasks

## 1. Web 管理端实现

- [x] 1.1 在 `ApiDocsPage` 移除接口列表区域冗余标题「系统接口」，不改名保留，不作为接口数据行过滤。
- [x] 1.2 为接口列表增加 `page`、`pageSize`、`totalPages` 与当前页数据切片。
- [x] 1.3 默认每页 20 条，并支持 10 / 20 / 50 / 100 每页条数选择。
- [x] 1.4 Method、Tag、Auth、关键字筛选变化时，将当前页重置为第 1 页。
- [x] 1.5 分页总数基于当前筛选结果计算，空态与单页结果不展示无效页码。
- [x] 1.6 分页 DOM/class 对齐管理端列表页：`page-summary`、`page-right`、`page-buttons`、`page-btn`、`active`、`page-size-wrap`、`page-size`。
- [x] 1.7 保持接口表格、筛选栏、状态 Badge、方法 Badge 使用既有暗色旗舰风与 semantic token，不新增裸 Hex。

## 2. 回归测试

- [x] 2.1 更新 `ApiDocsPage` 前端测试，覆盖列表区不再展示「系统接口」标题。
- [x] 2.2 覆盖分页 DOM：`page-summary`、`page-right`、页码按钮、每页条数选择。
- [x] 2.3 覆盖默认 pageSize 为 20，选项包含 10 / 20 / 50 / 100。
- [x] 2.4 覆盖分页切换后表格只展示当前页数据。
- [x] 2.5 覆盖筛选条件变化后当前页回到第 1 页。
- [x] 2.6 保持既有测试覆盖：admin 权限、employee 禁止访问、OpenAPI JSON、Swagger 生产只读策略、Orval 方法名和「未生成」状态。

## 3. 验证与文档同步

- [x] 3.1 运行相关前端测试。
- [x] 3.2 若只修改前端分页与标题，确认不需要执行后端 pytest、数据库迁移、Orval 或 Docker Compose 配置变更。
- [x] 3.3 对照 BUG-0053 acceptance.md 完成回归验收记录。
- [x] 3.4 若修复过程发现可复用故障经验，补充 `docs/knowledge-base/incidents/`；若无复用价值，在验收记录中说明不沉淀。
