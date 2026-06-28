---
bug_id: BUG-0036-banner-modal-datetime-picker
status: pending_review
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:20:00
---

# 临时规避方案

## 1. 功能规避（有限）

在正式修复前，运营可尝试以下方式 **部分** 配置有效期，但均 **不可靠**，**不能作为验收通过依据**：

1. **留空有效期**：`valid_from` / `valid_to` 均为空时可保存 Banner；上线后按状态与业务规则处理（空结束≈长期）。**无法**表达精确生效窗口。
2. **手动键盘输入**：在支持 `datetime-local` 的浏览器中，点击输入框后 **直接键入** `YYYY-MM-DDTHH:mm`（如 `2026-07-01T18:30`），再保存。部分浏览器/OS 下仍可能无法输入或格式校验失败。
3. **仅选日期**：若浏览器只展示日期选择器，所选时刻可能默认为 `00:00`，结束时间策略仍为提交时 `:59` — 运营无法精确到业务需要的时分。
4. **API 直调（仅开发/测试）**：通过 `POST/PUT /api/v1/admin/banners` 直接提交 ISO datetime（含秒）。**非运营路径**，不得作为产品验收依据。

## 2. 不可用规避

- **无法**在 UI 上稳定选择秒（当前设计与 HTML 原型均不要求 UI 选秒，但 capture 原述秒级需求在修复前无法满足）。
- **无法**在 UI 上获得与 prototype HTML 一致的单字段区间展示 `… 至 …`。
- 暗视口 + 原生控件交互差时，可能 **完全无法** 配置时分（仅能留空或碰运气键入）。

## 3. 验收规避

修复前，REQ-0016 相关 AC **不得标记通过**：

- **AC-027**（公共字段「有效期」可操作、形态对齐 prototype）
- **AC-051**（四套 modal HTML/PNG 并排，含有效期字段）
- **AC-013**（列表「有效期」列展示与配置一致）

验收报告 MUST 标注：BUG-0036 阻塞 Banner 有效期 DateTime 验收。

## 4. 风险说明

- 运营无法按分钟级窗口配置 Banner 生效/失效，`time_status`（待生效 / 已过期）可能与预期偏差。
- 不阻断「无有效期」或「仅到分钟且浏览器可键入」的保存路径，属 **medium** 可用性缺陷而非 hard blocker。
- 必须通过 `fix-banner-modal-datetime-picker`（或合并 change）关闭，键盘规避不能替代正式 DateTime 组件。

## 5. 建议优先级

severity **medium**；宜与 BUG-0031～0035（同一弹窗）同 Sprint、同 `fix-banner-modal-ui` Change 一并修复，避免多次改动 `BannerFormModal.tsx` 回归。
