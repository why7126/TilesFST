---
title: 管理端弹窗宽度 CSS 层叠最佳实践
purpose: 预防 modal-card 与专属类双挂载导致 Computed 宽度被 520px 规则覆盖
content: 提炼自 Sprint 003 BUG-0040、BUG-0048
source: /sprint-exps sprint-003
update_method: 新增管理端弹窗时更新
owner: 前端负责人
status: draft
created_at: 2026-06-28 19:42:56
updated_at: 2026-06-28 19:42:56
note: 个案见 issues/bugs/BUG-0048/；本文写模式与预防
---

# 管理端弹窗宽度 CSS 层叠最佳实践

## 背景

`BUG-0040` 将 Banner 弹窗源 CSS 改为 880px 对齐 SKU，但运行时 DevTools Computed 仍为 **520px**（`BUG-0048`）。

根因：`BannerFormModal` 同时挂载 `modal-card` + `banner-modal-card`；全站 bundle 中 `.admin-shell .modal-card { width: 520px }`（来自 `user-management.css`、`system-settings.css` 等）在层叠顺序上覆盖 `.banner-modal-card { width: 880px }`。

**正例**：`TileSkuFormModal` 仅使用 `sku-modal-card`，不挂载通用 `modal-card`。

证据：`issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/root-cause.md`

## 规则（MUST）

| 规则 | 说明 |
|------|------|
| **单一专属类** | 业务弹窗 TSX `className` **仅** `{feature}-modal-card`（如 `banner-modal-card`、`sku-modal-card`） |
| **禁止双类** | MUST NOT 同时挂载通用 `modal-card` |
| **宽度 token** | 宽弹窗 880px、窄弹窗 520px 须在 feature CSS 或 shared token 文档化 |
| **Computed 验收** | apply 完成前 MUST 在 1440 视口确认 DevTools Computed width，不仅看源文件 |
| **Vitest 层叠** | import 可能冲突的 admin CSS（user-management、system-settings、feature css），断言目标类 width |

## 可选加固

- 提高特异性：`.admin-shell .banner-modal-card` 或 `.admin-shell .modal-card.banner-modal-card`（仍推荐移除冗余 `modal-card`）
- 长期：统一 admin modal 宽度 semantic class，减少各 feature 重复定义 `.modal-card`

## 验收 gate（新增弹窗 MUST）

- [ ] TSX 无 `modal-card` 与专属类并存
- [ ] Computed width 与 SKU/设计稿一致（880px 或 520px）
- [ ] Vitest CSS 栈测试通过（参考 `BannerFormModal` fix change）
- [ ] 矮视口下 body scroll 无回归（BUG-0033）

## 关联 BUG（个案）

- `issues/bugs/archive/BUG-0040-banner-modal-width-too-narrow/`
- `issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/`

## 参考

- `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` §4
- `src/web/src/features/admin/components/BannerFormModal.tsx`（fix 后）
- `src/web/src/features/admin/components/TileSkuFormModal.tsx`（正例）
