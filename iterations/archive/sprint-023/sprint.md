---
note: workflow-sync — workflow-sync 自动同步 — 6/6 Change archived；0 applied；Sprint `completed`
created_at: 2026-08-12 09:15:58
updated_at: 2026-08-12 22:10:00
---

# sprint-023 迭代规划

## 1. 目标

- `optimize-release-workflow-ux`：固化 v1.1.0 发布流程中的操作体验优化。
- `BUG-0129-miniapp-rum-app-version-production`：修复小程序 RUM 与管理后台性能观测口径不一致，覆盖版本号、request_id、指标标签、空态样式和聚合分组展示。
- `REQ-0111-miniapp-media-four-part-acceptance-practice`：沉淀小程序媒体四联验收最佳实践，覆盖知识库、媒体规范、小程序 Network evidence、测试 helper 与审计 helper。
- `REQ-0112-admin-list-column-pagination-consistency-contract`：建立管理端列表页列展示与分页一致性契约，覆盖 nowrap、冻结操作列、分页 DOM 与真实分页。
- `REQ-0113-admin-performance-observability-filter-options`：补齐管理端性能观测筛选候选值接口，统一筛选区、聚合列表和样本页字段顺序。

Sprint 目标编号列表：

- optimize-release-workflow-ux
- BUG-0129-miniapp-rum-app-version-production
- strengthen-sprint-exps-ai-usage-fresh-gate
- REQ-0111-miniapp-media-four-part-acceptance-practice
- REQ-0112-admin-list-column-pagination-consistency-contract
- REQ-0113-admin-performance-observability-filter-options

### REQ-0111 要点

- 沉淀 BUG-0125、BUG-0126 暴露的小程序媒体四联验收最佳实践。
- 明确 key、object、URL、render 四联证据链及 DevTools / 真机 / 体验版 Network evidence 边界。
- 提供测试 helper 与审计 helper 范围，默认不新增上传、缩略图生成、CDN 或对象存储 provider。

### REQ-0112 要点

- 固化管理端列表页列展示、nowrap、有效期例外、冻结操作列和分页 DOM 一致性契约。
- 与 REQ-0095 字段语义 adapter 范围互补，聚焦布局与分页体验治理。

### REQ-0113 要点

- 新增管理端性能观测筛选候选值接口，返回端类型、版本号、页面、设备、网络、指标 6 大维度。
- 候选值仅按时间范围返回，不做端类型、版本号、页面、设备、网络或指标级联收敛。
- 固化性能观测筛选区（时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标）、聚合列表、样本页上下文和样本列表字段顺序，并继承 admin-list 横切 AC。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0111-miniapp-media-four-part-acceptance-practice | 沉淀小程序媒体四联验收最佳实践 | done | 1 人天 | archived `update-miniapp-media-four-part-acceptance-practice`（2026-08-12 14:54:20） |
| REQ | REQ-0112-admin-list-column-pagination-consistency-contract | 建立管理端列表页列展示与分页一致性契约 | done | 1 人天 | archived `update-admin-list-column-pagination-consistency-contract`（2026-08-12 21:38:05） |
| REQ | REQ-0113-admin-performance-observability-filter-options | 管理端性能观测提供筛选维度候选值接口 | done | 1 人天 | archived `add-admin-performance-observability-filter-options`（2026-08-12 21:33:00） |
| BUG | BUG-0129-miniapp-rum-app-version-production | 小程序 RUM 与管理后台性能观测口径不一致 | done | 1 人天 | archived `fix-miniapp-rum-performance-observability`（2026-08-12 15:19:57） |
| Change | optimize-release-workflow-ux | optimize release workflow ux | archived | 0.25 人天 | archived `optimize-release-workflow-ux`（2026-08-12 09:15:58） |
| Change | strengthen-sprint-exps-ai-usage-fresh-gate | strengthen sprint exps ai usage fresh gate | archived | 0.25 人天 | archived `strengthen-sprint-exps-ai-usage-fresh-gate`（2026-08-12 14:27:27） |

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0111 | 沉淀小程序媒体四联验收最佳实践 | P1 | done | archived `update-miniapp-media-four-part-acceptance-practice`（2026-08-12 14:54:20） |
| REQ-0112 | 建立管理端列表页列展示与分页一致性契约 | P1 | done | archived `update-admin-list-column-pagination-consistency-contract`（2026-08-12 21:38:05） |
| REQ-0113 | 管理端性能观测提供筛选维度候选值接口 | P1 | done | archived `add-admin-performance-observability-filter-options`（2026-08-12 21:33:00） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0129 | 小程序 RUM 与管理后台性能观测口径不一致 | medium | done | archived `fix-miniapp-rum-performance-observability`（2026-08-12 15:19:57） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `optimize-release-workflow-ux` | — | archived | archived `optimize-release-workflow-ux`（2026-08-12 09:15:58） |
| `strengthen-sprint-exps-ai-usage-fresh-gate` | — | archived | archived `strengthen-sprint-exps-ai-usage-fresh-gate`（2026-08-12 14:27:27） |
| `fix-miniapp-rum-performance-observability` | BUG-0129-miniapp-rum-app-version-production | archived | archived `fix-miniapp-rum-performance-observability`（2026-08-12 15:19:57） |
| `update-miniapp-media-four-part-acceptance-practice` | REQ-0111-miniapp-media-four-part-acceptance-practice | archived | archived `update-miniapp-media-four-part-acceptance-practice`（2026-08-12 14:54:20） |
| `update-admin-list-column-pagination-consistency-contract` | REQ-0112-admin-list-column-pagination-consistency-contract | archived | archived `update-admin-list-column-pagination-consistency-contract`（2026-08-12 21:38:05） |
| `add-admin-performance-observability-filter-options` | REQ-0113-admin-performance-observability-filter-options | archived | archived `add-admin-performance-observability-filter-options`（2026-08-12 21:33:00） |
<!-- workflow-sync:scope-changes:end -->

