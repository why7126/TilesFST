---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-24 15:02:14
updated_at: 2026-08-25 14:53:29
related_change: update-miniapp-certificate-detail-brand-card-entry
---

# REQ-0121 小程序证书详情页品牌入口复用 brand-card

## 1. 需求背景

小程序证书详情页已经承载单张证书的公开信息、媒体展示、品牌关联和分享入口。所属品牌入口是用户从证书资质继续进入品牌内容的重要路径，但如果证书详情页自行实现品牌区域，就容易与商品详情页、品牌详情页等页面的品牌卡片在 Logo 规格、点击区域、跳转参数、埋点事件和异常状态上出现口径分叉。

本需求要求证书详情页所属品牌入口复用小程序既有 `brand-card` 组件，并为证书详情 `brand` 数据补齐 `brand_logo_thumbnail_url`。品牌入口点击埋点统一使用 `brand_card_click`，以保证品牌入口展示、跳转、埋点和图片轻量化策略在小程序内保持一致。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 装修客户 | 在查看证书时快速识别所属品牌，并进入品牌主页继续了解品牌资质和产品。 |
| 设计师 | 从证书详情顺畅跳转到品牌内容，便于向客户说明品牌背书。 |
| 门店导购 | 在讲解证书时复用一致的品牌入口和跳转路径，减少页面差异造成的操作困惑。 |
| 产品与测试人员 | 用统一组件、字段和埋点口径验收品牌入口，不逐页维护差异化规则。 |

## 3. 范围

### 3.1 包含

- 小程序证书详情页所属品牌入口复用 `brand-card` 组件。
- 证书详情 `brand` 数据补齐品牌 Logo 缩略图字段 `brand_logo_thumbnail_url`。
- `brand-card` 在证书详情页优先消费 `brand_logo_thumbnail_url`，遵守小程序品牌 Logo 轻量图策略。
- 品牌入口点击跳转复用 `brand-card` 既有品牌详情跳转能力或既定品牌入口路径。
- 品牌入口点击埋点事件名统一为 `brand_card_click`。
- 证书详情页、商品详情页和其他使用 `brand-card` 的入口在展示、跳转和埋点参数上保持可比对的统一口径。
- 品牌 Logo 缺失、缩略图缺失、品牌不可跳转等异常状态按 `brand-card` 统一策略处理。

### 3.2 不包含

- 新增或重做小程序证书详情页整体信息架构、顶部媒体区、分享能力或证书字段展示。
- 新增品牌主页、品牌商品列表、证书列表或商品详情页的新业务能力。
- 管理端品牌、证书或媒体上传维护能力调整。
- 新增数据库表或改变品牌证书主数据模型；如实现阶段需要补充字段映射，应在 OpenSpec Change 中明确 API/Schema 同步范围。
- 新建 Web 端品牌卡片组件或跨端组件库。
- 新增图片派生能力、历史图片批量生成能力、对象存储 Bucket/Key 策略或 CDN 策略。
- 新增除 `brand_card_click` 之外的埋点体系改造。

## 4. 功能要求

### FR-001 证书详情页品牌入口必须复用 brand-card

- 证书详情页所属品牌入口 MUST 复用小程序 `brand-card` 组件，不再维护页面私有的品牌入口结构。
- 页面容器负责加载证书详情数据、组装 `brand-card` 所需品牌数据和传入来源上下文。
- `brand-card` 组件负责品牌 Logo、品牌名称、入口提示、点击态、不可用态和点击事件处理。
- 复用后，证书详情页品牌入口的点击区域、基础布局和触控反馈 SHOULD 与商品详情等既有品牌卡片场景保持一致。

### FR-002 证书详情 brand 数据必须补齐缩略图字段

- 证书详情接口或页面数据适配层 MUST 在 `brand` 数据中提供 `brand_logo_thumbnail_url`。
- `brand_logo_thumbnail_url` 表示适合品牌卡片、列表入口和小尺寸 Logo 区域使用的轻量缩略图 URL。
- 当后端已有品牌 Logo 缩略图字段时，证书详情响应 SHOULD 直接透出同名字段，避免小程序端自行拼接或推断媒体 URL。
- API 响应不得暴露对象存储原始 Key、本机路径、后台备注或内部审计字段。
- 若品牌无 Logo 或缩略图不可用，应返回空值并由 `brand-card` 使用统一占位或不可用策略，不得让页面 fallback 到原图扩大小程序冷加载资源体积。

### FR-003 图片轻量化消费策略必须一致

- 证书详情页 `brand-card` MUST 优先使用 `brand_logo_thumbnail_url` 展示品牌 Logo。
- 品牌 Logo 小尺寸入口不应直接消费原图 URL。
- 缩略图缺失、生成失败或加载失败时，组件 MUST 使用统一占位、品牌首字或既有安全兜底，不展示破图。
- 图片异常不得影响品牌名称、入口提示和证书详情主体内容浏览。
- 该策略应与小程序图片三规格消费矩阵一致：品牌卡片和小 Logo 场景主消费规格为 `thumbnail`。

### FR-004 品牌入口跳转必须复用统一策略

