---
requirement_id: REQ-0075-audit-log-task-trace-linking
title: 审计操作日志补齐任务链路关联字段 - 业务流程
status: done
owner: product
created_at: 2026-07-26 13:02:25
updated_at: 2026-07-26 17:09:06
---

# 业务流程

## 1. 总体流程

```text
管理员发起敏感操作
  |
  v
业务服务获得请求上下文
  |-- request_id
  |-- actor_user_id
  |-- client_type
  |-- task_trace_id/task_type（存在任务上下文时）
  |
  v
业务服务执行操作
  |-- 系统设置修改
  |-- 品牌证书维护
  |-- 媒体/上传相关管理操作
  |-- SKU/Banner 等多步骤管理操作
  |
  v
AuditLogRepository.insert()
  |-- 写入审计基础字段
  |-- 写入 task_trace_id/task_type（可为空）
  |-- 写入脱敏 metadata
  |
  v
日志审计页
  |-- 列表按 task_trace_id/request_id/路径查询
  |-- 详情展示审计上下文和任务链路分组
```

## 2. 审计日志写入流程

```text
调用方准备审计 payload
  |
  +-- 有任务上下文
  |     |
  |     v
  |   传入 task_trace_id + task_type
  |
  +-- 无任务上下文
        |
        v
      task_trace_id/task_type 留空
  |
  v
统一脱敏和长度限制
  |
  v
参数化写入 audit_logs
  |
  v
返回审计记录 ID 或写入结果
```

## 3. 日志审计查看流程

```text
系统管理员进入 /admin/logs
  |
  v
选择 audit 类型或输入 task_trace_id
  |
  v
日志列表返回相关审计操作
  |
  v
打开详情抽屉
  |
  +--> 基础信息：日志 ID、类型、结果、时间
  +--> 操作者 / 客户端：用户、角色、IP 摘要、User Agent 摘要
  +--> 操作上下文：动作、资源、摘要、失败原因
  +--> Task Trace：task_trace_id、task_type、状态、关键节点入口
  +--> metadata JSON：脱敏后展示
```

## 4. 首批接入候选

| 操作域 | 首批策略 | 说明 |
|---|---|---|
| 系统设置修改 | 普通审计为主，存在任务上下文时透传 | 不强制将所有系统设置修改包装为任务。 |
| 品牌证书管理 | 优先接入 | 证书上传、替换、删除等操作可与媒体链路关联。 |
| 媒体/上传相关管理 | 优先接入 | 上传类任务已具备 Task Trace 基础，审计日志应补齐关联字段。 |
| SKU / Banner 多步骤保存 | 条件接入 | 若操作产生或接收 Task Trace，应写入审计日志。 |
| 非任务型审计操作 | 保持兼容 | `task_trace_id`、`task_type` 可为空。 |

## 5. 与父需求及关联需求差异

| 项 | REQ-0024 产品使用日志 | REQ-0069 Task Trace | REQ-0075 本需求 |
|---|---|---|---|
| 追踪中心 | 请求、行为事件、审计操作统一查询 | 业务任务和节点时间线 | 审计操作与任务链路字段打通 |
| 主要对象 | `request_logs`、`usage_events`、`audit_logs` | `task_traces`、spans、日志关联 | `audit_logs.task_trace_id`、`audit_logs.task_type` |
| UI 变化 | 日志审计页基础能力 | 详情时间线 | audit 类型日志展示任务链路 |
| 范围边界 | 日志与埋点治理 | 上传等多节点任务 | 不扩大全量任务型接口覆盖 |

## 6. 异常流程

| 异常 | 处理要求 |
|---|---|
| 调用方未传任务上下文 | 审计日志正常写入，任务字段为空。 |
| `task_trace_id` 非法 | 后端拒绝或忽略不可信任务字段，记录安全摘要，不影响权限判断。 |
| Task Trace 查询不到 | 详情展示审计基础信息，并提示任务链路不可用或已过期。 |
| 审计 metadata 含敏感字段 | 统一脱敏后写入；不得保存原始敏感值。 |
| 审计写入失败 | 不暴露内部路径、堆栈、对象存储凭证；主业务按既有审计失败策略处理。 |
