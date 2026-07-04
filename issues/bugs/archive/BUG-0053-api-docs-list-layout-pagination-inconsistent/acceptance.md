---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表分页与冗余系统接口信息回归验收
severity: medium
status: pending_review
owner: product
created_at: 2026-07-01 13:53:45
updated_at: 2026-07-01 13:57:52
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
---

# 回归验收标准

## 功能验收

- [ ] **AC-001** 管理员访问 `/admin/api-docs` 时，接口列表区域 MUST 直接移除冗余标题「系统接口」，不得改名保留，也不得按接口数据行过滤处理。
- [ ] **AC-002** 接口列表 MUST 提供分页控件，支持上一页、当前页、下一页。
- [ ] **AC-003** 接口列表 MUST 支持每页条数选择，选项与瓷砖 SKU 页保持一致：10 / 20 / 50 / 100。
- [ ] **AC-004** 默认每页条数 SHOULD 与 SKU 页一致，为 20。
- [ ] **AC-005** 切换 Method、Tag、Auth 或关键字筛选后，当前页 MUST 回到第 1 页。
- [ ] **AC-006** 分页总数 MUST 基于当前筛选后的接口数量计算。
- [ ] **AC-007** 当筛选结果为空时，页面仍展示明确空态，且分页区不出现无效页码。
- [ ] **AC-008** 当总页数为 1 时，上一页与下一页按钮 MUST 处于禁用状态或等价不可操作状态。

## UI 一致性验收

- [ ] **AC-009** 分页 DOM 与瓷砖 SKU 页/管理端列表页保持一致：左侧 `page-summary`，右侧 `page-right`。
- [ ] **AC-010** 分页按钮样式使用既有 `page-buttons`、`page-btn`、`active` 等管理端列表页模式，不新增割裂的局部分页样式。
- [ ] **AC-011** 每页条数选择使用既有 `page-size-wrap` 与 `page-size` 模式。
- [ ] **AC-012** 接口列表表格、筛选栏、状态 Badge、方法 Badge 继续继承管理端暗色旗舰风，不新增裸 Hex。

## 回归验收

- [ ] **AC-013** `/admin/api-docs` 仍仅 `admin` 可访问，`employee` 不可访问且侧栏不展示入口。
- [ ] **AC-014** OpenAPI JSON 与 Swagger UI 入口仍可用。
- [ ] **AC-015** 生产环境 Swagger 仍保持只读策略，不启用 `Try It Out`。
- [ ] **AC-016** Orval 方法名展示与「未生成」原因展示不回退。
- [ ] **AC-017** 接口目录仍展示 `/api/v1/*`、`/health`、`/media/{object_key:path}` 和 schema 外路由。
- [ ] **AC-018** 修复不修改后端 API 契约、不修改数据库结构、不修改 MinIO 或媒体上传策略。

## 测试建议

- [ ] **AC-019** 前端 Vitest 覆盖分页 DOM：`page-summary`、`page-right`、页码按钮、每页条数选择。
- [ ] **AC-020** 前端 Vitest 覆盖筛选后回到第 1 页。
- [ ] **AC-021** 前端 Vitest 覆盖分页切换后表格只展示当前页数据。
- [ ] **AC-022** 如修复仅为前端分页与标题调整，不需要后端 pytest、Orval 或数据库迁移。

## 验收结论模板

| 验收项 | 结果 | 说明 |
|---|---|---|
| 冗余「系统接口」信息处理 | 待验收 | 待修复后确认 |
| 分页交互 | 待验收 | 待修复后确认 |
| UI 一致性 | 待验收 | 待修复后确认 |
| 权限与 Swagger 策略回归 | 待验收 | 待修复后确认 |
