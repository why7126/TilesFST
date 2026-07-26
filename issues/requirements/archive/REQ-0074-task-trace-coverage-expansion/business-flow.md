---
requirement_id: REQ-0074-task-trace-coverage-expansion
title: 任务型接口 Task Trace 覆盖扩展 - 业务流程
status: done
owner: product
created_at: 2026-07-26 13:02:05
updated_at: 2026-07-26 16:56:01
---

# 业务流程

## 1. 总体流程

```text
识别任务型接口候选
  |
  v
按判定标准确认首批接入清单
  |
  v
用户在管理端发起复杂任务
  |
  v
后端生成 / 校验 task_trace_id
  |
  +--> request log 绑定 request_id + task_trace_id
  |
  +--> Task Trace helper 建立任务上下文
  |
  +--> 业务服务写入关键 span
  |      ├── validate_input
  |      ├── business_validate
  |      ├── persist_main_record
  |      ├── process_related_resources
  |      ├── external_dependency 或 async_dispatch
  |      └── api_response / task_finished
  |
  +--> audit log 记录关键操作和资源摘要
  |
  v
任务结束 success / failed / timeout / partial_success
  |
  v
管理端反馈 task_trace_id，日志审计可查看时间线
```

## 2. 首批候选接口梳理流程

```text
扫描管理端业务接口
  |
  +--> 保存 SKU / 商品资料
  +--> 批量上下架 / 删除 / 排序
  +--> 导入 / 导出
  +--> 媒体处理 / 后处理
  +--> 异步任务 / 状态查询
  +--> 复杂查询 / 聚合统计
  |
  v
按任务型判定标准打标
  |
  v
输出接入优先级与 span 设计草案
  |
  v
进入后续 OpenSpec Change design / tasks
```

## 3. 同步接口处理流程

```text
API 收到请求
  |
  v
生成 / 继承 task_trace_id
  |
  v
span: api_receive
  |
  v
span: validate_input
  |
  v
span: business_process
  |
  v
span: persist_or_external_call
  |
  v
span: api_response
  |
  v
返回业务结果 + task_trace_id
```

## 4. 异步任务处理流程

```text
API 收到任务请求
  |
  v
生成 / 继承 task_trace_id
  |
  v
span: async_dispatch
  |
  v
返回 accepted / processing + task_trace_id
  |
  v
后台任务继承 task_trace_id
  |
  +--> span: worker_start
  +--> span: worker_process
  +--> span: worker_persist_result
  +--> span: worker_finished / worker_failed
  |
  v
管理端通过日志审计或任务状态查看追踪结果
```

## 5. 批量任务处理流程

```text
用户发起批量操作
  |
  v
span: batch_parse
  |
  v
span: batch_validate
  |
  v
逐项处理
  |-- span: item_process_success
  |-- span: item_process_failed
  |
  v
span: batch_summary
  |
  v
返回 success / failed / partial_success + task_trace_id
```

## 6. 与父需求 REQ-0069 的差异

| 项 | REQ-0069 上传 Task Trace | REQ-0074 任务型接口覆盖扩展 |
|---|---|---|
| 首要范围 | 图片、视频、文件上传链路 | 保存 SKU、批量操作、导入导出、媒体处理、异步任务、复杂查询等任务型接口 |
| 追踪重点 | 上传卡顿、对象存储、数据库落库、后处理 | 多业务域的关键步骤、子请求、异步任务、部分成功和失败分类 |
| UI 表达 | 日志审计列表和详情时间线 | 复杂任务反馈中的追踪标识展示与复制，以及复用日志审计查看 |
| 设计重点 | 建立 Task Trace 模型和上传样例 | 统一接入标准、helper 封装、首批接口清单和测试矩阵 |
| 验收重点 | 上传节点完整性和日志审计查看 | 首批接口覆盖、span 完整性、失败节点、未接入清单与后续排期 |

## 7. 异常流程

| 异常 | 处理要求 |
|---|---|
| `task_trace_id` 传入非法 | 后端拒绝或覆盖为可信 ID，并记录安全摘要。 |
| 子请求缺失任务上下文 | 写入降级 span 或关联缺失原因，不得静默丢失。 |
| span 写入失败 | 不掩盖主业务错误；记录最小 request log 或可观测性降级摘要。 |
| 批量任务部分失败 | 任务最终状态为 `partial_success` 或等价状态，记录成功数、失败数和失败分类。 |
| 异步任务失败 | 后台任务写入失败 span，并关联原始用户请求的 `task_trace_id`。 |
| metadata 包含敏感字段 | 统一脱敏、截断或拒绝写入敏感内容。 |
