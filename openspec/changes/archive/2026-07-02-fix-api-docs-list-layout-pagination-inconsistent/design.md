---
change_id: fix-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表标题移除与分页一致性修复 - 设计
created_at: 2026-07-02 08:57:28
updated_at: 2026-07-02 09:13:51
source_bug: BUG-0053-api-docs-list-layout-pagination-inconsistent
status: applied
---

# Design

## Context

`/admin/api-docs` 是 REQ-0022 引入的管理端接口文档页。当前页面已具备接口目录、筛选、Swagger/OpenAPI 入口、Orval 方法名展示与权限控制，但列表区域存在两个验收偏差：

- 列表上方固定渲染「系统接口」标题，产品确认该标题应直接移除。
- 列表底部仅展示统计文本，没有与瓷砖 SKU 页一致的分页 DOM 和交互。

本 change 只修复 Web 管理端前端表现，不改变接口目录数据来源和任何后端契约。

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | `/admin/api-docs` 列表区域展示冗余「系统接口」标题，且无上一页/下一页/每页条数分页控件 |
| 复现 | 管理员登录后打开 `/admin/api-docs`，查看接口列表首部和底部 |
| 根因分类 | code / design / test |
| 直接原因 | 页面局部实现没有分页状态，也未使用管理端列表页分页 DOM/class 契约 |
| 严重等级 | medium |
| 关联需求 | `REQ-0022-admin-api-docs-menu` |
| 关联 Sprint | `sprint-004` |
| API 影响 | 无 |
| DB 影响 | 无 |
| Orval 影响 | 无 |

## 修复方案

### D1. 标题处理

移除接口列表区域内固定标题「系统接口」。该文本不得以改名方式保留，也不得按接口数据行过滤处理。

页面仍可保留页面级标题、摘要指标和筛选区域；本修复只针对列表区冗余标题。

### D2. 分页状态

在 `ApiDocsPage` 前端维护以下派生状态：

- `page`：当前页，默认 1。
- `pageSize`：每页条数，默认 20。
- `totalItems`：当前筛选结果数量。
- `totalPages`：基于 `totalItems` 与 `pageSize` 计算，至少为 1。
- `pagedRoutes`：当前页实际渲染的接口条目。

当 Method、Tag、Auth 或关键字筛选条件变化时，`page` MUST 回到 1。当 `pageSize` 变化时，`page` 也 SHOULD 回到 1，避免出现空页。

### D3. 分页 UI 与 DOM

分页结构对齐 `/admin/tile-skus` 管理端列表页基准：

- 左侧使用 `page-summary` 仅展示接口总数文案 `共 x 个接口`。
- 右侧使用 `page-right` 包裹页码按钮和每页条数选择。
- 页码按钮使用 `page-buttons`、`page-btn` 与 `active`。
- 每页条数选择使用 `page-size-wrap` 与 `page-size`。
- 每页条数选项为 10 / 20 / 50 / 100。

上一页/下一页在不可操作时 MUST 置灰或禁用。总页数为 1 或筛选结果为空时，分页区不得展示无效页码。

### D4. 空态与回归边界

筛选结果为空时，页面继续展示明确空态；分页计算基于空结果稳定渲染，避免出现 `0 / 0` 或无效页码。

修复不得改变：

- admin/employee 权限边界。
- 侧栏入口可见性。
- OpenAPI JSON 与 Swagger UI 入口。
- 生产环境 Swagger 只读策略。
- Orval 方法名和「未生成」原因展示。
- `/api/v1/*`、`/health`、`/media/{object_key:path}` 与 schema 外路由展示。

### D5. 测试策略

更新前端 Vitest / Testing Library：

1. 断言 `/admin/api-docs` 不再渲染列表区标题「系统接口」。
2. 断言分页 DOM 包含 `page-summary`、`page-right`、页码按钮和每页条数选择。
3. 断言默认每页条数为 20，选项包含 10 / 20 / 50 / 100。
4. 断言分页切换后表格只展示当前页数据。
5. 断言筛选条件变化后当前页回到 1。
6. 保持既有权限、Swagger、OpenAPI、Orval 与筛选测试通过。

## Risks

| 风险 | 缓解 |
|---|---|
| 与 BUG-0052 指标卡修复同时修改 `ApiDocsPage` | 以同一页面测试覆盖摘要区、列表区和回归功能，避免互相覆盖 |
| 前端分页导致测试数据不足无法覆盖多页 | 在测试中构造超过 20 条 route 数据 |
| 筛选和分页状态耦合导致空页 | 筛选变化和 pageSize 变化时重置 page，并 clamp 当前页 |
| 管理端列表页视觉再次分叉 | 复用现有分页 class，不新增局部分页样式 |

## Non-Goals

- 不新增后端分页接口。
- 不修改 OpenAPI、Orval 生成物或接口文档聚合数据结构。
- 不修改数据库、MinIO、媒体上传、Docker Compose 或环境变量。
- 不改变生产 Swagger 策略。
