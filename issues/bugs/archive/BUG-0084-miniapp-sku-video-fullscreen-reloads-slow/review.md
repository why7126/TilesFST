---
bug_id: BUG-0084-miniapp-sku-video-fullscreen-reloads-slow
status: done
created_at: 2026-07-24 20:28:44
updated_at: 2026-07-24 21:13:29
reviewed_at: 2026-07-24 20:28:44
review_result: approved
reviewer:
---

# BUG Review

## 评审结论

确认修复，状态批准为 `approved`。

该缺陷描述清晰：小程序 SKU 详情页内嵌视频已可播放，但点击全屏入口后进入全屏态重新长时间加载，影响商品视频连续浏览体验。

## 评审清单

- [x] 可复现或根因充分
- [x] 严重等级合理
- [x] 回归验收明确
- [x] 已判断是否需要 hotfix 路径

## 严重等级确认

严重等级维持 `medium`。

理由：

- 内嵌视频播放主路径可用，未完全阻断 SKU 详情浏览。
- 全屏播放是客户查看商品视频的重要体验入口，长时间重新加载会明显打断浏览。
- 该问题与生产视频首播慢相关，但现象更聚焦于“内嵌态已播放成功后，切换全屏仍重新加载”。

## Hotfix 判断

暂不按 hotfix 处理。

理由：

- 当前缺陷影响体验连续性，但不阻断商品详情页基础浏览和内嵌视频播放。
- 后续可通过 `/bug-opsx` 创建修复 Change，并在 Sprint 中安排实现和真机验收。

## 后续动作

- 可执行 `/bug-opsx BUG-0084-miniapp-sku-video-fullscreen-reloads-slow` 创建 OpenSpec fix Change。
- 修复前必须保留小程序媒体安全 URL、内嵌播放、图片预览、收藏分享和页面隐藏暂停能力不回归。
