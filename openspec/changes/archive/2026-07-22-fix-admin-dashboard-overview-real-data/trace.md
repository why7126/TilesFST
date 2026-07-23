---
change_id: fix-admin-dashboard-overview-real-data
status: applied
created_at: 2026-07-22 08:35:05
updated_at: 2026-07-22 09:19:39
source: bug
source_bug: BUG-0079-admin-dashboard-overview-mock-data
related_requirement: null
iteration: sprint-010
capabilities:
  - admin-dashboard
---

# Trace - fix-admin-dashboard-overview-real-data

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | `BUG-0079-admin-dashboard-overview-mock-data` | 管理端首页数据概览仍使用 Mock 数据 |
| Capability | `admin-dashboard` | 管理端 Dashboard 数据概览真实数据源规范 |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | admin 管理端首页数据概览区域仍展示 Mock 数据，未接入真实业务数据 |
| 复现 | 登录管理端进入 `/admin/dashboard`，对比概览指标与后端真实数据、数据库记录或管理端列表页统计 |
| 影响 | 首页核心指标不可信，可能误导管理员对 SKU、品牌、Banner、用户等业务状态的判断 |
| 根因分类 | code / product-quality |
| 严重等级 | medium |
| Hotfix | 不需要 |
| 关联需求 | 无直接关联需求；现有 `admin-dashboard` 规格仍保留 Mock 数据约束，本 Change 修正该能力规格 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:19:39 | /opsx-apply | 已实现 Dashboard 概览真实数据 API、Web 接入、OpenAPI/Orval、文档与测试 |
| 2026-07-22 09:01:58 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-22 08:35:05 | /bug-opsx | 创建修复 Change，状态 proposed |

## 实现与验收证据

| 类型 | 证据 |
|---|---|
| 实现 | 新增 `GET /api/v1/admin/dashboard/summary`，通过 `AdminDashboardService` 聚合 SKU、品牌、有效 Banner 与用户总数；Web `/admin/dashboard` 数据概览改为调用 Orval client，不再引用 `dashboardMetrics` Mock 成功态。 |
| 回归测试 | `uv run pytest src/backend/tests/test_admin_dashboard.py` 通过 4 项；`pnpm --dir src/web exec vitest run src/pages/admin/DashboardPage.test.tsx` 通过 4 项；`pnpm --dir src/web run build` 通过。 |
| API / Orval | 已运行 `./scripts/generate-openapi-client.sh`，更新 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`；已更新 `docs/03-api-index.md`。 |
| 知识库 | 本次为局部 Mock 数据源替换，无跨项目复用事故模式，不新增 `docs/knowledge-base/incidents/`。 |
