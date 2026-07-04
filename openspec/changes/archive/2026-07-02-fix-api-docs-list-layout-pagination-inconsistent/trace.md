---
change_id: fix-api-docs-list-layout-pagination-inconsistent
status: applied
source_bug: BUG-0053-api-docs-list-layout-pagination-inconsistent
created_at: 2026-07-02 08:57:28
updated_at: 2026-07-02 09:13:51
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0053-api-docs-list-layout-pagination-inconsistent/`
- 关联需求: `REQ-0022-admin-api-docs-menu`
- Sprint: `sprint-004`

## 状态

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 08:57:28 | `/bug-opsx` | 创建 OpenSpec fix change，状态 proposed |
| 2026-07-02 09:05:55 | `/opsx-apply` | 完成接口列表标题移除、前端分页、分页 DOM 对齐与回归测试，状态 applied |
| 2026-07-02 09:13:51 | 用户反馈微调 | 删除列表工具栏排序/当前数量行；分页摘要改为仅显示 `共 x 个接口` |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | `/admin/api-docs` 列表区域存在冗余「系统接口」标题，且底部分页未与 `/admin/tile-skus` 一致 |
| 根因 | 页面局部实现缺少分页状态与管理端列表页分页 DOM/class 契约 |
| 严重等级 | medium |
| 修复类型 | Web 管理端 UI 与交互一致性 fix |
| API 影响 | 无 |
| DB 影响 | 无 |
| Orval 影响 | 无 |

## 追溯矩阵

| BUG AC | OpenSpec Artifact | 说明 |
|---|---|---|
| AC-001 | `specs/web-client/spec.md` | 直接移除冗余「系统接口」标题 |
| AC-002 ~ AC-008 | `specs/web-client/spec.md` | 分页状态、上一页/下一页、每页条数、筛选重置、空态 |
| AC-009 ~ AC-012 | `specs/web-client/spec.md` | 分页 DOM/class 与管理端列表页一致，semantic token 不回退 |
| AC-013 ~ AC-018 | `specs/web-client/spec.md` | 权限、Swagger、OpenAPI、Orval、接口目录与无 API/DB/MinIO 影响 |
| AC-019 ~ AC-022 | `specs/testing/spec.md` / `tasks.md` | 前端测试覆盖与无需后端/Orval/DB 验证 |

## 验证记录

| 时间 | 类型 | 结果 |
|---|---|---|
| 2026-07-02 09:05:28 | 前端测试 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx` 通过：1 file, 9 tests |
| 2026-07-02 09:05:48 | 前端回归 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` 通过：3 files, 17 tests |
| 2026-07-02 09:13:40 | 前端回归 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` 通过：3 files, 17 tests |
| 2026-07-02 09:05:55 | 工程影响 | 仅前端分页与标题调整；不需要后端 pytest、数据库迁移、Orval 或 Docker Compose 配置变更 |
| 2026-07-02 09:05:55 | 知识沉淀 | 未发现新的可复用生产故障经验；不新增 `docs/knowledge-base/incidents/` |
