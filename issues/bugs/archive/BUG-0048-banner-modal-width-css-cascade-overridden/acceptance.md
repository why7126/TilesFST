---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
status: pending_review
created_at: 2026-06-28 18:42:00
updated_at: 2026-06-28 18:42:00
related_requirement: REQ-0016-banner-management
related_bug: BUG-0040-banner-modal-width-too-narrow
note: 本 BUG 闭环 BUG-0040 运行时 880px 未生效问题；策略层 640→880 已由 BUG-0040 确立，此处不再重复 debate
---

# 回归验收标准

> 修复本缺陷 MUST 使 Banner 弹窗 **运行时 Computed width 为 880px**（非仅源 CSS 声明），且 MUST NOT 回归 BUG-0033 / BUG-0040 其余 AC。验收 MUST 以 DevTools Computed 或并排 SKU 弹窗为准，**不得**仅以源文件 regex 通过。

## AC-001 Banner 弹窗 Computed width MUST 为 880px

**Given** 视口宽度 ≥ 880px，local dev 或 Docker 构建产物  
**When** 打开「新增 Banner」或「编辑 Banner」弹窗  
**Then** DevTools 选中 `.banner-modal-card`，Computed `width` MUST 为 **880px**  
**And** MUST NOT 为 520px 或其他非 880px 值  
**And** `max-width: 100%` 响应式规则 MUST 保留

- [x] AC-001

## AC-002 生效 CSS 规则 MUST NOT 被 `.modal-card` 520px 覆盖

**Given** 修复完成，全站 admin CSS bundle 已加载（含 `user-management.css`、`system-settings.css`）  
**When** 在 Styles 面板检查 `.banner-modal-card` 的 `width`  
**Then** 生效规则 MUST 来自 `.banner-modal-card`（或更高特异性组合选择器）  
**And** `.admin-shell .modal-card { width: 520px }` MUST NOT 为最终生效的 width 规则

- [x] AC-002

## AC-003 Banner 弹窗 MUST 与 SKU 弹窗并排宽度一致

**Given** 管理员已登录，视口 ≥ 880px  
**When** 并排打开 Banner 弹窗与瓷砖 SKU 弹窗  
**Then** 两弹窗外卡片 Computed width MUST 均为 880px  
**And** 用户感知 MUST 为同一「管理端大表单」档位

- [x] AC-003

## AC-004 `BannerFormModal` MUST 不对齐 SKU 的单一专属类模式

**Given** 修复完成  
**When** 检查 `BannerFormModal.tsx` 弹窗外层 className  
**Then** MUST NOT 同时挂载 `modal-card` 与 `banner-modal-card`（除非组合选择器特异性已保证 880px 且 AC-001 通过）  
**And** SHOULD 对齐 `TileSkuFormModal` 仅使用 `sku-modal-card` 的模式（仅 `banner-modal-card`）

- [x] AC-004

## AC-005 BUG-0033 滚动与 footer MUST 无回归

**Given** 视口高度 ≤ 900px  
**When** 打开任一跳转类型 Banner 弹窗并滚动至底部  
**Then** `.modal-body` MUST 可纵向滚动  
**And** 「取消 / 保存 Banner」footer MUST 固定可见且可点击  
**And** 运营备注 `textarea` MUST 仍占满整行

- [x] AC-005

## AC-006 四套 jump_type 弹窗 MUST 均通过宽度验收

**Given** 修复完成，视口 1440×900  
**When** 分别打开 `NO_JUMP`、`SKU_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE` 弹窗  
**Then** AC-001～AC-003 MUST 全部通过  
**And** 条件字段显隐 MUST 仍符合 REQ-0016

- [x] AC-006

## AC-007 Vitest MUST 覆盖 CSS 层叠（非仅源文件 regex）

**Given** `fix-banner-modal-width-css-cascade`（或补修 change）apply 完成  
**When** 运行 `cd src/web && pnpm vitest run BannerFormModal`  
**Then** 测试 MUST 在 import 完整冲突 CSS 栈后断言 `.banner-modal-card` 宽度行为  
**And** MUST NOT 仅断言 `banner-management.css` 源字符串含 `880px`  
**And** `pnpm build` MUST pass

- [x] AC-007

## AC-008 修复范围 MUST 为纯前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite schema、权限、Orval 生成物  
**And** MUST NOT 重新修改 640→880 策略（已由 BUG-0040 delta 确立）

- [x] AC-008

## AC-009 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 审查 Web UI diff  
**Then** MUST 使用 semantic token  
**And** MUST NOT 新增裸 Hex

- [x] AC-009

## AC-010 BUG-0040 闭环 MUST 记录在 Change trace

**Given** 本 BUG 与 BUG-0040 一并验收  
**When** 完成 `/opsx-apply` 与 manual 验收  
**Then** Change `trace.md` MUST 记录 DevTools Computed 880px 证据  
**And** `fix-banner-list-and-modal-ui` MAY archive 仅当 AC-001～AC-010 全部 pass

- [x] AC-010
