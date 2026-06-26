---
title: 需求验收标准
purpose: REQ-0008 品牌列表启停二次确认验收标准
content: 基于 requirement.md 与 prototype/web/brand-status-confirm-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: approved
note: REQ-0008-brand-status-confirm
---

# 验收标准

## 1. 启停二次确认（O-01 / FR-001）

- [ ] **AC-001** 点击「停用」时 MUST NOT 直接调用 disable API；须先展示确认弹窗。
- [ ] **AC-002** 点击「启用」时 MUST NOT 直接调用 enable API；须先展示确认弹窗。
- [ ] **AC-003** 停用确认弹窗标题为「停用品牌」；正文为「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」
- [ ] **AC-004** 启用确认弹窗标题为「启用品牌」；正文为「确认启用品牌「{name}」？」
- [ ] **AC-005** 弹窗底部含「取消」与「确认停用」/「确认启用」；主按钮触发 API。
- [ ] **AC-006** 取消、点击遮罩、× 或 ESC 时弹窗关闭，品牌状态不变。
- [ ] **AC-007** 确认成功后 Toast「品牌已停用」/「品牌已启用」，列表与指标卡 summary 刷新。
- [ ] **AC-008** 启停确认弹窗视觉结构对齐现有「删除品牌」确认框（modal-backdrop / modal-card / modal-head / modal-body / modal-footer）。
- [ ] **AC-009** 删除确认流程独立，不受启停确认影响。
- [ ] **AC-010** 行内按钮文案仍为「启用」/「停用」；权限与可见性规则与 REQ-0005 一致。

## 2. 无障碍与样式（FR-002）

- [ ] **AC-011** 确认弹窗设置 `role="dialog"`、`aria-modal="true"`，`aria-labelledby` 指向标题 id。
- [ ] **AC-012** 样式使用 semantic token / 既有 brand-management.css，TSX 无裸 Hex。

## 3. 回归与不回归

- [ ] **AC-013** 4 指标卡、page-header、新增品牌、BrandFormModal 无回归。
- [ ] **AC-014** 删除规则不变：仅 SKU=0 且已停用可删；置灰提示不变。
- [ ] **AC-015** 筛选、分页、查询/重置无回归。
- [ ] **AC-016** `admin` / `employee` 可访问；未登录跳转登录页。
- [ ] **AC-017** 无 API / OpenAPI / Orval 变更。

## 4. 自动化与构建

- [ ] **AC-018** vitest：点击启停先出确认弹窗；确认前 mock API 未被调用。
- [ ] **AC-019** vitest：确认停用/启用后 mock enableBrand/disableBrand 被调用。
- [ ] **AC-020** vitest：取消或关闭弹窗后 API 未被调用。
- [ ] **AC-021** `cd src/web && npm run build` 通过。

## 5. 视觉与流程

- [ ] **AC-022** 1280×1024 与 `brand-status-confirm-context.md` 并排验收。
- [ ] **AC-023** 变更经 OpenSpec `fix-brand-status-confirm` 进入开发并 archive。
