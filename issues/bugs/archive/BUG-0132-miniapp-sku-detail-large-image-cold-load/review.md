---
bug_id: BUG-0132-miniapp-sku-detail-large-image-cold-load
review_status: approved
decision: approve
created_at: 2026-08-22 13:38:16
updated_at: 2026-08-22 13:38:16
reviewed_at: 2026-08-22 13:38:16
reviewer: user
severity: high
hotfix_required: false
---

# 缺陷评审

## 评审结论

批准修复。

`BUG-0132` 已完成 capture、正式 bug 文档、根因分析、临时规避和验收标准补齐。该问题有多组微信小程序开发者工具 Network 截图作为复现证据，能确认商品详情页冷加载阶段存在大图资源导致图片下载耗时过长。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户提供的多组 Network 证据显示 1MB 以上 JPEG、1.5MB PNG、3.6MB PNG 等图片冷加载耗时达到 5s-11s；根因状态保持 `probable`，并已列出后续实现前补证步骤。 |
| 严重等级合理 | 通过 | 维持 `high`；问题影响小程序商品详情页核心浏览体验，尤其影响首次访问、弱网和多图商品场景。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖大图体积阈值、PNG 展示版替代、原图仅预览、首屏外图片 lazy-load、Network 证据和媒体四联验收。 |
| 是否需 hotfix 路径 | 不需要 | 当前问题影响体验但不阻断商品详情接口返回或页面基础访问，适合纳入 Sprint 常规修复；若生产真机证据显示大面积不可用，可重新评估 hotfix。 |

## 批准范围

- 限制商品详情页冷加载普通展示路径直接请求 1MB 以上原图。
- 优先处理 PNG 大图展示版替代，非透明 PNG 可转为 JPG 或 WebP。
- 商品详情页首屏关键图片与普通详情展示图按验收阈值控制体积。
- 高清原图仅在点击预览或明确查看高清时加载。
- 首屏外详情图片 lazy-load。
- 修复阶段必须补充媒体四联验收和小程序 Network evidence。

## 范围外事项

- 通用 `thumbnail / display / original` 多规格媒体能力作为 `REQ-0115-media-multi-variant-images` 后续推进。
- CDN 或对象存储直出策略作为媒体能力增强或部署优化，不纳入本 BUG 的最小修复范围。

## 后续建议

1. 先纳入 Sprint 正式范围。
2. 再创建对应 `fix-*` OpenSpec Change。
3. 实现阶段补齐慢请求 URL、object key、MIME、大小、端侧绑定和修复前后 Network 对比证据。
