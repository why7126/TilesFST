---
change_id: add-admin-performance-observability-filter-options
status: applied
created_at: 2026-08-12 19:45:10
updated_at: 2026-08-12 21:33:00
source_requirement: REQ-0113-admin-performance-observability-filter-options
sprint: sprint-023
change_type: update
---

# 变更追踪

## 基本信息

```yaml
change_id: add-admin-performance-observability-filter-options
source_requirement: REQ-0113-admin-performance-observability-filter-options
source_requirement_status: applied
sprint: sprint-023
status: applied
type: update
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
linked_specs:
  - real-user-performance-monitoring
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
prototype_refs:
  - issues/requirements/archive/REQ-0113-admin-performance-observability-filter-options/prototype/web/context.md
ui_evidence:
  skeleton_1440: not_required_no_html_prototype
  desktop_1440: equivalent_vitest_dom_order_assertions
  overflow_or_narrow: not_run
  computed_style: not_run
  empty_or_error_state: equivalent_vitest_failure_state_assertion
```

## 冲突处理

当前无 HTML/PNG 原型；UI 事实源优先级为：

```text
prototype/web/context.md > acceptance.md > rules/ui-design.md > openspec/specs/real-user-performance-monitoring/spec.md
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-08-12 19:45:10 | `/req-opsx` | 从 REQ-0113 创建 OpenSpec Change，等待实现 |
| 2026-08-12 21:18:30 | `/opsx-apply` | 新增管理端性能观测候选值接口，接入 Web 候选值筛选和字段顺序，完成 OpenAPI/Orval、文档、测试与工作流同步 |
| 2026-08-12 21:33:00 | `/opsx-modify` | 验收反馈要求删除设备筛选项；已从管理端性能观测筛选区移除设备下拉，保留接口 `device_classes` 返回、聚合列表和样本页设备字段展示 |

## 实现摘要

- 后端新增 `GET /api/v1/admin/performance-events/filter-options`，复用 admin 鉴权，按 `start_time` / `end_time` 返回 `client_types`、`app_versions`、`page_keys`、`device_classes`、`network_types`、`metrics` 六大候选维度。
- 动态候选值仅按时间范围查询 `performance_events`，不随端类型、版本号、页面、设备、网络或指标级联收敛；固定候选值由后端枚举统一输出。
- Web 管理端性能观测页接入候选值接口，筛选区顺序为“时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标”，聚合查询携带新增筛选参数并在筛选变化后回到第一页；设备不作为本期筛选项展示。
- 聚合列表字段顺序调整为“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作”。
- 样本页上下文顺序调整为“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标”，样本表顺序调整为“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id”。
- 本次不涉及 DB 表结构、索引、迁移、对象存储、小程序和 Docker Compose 配置变更。

## 验证记录

```text
./scripts/generate-openapi-client.sh
uv run pytest src/backend/tests/test_performance_events.py
pnpm --dir src/web test -- PerformanceRumPage PerformanceSamplesPage
openspec validate add-admin-performance-observability-filter-options
python scripts/validate-openspec-language.py
pnpm --dir src/web test -- PerformanceRumPage PerformanceSamplesPage
openspec validate add-admin-performance-observability-filter-options --strict
```

## UI 证据

- 等价视觉证据：`PerformanceRumPage.test.tsx` 断言筛选标签顺序、候选值加载、聚合表字段顺序、筛选变化回到第一页、候选值失败态和空态。
- 样本页等价证据：`PerformanceSamplesPage.test.tsx` 断言上下文安全字段、样本表字段顺序、分页和 `request_id` 复制行为。
- 未运行浏览器 1440x1024 截图；本次无 HTML/PNG 原型，采用 Vitest DOM 断言作为等价证据。
