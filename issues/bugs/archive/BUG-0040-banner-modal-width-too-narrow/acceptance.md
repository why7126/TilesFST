---
bug_id: BUG-0040-banner-modal-width-too-narrow
status: pending_review
created_at: 2026-06-28 17:43:07
updated_at: 2026-06-28 17:43:07
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 将 Banner 弹窗宽度对齐 SKU 弹窗（880px），且 MUST NOT 回归 BUG-0033（滚动、textarea、footer）。现行 spec「640px」与 modal PNG 由本 BUG acceptance **覆盖**；`/bug-opsx` MUST MODIFIED `web-client` delta。

## AC-001 Banner 弹窗宽度 MUST 为 880px

**Given** 视口宽度 ≥ 880px  
**When** 打开「新增 Banner」或「编辑 Banner」弹窗  
**Then** `.banner-modal-card` 计算宽度 MUST 为 880px  
**And** `max-width: 100%` 响应式规则 MUST 保留（窄视口下不溢出屏幕）

## AC-002 Banner 弹窗宽度 MUST 与 SKU 弹窗一致

**Given** 管理员已登录  
**When** 并排打开 Banner 弹窗与瓷砖 SKU 弹窗（视口 ≥ 880px）  
**Then** 两弹窗外卡片宽度 MUST 视觉一致（均为 880px）  
**And** 用户感知 MUST 为同一「管理端大表单」档位

## AC-003 BUG-0033 滚动与 footer MUST 无回归

**Given** 视口高度 ≤ 900px  
**When** 打开任一跳转类型 Banner 弹窗并滚动至底部  
**Then** `.modal-body` MUST 可纵向滚动  
**And** 「取消 / 保存 Banner」footer MUST 固定可见且可点击  
**And** 运营备注 `textarea` MUST 仍占满整行（width: 100%）

## AC-004 四套 jump_type 弹窗 MUST 均通过宽度与滚动验收

**Given** 修复完成，视口 1440×900  
**When** 分别打开 `NO_JUMP`、`SKU_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE` 弹窗  
**Then** AC-001～AC-003 MUST 全部通过  
**And** 条件字段显隐 MUST 仍符合 REQ-0016 AC-031～AC-038

## AC-005 表单布局 MUST 利用加宽空间

**Given** Banner 弹窗已打开（880px）  
**When** 观察双列 `banner-form-grid`、图片上传区、Combobox、有效期区间  
**Then** 字段 MUST NOT 出现因宽度不足导致的异常挤压（对比修复前 640px 应有更充裕横向留白）  
**And** 双列 grid MUST 仍为两列布局（MUST NOT 因加宽错误变为三列）

## AC-006 修复范围 MUST 为纯前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite schema、权限  
**And** MUST NOT 引入新的后端逻辑

## AC-007 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI  
**Then** MUST 使用 semantic token  
**And** MUST NOT 新增裸 Hex  
**And** SHOULD 与 `.sku-modal-card` 边框/阴影规则保持一致（若 change design 采纳）

## AC-008 验收基准 MUST 对齐 SKU 弹窗（非 640px PNG）

**Given** 修复完成  
**When** 在 1440×1024 并排对比 Banner 弹窗与 SKU 弹窗  
**Then** 宽度一致性 MUST pass  
**And** MUST 在 Change `trace.md` 记录：modal PNG（640px）已由 spec delta 替代，不以 640px Golden 为 pass 条件

## AC-009 OpenSpec delta MUST 更新

**Given** BUG-0040 修复完成  
**When** 查阅 `openspec/specs/web-client/spec.md`  
**Then** Banner 弹窗宽度 MUST 为 880px（或与 SKU 弹窗同宽）  
**And** MUST NOT 仍要求 640px

## AC-010 测试与记录 MUST 补齐

**Given** 进入 `fix-banner-modal-width`（或合并 fix change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `BannerFormModal` Vitest 或样式断言（880px）  
**And** MUST 更新 Change trace checklist
