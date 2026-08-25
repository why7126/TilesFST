---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
title: 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段
severity: high
status: done
owner: null
discovered_at: 2026-08-24 14:54:45
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_change: fix-miniapp-lightweight-image-variant-consumption
created_at: 2026-08-24 14:58:47
updated_at: 2026-08-25 14:53:29
---

# 现象

小程序 Banner、品牌 Logo、分享图三类图片消费仍未完全符合 `thumb` / `display` / `original` 多规格规范：

- Banner schema 只有 `image_url`，缺少可明确表达轻量展示图的字段。
- 品牌 Logo 普通展示仍允许 fallback 到 `original`。
- 分享图可能退到 `preview` / `url`，存在绕过统一轻量图字段的风险。

这些路径会让普通展示场景继续冷加载原图或旧字段图片，偏离媒体多规格图片能力中“普通展示使用轻量图、原图仅在明确意图下加载”的边界。

# 复现步骤

1. 准备包含 Banner、品牌 Logo、分享图的测试数据，并确保对应媒体对象存在 `thumb`、`display`、`original` 多规格字段。
2. 打开小程序首页，观察 Banner 渲染使用的图片字段。
3. 进入品牌列表、品牌卡片或品牌详情相关入口，观察品牌 Logo 渲染使用的图片字段。
4. 触发分享图展示或生成链路，观察分享图字段优先级。
5. 在微信开发者工具 Network 面板检查上述普通展示路径是否请求原图、`preview` 或旧 `url` 字段。

# 期望结果

- Banner schema 与小程序消费侧能提供 `display_url`、`thumbnail_url` 或等价轻量展示字段；小程序 Banner 轮播图作为首屏大图展示位，普通展示优先使用 `display_url`，缺失或不可读时降级到 `thumbnail_url`。
- 品牌 Logo 普通展示禁止 fallback 到 `original`；缺少轻量字段时应使用占位图或明确降级状态。
- 分享图普通展示禁止退到 `preview` / `url` 原图路径；字段优先级应与媒体多规格消费矩阵一致。
- 只有明确的预览、下载、原图查看等用户意图才能加载 `original`。
- 小程序 Network/render evidence 能证明 Banner、品牌 Logo、分享图普通展示均未冷加载原图。

# 实际结果

- Banner schema 只有 `image_url`，无法明确约束普通展示使用轻量图。
- 品牌 Logo 仍可能通过 fallback 加载 `original`。
- 分享图可能继续兼容 `preview` / `url`，导致普通展示绕过轻量图字段。
- 当前缺少小程序 Network/render evidence 来证明三类图片消费已符合多规格规范。

# 影响范围

- 微信小程序首页 Banner 图片展示。
- 微信小程序品牌 Logo 展示链路，包括品牌列表、品牌卡片、品牌详情和商品详情品牌卡。
- 微信小程序分享图生成与渲染链路。
- 移动端弱网首屏加载、对象存储流量、图片缓存命中和媒体字段契约一致性。
- `REQ-0115-media-multi-variant-images` 的小程序端验收闭环。

# 严重等级说明

严重等级为 high。

原因：

- 问题影响小程序多处公开展示入口，触达面较广。
- 普通展示冷加载原图会直接影响弱网体验和首屏渲染稳定性。
- 原图 fallback 与多规格媒体治理目标冲突，会削弱后续 Network evidence 和渲染验收的可信度。
- 该问题关联已交付的媒体多规格图片能力，需要在进入后续 Sprint / OpenSpec 修复前补齐字段契约与证据要求。
openspec_changes:
  - change_id: fix-miniapp-lightweight-image-variant-consumption
    type: fix
    status: archived
