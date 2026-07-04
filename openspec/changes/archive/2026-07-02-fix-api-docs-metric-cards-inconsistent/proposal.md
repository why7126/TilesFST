---
change_id: fix-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式对齐
created_at: 2026-07-01 20:33:50
updated_at: 2026-07-02 08:58:31
source_bug: BUG-0052-api-docs-metric-cards-inconsistent
status: applied
---

## Why

BUG-0052 已评审通过并纳入 sprint-004。管理端 `/admin/api-docs` 页面标题下方的接口摘要指标卡，与 `/admin/tile-skus` 瓷砖 SKU 页同类指标卡视觉不一致。

根因是接口文档页仅复用了 `summary-grid` / `metric-card` 容器，但卡片内部使用 `p.metric-label` + `strong` + `span`，没有使用管理端基准结构 `.metric-value` 与 `.metric-desc`。这导致 `admin-home.css` 中通用 metric 样式不能完整命中，破坏 REQ-0022 的管理端一致性验收。

关联 BUG：`issues/bugs/archive/BUG-0052-api-docs-metric-cards-inconsistent/`

## What Changes

- 对齐 `/admin/api-docs` 摘要指标卡 DOM/class 到管理端基准结构。
- 每个接口摘要卡使用 `.metric-label`、`.metric-value`、`.metric-desc`。
- 保留现有 `summary-grid`、`metric-card`、Design System semantic token 与暗色旗舰风。
- 不新增裸 Hex，不修改后端 API、数据库、MinIO、上传、Orval 或 Docker Compose 配置。
- 补充 `ApiDocsPage` 前端回归测试，防止摘要卡再次退化为裸 `strong` / `span`。

## Capabilities

### Added Constraints

- `web-client`: 管理端接口文档页摘要指标卡必须对齐既有管理端 metric card DOM/class 与视觉层级。
- `testing`: 接口文档页前端测试必须覆盖摘要指标卡 class 结构和既有功能不回归。

### Modified Behavior

- `/admin/api-docs` 页面摘要区 UI 结构调整。
- 接口目录、筛选、Swagger 策略、Orval 方法名、权限边界保持不变。

## Rollback Plan

1. 回滚 `ApiDocsPage` 摘要指标卡 DOM/class 调整。
2. 回滚对应前端测试新增断言。
3. 不涉及数据库迁移、后端接口、对象存储、Orval 生成物或 Docker 配置回滚。
4. 若回滚导致 BUG-0052 复现，必须在 BUG trace 中记录原因并重新评审修复路径。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 不涉及 |
| API | 不新增或修改请求、响应、错误码 |
| 数据库 | 不涉及 |
| Web 管理端 | `/admin/api-docs` 摘要指标卡 DOM/class 与视觉层级 |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | 不需要执行 |
| Docker Compose | 不涉及 |
| 测试 | 更新 `ApiDocsPage` Vitest / Testing Library 覆盖摘要指标卡 |
| 文档 | OpenSpec trace 与 sprint acceptance 同步 |
