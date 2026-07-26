---
bug_id: BUG-0082-prod-miniapp-sku-video-slow-start
status: done
created_at: 2026-07-23 10:45:58
updated_at: 2026-07-23 23:13:08
---

# Root Cause

## 直接原因

生产环境小程序商品详情页视频播放使用后端受控媒体地址 `/media/{object_key}`。当前后端媒体读取链路存在整文件读取后再返回普通响应的实现特征，视频播放请求无法确认具备 `Range` 分段读取能力。

当视频文件较大、生产对象存储链路较远、网络质量波动或视频首帧元数据不靠前时，播放器需要等待更多数据后才能起播，表现为点击播放后长时间等待。

## 根本原因

媒体播放链路当前更偏向图片/小文件读取模型，尚未针对视频播放建立完整的生产优化约束：

- 后端 `/media/{object_key}` 未明确提供视频 `Range` 请求、`206 Partial Content`、`Accept-Ranges`、`Content-Range` 等流式播放能力。
- 小程序 SKU 详情视频项当前缺少稳定 `cover_url` 数据，等待期间容易出现空白或黑屏感知。
- 视频素材上传后尚未形成强制压缩、首帧优化、转码或多清晰度播放策略。
- 生产链路中对象存储、反代、CDN 或缓存配置是否适配视频播放仍待验证。

## 触发条件

- 小程序处于生产环境。
- 商品详情页 SKU 配置了视频媒体。
- 视频体积较大、码率较高、首帧元数据位置不佳，或生产对象存储/CDN/反代链路响应较慢。
- 用户点击视频播放控件后，播放器需要等待足够数据才可展示首帧。

## 分类

- 类型：code / architecture / media-performance
- 影响层：微信小程序、后端媒体读取接口、对象存储读取链路
- 关联能力：`REQ-0044-miniapp-sku-detail-page`
- 关联缺陷：`BUG-0069-miniapp-sku-detail-carousel-video-not-playable`

## 待验证项

- 使用生产视频 URL 发起 `Range: bytes=0-1023` 请求，确认是否返回 `206 Partial Content`。
- 记录生产 SKU 视频文件大小、编码、时长和首帧耗时。
- 确认 SKU 详情接口返回的视频媒体项是否具备可用 `cover_url`。
- 对比后端 `/media/{object_key}` 与对象存储/CDN 直读链路的首帧耗时。
