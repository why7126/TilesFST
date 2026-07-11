---
requirement_id: REQ-0028-admin-list-page-contract
title: AdminListPage 模板与管理端列表页契约原型说明
status: approved
created_at: 2026-07-05 10:18:38
updated_at: 2026-07-05 14:36:29
owner: product
prototype_file: admin-list-page-contract.html
---

# 原型说明

## 1. 目标

本原型用于表达 `AdminListPage` 在 `/design-system` 中应呈现的管理端列表页验收样例。它不是生产页面，也不替代后续 React 实现；后续 OpenSpec design 应以本 HTML、本文档、`acceptance.md`、`rules/ui-design.md` 和 `openspec/specs/web-client/spec.md` 为视觉与结构参考。

## 2. 页面结构

```text
AdminListPage
├── page-hero：标题、说明、主操作
├── metric-grid：四个摘要指标卡
├── filter-card：关键词、状态、类型、时间范围、重置
├── table-card：表格 + sticky action column
└── pagination：page-summary + page-right + page-buttons + page-size
```

## 3. 验收重点

- 模块顺序必须固定为标题、指标卡、筛选、列表。
- 分页左侧必须为 `page-summary`，右侧必须为 `page-right`。
- 行操作列必须使用 sticky action column 视觉，横向滚动时仍可达。
- 默认筛选区不展示「查询」或「搜索」提交按钮，只保留重置。
- 状态变更类操作必须通过 DS confirm modal，prototype 中只展示入口，不定义弹窗细节。
- 操作反馈应由 fixed toast 承载，不插入文档流。

## 4. 与 REQ-0029 的边界

本原型中展示了 MetricCard 与分页窗口样式，但 `MetricCard` 字段扩展、PaginationWindow 算法工具和更细组件 API 可由 `REQ-0029-admin-list-foundation-components` 继续细化。

## 5. 待导出

- [ ] PNG Golden Reference 待后续 `/req-complete` 或人工视觉评审导出。
- [ ] 如进入 `/req-opsx`，design.md MUST 写明本 HTML 优先级高于文字 acceptance 的视觉解释。
