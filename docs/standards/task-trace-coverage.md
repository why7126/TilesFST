---
purpose: Task Trace 覆盖清单
content: REQ-0074 首批任务型接口候选清单、接入优先级、span 策略与后续排期
source: /opsx-apply update-task-trace-coverage-expansion
created_at: 2026-07-26 15:34:18
updated_at: 2026-07-26 15:34:18
---

# Task Trace 覆盖清单

## 1. 判定标准

满足以下任一条件的接口 SHOULD 进入 Task Trace 候选清单；满足多项、已暴露排障痛点或影响大量业务数据的接口 MUST 优先接入首批范围。

| 条件 | 示例 |
|---|---|
| 长耗时 | 大文件处理、复杂查询、批量保存、导入导出 |
| 多步骤 | 保存 SKU 时同时处理基础信息、规格、价格、图片、视频、类目和品牌关联 |
| 跨服务 / 外部依赖 | 对象存储、媒体读取、导出文件生成、外部服务调用 |
| 异步或后台任务 | 用户请求返回后继续处理、轮询状态、后台 worker |
| 批量处理 | 批量上下架、批量删除、批量排序、批量导入 |
| 失败需精确定位 | 单条 request log 无法说明失败节点、慢节点或部分成功明细 |
| 安全审计价值高 | 影响商品、SKU、媒体、展示状态或大量业务数据的关键操作 |

## 2. 首批接入清单

| 场景 | 候选接口 / 任务 | 任务类型 | 优先级 | 关键步骤 | 预期 span | 异步 | 批量 | 对象存储 / 外部依赖 | 首批结论 |
|---|---|---|---|---|---|---|---|---|---|
| 保存 SKU | `POST /api/v1/admin/tile-skus`、`PUT /api/v1/admin/tile-skus/{tile_id}` | `sku_create` / `sku_update` | P1 | 接收请求、输入校验、业务校验、主记录保存、图片/视频关联、响应 | `api_receive`、`input_validate`、`business_process` / `business_persist`、`api_response`、失败 span | 否 | 否 | 关联已上传媒体 object key，不直接写对象存储 | 本期接入 |
| 批量操作 | SKU 上架、下架、删除及后续批量上下架/排序 | `sku_publish` / `sku_unpublish`，后续 `sku_batch_*` | P1 | 接收请求、状态校验、单项处理、成功/失败计数、最终结果 | 单项：`api_receive`、`input_validate`、`business_persist`、`api_response`；批量：`batch_parse`、`item_process`、`batch_result` | 否 | 后续批量接口是 | 否 | 本期接入单项状态任务；批量接口待业务能力出现后接入 |
| 导入 / 导出 | SKU 导入、SKU 导出、日志导出 | `sku_import` / `sku_export` / `log_export` | P2 | 文件接收/生成、解析、校验、持久化、结果文件生成、状态更新 | `file_receive`、`parse`、`validate_rows`、`persist_rows`、`build_result_file`、`task_finished` | 是 | 是 | 可能涉及对象存储和导出文件 | 未纳入；当前无正式导入导出业务能力，后续独立 REQ |
| 媒体处理 | 图片/视频上传后处理、元数据提取、封面或转码候选 | `media_post_process` | P1 | 校验、对象存储、元数据提取、后处理、数据库更新、失败补偿 | `validate_media`、`storage_get_object`、`extract_metadata`、`post_process`、`db_update`、`compensate_failed` | 可能 | 否 | 是 | 上传链路已由 REQ-0069 覆盖；后处理/转码不在本期扩展 |
| 异步任务 | 未来导入、导出、媒体后处理 worker | `async_*` | P2 | 分发、worker 启动、处理、持久化结果、完成/失败 | `async_dispatch`、`worker_start`、`worker_process`、`worker_persist_result`、`worker_finished` / `worker_failed` | 是 | 可能 | 视任务而定 | 本期提供上下文序列化策略；无现有 worker，不新增业务能力 |
| 复杂查询 | 日志审计聚合、链路观测摘要、复杂 SKU 检索 | `log_observability_query` / `sku_complex_query` | P2 | 条件解析、权限过滤、数据库查询、聚合统计、响应序列化 | `parse_filters`、`permission_filter`、`db_query`、`aggregate_metrics`、`serialize_response` | 否 | 否 | 否 | 未纳入；由 REQ-0076 链路观测仪表承接日志聚合 |

## 3. 接入约束

- 业务接口 MUST 通过 `TaskTraceService` helper 或等价封装写入 span，路由层不得直接拼 SQL 或直接持久化 `task_trace_spans`。
- 前端或子请求传入的 `x-task-trace-id` 只用于格式合法时透传，不得作为认证、授权或资源访问依据。
- 本期不新增任务状态查询接口；管理端通过既有日志审计 `task_trace_id` 筛选和日志详情 `task_trace` 时间线查看状态、耗时和失败节点。
- span 写入失败 MUST 降级，不得覆盖主业务错误。
- metadata MUST 经过统一脱敏、截断和安全 JSON 序列化，不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env`、真实客户数据、用户本地绝对路径、未授权对象存储地址或完整敏感请求体。
- 新增响应字段、查询参数或存储字段时 MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md` 和测试。

## 4. 后续排期建议

| 后续项 | 建议来源 | 原因 |
|---|---|---|
| SKU 批量上下架 / 批量排序 Task Trace | 新 REQ | 当前仅有单项状态接口；批量业务能力尚未形成正式接口 |
| SKU 导入 / 导出 Task Trace | 新 REQ | 本期不新增导入导出业务能力，需要先定义任务状态和文件结果契约 |
| 媒体后处理 / 转码 Task Trace | 新 REQ 或 BUG | 本期上传链路已有 Task Trace；转码、封面、多清晰度属于增强能力 |
| 链路观测复杂查询 span | REQ-0076 | 由观测仪表聚合 API 统一评估，避免与本期 SKU 接入交叉扩大 |
