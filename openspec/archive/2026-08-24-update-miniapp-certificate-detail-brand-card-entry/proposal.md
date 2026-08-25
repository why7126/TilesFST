# 小程序证书详情页品牌入口复用 brand-card

## 背景

证书详情页所属品牌入口需要与小程序其他品牌入口保持一致。若证书详情页继续维护页面私有品牌入口，品牌 Logo 字段、缩略图消费、跳转参数和埋点事件名容易与 `brand-card` 组件分叉，导致性能验收和行为分析口径不一致。

本 Change 将 REQ-0121 落为 OpenSpec 变更：证书详情页复用 `brand-card`，证书详情 `brand` 数据补齐 `brand_logo_thumbnail_url`，品牌入口点击统一上报 `brand_card_click`。

## 变更内容

- 小程序证书详情页所属品牌入口复用既有 `brand-card` 组件，不保留页面私有品牌入口结构。
- 证书详情 `brand` 数据提供 `brand_logo_thumbnail_url`，品牌卡普通展示优先消费缩略图，不 fallback 到品牌 Logo 原图。
- 品牌入口跳转复用 `brand-card` 既有策略，来源上下文标识证书详情页。
- `brand-card` 点击事件名统一为 `brand_card_click`，证书详情页传入 `certificateId` 等可用上下文。
- 验收补齐小程序媒体四联证据、Network evidence、UI 视口截图或等价摘要、既有 `brand-card` 调用方回归。

## 能力范围

### 新增能力

无。

### 修改能力

- `miniapp-brand-card-component`：补充证书详情页接入 `brand-card` 的数据、跳转、UI 与回归要求。
- `media-multi-variant-images`：补充证书详情 `brand` 数据中的品牌 Logo 缩略图字段和小图消费边界。
- `product-usage-logging`：补充 `brand_card_click` 在证书详情页的上下文参数与非阻断要求。

## 影响范围

- 后端 API / Schema：若当前证书详情 `brand` 数据缺少 `brand_logo_thumbnail_url`，需要补齐响应字段，并同步 OpenAPI、Orval 或小程序服务层类型。
- 微信小程序：证书详情页需要复用 `brand-card`，传入品牌缩略图、来源和证书上下文；`brand-card` 需要保持既有调用方兼容。
- 媒体与对象存储：不新增派生图能力，只消费既有缩略图 URL；验收不得将原图 fallback 写作轻量图通过。
- 行为日志：事件名统一为 `brand_card_click`，埋点失败不得阻断跳转。
- 数据库：不新增表或字段，优先复用既有品牌 Logo 缩略图数据来源。
- Web / 管理端：不涉及 UI 或业务能力调整。

