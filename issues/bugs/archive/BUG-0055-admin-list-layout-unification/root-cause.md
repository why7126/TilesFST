---
bug_id: BUG-0055-admin-list-layout-unification
title: 管理端多列表页布局与筛选分页交互未统一根因分析
severity: medium
status: approved
owner: product
created_at: 2026-07-03 18:41:17
updated_at: 2026-07-03 18:41:17
related_requirement: null
related_change: fix-admin-list-layout-unification
---

# 根因分析

## 直接原因

管理端列表页当前由各页面分别拼装标题、指标卡、筛选区、表格和分页，缺少统一的列表页结构约束与公共分页/表格操作列契约，导致同一类页面在后续迭代中出现局部修复、局部对齐、局部遗留并存。

已观察到的直接表现包括：

- `BannerManagementPage.tsx` 的模块顺序为「标题模块 → 筛选/搜索模块 → 指标卡模块 → 列表模块」，与目标顺序不一致。
- `TileSkuManagementPage.tsx`、`BrandManagementPage.tsx`、`TileCategoryManagementPage.tsx`、`TileSpecManagementPage.tsx` 仍保留【查询】按钮。
- `LogAuditPage.tsx` 仍保留【查询】按钮，并使用带图标的按钮组合，和 SKU 页筛选动作基线不一致。
- 多数页面分页仅渲染上一页、当前页、下一页，未按“最多 5 个可点击页码”展示页码窗口。
- 表格最后一列固定浮动样式只在接口文档页等局部页面实现，未作为管理端列表表格通用能力推广到 SKU、品牌、类目、规格、Banner、用户等页面。

## 根本原因

本缺陷的根本原因是管理端列表页一致性尚未沉淀为可复用页面模板或强约束组件：

1. 页面级实现重复：各列表页分别维护筛选 grid、按钮组、表格、分页和操作列样式。
2. 基线来源分散：筛选/搜索以 SKU 页为准，固定操作列以接口文档页为准，但尚未形成统一的 `AdminListPage` 或等价共享契约。
3. 回归测试偏页面局部：已有测试覆盖部分页面的分页 DOM 或单页 UI 约束，但缺少跨页面一致性矩阵，未同时验证模块顺序、无查询按钮、重置按钮尺寸、sticky action column、最多 5 页码。
4. 历史修复按页面推进：品牌、规格、Banner、接口文档等页面曾分别做过分页或布局修复，未在同一轮 Change 中收敛为横切规范。

## 触发条件

满足以下条件时可稳定触发：

1. 使用管理员账号登录 Web 管理端。
2. 依次访问瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计、接口文档。
3. 对比页面模块顺序、筛选/搜索区按钮、重置按钮尺寸、表格最后一列和分页页码。

## 问题分类

| 分类 | 结论 | 说明 |
|---|---|---|
| design | 是 | 管理端列表页布局、筛选、分页和操作列缺少统一视觉与交互契约 |
| code | 是 | 前端页面分别实现同类列表结构，公共组件/模板复用不足 |
| test | 是 | 缺少跨页面一致性测试矩阵，未覆盖最多 5 页码与 sticky action column 等横切规则 |
| api | 否 | 当前判断可通过前端布局与分页呈现修复，不要求 API 契约变化 |
| db | 否 | 不涉及数据库结构、索引或查询迁移 |
| security | 否 | 不影响鉴权、权限边界或敏感信息保护 |
| media | 否 | 不涉及 MinIO、图片、视频或文件上传链路 |

## 关联证据

- `src/web/src/pages/admin/TileSkuManagementPage.tsx`：SKU 页当前提供指标卡在筛选前的目标结构，但仍含【查询】按钮，且分页只展示当前页。
- `src/web/src/pages/admin/BannerManagementPage.tsx`：Banner 页筛选区位于指标卡之前，与目标模块顺序不一致。
- `src/web/src/pages/admin/LogAuditPage.tsx`：日志审计页含【查询】按钮，筛选区按钮形态与 SKU 页不完全一致。
- `src/web/src/pages/admin/ApiDocsPage.tsx` 与 `src/web/src/features/admin/styles/api-docs.css`：接口文档页已有 `position: sticky; right: 0;` 的操作列基线，可作为末列固定浮动参考。
- `src/web/src/features/admin/styles/user-management.css`：分页基础样式已存在，但页码窗口能力没有作为统一逻辑复用到各页面。

## 结论

该问题不是单个页面的孤立样式错误，而是管理端列表页缺少统一结构和横切验收导致的一组 UI/交互一致性偏差。后续修复应优先抽取或沉淀统一列表页契约，再按页面矩阵批量对齐。
