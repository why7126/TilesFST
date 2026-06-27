---
bug_id: BUG-0014-tile-sku-publish-action-missing
status: pending_review
created_at: 2026-06-27 12:18:20
updated_at: 2026-06-27 12:18:20
related_requirement: REQ-0006-tile-sku-management
suggested_fix_change: fix-tile-sku-publish-action-missing
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0006 **AC-018**（操作列）、**AC-037**（上下架/恢复）、**FR-007**，且不得回归 SKU 列表 CRUD、筛选、下架与删除规则。

## AC-001 已下架行 MUST 展示恢复/上架操作

**Given** 管理员已登录 Web 管理端  
**When** SKU 列表中存在 `status = DISABLED`（已下架）的行  
**Then** 操作列 MUST 含「编辑」与「恢复」或「上架」按钮  
**And** 点击后 MUST 调用 `POST /api/v1/admin/tile-skus/{id}/publish`

## AC-002 已上架行 MUST 保持下架操作

**Given** SKU 列表中存在 `status = PUBLISHED` 的行  
**When** 查看操作列  
**Then** MUST 含「编辑」「下架」  
**And** 「删除」MUST 展示但置灰，title 提示「已上架 SKU 不允许删除」

## AC-003 草稿/待完善行 MUST 保持上架操作

**Given** SKU 列表中存在 `status = DRAFT` 或 `NEEDS_COMPLETION` 的行  
**When** 查看操作列  
**Then** MUST 含「编辑」「上架」  
**And** 行为与修复前一致，无回归

## AC-004 恢复上架 MUST 刷新列表与 Toast

**Given** 已下架 SKU 满足 publish 前置条件（主图、必填项完整）  
**When** 点击「恢复」或「上架」  
**Then** MUST 显示成功 Toast（如「SKU 已上架」）  
**And** 列表刷新后该行 status MUST 变为「已上架」，操作变为「编辑」「下架」

## AC-005 publish 失败 MUST 展示错误信息

**Given** 已下架 SKU 缺少主图或不满足 publish 校验  
**When** 点击「恢复」或「上架」  
**Then** MUST 展示服务端错误信息（如「缺少主图，无法上架」）  
**And** 行状态 MUST 保持「已下架」

## AC-006 操作列 MUST 与删除按钮独立渲染

**Given** 任意 SKU 行  
**When** 检查操作列 DOM  
**Then** publish/unpublish 按钮 MUST NOT 与 `canDeleteTileSku` 结果互斥隐藏  
**And** 逻辑 MUST 对齐 BUG-0001 修复后的类目管理页模式

## AC-007 父需求回归

**Given** BUG-0014 修复完成  
**When** 对照 `REQ-0006-tile-sku-management/acceptance.md`  
**Then** AC-018（编辑、上下架/恢复、更多）、AC-037（上下架/恢复文案）MUST 全部满足  
**And** 筛选、指标卡、分页、弹窗无回归

## AC-008 修复范围 MUST 为纯前端（默认）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 默认 MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** 若仅补后端集成测试（`DISABLED → publish`），MUST NOT 改变既有 publish 业务规则

## AC-009 自动化 MUST 补齐

**Given** 进入 `fix-tile-sku-publish-action-missing`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** MUST 补充 `TileSkuManagementPage` Vitest：mock `DISABLED` 行断言存在「恢复」或「上架」  
**And** mock `PUBLISHED` 行断言存在「下架」且不存在误绑定的 publish 按钮

## AC-010 部署冒烟

**Given** Docker 或本地环境已启动  
**When** admin 登录 `/admin/tile-skus`，对一条 SKU 执行下架再恢复  
**Then** 下架后操作列 MUST 可见恢复入口  
**And** 恢复后 MUST 在列表与指标卡「已上架」计数中体现

## AC-011 文档与流程

**Given** 修复经 OpenSpec `fix-tile-sku-publish-action-missing` 进入开发  
**When** `/opsx-archive` 完成  
**Then** 本 BUG `trace.md` MUST 更新为 `done`  
**And** Change `trace.md` MUST 记录 AC-001～AC-004 手工或自动化验收结论
