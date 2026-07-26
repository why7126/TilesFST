---
requirement_id: REQ-0076-observability-dashboard
title: 链路观测仪表原型上下文
status: pending_review
owner: product
created_at: 2026-07-26 13:02:41
updated_at: 2026-07-26 13:02:41
---

# 链路观测仪表原型上下文

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `prototype/web/observability-dashboard.html` | 管理端链路观测仪表静态 HTML 原型策略。 |
| `prototype/web/observability-dashboard-context.md` | 页面结构、字段和交互说明。 |
| `prototype/web/observability-dashboard.png` | 待后续 UI Golden Reference 导出。 |

## 2. 页面定位

本页面是现有日志审计页的观测升级版，用于从聚合指标发现问题，再下钻到日志详情或 Task Trace 时间线。页面不替代日志列表，而是在日志审计入口增加“观测优先”的排障工作流。

## 3. 导航与信息架构

推荐第一版扩展现有 SYSTEM / 日志审计入口，在页面内部提供两个模式：

```text
日志审计
├── 链路观测
└── 日志列表
```

若实现阶段选择独立页面，可在 SYSTEM 分组新增“链路观测”，并保留与日志审计页互跳。

## 4. 布局结构

```text
.admin-shell
└── .admin-main
    ├── .page-head
    ├── .mode-tabs
    ├── .metric-grid
    ├── .filter-card
    ├── .dashboard-grid
    │   ├── .distribution-panel
    │   ├── .ranking-panel
    │   └── .trace-search-panel
    ├── .table-card
    └── .pagination
```

## 5. 关键区域

| 区域 | 内容 |
|---|---|
| 指标摘要 | 总日志量、API 错误率、任务成功率、慢任务、最慢 span、客户端异常占比。 |
| 筛选区 | 时间范围、日志类型、客户端、任务类型、接口路径、状态 / 结果、追踪 ID。 |
| 分布区 | 失败原因分布、客户端分布、接口错误率 Top N、任务状态分布。 |
| 排行区 | 慢任务排行、最慢 span 排行、慢请求排行。 |
| 追踪区 | `request_id` / `task_trace_id` 精确输入与关联结果。 |
| 明细区 | 关联日志、任务或 span 明细，支持打开日志详情或 Task Trace 时间线。 |

## 6. 交互规则

- 默认展示最近 24 小时或后续 design 确认的默认时间范围。
- 切换筛选条件后，摘要、分布、排行和明细同步刷新。
- 点击慢任务、最慢 span、慢请求或错误接口时，保留当前筛选并打开关联详情。
- 复制追踪 ID 使用 fixed toast，不能推挤页面布局。
- 无数据、加载失败、权限不足和追踪 ID 未命中必须有独立状态。

## 7. 数据映射

| UI 字段 | API / 数据字段 |
|---|---|
| 任务成功率 | `task_success_rate` |
| 慢任务数 | `slow_task_count` |
| 最慢 span | `slowest_spans[]` |
| 失败原因分布 | `failure_reasons[]` |
| 客户端分布 | `client_distribution[]` |
| 接口错误率 | `endpoint_error_rates[]` |
| 慢请求排行 | `slow_requests[]` |
| 追踪 ID | `request_id`, `task_trace_id` |

## 8. 实现约束

- MUST 复用管理端 Shell、列表页、筛选、分页、表格、指标卡和详情抽屉模式。
- MUST 使用 semantic token，禁止裸 Hex。
- MUST 通过后端鉴权聚合接口获取数据，不允许前端拉取全量日志后本地聚合。
- MUST 保持敏感字段脱敏，不在指标、排行或详情入口展示原始敏感值。