- 点击证书详情页品牌入口后，MUST 跳转到对应品牌详情页或既定品牌入口。
- 跳转参数 MUST 至少包含稳定品牌标识，如 `brandId` 或现有品牌路由所需参数。
- 页面来源 SHOULD 标记为证书详情页，例如 `sourcePage=certificate_detail` 或等价来源上下文。
- 品牌数据缺失、品牌不可公开或入口不可用时，MUST 阻止无效跳转，并按 `brand-card` 统一不可用提示或禁用态处理。
- 证书详情页不得绕过 `brand-card` 单独实现品牌跳转逻辑。

### FR-005 brand-card 点击埋点必须统一为 brand_card_click

- 所有 `brand-card` 点击行为的事件名 MUST 统一为 `brand_card_click`。
- 证书详情页所属品牌入口不得使用页面私有事件名或旧的品牌点击事件名。
- 埋点参数 SHOULD 包含 `brandId`、`brandName`、`sourcePage`、`sourceModule`、`certificateId`、`requestId` 等可用上下文。
- 对商品详情等其他使用 `brand-card` 的场景，若已存在不一致的点击事件名，后续实现应统一收敛到 `brand_card_click` 或在 Change 中明确兼容期。
- 埋点上报失败不得阻断品牌跳转。

### FR-006 复用回归必须覆盖主要 brand-card 场景

- 实现阶段 MUST 回归证书详情页、商品详情页和其他当前接入 `brand-card` 的页面，确认展示、跳转和埋点口径没有分叉。
- 证书详情页品牌入口缺失品牌数据时，页面应保持证书主体内容可浏览。
- 品牌 Logo 缺失或加载失败时，证书详情页与其他 `brand-card` 场景应呈现一致的兜底视觉。
- 若组件新增入参或字段映射，必须保证既有调用方兼容。

## 5. UI 约束

- 证书详情页品牌入口视觉 MUST 延续小程序“工业石材 · 暗色旗舰风”，并与既有 `brand-card` 视觉保持一致。
- 品牌 Logo 区域 MUST 使用稳定尺寸容器，避免缩略图加载前后造成布局跳动。
- 品牌名称、入口提示和副文案在 320px 小屏宽度下不得撑破卡片布局。
- 整个品牌入口的有效点击区域 SHOULD 不小于 44px 高度，适配小程序触控。
- 证书详情页不得为了品牌入口新增与 `brand-card` 冲突的独立卡片样式、私有箭头、私有 Logo 占位或私有点击反馈。
- 卡片内不展示管理端编辑、启停、删除等操作。

## 6. 数据与接口影响

| 范围 | 影响 |
|---|---|
| 微信小程序 | 证书详情页需要复用 `brand-card`，并传入品牌缩略图、来源和证书上下文。 |
| 后端 API / Schema | 若当前证书详情 `brand` 数据缺少 `brand_logo_thumbnail_url`，实现阶段需要补齐响应字段并同步 Schema、OpenAPI/Orval 或小程序服务层类型。 |
| SQLite/MySQL | 本需求不直接要求新增数据库字段，优先复用既有品牌 Logo 缩略图数据来源。 |
| 媒体 / 对象存储 | 不新增派生图能力；只要求证书详情品牌入口消费既有缩略图 URL，不直连对象存储原始 Key。 |
| Web 管理端 | 不涉及。 |
| 店主 Web | 不涉及。 |
| 测试 | 后续实现应覆盖证书详情 brand 数据字段、brand-card 复用、点击跳转、埋点事件名和缩略图消费策略。 |

## 7. 关联需求

| 需求 / 缺陷 | 关系 |
|---|---|
| `REQ-0115-media-multi-variant-images` | 父需求，提供图片多规格和轻量图能力背景。 |
| `REQ-0118-unified-web-miniapp-image-variant-consumption-matrix` | 关联需求，定义小程序品牌 Logo 和卡片场景使用缩略图的消费矩阵。 |
| `REQ-0054-brand-card-common-component` | 关联需求，定义小程序 `brand-card` 组件的展示、跳转、异常和埋点边界。 |
| `REQ-0080-miniapp-certificate-detail-page` | 关联需求，证书详情页品牌入口所在页面能力。 |
| `REQ-0092-brand-certificate-image-thumbnails` | 关联需求，品牌与证书图片缩略图能力来源。 |
| `BUG-0134-miniapp-certificate-detail-display-url` | 关联缺陷，证书详情媒体字段轻量化相关问题。 |
| `BUG-0137-miniapp-lightweight-image-variant-consumption` | 关联缺陷，小程序普通展示轻量图消费口径相关问题。 |

## 8. 状态块

```yaml
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
status: done
terminal: miniapp
version: v1
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
lifecycle_stage: archive
iteration: sprint-025
openspec_changes:
  - change_id: update-miniapp-certificate-detail-brand-card-entry
    type: update
    status: archived
scope_summary: 小程序证书详情页所属品牌入口复用 brand-card，补齐 brand_logo_thumbnail_url，统一 brand_card_click 埋点和缩略图消费策略
excluded_scope:
  - 证书详情页整体重构
  - 管理端品牌或证书维护能力调整
  - 新增数据库字段或图片派生能力
  - Web 端品牌卡片组件建设
next: 暂无可推进下一步
```
