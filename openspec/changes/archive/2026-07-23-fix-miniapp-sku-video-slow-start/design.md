## Context

BUG-0082 反馈生产环境小程序商品详情页视频播放启动很慢。当前小程序详情页将详情接口返回的媒体 URL 传给 `<video>`，媒体 URL 最终指向后端受控 `/media/{object_key}`。现有后端媒体读取实现存在整对象读取后返回普通响应的风险；视频播放链路未在规格中明确 Range/206、封面兜底和首帧体验验收。

## Goals / Non-Goals

**Goals:**

- 确保视频媒体通过受控 `/media/{object_key}` 读取时支持播放器需要的 Range 分段请求。
- 改善小程序 SKU 详情页视频点击后的等待体验，至少提供稳定封面或兜底图。
- 补充后端 Range/206 测试、小程序媒体静态测试和生产等价验收清单。
- 保持对象存储单桶、标准前缀和后端授权读取边界。

**Non-Goals:**

- 不实现视频转码、压缩、多清晰度或 HLS/DASH。
- 不引入前端直传、STS 临时凭证或小程序直连对象存储写入。
- 不要求本 Change 新增数据库字段；如实现选择持久化封面对象，需要在 apply 阶段同步 DB 文档和测试。
- 不改变 SKU 详情页路由、收藏、分享、品牌入口和推荐能力。

## Bug Analysis Report

- BUG：`BUG-0082-prod-miniapp-sku-video-slow-start`
- 现象：生产环境小程序 SKU 详情页视频点击后等待较久才开始播放。
- 影响：微信小程序 SKU 详情核心展示链路、后端媒体读取链路、生产对象存储读取链路。
- 严重等级：high。
- 关联需求：`REQ-0044-miniapp-sku-detail-page`。
- 关联历史缺陷：`BUG-0069-miniapp-sku-detail-carousel-video-not-playable`。

## Root Cause

直接原因是视频播放使用后端受控媒体地址，但媒体读取能力更偏向图片/小文件的一次性读取模型，规格未要求视频 Range 分段响应。生产视频体积、码率、首帧元数据位置、对象存储链路延迟和网络波动会共同放大慢启动。

根本原因是媒体播放链路缺少视频专项约束：

- `/media/{object_key}` 未明确支持 `Range`、`206 Partial Content`、`Accept-Ranges` 和 `Content-Range`。
- SKU 视频媒体项缺少稳定封面 URL 或兜底策略。
- 生产验收缺少首帧耗时、视频大小/编码/时长、机型与网络证据。

## Decisions

1. 优先修复受控读取链路，而不是让小程序直连对象存储。

   项目安全规则要求上传和读取经过后端鉴权或受控公开策略。Range/206 可以在后端受控路径内改善播放器起播，同时不暴露 bucket、endpoint、密钥或 raw object URL。

2. 视频 Range 支持应限定在合法 object_key 和视频媒体类型上。

   非 Range 请求仍可返回完整内容；非法 Range 应返回可诊断状态；不存在对象仍返回媒体不存在错误；所有路径仍执行 object_key 校验和 legacy key 兼容。

3. 小程序视频封面应有兜底。

   若接口提供 `cover_url`，小程序优先使用；否则可使用商品主图或安全兜底图，避免播放前空白或黑屏。实现不得展示原始 object key。

4. 转码、多清晰度和 CDN 播放是后续增强。

   本修复先解决已有能力慢启动的基础链路问题；更完整的视频资产优化可以通过独立需求或后续 Change 评估。

## Testing Strategy

- 后端测试：
  - `GET /media/{object_key}` 对视频对象支持 `Range: bytes=0-1023`。
  - 响应为 `206 Partial Content`，包含 `Accept-Ranges: bytes`、`Content-Range`、正确 `Content-Length` 和视频 `Content-Type`。
  - 非 Range 请求、非法 Range、对象不存在、非法 object_key 不回归。
- 小程序测试：
  - SKU 详情页视频项使用接口返回的安全 URL。
  - 视频 `poster` 使用 `cover_url`、商品主图或安全兜底图，不长期为空。
  - 播放、暂停、页面隐藏暂停、图片预览等既有行为不回归。
- 生产等价验收：
  - 至少记录一个生产 SKU 的视频文件大小、格式、编码、时长、机型、网络类型和点击到首帧耗时。
  - 验证实际 `/media/{object_key}` Range 响应头。

## Risks / Trade-offs

- 后端代理 Range 会增加对象存储读取实现复杂度，需要小心连接关闭和异常映射。
- 若对象存储 SDK 或代理层不支持高效范围读取，仍可能需要 CDN 或签名播放 URL 作为后续增强。
- 如果补视频封面需要新增持久化字段，会扩大 API/DB/Orval 同步范围；实现时应优先评估是否可使用现有主图兜底。
