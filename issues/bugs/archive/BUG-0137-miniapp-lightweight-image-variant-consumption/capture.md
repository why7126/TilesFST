---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
status: done
created_at: 2026-08-24 14:54:45
updated_at: 2026-08-25 09:43:46
severity_hint: high
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0126-miniapp-brand-media-slow-load
lifecycle_stage: plan
captured_via: capture
classification_rationale: 小程序 Banner、品牌 Logo、分享图均属于已交付媒体多规格图片能力的消费侧场景；用户指出仍存在原图 fallback 或缺少轻量字段，偏离 thumb/display/original 多规格规范，因此分类为 BUG。
---

# 现象

小程序仍有 Banner、品牌 Logo、分享图三类图片消费未完全符合 `thumb` / `display` / `original` 多规格规范：Banner schema 只有 `image_url`，品牌 Logo 仍允许 `original` fallback，分享图可能退到 `preview` / `url`。

# 复现步骤

1. 准备包含 Banner、品牌 Logo、分享图的测试数据，并确保后端媒体记录存在多规格字段。
2. 打开小程序首页 Banner、品牌相关卡片或详情、分享图生成或分享入口。
3. 检查接口响应 schema 与小程序渲染使用的图片字段。
4. 在小程序开发者工具 Network 面板观察普通展示路径是否请求原图、`preview` 或旧 `url` 字段。

# 期望 vs 实际

- 期望：普通展示场景统一消费轻量字段，优先使用 `thumbnail_url` / `thumb_url` 或 `display_url`，仅在明确预览、下载、原图查看等用户意图下使用 `original`。
- 实际：Banner schema 只有 `image_url`，品牌 Logo 仍允许退到原图，分享图可能退到 `preview` / `url`，导致普通展示仍有冷加载原图或旧字段的风险。

# 影响范围

- 微信小程序首页 Banner 图片展示。
- 微信小程序品牌 Logo 展示链路。
- 微信小程序分享图生成与渲染链路。
- 移动端弱网加载性能、对象存储流量、媒体字段契约一致性。
- `REQ-0115-media-multi-variant-images` 的小程序端验收证据完整性。

# 初步线索

- Banner 接口或 schema 可能缺少 `thumbnail_url` / `display_url` 等轻量字段。
- 品牌 Logo 组件或字段组装逻辑可能保留 `original` fallback。
- 分享图字段优先级可能仍兼容旧 `preview` / `url`，未明确阻断普通展示场景的原图退路。
- 需要补充小程序 Network 和 render evidence，证明普通展示不再请求原图。

# 建议验收或复现要点

- [ ] Banner schema 暴露并消费符合规范的轻量图字段，普通展示不只依赖 `image_url`。
- [ ] 品牌 Logo 普通展示禁止 fallback 到 `original`，缺轻量图时使用占位或明确降级状态。
- [ ] 分享图普通展示禁止退到 `preview` / `url` 原图路径，字段优先级与消费矩阵一致。
- [ ] 小程序 Network evidence 显示首页 Banner、品牌 Logo、分享图普通展示均未冷加载原图。
- [ ] 小程序 render evidence 显示上述三类图片在有轻量图、缺轻量图、字段缺失时均表现稳定。

# 来源

- 来源命令：`/capture`
- 来源描述：小程序 Banner、品牌 Logo、分享图三类图片消费未完全符合 `thumb` / `display` / `original` 多规格规范，需要统一轻量图字段、禁止普通展示冷加载原图，并补 miniapp Network/render evidence。

# 拆分说明

本次不拆分为三条 BUG。Banner、品牌 Logo、分享图都属于同一媒体多规格消费矩阵在小程序端的字段与 fallback 偏差，可由同一修复闭环统一处理字段契约、渲染优先级和 Network/render evidence。

# 附件

- 暂无。
