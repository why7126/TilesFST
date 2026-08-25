---
req_id: REQ-0115-media-multi-variant-images
status: done
created_at: 2026-08-22 10:40:11
updated_at: 2026-08-22 18:25:13
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0012-object-storage-key-layout
captured_via: capture
classification_rationale: 上传后生成 thumbnail、display、original，多端按场景选择 URL，涉及新增媒体派生对象、接口字段、小程序加载策略和后续 CDN/对象存储直出治理，超出单个已交付页面缺陷修复范围，因此分类为需求增强。
---

# 一句话

媒体图片需要支持多规格展示图能力，上传后生成 `thumbnail / display / original`，并让小程序列表、详情展示和高清预览按场景使用不同 URL。

# 原始描述

标题：媒体图片支持多规格展示图能力

背景：小程序商品详情页冷加载性能分析显示，直接加载原图或大 PNG 会导致图片下载阶段耗时过长。当前需要将单次缺陷修复背后的通用能力沉淀为媒体多规格图机制。

影响范围：媒体上传、对象存储 key、后端媒体服务、商品接口、微信小程序列表与详情页、图片预览、后续 CDN 或对象存储直出策略。

建议验收或复现要点：

- 上传后生成 `thumbnail / display / original` 三类资源。
- API 返回 `thumbnail_url`、`display_url`、`original_url`。
- 小程序列表使用 `thumbnail`，详情普通展示使用 `display`，点击预览高清时使用 `original`。
- 详情页首屏外图片开启 lazy-load。
- 后续支持 CDN 或对象存储直出，降低后端 `/media` 代理压力。

# 背景与关联

- 关联 BUG：`BUG-0132-miniapp-sku-detail-large-image-cold-load`
- 关联历史问题：`BUG-0125-miniapp-sku-detail-media-original-load`、`BUG-0110-miniapp-card-banner-thumbnail-usage`
- 关联媒体治理：`REQ-0099-global-thumbnail-size-limit`、`REQ-0012-object-storage-key-layout`
- 业务价值：减少小程序和 Web 在列表、详情、预览场景中对原图的直接依赖，提升冷加载体验并降低媒体流量成本。

# 待澄清

- [ ] `display` 规格的目标宽高、质量、格式和体积上限。
- [ ] 透明 PNG 是否保留 PNG，非透明 PNG 是否统一转 JPG 或 WebP。
- [ ] 存量图片是否需要批量生成多规格资源，以及是否需要 dry-run / apply 维护入口。
- [ ] API 返回多规格 URL 是在商品详情接口中扩展字段，还是通过媒体服务统一适配。
- [ ] 生产环境是否同时纳入 CDN 或对象存储直出，还是先完成应用内多规格图选择。

# 建议验收要点

- [ ] 新上传图片可生成 `thumbnail`、`display`、`original` 三类资源，key 前缀、MIME、体积和对象存在性可追溯。
- [ ] 商品相关 API 能返回或派生 `thumbnail_url`、`display_url`、`original_url`，并明确缓存策略。
- [ ] 小程序列表页使用 `thumbnail_url`，商品详情页默认使用 `display_url`，图片预览使用 `original_url`。
- [ ] 详情页首屏外图片 lazy-load，不阻塞首屏基础浏览。
- [ ] 存量媒体迁移或重生成具备 dry-run、apply、幂等性、失败统计和脱敏输出。
- [ ] 若涉及 OpenAPI / Orval / DB / 对象存储字段变化，相关文档、Schema 和测试同步更新。

# 探索结论

`/explore` 综合多张微信小程序开发者工具 Network 截图后判断：商品详情页冷加载存在大图资源导致的明确性能偏差，同时也暴露出媒体多规格图能力缺口。当前 capture 拆分为 BUG-0132 处理已交付详情页性能偏差，本 REQ 负责后续通用能力建设。
