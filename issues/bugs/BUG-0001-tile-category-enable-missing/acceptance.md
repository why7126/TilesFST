---
title: 缺陷验收标准
purpose: BUG-0001 修复回归验收
bug_id: BUG-0001-tile-category-enable-missing
status: draft
note: 修复 change 建议 fix-tile-category-enable-action
---

# 验收标准

## 1. 操作列展示（核心）

- [ ] **AC-001** 状态 = **启用** 的行：操作列含「编辑」「停用」；**不含**「删除」。
- [ ] **AC-002** 状态 = **停用** 且 **SKU = 0** 的行：操作列含「编辑」「**启用**」「删除」（删除可点击）。
- [ ] **AC-003** 状态 = **停用** 且 **SKU > 0** 的行：操作列含「编辑」「**启用**」；「删除」展示但置灰，hover/title 提示删除规则。
- [ ] **AC-004** 点击「启用」后：Toast 成功、列表与树刷新、该行状态变为启用，操作变为「编辑」「停用」。
- [ ] **AC-005** 点击「停用」后：行为与修复前一致，无回归。

## 2. 与品牌管理一致性

- [ ] **AC-006** 启停按钮与删除按钮 **独立渲染**（逻辑同 `BrandManagementPage`），不得再用 `deletable ? null : 启用` 模式。

## 3. 需求回归

- [ ] **AC-007** 满足父需求 `REQ-0005-tile-category-management` AC-015（编辑、启用/停用）、AC-016、AC-017。
- [ ] **AC-008** 弹窗、树、筛选、指标卡、分页无回归。

## 4. 自动化

- [ ] **AC-009** vitest：mock 停用+SKU=0 列表项，断言同时存在「启用」「删除」按钮。
- [ ] **AC-010** vitest：mock 启用行，断言存在「停用」且不存在「删除」。
- [ ] **AC-011** `cd src/web && npm run build` 通过。

## 5. 部署冒烟

- [ ] **AC-012** Docker 或本地：`/admin/tile-categories` 200；admin 登录后手工确认 AC-002 场景。

## 6. 文档与流程

- [ ] **AC-013** 修复经 OpenSpec `fix-tile-category-enable-action`（或等价 fix-*）进入开发并 archive。
- [ ] **AC-014** 本 BUG `trace.md` 修复后更新为 `done`。
