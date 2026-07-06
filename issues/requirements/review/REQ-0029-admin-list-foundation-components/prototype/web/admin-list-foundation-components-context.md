---
title: 原型上下文
purpose: REQ-0029 管理端列表基础组件原型说明
content: 说明 MetricCard、MetricCardGrid、分页窗口工具与设计验收策略
source: AI 根据 requirement.md、acceptance.md 与知识库横切规则生成
update_method: 组件 API、页面接入范围或设计验收策略变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 14:14:26
updated_at: 2026-07-05 14:14:26
note: REQ-0029-admin-list-foundation-components
---

# 原型上下文

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `admin-list-foundation-components.html` | 展示 MetricCardGrid、MetricCard 状态、分页窗口边界与管理端分页 DOM |
| `admin-list-foundation-components-context.md` | 本文件，说明原型意图与验收边界 |

PNG Golden Reference：待后续设计验收导出。当前 `req-complete` 阶段以 HTML + context 作为 UI 类 prototype 策略。

## 2. 目标

该原型不表达具体业务列表页，而表达可复用基础组件的视觉和 DOM 契约：

- 指标卡必须保留 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。
- 指标卡容器必须能展示 2、3、4 卡片布局。
- danger 描述、空值和 loading 占位需要有清晰示例。
- 分页窗口默认最多 5 页码，并保持 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`。

## 3. 页面接入建议

首批页面建议：

1. `TileSkuManagementPage`：覆盖普通指标卡和 SKU 主列表分页。
2. `LogAuditPage`：覆盖 danger / 异常描述指标卡。
3. `ApiDocsPage`：覆盖接口文档页历史分页与 metric DOM 回归风险。

若 Sprint 容量不足，可先选择 `TileSkuManagementPage` + `LogAuditPage` 两页，`ApiDocsPage` 作为后续推广项。

## 4. 与 REQ-0028 的边界

- 本原型只表达基础组件和分页工具。
- `AdminListPage` 页面级模块顺序、筛选区、表格、操作列、toast、confirm modal 由 `REQ-0028-admin-list-page-contract` 继续承载。
- 后续 `/req-opsx` 的 design.md MUST 引用 `trace.md` 中的 `knowledge_base_refs`。

## 5. 验收优先级

```text
1. prototype/web/admin-list-foundation-components.html
2. prototype/web/admin-list-foundation-components-context.md
3. acceptance.md
4. docs/knowledge-base/best-practices/admin-list-page-consistency.md
5. rules/ui-design.md
6. REQ-0028-admin-list-page-contract
```
