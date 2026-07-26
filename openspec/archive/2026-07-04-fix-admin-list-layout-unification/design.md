---
change_id: fix-admin-list-layout-unification
title: 管理端多列表页布局与筛选分页交互统一修复 - 设计
created_at: 2026-07-03 18:51:13
updated_at: 2026-07-03 18:51:13
source_bug: BUG-0055-admin-list-layout-unification
status: proposed
---

# Design

## Context

BUG-0055 指向 Web 管理端列表页的横切一致性问题。当前实现中，各页面分别拼装标题、指标卡、筛选区、表格和分页，历史修复也多按页面局部推进，导致同类页面仍存在差异：

- `BannerManagementPage.tsx` 的模块顺序为「标题 → 筛选 → 指标卡 → 列表」，与目标顺序不一致。
- SKU、品牌、类目、规格、日志审计等页面仍存在【查询】按钮。
- 多数页面分页只渲染上一页、当前页、下一页，未实现最多 5 个可点击页码窗口。
- sticky action column 仅在接口文档页等局部实现，未统一到管理端列表页。

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | 管理端多列表页模块顺序、筛选区、操作列和分页页码不统一 |
| 复现 | 登录管理端，依次访问 SKU、品牌、类目、规格、Banner、用户、日志审计、接口文档页面并对比布局/交互 |
| 根因分类 | design / code / test |
| 直接原因 | 各页面分别实现列表结构，缺少统一列表页结构、分页窗口和 sticky action column 契约 |
| 根本原因 | 管理端列表页一致性没有沉淀为共享组件/模板或横切 spec，测试缺少跨页面矩阵 |
| 严重等级 | medium |
| 关联需求 | `REQ-0005-brand-management`、`REQ-0005-tile-category-management`、`REQ-0005-user-management`、`REQ-0006-tile-sku-management`、`REQ-0009-tile-spec-management`、`REQ-0016-banner-management`、`REQ-0022-admin-api-docs-menu`、`REQ-0024-product-usage-logging` |
| API 影响 | 无 |
| DB 影响 | 无 |
| Orval 影响 | 默认无 |

## 修复方案

### D1. 统一页面结构

所有受影响页面应按以下顺序渲染：

1. 标题模块：`page-hero` 或等价结构，包含 eyebrow、标题、说明和主操作入口。
2. 指标卡模块：`summary-grid`，展示页面摘要指标。
3. 筛选/搜索模块：`filter-card`，展示关键词、select、日期/状态等筛选控件与重置入口。
4. 列表模块：`table-card`，包含表格和分页。

Banner 管理等顺序不一致页面必须调整。表格上方不得新增旧版 `section-head`、`table-toolbar` 或重复列表标题。

### D2. 筛选/搜索交互

筛选/搜索模块以 SKU 页字段密度和控件视觉为基线，但所有页面移除显式【查询】/【搜索】按钮。

实现可采用以下任一策略，并在 implementation trace 中记录：

1. 筛选控件变化即时更新本地状态并触发请求或重新计算列表。
2. 对文本关键词输入采用轻量 debounce。
3. Enter 键可保留为提交关键词的便捷方式，但不得显示【查询】按钮。

所有筛选变化和重置动作必须将页码重置到第 1 页。

### D3. 固定操作列

以接口文档页 `api-docs-action-cell` 为基线沉淀通用 sticky action column 样式：

- `position: sticky`
- `right: 0`
- 右侧背景与卡片背景一致
- 左侧细分割线
- 左侧阴影提示横向滚动层级
- 表头和表体最后一列保持宽度与 z-index 协调

实现应优先抽取通用 class 或 helper，而不是在每个页面复制一份略有差异的 CSS。

### D4. 统一分页窗口

分页组件或等价 helper 必须支持：

- 左侧 `page-summary`
- 右侧 `page-right`
- `page-buttons` + `page-btn` + `active`
- 上一页/下一页按钮
- 最多 5 个可点击页码，不包含上一页/下一页
- 总页数为 1 时仍展示统一结构，上一页/下一页禁用，`1` 为当前页
- 切换筛选和 page_size 时回到第 1 页

建议将页码窗口计算抽成可测试函数，覆盖总页数 1、5、6、当前页靠前、居中、靠后等场景。

### D5. 测试策略

测试应覆盖横切矩阵，而不是只针对单页：

1. 受影响页面不渲染【查询】/【搜索】按钮。
2. 受影响页面模块顺序符合标题 → 指标卡 → 筛选 → 列表。
3. 分页页码最多 5 个。
4. 筛选变化和每页条数变化回到第 1 页。
5. 最后一列表头/单元格具有 sticky action column 契约。

## Risks

| 风险 | 缓解 |
|---|---|
| 移除查询按钮后请求过于频繁 | 文本输入使用 debounce；select 变化可即时刷新 |
| 统一 sticky column 后窄屏表格出现层级遮挡 | 对 1366/1440/1920 及移动 smoke 做视觉回归 |
| 多页面同时调整导致业务操作回归 | 针对新增、编辑、启停、删除、查看、重置密码等关键操作保留回归测试 |
| 与日志审计在研 Change 交叉 | 本 Change 限定为布局/筛选/表格/分页一致性，不改日志 API 与数据模型 |

## Non-Goals

- 不新增管理端业务页面。
- 不调整后端列表 API、分页响应结构或错误码。
- 不修改数据库、MinIO、媒体上传、Docker Compose、环境变量。
- 不重做 Design System token 值。
- 不处理 BUG-0054 的全局内容区 padding 问题。
