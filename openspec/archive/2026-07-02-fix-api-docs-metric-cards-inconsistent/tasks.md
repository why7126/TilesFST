---
change_id: fix-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式对齐 - 任务
created_at: 2026-07-01 20:33:50
updated_at: 2026-07-02 08:58:31
source_bug: BUG-0052-api-docs-metric-cards-inconsistent
status: applied
---

# Tasks

## 1. 前端修复

- [x] 1.1 对照 `/admin/tile-skus` 摘要指标卡结构，确认 `ApiDocsPage` 当前 summary DOM 差异。
- [x] 1.2 将 `/admin/api-docs` 四个摘要卡改为 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`。
- [x] 1.3 保留接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数的数据来源与展示含义。
- [x] 1.4 确认修复不改变接口筛选、路由表、Swagger panel、OpenAPI JSON 链接或 Orval 方法名展示。
- [x] 1.5 确认新增/修改 TSX/CSS 不包含裸 Hex，继续复用 semantic token 与既有管理端 metric class。

## 2. 前端测试

- [x] 2.1 更新 `ApiDocsPage` 测试，断言摘要区存在 `.metric-value` 与 `.metric-desc`。
- [x] 2.2 保持既有测试覆盖：Orval 方法名展示、「未生成」状态、筛选、生产 Swagger 只读入口。
- [x] 2.3 如 BUG-0053 并行修改列表分页，确保测试职责不互相覆盖：本 change 只验证 summary metric。

## 3. 验收

- [x] 3.1 人工对照 `/admin/api-docs` 与 `/admin/tile-skus` 摘要指标卡，确认视觉层级一致。
- [x] 3.2 确认 admin 仍可访问 `/admin/api-docs`，employee 仍不可访问。
- [x] 3.3 确认不需要执行 Orval、数据库迁移或 Docker Compose 配置变更。
- [x] 3.4 运行 `openspec validate fix-api-docs-metric-cards-inconsistent --strict`。

## 4. 知识沉淀

- [x] 4.1 修复完成后评估是否更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：若确认 metric card DOM 也属于管理端列表/页面基准，应追加一条摘要指标卡结构 gate。
