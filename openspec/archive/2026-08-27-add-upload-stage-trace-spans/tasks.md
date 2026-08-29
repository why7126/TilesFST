---
change_id: add-upload-stage-trace-spans
source_requirement: REQ-0123-upload-stage-trace-spans
sprint: sprint-026
created_at: 2026-08-25 18:58:00
updated_at: 2026-08-25 18:58:00
---

# 任务

## 1. Trace Span 基础能力

- [x] 1.1 梳理现有 Task Trace 写入与持久化结构，确认是否已支持阶段 spans。
- [x] 1.2 定义上传阶段 span 写入辅助方法，统一 `span_name`、`duration_ms`、`status`、时间戳、错误摘要和脱敏 metadata。
- [x] 1.3 使用单调时钟记录阶段耗时，避免系统时间跳变影响 `duration_ms`。

## 2. 上传链路接入

- [x] 2.1 在头像上传分支接入 `file_read` 与 `original_put_object` spans。
- [x] 2.2 若头像上传生成 thumbnail 或 display，接入对应派生图生成和对象写入 spans；否则记录或说明跳过语义。
- [x] 2.3 在通用图片上传分支接入 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` spans。
- [x] 2.4 在对象存储写入失败、派生图生成失败和派生图跳过路径保留已完成 spans 与当前阶段状态。

## 3. 合同同步

- [x] 3.1 若新增或调整上传响应、任务查询响应或 Pydantic Schema，同步 OpenAPI、Orval、API 文档和测试。
- [x] 3.2 若新增或调整 Task Trace 存储结构，同步 SQLite/MySQL schema、数据库文档、迁移和回滚说明。
- [x] 3.3 确认对象存储仍通过后端适配层访问，且不改变 Bucket、key 与 MinIO 前缀策略。

## 4. 测试与验证

- [x] 4.1 补充头像上传成功路径测试，验证阶段 spans 名称、耗时和状态。
- [x] 4.2 补充通用图片上传成功路径测试，验证六个基础阶段均出现。
- [x] 4.3 补充对象存储写入失败或派生图失败测试，验证失败阶段、已完成阶段和脱敏错误摘要。
- [x] 4.4 运行后端聚焦测试、OpenSpec 校验、目录结构校验与 Workflow Sync。

## 实现记录

- API：未新增上传响应字段；继续使用既有 `task_trace_id` / `task_type`，不需要 OpenAPI 或 Orval。
- 数据库：复用既有 `task_traces` 与 `task_trace_spans`，不需要 SQLite/MySQL schema 或 migration。
- 对象存储：仍通过后端 `MediaStorageClient.put_object()` 适配层写入，不改变 Bucket、key 或 MinIO 前缀策略。
- Web / 小程序：未修改 UI；原型 UI Gate 为 N/A。
- product_data_collection_observability：适用层级为后端 Task Trace 与对象存储调用周边流程节点；`usage_events`、客户端请求封装、Web、小程序和 App 行为采集为 N/A（本 Change 不改端侧请求或可见 UI）；验证通过 `task_trace_spans` 聚焦测试、OpenSpec 校验和目录结构校验。
