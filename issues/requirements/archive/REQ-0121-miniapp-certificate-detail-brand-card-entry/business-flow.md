---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card 业务流程
owner: product
source: requirement.md
created_at: 2026-08-24 15:26:47
updated_at: 2026-08-24 15:26:47
---

# 业务流程

## 1. 主流程

```text
用户进入证书详情页
  ↓
小程序请求证书详情数据
  ↓
证书详情响应返回 certificate + brand
  ↓
brand 数据包含 brand_id / brand_name / brand_logo_thumbnail_url / entry 参数
  ↓
页面容器将 brand 数据和 sourcePage=certificate_detail 传给 brand-card
  ↓
brand-card 渲染品牌 Logo、名称、入口提示和点击态
  ↓
用户点击品牌入口
  ↓
brand-card 上报 brand_card_click
  ↓
跳转到品牌详情页或既定品牌入口
```

## 2. 异常流程

```text
brand 缺失或品牌不可公开
  ↓
证书详情页不展示品牌入口，或 brand-card 进入不可用态
  ↓
证书主体信息仍可浏览
```

```text
brand_logo_thumbnail_url 缺失或图片加载失败
  ↓
brand-card 使用统一占位 / 品牌首字 / 安全兜底
  ↓
不得 fallback 到品牌原图扩大小程序加载体积
```

```text
品牌入口参数缺失
  ↓
brand-card 阻止无效跳转
  ↓
按统一不可用策略提示或保持禁用态
  ↓
记录可诊断参数，不暴露内部字段
```

## 3. 与父需求差异

| 对象 | 本需求边界 | 与父需求关系 |
|---|---|---|
| `REQ-0115-media-multi-variant-images` | 只要求证书详情品牌入口消费品牌 Logo 缩略图，不新增图片派生能力。 | 复用父需求定义的图片多规格与轻量化策略。 |
| `REQ-0054-brand-card-common-component` | 只要求证书详情接入并保持点击/埋点一致，不重做组件全量能力。 | 复用品牌卡片组件的展示、跳转和异常状态。 |
| `REQ-0080-miniapp-certificate-detail-page` | 只调整所属品牌入口，不重做证书详情页整体结构。 | 在既有证书详情页内补齐品牌入口复用契约。 |
| `REQ-0118-unified-web-miniapp-image-variant-consumption-matrix` | 只落到品牌 Logo 小卡片场景。 | 遵循品牌卡片消费 `thumbnail` 的矩阵规则。 |

## 4. 角色责任

| 角色 | 责任 |
|---|---|
| 后端 / API | 确认证书详情 `brand` 数据可提供 `brand_logo_thumbnail_url`，并遵守公开字段与媒体 URL 安全边界。 |
| 小程序页面 | 负责请求证书详情、传入 `brand-card` 所需数据和来源上下文。 |
| `brand-card` 组件 | 负责展示、图片兜底、点击跳转、不可用态和 `brand_card_click` 埋点。 |
| 测试 | 使用字段、Network、render 和埋点证据确认没有原图 fallback 和事件名分叉。 |
