---
bug_id: BUG-0082-prod-miniapp-sku-video-slow-start
status: done
created_at: 2026-07-23 10:34:30
updated_at: 2026-07-23 23:13:08
severity_hint: high
environment: prod
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
captured_via: capture
classification_rationale: 已有小程序商品详情页视频播放能力在生产环境切换后出现长时间等待，属于既有能力/规范下的体验偏差，按 BUG 记录。
lifecycle_stage: plan
---

# 现象

小程序切换到生产环境后，进入商品详情页播放商品视频时，需要等待很久才能开始播放。

# 复现步骤

1. 将微信小程序环境切换为生产环境。
2. 打开包含商品视频的商品详情页。
3. 点击商品详情页轮播区域中的视频播放控件。
4. 观察从点击播放到视频实际开始播放的等待时间。

# 期望 vs 实际

- 期望：商品详情页视频点击后能较快出现首帧并开始播放；封面图应稳定展示，播放等待期间不应长时间黑屏或无反馈。
- 实际：生产环境下视频播放启动等待时间较长，影响店主或客户查看商品视频素材。

# 影响范围

- 微信小程序商品详情页：`src/miniapp/pages/tile-detail/`
- 后端受控媒体读取接口：`/media/{object_key}`
- 生产对象存储或 S3 兼容存储视频读取链路
- 商品 SKU 视频素材展示体验

# 初步线索

- 小程序详情页通过 `<video src="{{item.url}}">` 播放后端返回的媒体地址，并依赖 `poster="{{item.cover_url || ''}}"` 展示封面。
- 后端 `/media/{object_key}` 当前受控读取链路存在整文件读取后返回的实现线索，可能不利于视频 Range 分段播放和首帧快速加载。
- 生产环境链路还需排查 HTTPS 反代、对象存储/CDN、视频文件编码与文件大小。

# 建议验收或复现要点

- 记录至少 1 个生产 SKU、视频文件大小、格式、编码、视频时长、机型、网络类型和首播等待时间。
- 验证 `/media/{object_key}` 对视频请求是否支持 `Range`、`206 Partial Content`、`Accept-Ranges`、`Content-Range`。
- 验证视频封面 `cover_url` 是否存在且可快速加载。
- 验证同一视频在浏览器、对象存储直链或 CDN 链路下的首帧时间差异。

# 附件

暂无。待补充真机录屏、生产 URL 诊断信息或网络抓包摘要。
