## Why

Sprint 004 复盘与 `BUG-0055-admin-list-layout-unification` 暴露出管理端列表页在指标卡 DOM、分页窗口和分页结构上反复漂移。`REQ-0029-admin-list-foundation-components` 已评审通过，需把 `MetricCard`、`MetricCardGrid` 与分页窗口工具提升为可复用、可测试、可验收的 OpenSpec 事实源，支撑 `REQ-0028` 的管理端列表页契约。

## What Changes

- 新增管理端列表基础组件能力：`MetricCard`、`MetricCardGrid` 稳定输出既有 `.metric-*` DOM class，并覆盖空值、loading/占位与 danger 描述。
- 将管理端分页窗口算法沉淀到共享工具或管理端共享层，默认最多展示 5 个页码，并覆盖非法输入兜底。
- 明确管理端列表页分页 DOM 契约：`.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`。
- 首批接入 2–3 个基准页面，在保持业务行为不变的前提下验证组件与分页工具复用。
- 在 `/design-system` 或管理端设计验收区展示基础组件与分页窗口边界样例，并补充 Vitest / Testing Library 覆盖。

## Capabilities

### New Capabilities

- 无

### Modified Capabilities

- `design-system`：增加管理端列表基础组件展示、语义样式、组件 DOM 与测试治理要求。
- `web-client`：增加管理端列表页 `MetricCard` / `MetricCardGrid`、分页窗口工具、分页 DOM 契约与首批页面接入要求。

## Impact

- Web 管理端：影响管理端列表页共享 UI、分页工具、`/design-system` 展示与首批接入页面。
- API：不修改后端分页 API、不新增接口、不改变响应结构。
- 数据库：不修改 SQLite/MySQL 表结构。
- Orval：不需要重新生成 OpenAPI / Orval 客户端。
- 小程序与店主 Web：不受影响。
- 测试：需要补充或迁移 Vitest / Testing Library 覆盖，包括组件渲染、分页窗口边界和首批页面结构 smoke。
