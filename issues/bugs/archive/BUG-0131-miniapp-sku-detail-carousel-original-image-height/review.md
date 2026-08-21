---
bug_id: BUG-0131-miniapp-sku-detail-carousel-original-image-height
review_status: approved
decision: approve
created_at: 2026-08-21 13:11:55
updated_at: 2026-08-21 13:11:55
reviewed_at: 2026-08-21 13:11:55
reviewer: user
severity: medium
hotfix_required: false
---

# 缺陷评审

## 评审结论

批准修复。

`BUG-0131` 已完成 capture、正式 bug 文档、根因分析、临时规避和验收标准补齐。用户已明确要求按 `/bug-review BUG-0131 --approve` 推进。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户截图、代码定位和现行规格能共同解释详情页首屏 `.thumb` 放大后清晰度不足，以及 `680rpx` 固定高度不满足详情大图预期的问题。 |
| 严重等级合理 | 通过 | 维持 `medium`；问题影响商品详情关键视觉体验，但不阻断页面浏览、收藏或分享。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖详情首屏高清展示、预览原图、列表保留 `.thumb`、轮播高度、首屏商品信息露出和媒体四联验收。 |
| 是否需 hotfix 路径 | 不需要 | 该问题属于体验偏差与策略回归，适合纳入 Sprint 常规修复；若后续真机证据显示大面积严重模糊，可重新评估优先级。 |

## 批准范围

- 商品详情页轮播首屏展示图清晰度修复。
- 商品详情页轮播高度和首屏商品信息露出修复。
- 后端 SKU 详情媒体字段语义、小程序绑定、正式规格和测试断言同步。
- 商品列表、商品卡片、推荐位和 Banner 的 `.thumb` 使用策略不纳入回退范围。

## 后续建议

1. 先纳入 Sprint 正式范围。
2. 再创建对应 `fix-*` OpenSpec Change。
3. 实现阶段必须补充媒体四联证据，尤其是小程序 render evidence。
