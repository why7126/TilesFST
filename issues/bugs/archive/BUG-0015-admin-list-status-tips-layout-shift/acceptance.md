---
bug_id: BUG-0015-admin-list-status-tips-layout-shift
status: pending_review
created_at: 2026-06-27 12:40:41
updated_at: 2026-06-27 12:40:41
related_requirement: REQ-0005-brand-management
suggested_fix_change: fix-admin-list-status-toast-layout
related_requirements:
  - REQ-0005-brand-management
  - REQ-0005-user-management
  - REQ-0005-tile-category-management
  - REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 BUG-0003 **AC-004**、**AC-005**（品牌 Tips 不推挤）在四页的等价扩展，且 MUST NOT 回归各列表页 CRUD、筛选、分页与权限。

## AC-001 四页 MUST 使用 fixed toast，禁止文档流 notice（成功/错误反馈）

**Given** 管理员或员工已登录 Web 管理端  
**When** 在以下任一页执行会触发 `setNotice()` 的操作（见 AC-002～AC-005）  
**Then** 反馈 MUST 渲染为 `.admin-toast-region` + `.admin-toast`（或等价共享 `AdminToast` 组件）  
**And** toast 容器 MUST 为 `position: fixed`（或 overlay），MUST NOT 占用 `page-hero` 上方文档流空间  
**And** MUST NOT 在列表页主体顶部使用 `<p className="admin-notice">` 承载自动消失的操作反馈

| 页面 | 路由 |
|---|---|
| 瓷砖品牌 | `/admin/brands` |
| 用户管理 | `/admin/users` |
| 瓷砖类目 | `/admin/tile-categories` |
| 瓷砖 SKU | `/admin/tile-skus` |

## AC-002 Tips 出现/消失 MUST NOT 改变主体纵向位置

**Given** 管理员位于四页中任一页，且已记录 `page-hero` 或首行表格的 `getBoundingClientRect().top`（或目视基准）  
**When** 操作触发 Tips 出现  
**And** 等待约 3.2s Tips 自动消失  
**Then** `page-hero`、指标卡（若有）、筛选区、表格、分页区纵向位置 MUST 与 Tips 出现前一致（允许 ±1px 舍入误差）  
**And** MUST NOT 出现整页上下跳动

## AC-003 四页 toast 视觉与行为 MUST 一致

**Given** 修复完成  
**When** 对比四页成功 Tips（如「品牌已启用」「用户已冻结」「类目已启用」「SKU 已上架」）  
**Then** 位置、圆角、边框、背景、字号、阴影 MUST 一致  
**And** 自动消失时长 MUST 为 3200ms（与现网一致，四页统一）  
**And** MUST 保留 `aria-live="polite"`（或 `aria-atomic="true"`）可访问性语义

## AC-004 瓷砖品牌页 MUST NOT 回归 BUG-0003 验收

**Given** 管理员位于「瓷砖品牌」列表页  
**When** 执行启用、停用、删除、保存品牌或加载失败  
**Then** MUST 展示 toast 反馈  
**And** `BrandManagementPage.test.tsx` 现有断言 MUST 保持通过（`.admin-toast-region` 存在、无文档流 `.admin-notice`）  
**And** 品牌 Logo 展示、上传进度（BUG-0003/0004/0007）MUST NOT 回归

## AC-005 用户管理页 MUST 覆盖典型 notice 路径

**Given** 管理员位于「用户管理」列表页  
**When** 依次或抽样执行：冻结/解冻、删除、重置密码、新建/编辑用户成功、列表加载失败  
**Then** 每条路径 MUST 使用 fixed toast  
**And** MUST NOT 推挤 hero、筛选区、表格

## AC-006 瓷砖类目页 MUST 覆盖典型 notice 路径

**Given** 管理员位于「瓷砖类目」列表页  
**When** 依次或抽样执行：启用/停用、删除、保存类目成功、列表加载失败  
**Then** MUST 使用 fixed toast 且 MUST NOT 推挤主体布局

## AC-007 瓷砖 SKU 页 MUST 覆盖典型 notice 路径

**Given** 管理员位于「瓷砖 SKU」列表页  
**When** 依次或抽样执行：上架、下架、删除、保存 SKU 成功、列表加载失败  
**Then** MUST 使用 fixed toast 且 MUST NOT 推挤主体布局

## AC-008 共享样式 MUST 抽至管理端公共层

**Given** 修复已合并  
**When** 检查样式定义位置  
**Then** `.admin-toast-region` / `.admin-toast` MUST 位于共享样式（如 `admin-home.css`）或共享组件目录  
**And** MUST NOT 仅存在于 `brand-management.css` 私有文件  
**And** 新增样式 MUST 使用管理端 CSS 变量 / semantic token，禁止裸 Hex

## AC-009 弹窗内 inline 错误 MAY 保留 `.admin-notice`

**Given** 品牌/用户/类目/SKU 表单弹窗内字段级或提交错误  
**When** 错误文案展示  
**Then** MAY 继续使用弹窗内 inline 错误（如 `.form-error`、弹窗 body 内 `.admin-notice`）  
**And** 列表页顶部文档流 MUST NOT 用于自动消失的全局操作反馈

**不在 scope**：`AdminLayout.tsx` 侧栏「功能建设中」`.admin-notice` 可保持现状。

## AC-010 自动化 MUST 补齐

**Given** 进入 `fix-admin-list-status-toast-layout`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** MUST 保留或更新 `BrandManagementPage.test.tsx` toast 断言  
**And** MUST 为用户/类目/SKU 至少各补 1 条 Vitest：mock 成功操作后存在 `.admin-toast-region`，不存在列表顶文档流 `.admin-notice`

## AC-011 修复范围 MUST 为纯前端（默认）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 默认 MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 需要 Orval 重新生成（除非无关变更误入）

## AC-012 父需求回归

**Given** BUG-0015 修复完成  
**When** 对照各父需求 acceptance  
**Then** 品牌/用户/类目/SKU 列表的查询、分页、CRUD、权限边界 MUST 无回归  
**And** 各页指标卡、筛选、Sidebar 布局 MUST 无回归

## AC-013 部署冒烟

**Given** Docker 或本地环境已启动  
**When** admin 登录并分别在四页执行至少一次成功状态变更或 CRUD  
**Then** 右上角（或约定位置）toast MUST 可见  
**And** 主体内容 MUST 无上下跳动

## AC-014 文档与流程

**Given** 修复经 OpenSpec `fix-admin-list-status-toast-layout` 进入开发  
**When** `/opsx-archive` 完成  
**Then** 本 BUG `trace.md` MUST 更新为 `done`  
**And** Change `trace.md` MUST 记录 AC-001～AC-004 手工或自动化验收结论
