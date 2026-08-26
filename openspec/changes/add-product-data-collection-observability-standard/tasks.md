## 1. 规范文档

- [x] 1.1 新增 `docs/standards/product-data-collection-observability.md`，覆盖适用范围、四层链路模型、两类入口、字段语义、Task Trace 分级覆盖、保留周期、脱敏边界和新产品接入 checklist。
- [x] 1.2 更新 `docs/README.md` 或相关文档索引，确保新规范可被后续 REQ、BUG、OpenSpec Change 和 Sprint 验收引用。
- [x] 1.3 更新 `docs/standards/task-trace-coverage.md`、`docs/standards/api-governance.md` 或等价引用位置，指向通用规范并避免重复完整规则。

## 2. 验收与治理引用

- [x] 2.1 在规范中明确所有业务 API 必须记录 `request_logs`，并记录健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活等可排除项。
- [x] 2.2 在规范中明确“可命名业务行为必须采集，纯 UI 噪音可排除”的行为事件口径。
- [x] 2.3 在规范中明确直接 API 调用不伪造 `usage_events`，允许 `behavior_trace_id` 为空，并通过 `request_logs.request_id` 进入任务链路。
- [x] 2.4 在规范中明确默认保留周期：`request_logs` 90 天、`usage_events` 180 天、`task_traces/task_trace_spans` 90 天、聚合数据 1 年。
- [x] 2.5 在规范中明确禁止采集或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO 凭据、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 和真实客户敏感数据。

## 3. 校验与追溯

- [x] 3.1 补充或更新轻量校验，确认新标准文档和索引引用存在。
- [x] 3.2 运行 `python scripts/validate-openspec-language.py`，确保 Change 文档中文优先且无英文脚手架标题。
- [x] 3.3 运行 `openspec validate add-product-data-collection-observability-standard --strict`，确保新增能力 spec 可通过 OpenSpec 校验。
- [x] 3.4 更新 REQ-0126 验收记录和 trace，说明本 Change 不直接修改 API、DB、Web、小程序或 App 代码；后续具体接入按独立 Change 同步 Orval、数据库文档和测试。

## 验收返修记录

- [x] 2026-08-26 19:36:50：补充标准数据结构章节，明确 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 的最小标准字段、中文注释、可空规则、生成方、关联关系、索引建议和脱敏边界。
- [x] 同步 OpenSpec delta spec 与设计决策，明确数据结构属于通用规范组成部分，但不锁死具体产品物理 DDL。
- [x] 更新轻量校验脚本，增加标准数据结构、`parent_request_id`、可空关联规则、产品扩展规则和索引建议关键内容检查。
