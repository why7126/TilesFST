---
req_id: REQ-0120-webp-derived-image-variants
status: done
created_at: 2026-08-22 21:32:10
updated_at: 2026-08-25 14:38:06
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0115-media-multi-variant-images
---

# 一句话

图片上传后应生成 WebP 格式的展示图和缩略图，原图保留上传格式，Web 与小程序优先消费 WebP 派生图以提升图片密集页面加载性能。

# 原始描述

图片上传后生成 WebP 展示图和缩略图，原图保留上传格式，前端和小程序优先使用 WebP 派生图。

已确认采用推荐策略：原图保留原格式，派生图统一 WebP。

# 背景与关联

- 父需求：`REQ-0115-media-multi-variant-images`
- 涉及端与模块：后端媒体上传、对象存储、Web 管理端、店主 Web、小程序图片展示
- 业务价值：降低 SKU 列表、详情图、品牌 Logo、Banner、证书图片等图片密集页面的传输体积，改善移动端和小程序加载体验
- 技术取舍：保留原图用于审计、素材复用和特殊格式兼容；将真实用户访问链路优先切到 WebP 派生图

# 待澄清

- [ ] WebP 派生图覆盖范围：头像、品牌 Logo、Banner、SKU 图片、证书图片是否全部纳入首期
- [ ] SVG、GIF、HEIC、TIFF、BMP 等非 JPEG/PNG/WebP 图片是否继续允许上传，以及是否生成派生图
- [ ] 历史已上传图片是否需要批量补生成 WebP 派生图，还是仅新上传生效
- [ ] 前端和小程序 fallback 顺序是否统一为 `thumbnail/display WebP → original`
- [ ] 是否需要在管理端设置页暴露 WebP 质量、尺寸或体积目标配置

# 建议验收要点

- [ ] 上传 JPEG、PNG、WebP 图片后，原图对象 Key 与 MIME 保持上传格式不变。
- [ ] 上传后自动生成同目录 WebP 展示图与 WebP 缩略图，返回或可解析 `display_url`、`thumbnail_url`。
- [ ] Web 管理端、店主 Web 与小程序在列表、详情、预览等图片展示场景优先使用 WebP 派生图，并在缺失时降级到原图。
- [ ] SVG、GIF、PDF 等不适合转 WebP 的资源有明确跳过、拒绝或降级规则。
- [ ] 对象存储验收覆盖 key、object、URL、render，以及派生图 MIME、扩展名、大小和缓存策略。
- [ ] 若涉及 API 响应字段或 OpenAPI 契约，必须同步 Orval 与前端调用。

# 探索结论

`/explore` 已确认 WebP 通常有助于提升图片加载性能，但不建议替换原图。推荐策略为原图保留上传格式，展示图和缩略图统一生成 WebP，端侧优先消费派生图并保留原图 fallback。
