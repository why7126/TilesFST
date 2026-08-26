---
requirement_id: REQ-0126-product-data-collection-observability-standard
title: 建立通用产品数据采集与链路观测规范 - 业务流程
created_at: 2026-08-26 10:20:20
updated_at: 2026-08-26 10:23:12
---

# 业务流程

## 1. 总体链路

```text
产品设计 / 新模块开发
  -> 引用通用产品数据采集与链路观测规范
      -> 识别客户端类型与行为事件
          -> 记录 usage_events
              -> 行为触发 API 透传 behavior_trace_id / behavior_event_id
                  -> 后端记录 request_logs
                      -> 任务类请求按分级策略记录 task_traces
                          -> 关键流程节点记录 task_trace_spans
                              -> 日志审计 / 链路查询 / 聚合分析消费
```

## 2. 界面触发入口

```text
用户访问页面 / 点击业务按钮 / 搜索筛选 / 保存上传
  -> 客户端生成 behavior_trace_id
  -> 客户端生成 behavior_event_id
  -> 上报 usage_events
  -> 行为触发的 API 请求携带 behavior_trace_id / behavior_event_id
  -> 后端 request_logs 保存 behavior_trace_id / parent_behavior_event_id
  -> 如果请求触发任务：
       request_logs.request_id -> task_traces.parent_request_id
       task_traces.task_trace_id -> task_trace_spans.task_trace_id
```

关键规则：

- 同一次用户行为触发多个 API 请求时共享同一个 `behavior_trace_id`。
- `behavior_event_id` 标识单条行为事件。
- `request_id` 仍由后端生成，是服务端可信请求 ID。
- 采集失败不得阻断主业务流程。

## 3. 直接 API 调用入口

```text
外部系统 / 脚本 / API 客户端 / 后台服务 调用业务 API
  -> 不伪造 usage_events
  -> request_logs 记录服务端 request_id
  -> behavior_trace_id 允许为空
  -> 如果请求触发任务：
       request_logs.request_id -> task_traces.parent_request_id
       task_traces.task_trace_id -> task_trace_spans.task_trace_id
```

关键规则：

- 直接 API 调用不要求存在 `usage_events`。
- 直接 API 调用允许 `behavior_trace_id` 和 `parent_behavior_event_id` 为空。
- 直接 API 调用仍必须能通过 `request_id` 进入任务链路。

## 4. Task Trace 分级判定流程

```text
业务 API / 后台任务
  -> 是否长耗时？
  -> 是否多步骤？
  -> 是否批量 / 异步 / 导入导出？
  -> 是否涉及上传、对象存储或第三方服务？
  -> 是否失败后需要定位具体节点？
  -> 是否影响关键业务数据、权限、安全或发布状态？
      -> 任一为是：MUST 接入 Task Trace
      -> 全部为否：MAY 仅保留 request_logs
```

分级策略：

| 类型 | 采集要求 |
|---|---|
| 所有业务 API | MUST 写入 `request_logs` |
| 长耗时 / 多步骤 / 批量 / 异步 / 外部依赖 / 高风险写操作 | MUST 写入 `task_traces` 和关键 `task_trace_spans` |
| 普通简单写操作 | MAY 只保留 `request_logs`，除非产品或安全要求需要下钻 |

## 5. 数据保留流程

```text
明细数据写入
  -> 按类型设置默认保留周期
      -> request_logs：90 天
      -> usage_events：180 天
      -> task_traces / task_trace_spans：90 天
      -> 聚合数据：1 年
  -> 超期扫描
      -> 删除或匿名化明细
      -> 保留长期聚合趋势
```

关键规则：

- 明细数据不得无限期保留。
- 产品如需调整保留周期，必须记录原因、范围和审批依据。
- 长期趋势分析优先消费聚合数据，不应依赖长期保存敏感明细。

## 6. 与父 REQ 的差异

| 项 | REQ-0124 | REQ-0126 |
|---|---|---|
| 定位 | 本项目日志审计行为链路模型落地 | 通用产品数据采集与链路观测规范 |
| 范围 | Web 管理端、后端 API、本项目数据库与日志审计页 | 小程序、店主端、App、Web 管理端、后端 API |
| 交付 | 字段、查询、透传、Task Trace 关联和测试实现 | 标准正文、接入清单、验收门禁、保留周期和治理边界 |
| Task Trace | 支持本项目任务链路采集模型 | 明确跨产品 Task Trace 分级覆盖策略 |
| 保留周期 | 未作为核心交付 | 明确 request_logs 90 天、usage_events 180 天、task trace 90 天、聚合 1 年 |
| 历史数据 | 兼容空行为链路 | 明确不强制历史数据回填，后续按产品分批接入 |

## 7. 标准落地后续流程

```text
/req-review REQ-0126
  -> /sprint-propose --req REQ-0126
      -> /req-opsx REQ-0126
          -> OpenSpec Change 生成 docs/standards 规范
              -> 同步 API / DB / Task Trace / 安全 / 测试引用
                  -> 后续新产品和新模块引用该规范
```
