---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
title: SKU 商品详情页轮播图视频不能显示和播放
status: done
created_at: 2026-07-19 23:36:55
updated_at: 2026-07-20 22:47:36
severity_hint: high
environment: 微信小程序
source: 用户反馈
source_command: /capture
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug:
captured_via: capture
classification_rationale: SKU 商品详情页属于已交付小程序能力，轮播图中的视频媒体不能显示和播放是既有详情页媒体展示与播放行为偏差，因此归类为 BUG。
---

# 现象

SKU 商品详情页轮播图中配置的视频不能正常显示，也不能播放。用户在详情页预期可通过轮播区域查看商品图片和视频素材，但视频项不可见或无法播放。

# 复现步骤

1. 使用微信开发者工具或真机打开小程序。
2. 进入任意包含视频素材的 SKU 商品详情页。
3. 查看详情页顶部轮播图中的媒体项。
4. 切换到视频媒体项并尝试播放。

# 期望 vs 实际

期望：SKU 商品详情页轮播图能正确展示视频封面或视频播放器；用户切换到视频项后可以正常播放、暂停，并且图片轮播项不受影响。

实际：轮播图中的视频不能显示和播放，导致商品详情页视频素材不可用，影响店主端商品展示完整性。

# 附件

- 暂无截图或日志；后续 `/bug-explore` 阶段补充具体 SKU、视频 URL / media key、微信开发者工具或真机表现截图。
