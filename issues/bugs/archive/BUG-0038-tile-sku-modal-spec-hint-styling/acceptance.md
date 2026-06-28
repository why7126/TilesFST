---
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
status: pending_review
created_at: 2026-06-28 17:02:26
updated_at: 2026-06-28 17:02:26
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

## AC-001 规格未匹配提示 MUST 使用 form-help

**Given** 编辑一条 `spec_id` 为 NULL 的历史 SKU  
**When** 「编辑 SKU」弹窗打开且规格下拉未选择  
**Then** 提示「历史 SKU 未匹配规格，请手动选择后保存」MUST 存在  
**And** 元素 MUST 使用 class `form-help`  
**And** MUST NOT 使用 `form-hint` 或未定义样式类名

## AC-002 提示 Typography MUST 对齐管理端字段辅助文案

**Given** AC-001 场景  
**Then** 提示 MUST 呈现 `11px`、`var(--admin-weak)`、`margin-top: 7px`（与 `user-management.css` `.form-help` 一致）  
**And** 视觉层级 MUST 低于字段标签（12px `--admin-muted`）与同弹窗 `modal-desc`（12px `--admin-weak`）的正文说明

## AC-003 提示文案与显隐逻辑 MUST 不变

**Given** 编辑 SKU 弹窗  
**When** `spec_id` 为 NULL 且未选择规格  
**Then** MUST 展示上述提示文案  
**When** 用户从下拉选择有效规格  
**Then** 提示 MUST 消失  
**And** 保存/上架校验逻辑 MUST NOT 回归

## AC-004 非触发场景 MUST NOT 误展示

**Given** 新增 SKU 弹窗，或编辑已有有效 `spec_id` 的 SKU  
**Then** MUST NOT 展示「历史 SKU 未匹配规格…」提示

## AC-005 修复 MUST NOT 回归同弹窗既有修复

**Given** 本 fix 已合并  
**Then** BUG-0010（modal-desc 副标题）、BUG-0011（弹窗滚动）、BUG-0012（字段规则）相关行为与样式 MUST 保持

## AC-006 测试 MUST 覆盖

**Given** fix change 完成  
**Then** `TileSkuFormModal.test.tsx` MUST 包含：`spec_id: null` 编辑模式断言提示文案与 `form-help` 类名  
**And** vitest MUST 通过
