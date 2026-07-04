---
title: 日志审计列表页原型上下文
purpose: 为开发和 AI Coding 提供日志审计列表页的 UI/UE、布局、字段、状态和交互上下文
content: prototype/web/log-audit-list.html 配套说明
source: ui-design.md + admin-superuser-protection.html + requirement.md
update_method: UI 策略、权限或日志字段变更时同步更新
owner: product
status: draft
note: REQ-0024-log-audit-page-v2-list
created_at: 2026-07-02
updated_at: 2026-07-02
---

# 日志审计列表页原型上下文

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `prototype/web/log-audit-list.html` | 日志审计列表页静态 HTML Golden Reference |
| `prototype/images/log-audit-list.png` | 与 HTML 一致的产品原型图 |
| `requirement.md` | 日志审计页面 v2 需求文档 |

## 2. 页面定位

列表页是系统管理员进入“日志审计”的默认页面，用于查询 API 请求日志、产品行为事件和审计操作。页面强调“快速筛选 + 表格定位 + 查看详情”，不承载复杂 BI 分析。

## 3. 导航结构

SYSTEM 分组菜单顺序必须为：

```text
用户管理
系统设置
日志审计  ← 当前激活
接口文档
```

## 4. 布局结构

```text
.shell
├── .sidebar
└── .main
    ├── .page-head
    ├── .metric-grid
    ├── .filter-card
    ├── .table-toolbar
    ├── .table-card
    └── .pagination
```

## 5. 核心组件

### 5.1 指标摘要卡

展示 4 个核心指标：今日日志、异常请求、慢请求、敏感操作。卡片使用暗色底、极细边框，异常类指标使用红色弱背景标签，正常类指标使用金色或绿色弱背景标签。

### 5.2 筛选区

字段包括：日志类型、时间范围、客户端、结果/状态码、操作者、关键词/request_id。筛选区不使用大面积高亮，保持管理端列表页克制风格。

### 5.3 表格

表格列：时间、类型、摘要、操作者、客户端、结果、耗时、request_id、操作。request_id 采用短展示 + 复制按钮，完整值在 title 或详情中展示。

### 5.4 分页

分页遵循既有规则：左侧展示“共 x 条”，右侧展示页码、跳至 x 页、每页显示 x。

## 6. 交互规则

- 默认展示最近 24 小时日志。
- 点击“查看详情”进入详情抽屉状态，对应 `log-audit-detail-drawer.html`。
- 点击“重置”恢复默认筛选。
- 点击“刷新”重新请求当前筛选条件。
- 复制 request_id 时使用轻反馈，不引发表格布局跳动。

## 7. 数据映射

| UI 字段 | API 字段 |
|---|---|
| 时间 | `created_at` |
| 类型 | `log_type` |
| 摘要 | `summary` |
| 操作者 | `actor_name`, `actor_role` |
| 客户端 | `client_type` |
| 结果 | `result`, `status_code` |
| 耗时 | `duration_ms` |
| request_id | `request_id` |

## 8. 实现约束

- MUST 使用统一 `AdminShell` 与现有管理端列表页组件。
- MUST 使用语义化 Design Token，禁止硬编码业务外观到组件内部。
- MUST 分页请求，不允许前端加载全量日志后过滤。
- MUST 校验系统管理员权限。
