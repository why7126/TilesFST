---
bug_id: BUG-0011-tile-sku-modal-content-overflow
status: pending_review
created_at: 2026-06-27 09:17:24
updated_at: 2026-06-27 09:17:24
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0006 **AC-022**（弹窗主体可滚动），且不得回归 AC-028～AC-036 功能。

## AC-001 弹窗主体 MUST 可垂直滚动

**Given** 管理员已登录，视口高度 ≤ 900px（或 1080p 浏览器非最大化）  
**When** 打开「新增SKU」或「编辑SKU」弹窗  
**Then** 弹窗 `.modal-body`（或等价内容区）MUST 出现垂直滚动条或支持滚轮/触控板滚动  
**And** 用户 MUST 能滚动至表单最底部

## AC-002 页眉与页脚 MUST 保持可达

**Given** 弹窗已打开且内容超出视口  
**When** 用户滚动内容区  
**Then** 标题、副标题、关闭按钮 MUST 保持可见（固定于头部）  
**And** 「取消 / 保存草稿 / 创建SKU（或保存）」footer MUST 保持可见且可点击（固定于底部）

## AC-003 全部字段 MUST 可操作

**Given** 弹窗处于矮视口  
**When** 滚动至底部  
**Then** MUST 可访问并操作：SKU 图片上传区、主图标记、SKU 视频上传区、备注说明 textarea  
**And** 各输入控件 MUST 可聚焦、可输入、可点击

## AC-004 滚动 MUST 不影响遮罩交互

**Given** 弹窗打开  
**When** 用户在内容区滚动或按 ESC / 点击遮罩 / 点击关闭  
**Then** 滚动行为 MUST 不导致意外关闭（除非用户明确关闭）  
**And** ESC、遮罩点击、× 关闭 MUST 仍正常工作

## AC-005 视口回归矩阵

**Given** 修复完成  
**When** 在以下视口打开新增弹窗并滚动到底部  
**Then** 全部 AC-001～AC-003 MUST 通过：

| 视口 | 说明 |
|------|------|
| 1440×900 | 常见笔记本 |
| 1280×720 | 矮视口 |
| 1920×1080 非全屏 | 浏览器窗口约 900px 高 |

## AC-006 修复范围 MUST 为纯前端布局

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 引入新的后端校验逻辑

## AC-007 测试与记录

**Given** 进入 `fix-tile-sku-modal-content-overflow`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 TileSkuFormModal 相关 Vitest（modal-body scroll 或布局 class）  
**And** MUST 在 Change `trace.md` 记录矮视口滚动验收结论

## AC-008 REQ-0006 AC-022 对齐确认

**Given** BUG-0011 修复完成  
**When** 对照 `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` AC-022  
**Then** 「弹窗宽 880px，`max-height` 不超过视口，**主体可滚动**」MUST 全部满足
