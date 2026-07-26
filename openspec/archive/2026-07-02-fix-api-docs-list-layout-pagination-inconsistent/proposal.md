---
change_id: fix-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表标题移除与分页一致性修复
created_at: 2026-07-02 08:57:28
updated_at: 2026-07-02 09:05:55
source_bug: BUG-0053-api-docs-list-layout-pagination-inconsistent
status: applied
---

## Why

BUG-0053 已评审通过并纳入 sprint-004。管理端 `/admin/api-docs` 接口文档列表区域存在冗余标题「系统接口」，且列表底部分页未与 `/admin/tile-skus` 等管理端列表页保持一致。

产品已确认：用户反馈中的「第一行【系统接口】信息」指接口列表区标题，修复时应直接移除该标题，不改名、不作为真实接口数据行过滤处理。

根因是 REQ-0022 实现阶段将接口目录作为前端数组一次性渲染，未维护 `page`、`pageSize`、`totalPages` 等分页状态，也未复用管理端列表页 `page-summary` / `page-right` / `page-buttons` / `page-size-wrap` 的分页 DOM 契约。

关联 BUG：`issues/bugs/archive/BUG-0053-api-docs-list-layout-pagination-inconsistent/`

## What Changes

- 移除 `/admin/api-docs` 接口列表区域冗余标题「系统接口」。
- 为接口列表增加前端分页状态与分页控件，支持上一页、当前页、下一页和每页条数选择。
- 每页条数选项与瓷砖 SKU 页一致：10 / 20 / 50 / 100，默认 20。
- 筛选条件变化后分页回到第 1 页，分页总数基于当前筛选结果计算。
- 分页 DOM/class 对齐管理端列表页模式：`page-summary`、`page-right`、`page-buttons`、`page-btn`、`active`、`page-size-wrap`、`page-size`。
- 保留接口目录数据来源、筛选、状态 Badge、方法 Badge、Swagger 策略、Orval 方法名、权限边界。
- 不新增裸 Hex，不修改后端 API、数据库、MinIO、上传、Orval 或 Docker Compose 配置。
- 补充 `ApiDocsPage` 前端回归测试，覆盖分页 DOM、分页切换、每页条数、筛选回到第一页和标题移除。

## Capabilities

### Added Constraints

- `web-client`: 管理端接口文档列表必须移除冗余标题并提供与管理端列表页一致的分页交互和 DOM/class。
- `testing`: 接口文档页前端测试必须覆盖列表标题移除、分页 DOM 与分页交互。

### Modified Behavior

- `/admin/api-docs` 接口列表区域不再展示「系统接口」标题。
- `/admin/api-docs` 接口列表从一次性展示全部筛选结果变为按当前页展示。
- 接口目录、筛选维度、Swagger 入口、生产只读策略、Orval 方法名、权限访问保持不变。

## Rollback Plan

1. 回滚 `ApiDocsPage` 中分页状态、分页切片和分页控件的变更。
2. 回滚接口列表区域标题移除相关修改，若需要恢复标题必须重新评审 BUG-0053。
3. 回滚对应前端测试新增断言。
4. 不涉及数据库迁移、后端接口、对象存储、Orval 生成物或 Docker 配置回滚。
5. 若回滚导致 BUG-0053 复现，必须在 BUG trace 中记录原因并重新评审修复路径。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 不涉及 |
| API | 不新增或修改请求、响应、错误码 |
| 数据库 | 不涉及 |
| Web 管理端 | `/admin/api-docs` 接口列表标题与分页 UI/交互 |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | 不需要执行 |
| Docker Compose | 不涉及 |
| 测试 | 更新 `ApiDocsPage` Vitest / Testing Library 覆盖列表分页与标题移除 |
| 文档 | OpenSpec trace、BUG trace 与 sprint 同步 |
