---
requirement_id: REQ-0124-log-audit-behavior-trace-model
title: 日志审计补齐行为链路与任务链路采集模型 - 业务流程
owner: product
source: requirement.md
created_at: 2026-08-25 22:31:11
updated_at: 2026-08-25 22:31:11
---

# 业务流程

## 1. 界面触发入口

```text
用户访问页面 / 点击按钮 / 提交表单 / 上传文件
  ↓
前端记录 usage_events
  - behavior_trace_id：一次行为链路 ID
  - behavior_event_id：单条行为事件 ID
  ↓
前端请求封装发起一个或多个 API 请求
  - 透传 behavior_trace_id
  - 透传 behavior_event_id
  ↓
后端请求中间件写入 request_logs
  - request_id：服务端可信请求 ID
  - behavior_trace_id：来自前端行为链路，可空但界面触发时应有值
  - parent_behavior_event_id：来源行为事件 ID
  ↓
若请求触发任务类处理，写入 task_traces
  - task_trace_id：任务链路 ID
  - parent_request_id：来源 request_logs.request_id
  ↓
任务执行过程中写入 task_trace_spans
  - 每条 span 对应一个流程节点
  ↓
日志审计按 behavior_trace_id 联动查看：
  行为事件 -> API 请求 -> 任务链路 -> 流程节点
```

## 2. 直接 API 调用入口

```text
外部系统 / 脚本 / 后台调用直接请求 API
  ↓
后端请求中间件写入 request_logs
  - request_id：服务端可信请求 ID
  - behavior_trace_id：空
  - parent_behavior_event_id：空
  ↓
若请求触发任务类处理，写入 task_traces
  - parent_request_id：来源 request_logs.request_id
  ↓
任务执行过程中写入 task_trace_spans
  ↓
日志审计按 request_id 或 task_trace_id 联动查看：
  API 请求 -> 任务链路 -> 流程节点
```

## 3. 日志审计查询流程

```text
管理员进入日志审计页
  ↓
选择查询入口
  ├─ behavior_trace_id：查看一次界面行为及其触发的所有请求
  ├─ request_id：查看单次 API 请求及其任务链路
  └─ task_trace_id：查看任务摘要及流程节点，并回溯来源请求
  ↓
后端按链路字段查询并组合结果
  ↓
前端以列表 + 详情展示
  - 行为来源
  - 请求摘要
  - 任务摘要
  - 流程节点
  ↓
缺少行为来源时显示“无界面行为来源”，不阻断请求与任务排障
```

## 4. 写入边界

| 对象 | 写入方 | 关键字段 | 说明 |
|---|---|---|---|
| `usage_events` | 前端行为采集入口 / 后端接收接口 | `behavior_trace_id`、`behavior_event_id` | 表达用户行为事实，不替代请求日志。 |
| `request_logs` | 后端请求中间件或统一日志服务 | `request_id`、`behavior_trace_id`、`parent_behavior_event_id` | 表达单次 HTTP 请求事实，`request_id` 由服务端生成。 |
| `task_traces` | 任务编排 / 任务服务入口 | `task_trace_id`、`parent_request_id` | 表达任务级摘要，来源请求通过 `parent_request_id` 关联。 |
| `task_trace_spans` | 任务各流程节点 | `task_trace_id`、`span_name`、`status`、`duration_ms` | 表达任务内部流程节点事实。 |

## 5. 横切复盘吸收

- 来自 `admin-list-page-consistency.md`：日志审计属于管理端列表 / 筛选 / 分页页面，后续实现必须复用管理端列表页基准、真实后端分页、固定 toast 和统一筛选控件。
- 来自 sprint-022 复盘：日志审计和 RUM 观测页都容易在主列表、样本页、敏感字段、分页方式上反复返修，本需求在 PRD 阶段明确“主列表 + 详情链路 + 后端分页 + 链路 ID 查询”的展示策略。
- 来自本需求探索结论：`behavior_trace_id` 负责行为链路，`behavior_event_id` 负责具体行为事件，`request_id` 负责服务端请求事实，三者不得混用。
