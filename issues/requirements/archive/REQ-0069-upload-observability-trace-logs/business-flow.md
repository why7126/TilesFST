---
requirement_id: REQ-0069-upload-observability-trace-logs
title: 任务链路追踪与审计日志查看 - 业务流程
status: done
owner: product
created_at: 2026-07-25 11:45:49
updated_at: 2026-07-26 11:56:45
---

# 业务流程

## 1. 总体链路

```text
用户发起任务
  |
  v
生成 / 接收 task_trace_id
  |
  +--> 前端记录任务开始、进度、完成/失败
  |
  +--> API 请求日志记录 request_id + task_trace_id
  |
  +--> 后端服务记录 task span
  |      ├── validate
  |      ├── storage / external dependency
  |      ├── db commit
  |      └── post process
  |
  +--> 审计日志记录关键业务操作
  |
  v
任务结束 success / failed / timeout / cancelled
  |
  v
管理端日志审计
  ├── 列表按 task_trace_id / request_id / task_type 查询
  └── 详情抽屉展示任务时间线
```

## 2. 上传首批流程

```text
管理员选择图片/视频/文件
  |
  v
前端创建上传任务上下文
  |-- span: frontend_select_file
  |-- span: frontend_upload_start
  |
  v
POST /api/v1/uploads/...
  |-- request_id
  |-- task_trace_id
  |
  v
FastAPI uploads API
  |-- span: api_receive
  |-- span: validate_file
  |
  v
Object Storage Adapter
  |-- span: storage_put_object
  |-- metadata: bucket/prefix/object_key 摘要
  |
  v
Media Repository
  |-- span: db_create_media
  |
  v
Post Process（按类型可 N/A）
  |-- span: post_process
  |
  v
API response
  |-- span: api_response
  |
  v
前端 done / failed
  |-- span: frontend_done 或 frontend_failed
  |-- 同会话即时回显或控件内错误
```

## 3. 审计日志查看流程

```text
系统管理员进入 /admin/logs
  |
  v
输入 task_trace_id / request_id / task_type
  |
  v
日志列表返回相关日志
  |
  v
打开详情抽屉
  |
  +--> 基础信息
  +--> 请求信息
  +--> 操作者 / 客户端
  +--> 任务时间线
  |      ├── 节点
  |      ├── 耗时
  |      ├── 状态
  |      ├── request_id
  |      └── error_code
  +--> metadata JSON（脱敏）
```

## 4. 与父需求 REQ-0024 的差异

| 项 | REQ-0024 产品使用日志 | REQ-0069 Task Trace |
|---|---|---|
| 追踪中心 | request / usage_event / audit 单条日志 | 一次业务任务及其多个节点 |
| 主要 ID | `request_id` | `task_trace_id` + `request_id` |
| 主要视角 | 日志列表与日志详情 | 任务时间线与节点耗时 |
| 首批场景 | 页面行为、请求日志、审计操作 | 图片/视频/文件上传，后续扩展长耗时任务 |
| 排障能力 | 定位单次接口异常 | 定位任务跨节点慢点与失败节点 |

## 5. 异常流程

| 异常 | 处理要求 |
|---|---|
| 前端上传失败 | 记录 `frontend_failed`，控件内展示错误；已有 `task_trace_id` 时上报失败事件。 |
| 后端校验失败 | 记录 `validate_file failed`，返回统一错误码，日志不暴露内部路径。 |
| 对象存储写入慢或失败 | 记录 `storage_put_object` 耗时和错误摘要，保留对象 key 前缀或脱敏标识。 |
| 数据库落库失败 | 记录 `db_create_media failed`，任务最终状态为 failed。 |
| 任务追踪写入失败 | 不吞掉主业务错误；按降级策略记录最小 request log 或错误摘要。 |
| 用户刷新页面 | 后端仍可通过 `task_trace_id` 查询已写入节点；前端即时回显可丢失但审计事实源保留。 |
