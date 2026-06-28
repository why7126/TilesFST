---
bug_id: BUG-0040-banner-modal-width-too-narrow
status: pending_review
created_at: 2026-06-28 17:43:07
updated_at: 2026-06-28 17:43:07
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断 Banner 新增/编辑功能（BUG-0033 已修滚动与备注宽度）：

1. 640px 弹窗内可完成全部字段填写与保存。
2. 将浏览器窗口最大化或提高视口高度，可改善纵向空间（横向仍 640px）。
3. 使用浏览器缩放（Zoom out）可间接增加可视横向空间（非正式方案）。

## 2. 验收规避

正式修复前：

- Banner 弹窗宽度 **按现行 spec 640px 验收**（与 modal HTML/PNG 一致）。
- 与 SKU 弹窗宽度差异 **暂不作为 REQ-0016 阻塞项**（待 BUG-0040 评审与 spec delta）。

## 3. 运营规避

字段较多时（如 SKU 详情跳转）：

1. 全屏或拉大浏览器窗口高度，利用 modal-body 滚动查看全部字段。
2. 分步填写：先完成基础字段，滚动至底部保存。

## 4. 风险说明

规避不能消除：

- 横向空间偏紧、与 SKU 弹窗体验不一致。
- 图片上传区、双列 grid 在 640px 下仍显拥挤。

加宽至 880px 须产品确认偏离 modal 原型，并经 `/bug-review` + `/bug-opsx` 更新 OpenSpec。可与 BUG-0039 合并 fix change。
