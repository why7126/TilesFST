---
req_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
status: done
created_at: 2026-08-22 20:32:30
updated_at: 2026-08-22 21:35:42
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0115-media-multi-variant-images
---

# 一句话

统一沉淀 Web 与微信小程序对 `thumbnail`、`display`、`original` 三类图片规格的消费矩阵，并收敛各页面、组件和对象类型的使用规则。

# 原始描述

记录“统一 Web 与小程序图片三规格消费矩阵”。

# 背景与关联

- 关联需求：`REQ-0115-media-multi-variant-images`
- 现有规范：`openspec/specs/media-multi-variant-images/spec.md` 已定义 `thumbnail`、`display`、`original` 三类图片规格的通用语义。
- 当前缺口：Web 端与微信小程序端的页面级消费规则分散在多个 spec、README、组件实现和历史验收口径中，缺少一份统一矩阵说明各端、各页面、各图对象在列表、详情展示、预览和下载等场景下应使用的图片规格。
- 涉及端与模块：Web 管理端、店主 Web 展示端、微信小程序、媒体上传、对象存储、多规格图片 API、Orval 类型、媒体验收模板。
- 业务价值：减少缩略图、展示图和原图混用导致的加载性能、清晰度、预览体验和验收口径不一致问题，提升媒体类需求、BUG 和发布验收的可复用性。

# 待澄清

- [ ] 矩阵是否只沉淀规范和验收口径，还是同步修正 Web 与小程序现有不一致实现。
- [ ] 店主 Web 展示端当前是否需要纳入真实页面验收，还是先作为规范预留消费端。
- [ ] Banner、品牌 Logo、用户头像、品牌证书是否全部纳入同一矩阵，还是按商品、品牌、证书、头像分对象拆分。
- [ ] 缺少目标规格时是否统一使用安全占位，还是允许按场景回退到下一规格。
- [ ] 是否要求 API 文档明确每个 URL 字段的 fallback、缓存、签名和过期边界。

# 建议验收要点

- [ ] 形成 Web 管理端、店主 Web 展示端、微信小程序的图片三规格消费矩阵，覆盖列表/卡片、表单小预览、详情普通展示、图册浏览、高清预览、下载和分享场景。
- [ ] 明确商品、Banner、品牌 Logo、品牌证书、用户头像和视频封面等图对象的推荐规格与 fallback 顺序。
- [ ] 明确 `thumbnail` 用于列表、卡片和轻量预览；`display` 用于详情普通展示和图册浏览；`original` 用于高清预览、下载或保真场景。
- [ ] 识别并记录当前 Web 与小程序实现中不一致的消费点，例如 Banner 表单、品牌 Logo 回显、证书详情展示、头像展示等，并给出是否纳入本需求修正的范围判断。
- [ ] 媒体类验收模板或测试 helper 能引用该矩阵，避免将原图 fallback 写作缩略图或展示图性能通过。

# 探索结论

（/req-explore 后人工确认写入）
