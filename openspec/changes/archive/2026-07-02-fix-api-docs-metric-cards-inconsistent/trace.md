---
change_id: fix-api-docs-metric-cards-inconsistent
status: applied
source_bug: BUG-0052-api-docs-metric-cards-inconsistent
created_at: 2026-07-01 20:33:50
updated_at: 2026-07-02 08:58:31
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0052-api-docs-metric-cards-inconsistent/`
- 关联需求: `REQ-0022-admin-api-docs-menu`
- Sprint: `sprint-004`

## 状态

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 08:58:31 | `/opsx-apply` | 完成摘要指标卡 DOM/class 修复、前端回归测试与知识库 gate 更新，状态 applied |
| 2026-07-01 20:33:50 | `/bug-opsx` | 创建 OpenSpec fix change，状态 proposed |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | `/admin/api-docs` 摘要指标卡与 `/admin/tile-skus` 同类指标卡不一致 |
| 根因 | 缺少 `.metric-value` / `.metric-desc` 基准 class，通用 metric 样式不能完整命中 |
| 严重等级 | medium |
| 修复类型 | Web 管理端 UI 一致性 fix |
| API 影响 | 无 |
| DB 影响 | 无 |
| Orval 影响 | 无 |

## 追溯矩阵

| BUG AC | OpenSpec Artifact | 说明 |
|---|---|---|
| AC-001 | `specs/web-client/spec.md` | 指标卡 DOM 结构对齐 |
| AC-002 | `specs/web-client/spec.md` | 视觉层级与 SKU 页一致 |
| AC-003 | `specs/web-client/spec.md` | semantic token 与无裸 Hex |
| AC-004 | `specs/web-client/spec.md` | 接口文档页功能不回归 |
| AC-005 | `specs/web-client/spec.md` | 权限边界不回归 |
| AC-006 | `specs/testing/spec.md` | 前端测试覆盖 |
| AC-007 | `proposal.md` / `tasks.md` | 确认无 API/DB/MinIO/Orval/Docker 影响 |
