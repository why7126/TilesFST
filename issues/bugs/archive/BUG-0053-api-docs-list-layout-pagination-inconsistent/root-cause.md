---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表分页与冗余系统接口信息根因分析
severity: medium
status: pending_review
owner: product
created_at: 2026-07-01 13:53:45
updated_at: 2026-07-01 13:57:52
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
---

# 根因分析

## 直接原因

`/admin/api-docs` 接口文档页在表格区域使用了页面局部实现：

- 表格上方固定渲染 `系统接口` 标题，导致用户看到接口列表第一行或列表区域首部存在冗余信息。
- 表格底部仅展示统计文本 `共 x 个接口` 与 `当前筛选 x 条`。
- 当前页没有维护 `page`、`pageSize`、`totalPages` 等分页状态，也没有复用 SKU 页或管理端列表页的分页 DOM 契约。

因此，接口文档列表虽然具备筛选能力，但不具备与瓷砖 SKU 页一致的分页交互与视觉结构。

## 根本原因

REQ-0022 实现时重点覆盖了接口目录、权限、Swagger 策略、OpenAPI/Orval 映射等功能性验收，但列表页横切一致性验收未被完整落实：

- `acceptance.md` 已要求接口目录表格若有分页，分页 DOM MUST 对齐管理端列表页。
- 实现阶段将接口目录作为一次性前端数组渲染，没有将其纳入管理端标准列表页分页模式。
- 前端测试只断言了统计文本与筛选结果，没有断言页码按钮、每页条数选择、筛选回到第一页等交互。

## 触发条件

满足以下条件时可稳定触发：

1. 使用管理员账号访问 `/admin/api-docs`。
2. 接口目录返回多条 route 数据。
3. 查看接口列表区域首部与表格底部分页。

## 问题分类

| 分类 | 结论 | 说明 |
|---|---|---|
| code | 是 | 前端页面局部实现缺少分页状态与分页控件 |
| design | 是 | 列表区域标题与管理端列表页信息层级不一致 |
| test | 是 | 前端测试缺少分页 DOM 与交互断言 |
| api | 否 | 当前可通过前端分页修复，不要求后端接口契约变化 |
| db | 否 | 不涉及数据库结构或查询 |
| security | 否 | 不影响鉴权、敏感信息隐藏或 Swagger 生产策略 |

## 关联证据

- `src/web/src/pages/admin/ApiDocsPage.tsx`：接口列表区固定标题为 `系统接口`，底部仅展示统计文本。
- `src/web/src/pages/admin/TileSkuManagementPage.tsx`：SKU 页已有标准分页结构，包括页码按钮与每页条数选择。
- `issues/requirements/archive/REQ-0022-admin-api-docs-menu/acceptance.md`：横切 AC 要求分页 DOM 对齐管理端列表页。

## 产品确认

用户反馈中的「第一行【系统接口】信息」已确认指接口列表区标题。修复时 MUST 直接移除该标题，不改名、不作为真实接口数据行过滤处理。
