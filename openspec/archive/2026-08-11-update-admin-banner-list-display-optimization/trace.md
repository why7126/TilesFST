---
change_id: update-admin-banner-list-display-optimization
status: proposed
type: update
created_at: 2026-08-11 08:48:00
updated_at: 2026-08-11 23:19:21
source_requirement: REQ-0108-admin-banner-list-display-optimization
source_sprint: sprint-022
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-020-retrospective.md
ui_contract:
  required: true
  source: issues/requirements/archive/REQ-0108-admin-banner-list-display-optimization/prototype/admin/context.md
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 23:19:21 | acceptance.signoff | 用户执行 `/opsx-archive REQ-0108`，接受当前后端测试、Web Vitest、OpenAPI/Orval 与 CSS/DOM 等价 UI 证据，进入归档。 |
| 2026-08-11 22:56:03 | opsx.modify | 验收返修：Banner 管理列表除有效期列外，所有表头字段和其他列表字段均不换行；有效期保留起止时间换行。`BannerManagementPage.test.tsx` 聚焦测试通过，作为本轮等价 UI 证据。 |
| 2026-08-11 09:00:36 | test.web | `pnpm --dir src/web exec vitest run src/pages/admin/BannerManagementPage.test.tsx` 通过；作为本轮 Banner 列表 DOM/布局等价 UI 证据。 |
| 2026-08-11 08:57:33 | test.web-all | `pnpm --dir src/web test -- BannerManagementPage.test.tsx` 触发全量 Vitest，5 个非 Banner 用例超时；随后使用精确文件命令验证 Banner 页通过。 |
| 2026-08-11 08:56:00 | test.backend | `uv run pytest src/backend/tests/test_admin_banners.py` 通过。 |
| 2026-08-11 08:55:00 | generate.api | 运行 `./scripts/generate-openapi-client.sh`，同步 OpenAPI 与 Orval。 |
| 2026-08-11 08:48:00 | req.opsx | 基于 REQ-0108 创建 OpenSpec Change。 |

## UI 证据计划

- 本轮以 Vitest DOM/布局合同作为等价视觉证据：覆盖 Banner 列只显示图片、跳转对象列、既有列保留、分页 DOM 和图片 fallback。
- 验收返修后，旧 UI 证据已更新为 CSS/DOM 契约：覆盖表头和非有效期字段 `nowrap`，有效期列 `normal` 并保留 `<br />`。
- 未记录浏览器截图；归档前如需要更强 UI 证据，可补充 1440px 浏览器截图。