REQ：3 个已纳入正式范围并完成归档；BUG：1 个已纳入正式范围并完成归档；当前完成度与验收结论以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：6 个范围项均已归档，其中 4 个关联 REQ/BUG、2 个为纯治理 Change。Sprint close 前 readiness、stale scan 与归档证据均已通过。

## 3. 工作量

| 范围项 | Story Points | 人天 | 说明 |
|---|---:|---:|---|
| BUG-0129-miniapp-rum-app-version-production | 1 | 1 | 小程序 RUM 与管理后台性能观测口径修复 |
| optimize-release-workflow-ux | 0.5 | 0.25 | 纯治理文档修改 |
| strengthen-sprint-exps-ai-usage-fresh-gate | 0.5 | 0.25 | 纯治理命令与脚本 gate 优化 |
| REQ-0111-miniapp-media-four-part-acceptance-practice | 1 | 1 | 小程序媒体四联验收最佳实践、测试 helper 与审计 helper |
| REQ-0112-admin-list-column-pagination-consistency-contract | 1 | 1 | 管理端列表列展示与分页一致性契约 |
| REQ-0113-admin-performance-observability-filter-options | 1 | 1 | 管理端性能观测候选值接口与筛选/字段顺序契约 |

当前合计 5 SP / 4.5 人天；REQ-0111、REQ-0112、REQ-0113 均为 P1 治理/契约或管理端体验增强项，后续若 OpenSpec design 判定需要扩大业务页面改造范围，应拆分或移出低优先级项。

## 4. 风险

- 治理资产、管理端性能观测、小程序 RUM 与 admin-list 横切契约均已通过对应 OpenSpec Change 归档。
- 后续风险主要转为运行期观察：Web RUM 版本号、指标映射、request_id 行为，以及性能观测筛选候选值失败态展示需在回归中持续关注。
- 若后续继续扩大多个管理端列表页面改造，应另起 REQ/BUG 或 OpenSpec Change，不回写本 Sprint 范围。

## 5. 验证

- `openspec validate optimize-release-workflow-ux`
- `openspec validate strengthen-sprint-exps-ai-usage-fresh-gate`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `pnpm --dir src/web test -- PerformanceRumPage PerformanceSamplesPage`
- `python tests/test_miniapp_static.py` 相关小程序 RUM 静态断言
- `python scripts/check-sprint-close-stale-scan.py --sprint sprint-023`
- `python scripts/validate-sprint-archive-readiness.py --sprint sprint-023`

## 6. 复盘

- 知识库复盘：`docs/knowledge-base/retrospectives/sprint-023-retrospective.md`
