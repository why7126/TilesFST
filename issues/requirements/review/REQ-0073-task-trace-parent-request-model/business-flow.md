---
requirement_id: REQ-0073-task-trace-parent-request-model
title: Task Trace 主请求与子请求关联模型 - 业务流程
status: approved
owner: product
created_at: 2026-07-26 13:03:43
updated_at: 2026-07-26 13:09:26
---

# 业务流程

## 1. 主请求创建 Task Trace

```text
用户发起任务型 API 请求
  |
  v
后端生成 request_id
  |
  v
识别 / 创建 Task Trace
  |-- task_trace_id
  |-- parent_request_id = 当前 request_id
  |
  v
写入 request_log
  |-- request_id
  |-- task_trace_id
  |
  v
业务服务执行任务节点
  |
  v
写入 task spans
```

## 2. 子请求与 span 关联

```text
同一任务后续请求 / 事件上报
  |
  v
携带或解析 task_trace_id
  |
  v
后端生成新的 request_id
  |
  +--> request_log: request_id + task_trace_id
  |
  +--> usage_event / audit_log: task_trace_id + request_id（如适用）
  |
  +--> task_span: task_trace_id + request_id + span_name + status
```

## 3. 双向定位流程

```text
入口 A：主请求 request_id
  |
  v
请求日志详情
  |
  v
关联 Task Trace 摘要 / task_trace_id
  |
  v
任务时间线

入口 B：Task Trace 时间线
  |
  v
span 列表
  |
  v
span.request_id
  |
  v
对应请求日志详情
```

## 4. 上传首批验证流程

```text
管理员上传图片 / 视频 / 文件
  |
  v
POST /api/v1/uploads/...
  |-- request_id = 主请求
  |-- task_trace_id
  |
  v
task_traces
  |-- task_trace_id
  |-- parent_request_id = 上传主请求 request_id
  |
  v
task_trace_spans 或等价结构
  |-- api_receive.request_id
  |-- validate_file.request_id
  |-- storage_put_object.request_id
  |-- db_create_media.request_id
  |-- api_response.request_id
  |
  v
日志详情可从上传主请求与 task_trace_id 双向查看
```

## 5. 与父需求差异

| 项 | REQ-0069 Task Trace | REQ-0073 请求关联模型 |
|---|---|---|
| 关注中心 | 建立任务时间线、状态、耗时、span 和上传首批场景 | 明确主请求、子请求、span 的强关联字段和写入策略 |
| 主要 ID | `task_trace_id` + `request_id` | `parent_request_id` + span `request_id` + `task_trace_id` |
| 数据模型重点 | 是否新增 task traces / spans 或组合方案 | `parent_request_id` 使用独立字段还是结构化 metadata |
| 验收重点 | 能看任务时间线和慢节点 | 能从主请求到任务、从 span 到请求双向定位 |
| 历史数据 | 不要求为历史日志生成 `task_trace_id` | 不要求回填历史 `parent_request_id`，但必须兼容缺失字段 |

## 6. 异常流程

| 异常 | 处理要求 |
|---|---|
| 前端传入非法 `task_trace_id` | 后端拒绝信任并生成或返回明确校验错误；主请求日志仍必须落库。 |
| Task Trace 创建失败 | 不得吞掉主业务错误；记录最小 request log 和安全错误摘要。 |
| span 写入失败 | 不覆盖业务响应；记录追踪降级摘要，便于后续排障。 |
| 历史日志缺少 `parent_request_id` | API 和页面安全兜底，不展示误导性关联。 |
| 一个主请求触发多个 Task Trace | 日志详情以列表或分组展示多个任务摘要，不覆盖关联。 |
