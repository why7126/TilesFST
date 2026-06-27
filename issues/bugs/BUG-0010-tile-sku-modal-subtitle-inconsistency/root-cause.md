---
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
status: pending_review
created_at: 2026-06-27 12:02:52
updated_at: 2026-06-27 12:02:52
root_cause_type: design
---

# 根因分析

## 1. 直接原因

- SKU 弹窗副标题使用 `modal-subtitle`，项目 CSS 中无对应规则。
- 品牌弹窗使用局部类 `brand-modal-desc`，未抽取为管理端共享 modal 描述样式。
- 通用 `.modal-head` 固定 `height: 64px`，多行标题区（含副标题）排版不一致。

## 2. 根本原因

SKU 管理页 CSS Port 时未复用品牌弹窗已验收的副标题模式；管理端弹窗组件缺少共享 `.modal-desc` token，导致新增页面各自定义或遗漏样式。

## 3. 触发条件

并排打开 SKU 与品牌新增弹窗即可稳定复现。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 修复面 | 共享 `.modal-desc` + SKU/品牌弹窗头部布局 |

## 5. 修复方案（已实施）

1. 在 `user-management.css` 新增共享 `.modal-desc`。
2. SKU / 品牌弹窗均改用 `modal-desc`；移除 `brand-modal-desc`。
3. SKU / 品牌 modal-head 改为 `min-height: 64px`、自适应 padding。
4. SKU 副标题文案对齐品牌句式，保留 AC-023 语义。
