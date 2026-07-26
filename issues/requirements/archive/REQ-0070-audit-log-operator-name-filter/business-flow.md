---
requirement_id: REQ-0070-audit-log-operator-name-filter
title: 日志审计页面操作者名称筛选 - 业务流程
status: done
owner: product
created_at: 2026-07-25 11:57:39
updated_at: 2026-07-26 11:42:52
---

# 业务流程

## 1. 总体流程

```text
系统管理员进入 /admin/logs
  |
  v
打开“操作者”单选可搜索下拉
  |
  v
输入用户名称 / 账号关键字
  |
  v
前端查询用户候选
  |-- 优先复用 GET /api/v1/admin/users?keyword=...
  |-- 仅系统管理员可访问
  |
  v
下拉展示候选项
  |-- 第一行 username
  |-- 第二行 display_name || username
  |
  v
管理员选择一个操作者
  |
  v
前端保存 selected_user.id
  |
  v
GET /api/v1/admin/logs?actor_user_id=<selected_user.id>&...
  |
  v
日志列表按操作者精确过滤
```

## 2. 清空与重置流程

```text
已选择操作者
  |
  +-- 点击控件清空
  |     |
  |     v
  |   actor_user_id 置空 -> 回到第一页 -> 重新查询日志
  |
  +-- 点击页面“重置”
        |
        v
      清空日志类型 / 时间范围 / 操作者 / 状态 / Task Trace ID / 路径 Request ID
        |
        v
      使用默认筛选重新查询日志
```

## 3. 候选异常流程

```text
下拉展开 / 输入关键字
  |
  v
查询用户候选
  |
  +-- loading
  |     -> 下拉显示加载中，不阻塞已有日志列表
  |
  +-- empty
  |     -> 下拉显示无匹配结果
  |
  +-- failed
        -> 页面显示候选加载失败提示
        -> 允许继续使用日志类型、状态、时间范围、Task Trace ID、路径 / Request ID 等其他筛选
        -> 已选操作者可清空
```

## 4. 与现有日志审计能力的关系

| 项 | 现有能力 | REQ-0070 变化 |
|---|---|---|
| 日志列表展示 | 操作者列已显示 `actor_name` / role / anonymous | 列表改为显示 `actor_username`，单行展示账号；详情仍可展示名称 |
| 操作者筛选 | 用户手动输入 User ID | 改为按用户名称或账号搜索并单选 |
| 日志查询参数 | `actor_user_id` | 保持不变，由前端选中用户后填入 |
| 用户数据来源 | 用户管理列表 API | 优先复用现有 keyword 搜索能力 |
| 审计事实源 | 日志表记录 `actor_user_id` | 不改写历史日志事实源 |

## 5. UI 状态流

```text
idle
  |
  v
dropdown_open
  |
  +-- search_loading
  |     -> show loading option
  |
  +-- search_done
  |     -> show options
  |
  +-- search_empty
  |     -> show empty option
  |
  +-- search_failed
  |     -> show error feedback
  |
  v
selected
  |
  +-- clear -> idle
  +-- reset -> idle
```

## 6. 与父需求或相近需求差异

当前 REQ 未挂父需求。它不是用户管理能力扩展，也不是日志审计数据模型扩展，而是日志审计列表页的筛选体验优化。

| 相近能力 | 差异 |
|---|---|
| 用户管理 | 用户管理维护用户资料；本需求只读取候选用户用于日志筛选。 |
| 日志审计列表 | 本需求仅优化操作者筛选控件，不改变日志列表核心分页与详情能力。 |
| REQ-0069 任务链路追踪 | REQ-0069 扩展日志审计追踪维度；REQ-0070 优化操作者筛选交互。 |
