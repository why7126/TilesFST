---
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
status: pending_review
created_at: 2026-06-27 12:02:52
updated_at: 2026-06-27 12:02:52
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

## AC-001 SKU 弹窗副标题 MUST 使用共享 modal-desc

**Given** 打开 SKU 新增/编辑弹窗  
**Then** 副标题元素 MUST 使用 class `modal-desc`  
**And** MUST NOT 使用 `modal-subtitle` 或未 styled 类名

## AC-002 副标题 Typography MUST 与品牌弹窗一致

**Given** 并排打开 SKU 与品牌新增弹窗  
**Then** 副标题 MUST 为 12px、`var(--admin-weak)`、上间距 8px  
**And** 视觉层级 MUST 一致

## AC-003 弹窗头部 MUST 自适应副标题高度

**Given** 弹窗含标题 + 副标题  
**Then** `.modal-head` MUST 使用 `min-height: 64px` 与 `height: auto`  
**And** 副标题 MUST NOT 被固定 64px 裁切

## AC-004 SKU 副标题文案 MUST 保留 AC-023 语义

**Given** SKU 新增弹窗  
**Then** 副标题 MUST 说明弹窗内不提供状态选择  
**And** 句式 SHOULD 与品牌弹窗「维护…、…与…。」结构一致

## AC-005 修复 MUST NOT 回归 BUG-0011 / BUG-0012

**Given** 副标题样式修复已合并  
**Then** 弹窗滚动布局（BUG-0011）与表单字段规则（BUG-0012）MUST 保持

## AC-006 测试 MUST 覆盖

**Given** fix change 完成  
**Then** `TileSkuFormModal.test.tsx` MUST 断言 `.modal-desc` 存在与文案
